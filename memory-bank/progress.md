# Progress

Status verified directly against the repository state on 2026-09-01. Nothing below is marked done unless
a corresponding file/route was found.

## Done (verified)

- `CONTEXT.md` contains the real Brasaland · Talent Pipeline Tracker briefing (verified by reading the
  file directly).
- `uis/talent-pipeline-tracker` app scaffolded with Next.js 15 + React 19 + TypeScript, `strict` mode
  (verified: `package.json`, `tsconfig.json`).
- Routes exist for all four required screens: candidates list (`app/page.tsx`), create
  (`app/candidates/new/page.tsx`), detail (`app/candidates/[id]/page.tsx`), edit
  (`app/candidates/[id]/edit/page.tsx`).
- UI components implemented for each screen plus a shared form: `records-list-page.tsx`,
  `candidate-detail-page.tsx`, `candidate-create-page.tsx`, `candidate-edit-page.tsx`,
  `candidate-form.tsx`.
- Typed API integration layer implemented: `lib/api-client.ts` (fetch wrapper) and `lib/records.ts`
  (records + notes endpoints: get/create/update/patch-status, get/add/delete note).
- Status/stage label mapping implemented in `types/records.ts` (`STATUS_LABELS`, `STAGE_LABELS`),
  matching the label tables required by CONTEXT.md.
- `AGENTS.md` created at the repo root defining required reading, the mandatory pre-commit workflow, and
  the protected-files list for any coding agent working in this repo.
- `.agents/rules/no-raw-api-status-values-in-ui.md` — file-pattern-scoped rule enforcing the CONTEXT.md
  requirement that raw API `status`/`stage` values never render in the UI.
- `.agents/skills/verify-frontend-typecheck/SKILL.md` — documented skill (objective, inputs, pass/fail
  acceptance criteria) formalizing the `npm run typecheck` check already required by `AGENTS.md`.
- `uis/website` initialized (Next.js 15.4.6 / React 19.1.0 / TS 5.8.3 strict) with a home route rendering
  company facts from CONTEXT.md (name, industry, 14 locations, Colombia & Florida, Medellín HQ). Verified:
  `npm run typecheck` clean, `npm run dev` served `GET / 200` on a fresh run, content confirmed via `curl`.
- `uis/backoffice` initialized with its own sidebar+topbar admin layout (structurally distinct from
  `uis/website`), rendering the CONTEXT.md active-search table and status/stage label reference on screen.
  Verified: `npm run typecheck` clean, `npm run dev` served `GET / 200` on a fresh run, content confirmed
  via `curl`.
- Confirmed (via `grep_search`, no matches) that neither `uis/website` nor `uis/backoffice` calls any
  backend — both are fully static, so no service was added under `./services` for this milestone.

## Not verified / not started

- **No backend/service code in this repo.** `services/` only contains README placeholders — the mock API
  is external and not deployed or configured from here.
- **No environment configuration.** No `.env`/`.env.example` file exists, so `NEXT_PUBLIC_API_URL` is
  unset; `apiRequest()` will throw at runtime until it's configured. The app has not been verified to run
  against a live API.
- **No automated tests** were found anywhere under `uis/talent-pipeline-tracker`.
- **No README** exists inside `uis/talent-pipeline-tracker`, `uis/website`, or `uis/backoffice`
  documenting setup/run steps, despite the root `README.md` convention of "each new app... gets a
  subfolder + README."
- **`@repo/shared-types` (`packages/shared`) is not consumed** by any of the three UIs — each defines its
  own local `types/`/constants, so the shared-types package currently has no effect.
- **No `docker-compose.yml` or `infra/` wiring** exists at the repo root.
- Git history is a single "Initial commit" plus this milestone's uncommitted work — no incremental commit
  trail beyond this session's direct file verification.
- **No environment configuration exists for `uis/website`/`uis/backoffice` either** — not needed today
  since both are fully static, but flagged for whenever either needs live data.

## Concrete next steps

1. Create `.env.local` (or equivalent) in `uis/talent-pipeline-tracker` with `NEXT_PUBLIC_API_URL` pointing
   at the course's centrally deployed mock API, then manually verify list/detail/create/edit/notes flows.
2. Add a `README.md` in `uis/talent-pipeline-tracker` covering local setup and run instructions, per the
   monorepo convention.
3. Decide whether to migrate the app's local `types/` to consume `@repo/shared-types` from
   `packages/shared`, or intentionally keep them separate — currently undecided/unverified.
4. Add basic automated tests (component and/or API-layer) — none exist today.
5. Confirm whether a backend/service under `/services` is in scope for this milestone, or whether the
   external mock API is sufficient for the remainder of the project.
