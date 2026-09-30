# Brasaland Incident Analyzer — Phase 1–4

## Summary

This pull request delivers the Brasaland incident analyzer across the CLI,
FastAPI backend, and Next.js backoffice. The CLI and API consume one shared
Python analysis module, and the backoffice uploads CSV files, presents the
returned summary, communicates invalid records, and downloads the exported CSV.

## What changed

- Added the shared Brasaland analyzer and CLI under `scripts/`.
- Added the official `scripts/incidents-brasaland.csv` test file.
- Added FastAPI analysis and export endpoints under `services/api/`.
- Added API endpoint tests for success, parity, export, errors, and CORS.
- Added the backoffice upload, results, invalid-record notice, and download UI.
- Added run instructions and the Phase 4 audit report.

## Evidence

Official 100-record dataset results:

- Total: `100`
- Valid: `96`
- Invalid: `4`
- Average satisfaction: `3.46`
- Closed scored cases: `50`

Tests and checks:

- Python analyzer tests: `6 passed`
- API endpoint tests: `5 passed`
- Frontend typecheck: passed
- Frontend production build: passed

### Required submission screenshots

- `docs/Screenshots/5CCE738F-21BA-4367-9D56-802177F3E1DA.jpeg` — CLI console output using `scripts/incidents-brasaland.csv`.
- `docs/Screenshots/ABCE32A0-D14E-49A9-8BCD-C227295EC21E.jpeg` — backoffice with the loaded analysis.

These two screenshots are still required before submitting the pull request;
they cannot be generated or attached by the repository build itself.

## Run locally

From the repository root:

```bash
pip install -r services/api/requirements.txt
uvicorn services.api.main:app --reload
```

In a second terminal:

```bash
cd uis/backoffice
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

Open `http://localhost:3000` and upload `scripts/incidents-brasaland.csv`.

To run the CLI:

```bash
python scripts/analyze.py scripts/incidents-brasaland.csv
```

## Review notes

Analysis and validation logic is implemented once in
`scripts/analyzer_core.py`; the script and API import it directly, while the
frontend renders API response values without recomputing business metrics.

Known unverified item: a live browser smoke test was not executed in the audit
environment. The frontend typecheck and production build succeeded, and the
API contract tests passed.
