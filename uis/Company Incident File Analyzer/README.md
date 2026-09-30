# talent-pipeline-tracker

Brasaland Digital's candidate management dashboard for the Executive Assistant hiring search.

- **Objective:** manage the full candidate lifecycle for the active hiring process: review applicants,
  filter and search the pipeline, update status/stage, add internal notes, and create or correct records.
- **Stack:** Next.js 15.4.6 (App Router), React 19.1.0, TypeScript 5.8.3 (strict).
- **Routes:**
  - `/` — candidate list with filters and search
  - `/candidates/new` — register a new candidate
  - `/candidates/[id]` — candidate detail and notes
  - `/candidates/[id]/edit` — update candidate details
- **Data note:** the app talks to the shared company mock API. Before running locally, set
  `NEXT_PUBLIC_API_URL` in a local environment file for your course environment. This repo does not
  include a checked-in `.env` file.

## Run locally

```bash
npm install
npm run dev
```

## Verify

```bash
npm run typecheck
npm run build
```

The app is expected to pass strict TypeScript validation and compile successfully once the mock API URL
is configured in the local environment.
