# Phase 4 Cross-Cutting Audit

Date: 2026-10-13

## Evaluation checklist

### Script

| Criterion | Result | Evidence |
|---|---|---|
| Accepts CSV path without code changes | **Met** | `scripts/analyze.py` uses argparse positional `csv_path`; `python scripts/analyze.py scripts/incidents-brasaland.csv` ran successfully. |
| Detects and classifies invalid records | **Met** | `scripts/analyzer_core.py` produces `invalid_details` and `invalid_by_reason`; official run reported 4 invalid records with four reason types. |
| Prints required metrics readably | **Met** | CLI output includes totals, category/status breakdowns, and satisfaction index. |
| CSV export | **Met** | `results_csv()` writes one `metric,value` row per result and CLI prompts for export. |
| Expected values match context | **Met** | Side-by-side expected/actual comparison is recorded below; official CLI output was rerun in this audit. |

### Backend

| Criterion | Result | Evidence |
|---|---|---|
| Analysis endpoint | **Met** | `services/api/main.py`, `POST /api/incidents/analyze`; `services/api/test_main.py` official-file test passes. |
| Export endpoint | **Met** | `GET /api/incidents/results/export` uses shared `results_csv`; endpoint test verifies CSV media type and attachment filename. |
| Input errors | **Met** | Endpoint tests verify empty/non-CSV `400`, invalid UTF-8/missing columns `422`, and export-before-analysis `404`. |

### Frontend

| Criterion | Result | Evidence |
|---|---|---|
| Browser upload | **Met** | `uis/backoffice/components/analysis-upload.tsx` supports file selection and drag/drop. |
| Clear summary | **Met** | `analysis-results.tsx` renders general metrics, categories, statuses, satisfaction, and invalid reasons from API response. |
| Export button | **Met** | `analysis-results.tsx` links to the configured export endpoint with download filename. |
| Invalid-record notice | **Met** | Results page renders invalid count and each API-provided reason count. |
| Automated frontend tests | **Partially met** | No committed frontend test runner exists in `uis/backoffice/package.json`; typecheck and production build pass. A live Playwright smoke uploaded the official CSV and asserted 100/96/4 totals and 3.46 average; the resulting UI screenshot is included. |

### Cross-cutting

| Criterion | Result | Evidence |
|---|---|---|
| One analysis implementation | **Met** | `scripts/analyze.py` imports `analyze_csv`/`results_csv`; `services/api/main.py` imports the same functions; UI only renders API response fields. Search found no second metric implementation. |
| Required organization | **Met** | `scripts/`, `services/api/`, and `uis/backoffice/` exist, including the official CSV at `scripts/incidents-brasaland.csv`. The extra root copy is not required by the submission layout. |

## Expected versus actual values

| Metric | Expected | Actual CLI result |
|---|---:|---:|
| Total / valid / invalid records | 100 / 96 / 4 | 100 / 96 / 4 |
| Categories: complaint / equipment / supply / food quality / staff | 29 / 17 / 22 / 19 / 9 | 29 / 17 / 22 / 19 / 9 |
| Statuses: open / closed / discarded | 32 / 50 / 14 | 32 / 50 / 14 |
| Invalid reasons: location / category / description / closed without score | 1 / 1 / 1 / 1 | 1 / 1 / 1 / 1 |
| Closed scored cases / average satisfaction | 50 / 3.46 | 50 / 3.46 |
| Satisfaction distribution, scores 1 through 5 | 4 / 6 / 12 / 19 / 9 | 4 / 6 / 12 / 19 / 9 |

## Structure verification

```text
scripts/
├── analyze.py
├── analyzer_core.py
├── incidents-brasaland.csv
└── test_analyzer_core.py

services/api/
├── main.py
├── requirements.txt
├── requirements-test.txt
└── test_main.py

uis/backoffice/
├── app/
├── components/
├── lib/
├── package.json
└── types.ts
```

## Full verification

Commands and results:

```text
PYTHONPATH=. python -m unittest discover -s scripts -p 'test_*.py'
........
Ran 8 tests in 0.002s
OK

pip install -r services/api/requirements-test.txt
PYTHONPATH=. python services/api/test_main.py
.....
Ran 5 tests in 0.036s
OK

cd uis/backoffice && npm run typecheck
passed after adding the existing @/ alias mapping to tsconfig.json

cd uis/backoffice && npm run build
passed; Next.js production build completed

CLI CSV export
Export prompt answered y; results.csv was created with a metric,value header
and populated metric rows (written under /tmp to keep the repository clean)
```

No frontend test runner is declared.

## Shared-logic audit

The authoritative analysis symbols are defined only in `scripts/analyzer_core.py`:

- `analyze_rows`
- `analyze_csv`
- `results_csv`
- `_validation_reasons`

The CLI and API import these functions. The frontend's TypeScript code has no
CSV parsing, validation rules, or metric calculations; it displays API fields
and calculates only presentation percentages for already-returned counts.

## Defects fixed during this audit

1. Added TypeScript path mapping for the existing `@/` imports. Reason: the
  required frontend typecheck could not resolve existing components.
2. Added `services/api/requirements-test.txt` and documented the test command.
  Reason: the current Starlette TestClient requires `httpx2`, which was not
  included in the documented test setup.
3. Updated the backoffice Next.js pin from 15.4.6 to 15.5.27 and re-ran its
  typecheck and production build. This non-major update does not clear all
  current npm audit advisories; see the deferred security finding below.

No feature logic, expected values, backend endpoints, or shared analyzer code
were changed.

## Deferred/unverified findings

- A committed automated browser test runner is not included; the live browser
  smoke test was run with temporary Playwright tooling during this audit.
- The root `incidents-brasaland.csv` remains alongside the required `scripts/`
  copy. Removing it could affect prior documentation or workflows, so it is
  reported rather than removed.
- The checked-in `docs/docs/PROJECT-BRIEF.md` is a generic docs-folder README;
  the evaluation brief used for this audit is `.project_requirements/rubric.md`.
- The protected root `CONTEXT.md` and `memory-bank/` still describe the Talent
  Pipeline Tracker rather than this incident analyzer. `AGENTS.md` requires
  explicit confirmation before changing them, so they were left untouched.
- A multi-worker deployment would require durable/shared result storage because
  the API currently keeps only the latest summary in process memory.
- `npm audit` still reports 4 advisories (1 critical, 3 high) in Next.js,
  PostCSS, Sharp, and source-map-js after the non-major Next.js update. A
  complete fix requires evaluating a major Next.js upgrade; this remains a
  production-security item, separate from the functional grading rubric.

## PR evidence

The human submission should attach:

- `docs/Screenshots/ABCE32A0-D14E-49A9-8BCD-C227295EC21E.jpeg` — valid backoffice
  evidence showing the loaded 100-record analysis.
- `docs/Screenshots/71332CD3-EA8B-41D4-BCC6-7F8E71886A64.jpeg` — valid CLI
  evidence showing the analyzer command and its 100-record summary.

The implementation, automated checks, and both required screenshots are
present. The CLI screenshot replaces the earlier pytest image.
