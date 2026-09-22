# Brasaland Incident Analyzer — Persistent Instructions

## Project purpose

This repository delivers a Brasaland incident-file analyzer. It validates and summarizes the official incident CSV through a Python CLI, exposes the same analysis through a FastAPI service, and provides a Next.js/React backoffice for CSV upload and results export.

## Standing rules

- Requirements, evaluation criteria, and screenshots define WHAT must be delivered.
- Repository instructions and approved prior artifacts define project context.
- Source code, configuration, dependencies, tests, and verified runtime behavior define technical facts. Important claims are verified against the repository.
- Uncertainty is reported explicitly; guesses are never presented as facts.
- Field names, categories, statuses, and expected values come only from CONTEXT-company.md; nothing generic is substituted.
- Validation and analysis logic exists in exactly one shared module; the script and the API both consume it.
- Invalid records are counted, classified by reason, and reported, never silently dropped.
- Work stays inside the phase currently being executed.

## Authoritative Brasaland CSV contract

The authoritative context is `CONTEXT-brasaland.en.md` at the repository root. The official dataset is `incidents-brasaland.csv` at the repository root. The CSV uses UTF-8, comma separators, and a header row.

Exact fields:

- Required: `incident_id`, `date`, `location_id`, `category`, `description`, `status`, `reporter_id`
- Optional: `customer_id`, `satisfaction_score`
- `satisfaction_score` is required when `status` is `CLOSED`.

Valid categories:

- `CUSTOMER_COMPLAINT`
- `EQUIPMENT`
- `SUPPLY`
- `FOOD_QUALITY`
- `STAFF`

Allowed statuses: `OPEN`, `CLOSED`, `DISCARDED`.

Valid locations are `COL-01` through `COL-10` and `FLA-01` through `FLA-04`. Descriptions must contain at least five characters. A record is invalid for a missing/invalid location, missing/invalid category, empty or too-short description, missing reporter, a closed status without a satisfaction score, or a present satisfaction score outside 1–5 inclusive.

Expected values from the context and official dataset:

- Total records: `100`; valid: `96`; invalid: `4`
- Categories: `CUSTOMER_COMPLAINT=29`, `EQUIPMENT=17`, `SUPPLY=22`, `FOOD_QUALITY=19`, `STAFF=9`
- Statuses: `OPEN=32`, `CLOSED=50`, `DISCARDED=14`
- Invalid reasons: missing location `1`, invalid/missing category `1`, empty/too-short description `1`, closed without score `1`
- Satisfaction scores: 1=`4`, 2=`6`, 3=`12`, 4=`19`, 5=`9`; average `3.46` across 50 closed/scored cases

## Target folder structure

- `scripts/analyze.py`
- `scripts/incidents-brasaland.csv`
- `services/api/`
- `uis/backoffice/`
