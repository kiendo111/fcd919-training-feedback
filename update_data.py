#!/usr/bin/env python3
"""Fetch the six FCD 919 feedback tabs and write name-sanitized CSV snapshots into data/.

Runs unattended (nightly GitHub Action) and locally. It reads the workbook while that
workbook is world-readable, so no credential is needed. Every column whose header carries a
whole word "NAME" (EXAMINER NAME, INSTRUCTOR NAME) is dropped BEFORE anything is written, so a
staff name can never reach the committed data even if the form's columns are reordered. That
by-header rule is the same one the report itself uses to refuse to render a name column.

Uses the CSV export endpoint (export?format=csv&gid=...), which returns raw cell values with
no type coercion -- the gviz endpoint silently blanks non-numeric cells in numeric columns.
Each tab carries a signature string unique to that form; if a gid ever goes stale and returns
the wrong sheet, the fetch fails loud rather than writing the wrong form's data.

If the workbook is ever locked down, anonymous fetch stops working and this needs a Google
service-account key instead (see mirror-setup.md / the deferred lock-down plan).
"""

import csv
import io
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

WORKBOOK_ID = "1Jh0yDNt-w8TeVDgd-qfS_ApOtVRHQGoTh92Wti832PQ"

# (output filename, tab gid, signature substring present in that tab's header row).
TABS = [
    ("post.csv",         605699295,  "SIM REGISTRATION"),
    ("simdpefi.csv",     721893277,  "Adaptation to Trainee"),
    ("simday1.csv",      1802423630, "Scenario Validity"),
    ("lifusinstr.csv",   1674842804, "Line TEM Training Effectiveness"),
    ("lifustrainee.csv", 2040670137, "FEEDBACK DATE"),
    ("lineassess.csv",   1966655020, "Assessment criteria clearly understood"),
]

NAME_COL = re.compile(r"\bNAME\b", re.I)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def fetch(gid: int) -> list[list[str]]:
    url = f"https://docs.google.com/spreadsheets/d/{WORKBOOK_ID}/export?format=csv&gid={gid}"
    req = urllib.request.Request(url, headers={"User-Agent": "fcd919-nightly/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        text = resp.read().decode("utf-8-sig")
    if re.match(r"\s*<(!DOCTYPE|html)", text, re.I):
        raise RuntimeError("got an HTML page, not CSV -- gid stale or workbook not readable")
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        raise RuntimeError("empty response")
    return rows


def sanitize(rows: list[list[str]]) -> tuple[list[list[str]], list[str]]:
    header = rows[0]
    drop = [i for i, h in enumerate(header) if NAME_COL.search(h)]
    dropped = [header[i] for i in drop]
    keep = [i for i in range(len(header)) if i not in drop]
    out = [[r[i] if i < len(r) else "" for i in keep] for r in rows]
    return out, dropped


def main() -> int:
    os.makedirs(DATA_DIR, exist_ok=True)
    failed = []
    for fname, gid, sig in TABS:
        try:
            rows = fetch(gid)
            joined = " | ".join(re.sub(r"\s+", " ", h).strip() for h in rows[0])
            if sig not in joined:
                raise RuntimeError(f"signature {sig!r} not in header -- wrong tab for gid {gid}")
            clean, dropped = sanitize(rows)
            with open(os.path.join(DATA_DIR, fname), "w", encoding="utf-8", newline="") as fh:
                csv.writer(fh).writerows(clean)
            note = f"dropped {dropped}" if dropped else "no name columns"
            print(f"  {fname:18} {len(clean)-1:4d} rows, {len(clean[0])} cols  ({note})")
        except Exception as e:  # noqa: BLE001 - report and continue; one bad tab is not fatal
            failed.append((fname, str(e)))
            print(f"  {fname:18} FAILED: {e}", file=sys.stderr)
    if failed:
        print(f"\n{len(failed)} tab(s) failed: {[f for f, _ in failed]}", file=sys.stderr)
        return 1
    # Stamp the build date (Vietnam time) so the report shows when the data was last fetched.
    built = datetime.now(timezone(timedelta(hours=7))).date().isoformat()
    with open(os.path.join(DATA_DIR, "updated.txt"), "w", encoding="utf-8") as fh:
        fh.write(built + "\n")
    print(f"  {'updated.txt':18} {built}")
    print(f"\nWrote {len(TABS)} sanitized CSV files to {DATA_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
