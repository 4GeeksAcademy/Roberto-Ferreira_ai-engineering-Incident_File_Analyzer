# Architecture Decision — Brasaland Incident Analyzer

**Status:** Recommendation for human approval. This Phase 0 document records verified repository facts and does not change feature implementation.

## Verified technology stack

| Area | Verified fact | Source |
|---|---|---|
| CLI/shared analysis | Python; CLI entry point is `scripts/analyze.py` and shared module is `scripts/analyzer_core.py`. | `scripts/analyze.py`, `scripts/analyzer_core.py` |
| API framework | FastAPI application. | `services/api/main.py` (`FastAPI`, route decorators) |
| API runtime/package manager | Python package installation through pip requirements; Uvicorn run command. | `services/api/requirements.txt`, `services/api/README.md` |
| API test runner | No API test runner or API tests were found during Phase 0 inspection. | `services/api/` listing; `scripts/test_analyzer_core.py` is the only discovered focused test file |
| Backoffice framework | Next.js 15.4.6 with React 19.1.0 and TypeScript 5.8.3. | `uis/backoffice/package.json` |
| Backoffice package manager | npm, evidenced by `package-lock.json` and npm scripts. | `uis/backoffice/package-lock.json`, `uis/backoffice/package.json` |
| Backoffice test runner | No frontend test runner is declared. | `uis/backoffice/package.json` |

## Shared analysis module decision

### Recommendation

Keep one Python analysis module at `scripts/analyzer_core.py`. The CLI imports it directly, and the FastAPI application imports the same module by adding the repository root's `scripts` directory to its import path, as currently shown in `services/api/main.py`.

### Why this option

- It preserves exactly one implementation of CSV validation, invalid-reason classification, metrics, and export serialization.
- It is already compatible with the current Python CLI and FastAPI service.
- It avoids duplicating business rules in the API endpoint.
- It does not require a new package or dependency during this phase.

### Alternatives considered

1. **Duplicate logic in `scripts/analyze.py` and `services/api/main.py`:** rejected because rules would drift and violate the standing rule requiring one shared module.
2. **Move the module into `services/` or a new top-level package:** possible, but unnecessary for the current verified layout and would require changing import paths and potentially packaging conventions.
3. **Expose analysis only through the API and make the CLI call HTTP:** rejected because the CLI should remain usable independently and would introduce a runtime service dependency.
4. **Create a shared TypeScript implementation for the backoffice:** rejected because the authoritative CLI/API validation is Python and the backoffice currently consumes API results rather than reimplementing metrics.

## Last-analysis state and export endpoint

The current API stores the most recent successful summary in the module-level variable `last_summary` in `services/api/main.py`. `POST /api/incidents/analyze` replaces it after a successful upload. `GET /api/incidents/results/export` serializes that state using the shared `results_csv` function. If no analysis has succeeded, the endpoint returns HTTP 404.

This is an in-process, single-worker recommendation/implementation fact, not durable storage. It is suitable for the current small application but would need a database, shared cache, or explicit job/result store for multi-worker or restart-safe behavior.

## Context restatement

Authoritative source: `CONTEXT-brasaland.en.md`.

### Fields

Required fields are `incident_id`, `date`, `location_id`, `category`, `description`, `status`, and `reporter_id`. Optional fields are `customer_id` and `satisfaction_score`; satisfaction is required when `status` is `CLOSED`. The CSV is UTF-8, comma-separated, and has a header row.

### Categories and statuses

Categories: `CUSTOMER_COMPLAINT`, `EQUIPMENT`, `SUPPLY`, `FOOD_QUALITY`, `STAFF`.

Statuses: `OPEN`, `CLOSED`, `DISCARDED`.

Locations are `COL-01` through `COL-10` and `FLA-01` through `FLA-04`. Descriptions must have at least five characters.

### Invalid records

A record is invalid when its location is missing or not one of the 14 valid location codes; its category is missing or invalid; its description is empty or shorter than five characters; its reporter is missing; it is `CLOSED` without a satisfaction score; or it has a present satisfaction score outside the inclusive range 1–5. Invalid rows must be counted and classified, not silently dropped.

### Satisfaction average

The expected average is calculated over the 50 closed records with scores. Expected score counts are: 1=`4`, 2=`6`, 3=`12`, 4=`19`, 5=`9`; average `3.46 / 5.00`.

### Expected values

- Total rows: `100`
- Valid records: `96`
- Invalid records: `4`
- Valid category counts: `CUSTOMER_COMPLAINT=29`, `EQUIPMENT=17`, `SUPPLY=22`, `FOOD_QUALITY=19`, `STAFF=9`
- Valid status counts: `OPEN=32`, `CLOSED=50`, `DISCARDED=14`
- Invalid breakdown: missing location=`1`, invalid/missing category=`1`, empty/too-short description=`1`, closed without score=`1`
- Satisfaction distribution: score 1=`4`, score 2=`6`, score 3=`12`, score 4=`19`, score 5=`9`

## Ambiguities and questions for human approval

1. The opening context says the test file has **1,000 rows**, while the distribution and expected output specify **100 rows**. The official downloaded dataset in this workspace contains 100 data rows and matches the latter values.
2. The context names the CSV `incidents.csv` in the schema but refers to the supplied test file as `incidents-brasaland.csv`. The repository currently contains both a root `incidents.csv` artifact and the official `incidents-brasaland.csv`; the latter is the verified dataset matching the expected metrics.
3. The phase brief requests `scripts/incidents-COMPANY.csv`, while the verified official dataset is currently at the repository root as `incidents-brasaland.csv`. Should the dataset be copied to `scripts/incidents-brasaland.csv` in a later approved phase, or should the root location be canonical?
4. The exact test-runner choice for the API and frontend is not specified in the manifests; no such runner is currently declared.
5. The expected invalid-output labels are presentation labels; the context does not prescribe machine-readable reason keys.

## Scope confirmation

This is an architecture recommendation for Phase 0. No new endpoints, UI components, analysis logic, tests, dependencies, or manifest changes were made as part of this Phase 0 deliverable.
