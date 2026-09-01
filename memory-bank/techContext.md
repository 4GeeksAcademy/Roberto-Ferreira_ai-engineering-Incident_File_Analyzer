# Tech Context

Every fact below is verified against a file in the repo (path noted) or against [CONTEXT.md](../CONTEXT.md).
Nothing here is assumed.

## Repository layout in use

- `uis/talent-pipeline-tracker/` — the only implemented application in the repo (the "Talent Pipeline
  Tracker" frontend). Verified via `list_dir` on `uis/`.
- `services/` contains only `README.md`/`README.es.md` — **no backend service is implemented in this
  repo**. Per CONTEXT.md, "the mock API is centrally deployed and shared across all company contexts in
  the course" — the backend is an external, pre-built dependency, not code owned here.
- `packages/shared/package.json` declares `@repo/shared-types` (types package), but no root workspace
  runner is configured (confirmed in root `README.md`: "no workspace runner is configured at root"), and
  `uis/talent-pipeline-tracker` does not import from `@repo/shared-types` — it defines its own local
  `types/` folder instead.
- No `docker-compose.yml`, `.env`, or `.env.example` exists anywhere in the repo (verified with
  `file_search`). No `infra/` config beyond the placeholder README.

## Frontend stack — `uis/talent-pipeline-tracker/package.json`

- **Framework:** Next.js `15.4.6` (App Router — routes live under `app/`).
- **UI library:** React `19.1.0` / `react-dom` `19.1.0`.
- **Language:** TypeScript `5.8.3`, `strict: true`, `noEmit: true` (type-checking only, via `tsc --noEmit`
  in the `typecheck` script).
- **Module/path setup** (`tsconfig.json`): `moduleResolution: "bundler"`, path alias `@/*` → project root.
- **Scripts:** `dev` (`next dev`), `build` (`next build`), `start` (`next start`), `typecheck`.
- `next.config.ts` has no custom configuration (empty `NextConfig` object).

## Application architecture (as implemented)

- **Routing** (`app/`): `/` (candidates list), `/candidates/new` (create), `/candidates/[id]` (detail),
  `/candidates/[id]/edit` (edit). Verified via `list_dir`.
- **Presentation components** (`components/`): `records-list-page.tsx`, `candidate-detail-page.tsx`,
  `candidate-create-page.tsx`, `candidate-edit-page.tsx`, and a shared `candidate-form.tsx` reused by
  create/edit.
- **API access layer:**
  - `lib/api-client.ts` — a generic `apiRequest<T>()` fetch wrapper. It reads the API base URL from
    `process.env.NEXT_PUBLIC_API_URL` and **throws if that env var is not set** — there is currently no
    `.env` file defining it, so the app cannot reach a real API out of the box.
  - `lib/records.ts` — typed functions over `apiRequest`: `getRecords`, `getRecordById`, `createRecord`,
    `updateRecord` (PUT), `patchRecordStatus` (PATCH), `getNotes`, `addNote`, `deleteNote`. Endpoints used:
    `records`, `records/:id`, `records/:id/notes`, `records/:id/notes/:noteId`.
- **Domain types** (`types/records.ts`, `types/api.ts`): `RecordBase`/`RecordListItem`/`RecordDetail`,
  `RecordNote`, plus `RECORD_STATUSES`/`RECORD_STAGES` and `STATUS_LABELS`/`STAGE_LABELS` lookup maps that
  translate raw API values into the human-readable labels required by CONTEXT.md.

## API contract (per CONTEXT.md, "no adaptation required")

- `status` values: `received`, `in_progress`, `selected`, `discarded`.
- `stage` values: `pending`, `review`, `personal_interview`, `technical_interview`, `offer_presented`.
- The UI must always render the mapped label, never the raw value.

## Constraints

- Do not change the shape of the mock API — it is centrally deployed and shared across all company
  contexts in the course (CONTEXT.md).
- Strict TypeScript compilation must pass (`strict: true` in `tsconfig.json`).
- Notes must only be visible in the candidate detail view (CONTEXT.md acceptance criteria).

## Unverified / flagged

- There is no documented deployment target, hosting setup, or CI pipeline for this app (`.github/`
  contents were not inspected as part of this task — flag for follow-up, not assumed here).
- The exact value/host for `NEXT_PUBLIC_API_URL` is not present anywhere in the repo and must be sourced
  from course material, not invented.
