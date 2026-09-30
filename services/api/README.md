# Incident Analyzer API

Install dependencies and run from the repository root:

```bash
pip install -r services/api/requirements.txt
uvicorn services.api.main:app --reload
```

Endpoints:

- `POST /api/incidents/analyze` with a multipart field named `file`. The file
	must have a `.csv` filename and UTF-8 content. A successful response is the
	shared analysis summary as JSON.
- `GET /api/incidents/results/export` after a successful analysis. It returns
	`results.csv` with the shared serializer's `metric,value` rows.

Upload example:

```bash
curl -F "file=@incidents-brasaland.csv" http://localhost:8000/api/incidents/analyze
curl -OJ http://localhost:8000/api/incidents/results/export
```

The API keeps only the most recent successful summary in process memory; it
does not persist uploaded raw CSV data. Start the service from the repository
root with `uvicorn services.api.main:app --reload` and use the backoffice with
`npm run dev` in `uis/backoffice`. In a forwarded or remote workspace, the
backoffice proxies `/api/incidents/*` to the backend, so the browser does not
resolve `localhost:8000` on the user's own computer.

Errors use FastAPI's JSON error shape (`{"detail": "..."}`): empty or
non-CSV uploads return `400`, invalid UTF-8/CSV or missing required columns
return `422`, and exporting before a successful analysis returns `404`.

The API imports `scripts/analyzer_core.py`; validation and metrics must not be
duplicated in the endpoint layer. CORS permits the local backoffice origins
`http://localhost:3000` and `http://127.0.0.1:3000`.
