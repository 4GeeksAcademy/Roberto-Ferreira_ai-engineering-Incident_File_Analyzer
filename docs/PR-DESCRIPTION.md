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
- Updated the backoffice Next.js pin to `15.5.27` and configured TypeScript path aliases.
- Added run instructions and the Phase 4 audit report.

## Evidence

Official 100-record dataset results:

- Total: `100`
- Valid: `96`
- Invalid: `4`
- Average satisfaction: `3.46`
- Closed scored cases: `50`

Tests and checks:

- Python analyzer tests: `8 passed`
- API endpoint tests: `5 passed`
- Frontend typecheck: passed
- Frontend production build: passed

### Required submission screenshots

- `docs/Screenshots/71332CD3-EA8B-41D4-BCC6-7F8E71886A64.jpeg` — CLI console output from `python scripts/analyze.py scripts/incidents-brasaland.csv`, showing the 100-record summary.
- `docs/Screenshots/ABCE32A0-D14E-49A9-8BCD-C227295EC21E.jpeg` — backoffice with the loaded 100-record analysis.

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
npm run dev
```

Leave `NEXT_PUBLIC_API_URL` unset for local development; the Next.js app proxies
`/api/incidents/*` to the API on port 8000, including in forwarded workspaces.

Open `http://localhost:3000` and upload `scripts/incidents-brasaland.csv`.

To run the CLI:

```bash
python scripts/analyze.py scripts/incidents-brasaland.csv
```

## Review notes

Analysis and validation logic is implemented once in
`scripts/analyzer_core.py`; the script and API import it directly, while the
frontend renders API response values without recomputing business metrics.

The live browser smoke test uploaded the official CSV and verified the displayed
100 total, 96 valid, 4 invalid, and 3.46 average. Frontend typecheck, production
build, analyzer tests, and API contract tests all passed.

Security note: `npm audit` still reports 4 advisories (1 critical, 3 high) in
Next.js and transitive dependencies. A major framework upgrade is not included
in this grading submission; resolve these advisories before production use.
