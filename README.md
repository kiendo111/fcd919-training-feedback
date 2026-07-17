# FCD 919 Training Feedback Report

A name-sanitized snapshot of the six Vietnam Airlines FCD 919 training-feedback forms,
published as a single static page. Presentation only — no interpretation.

- **Live report:** https://kiendo111.github.io/fcd919-training-feedback/
- **`index.html`** — the report (self-contained; reads the CSVs in `data/`).
- **`data/*.csv`** — the six forms, name-sanitized. Examiner/instructor name columns are
  stripped before anything is committed.
- **`update_data.py`** — fetches the tabs and re-writes `data/`, dropping any column whose
  header contains the word NAME.
- **`.github/workflows/nightly.yml`** — runs `update_data.py` nightly (01:00 GMT+7) and
  commits the refreshed CSVs, so the page picks up new responses. Can also be run by hand
  from the Actions tab.
- **`serve.sh`** — preview locally (`./serve.sh`, then open http://localhost:8899/).
- **`mirror-setup.md`** — the fallback live-mirror path, if the source workbook is ever
  locked down and the credential-free nightly fetch stops working.

## Refreshing by hand

    python update_data.py    # rewrites data/*.csv from the live workbook

Then commit and push. The nightly job does the same thing on a schedule.

## Privacy

Staff names live only in the source workbook's Post-Rec tab and are removed by header before
any CSV is written here. Free-text comments pass through verbatim; a name typed into a comment
box would not be caught by column stripping (none present at last review). If the source
workbook is ever locked down, the nightly fetch needs a Google service-account key instead of
anonymous access.
