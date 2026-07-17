# Sanitized mirror sheet — setup guide

Goal: a Google Sheet **you own** that live-mirrors the six feedback forms but drops the two name columns, so the public report can read it without ever exposing examiner/instructor names.

Why this is needed: the original forms workbook is shared "anyone with the link can view". Hosting the report publicly puts that workbook's ID into the page source, and anyone could then pull the raw CSV — including the `EXAMINER NAME` / `INSTRUCTOR NAME` columns the report hides. The mirror has no name columns, so its ID is safe to expose.

Only the **Post-Rec Simulator** tab has name columns (they get dropped). The other five have none and pass through whole.

Source workbook ID (already in the formulas below): `1Jh0yDNt-w8TeVDgd-qfS_ApOtVRHQGoTh92Wti832PQ`

---

## Steps

1. Go to **sheets.new** to create a new blank spreadsheet. Name it e.g. `FCD919 feedback — public mirror`.
2. Make **6 tabs**. Names don't matter (I detect each form by its content), but simple ones help: `post`, `simdpefi`, `simday1`, `lifusinstr`, `lifustrainee`, `lineassess`.
3. In **cell A1** of each tab, paste the matching formula below. **Paste, don't retype** — the Post-Rec formula's tab name ends in two spaces that must be preserved.
4. The first formula shows `#REF!` with "You need to connect these sheets." Hover it, click **Allow access**. That one grant covers all six.
5. Share the mirror: top-right **Share → General access → Anyone with the link → Viewer**.
6. Send me the mirror's **URL**. I'll pull its tab IDs, verify each tab matches the right form, repoint the report, re-verify, and host it.

---

## Formulas (paste into A1 of each tab)

**post** (Post-Rec Simulator — drops EXAMINER NAME col D and INSTRUCTOR NAME col R):
```
=QUERY(IMPORTRANGE("1Jh0yDNt-w8TeVDgd-qfS_ApOtVRHQGoTh92Wti832PQ","'POST REC SIMULATOR TRAINEE FEEDBACK FORM  '!A1:AH"),"select Col1,Col2,Col3,Col5,Col6,Col7,Col8,Col9,Col10,Col11,Col12,Col13,Col14,Col15,Col16,Col17,Col19,Col20,Col21,Col22,Col23,Col24,Col25,Col26,Col27,Col28,Col29,Col30,Col31,Col32,Col33,Col34",1)
```

**simdpefi** (SIM Recurrent DPE/FI):
```
=IMPORTRANGE("1Jh0yDNt-w8TeVDgd-qfS_ApOtVRHQGoTh92Wti832PQ","'SIM RECURRENT FOR DPE, FI (TRAINING SYSTEM)'!A1:N")
```

**simday1** (SIM Recurrent Day 1):
```
=IMPORTRANGE("1Jh0yDNt-w8TeVDgd-qfS_ApOtVRHQGoTh92Wti832PQ","'SIM RECURRENT DAY 1 FOR DPE ONLY (EVALUATION SYSTEM)'!A1:K")
```

**lifusinstr** (LIFUS Instructors):
```
=IMPORTRANGE("1Jh0yDNt-w8TeVDgd-qfS_ApOtVRHQGoTh92Wti832PQ","'LIFUS FOR ALL INSTRUCTORS'!A1:O")
```

**lifustrainee** (LIFUS Trainee):
```
=IMPORTRANGE("1Jh0yDNt-w8TeVDgd-qfS_ApOtVRHQGoTh92Wti832PQ","'LIFUS TRAINEE FEEDBACK FORM'!A1:BD")
```

**lineassess** (Line Assessment):
```
=IMPORTRANGE("1Jh0yDNt-w8TeVDgd-qfS_ApOtVRHQGoTh92Wti832PQ","'LINE ASSESSMENT FEEDBACK FORM'!A1:I")
```

---

## Notes

- **Freshness:** IMPORTRANGE refreshes roughly hourly (Google's cache), not instantly. The report still re-reads the mirror every 5 minutes, so numbers lag new submissions by up to about an hour. For a feedback report that's fine; if you need it faster, tell me.
- **If Post-Rec shows `#REF! ... not found`:** the tab name spacing got lost on paste. Re-copy the `post` formula from this file verbatim.
- **Comments still verbatim:** free-text comments pass through unchanged (current scan found no names in them). A name typed into a future comment would still appear — that was your accepted call.
