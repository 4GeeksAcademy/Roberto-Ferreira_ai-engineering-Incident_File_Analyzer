# Incident Analyzer backoffice

```bash
npm install
npm run dev
```

Start the API first from the repository root:

```bash
pip install -r services/api/requirements.txt
uvicorn services.api.main:app --reload
```

Then open `http://localhost:3000`, choose or drag
`scripts/incidents-brasaland.csv` into the upload area, and confirm the loaded
summary. The page uploads a CSV to `POST /api/incidents/analyze`, displays the
JSON summary, and downloads the latest exported results from
`GET /api/incidents/results/export`.

The default browser requests are same-origin and are proxied by Next.js to
the API on port 8000. This is important in Codespaces or other remote
workspaces, where the browser's `localhost` is not the API container. Set
`NEXT_PUBLIC_API_URL` only when the API is intentionally hosted at a separate
browser-reachable origin.

The frontend has no dedicated test runner in `package.json`; verify it with:

```bash
npm run typecheck
npm run build
```
