# backoffice

Brasaland Digital's internal operations dashboard.

- **Objective:** give internal teams a dashboard shell — distinct from the public `website` layout —
  surfacing company-relevant business data straight from [`CONTEXT.md`](../../CONTEXT.md): the active
  hiring search and the candidate status/stage label reference.
- **Stack:** Next.js 15.4.6 (App Router), React 19.1.0, TypeScript 5.8.3 (strict). Same versions as the
  other apps in `uis/`.
- **Structure:** `app/` (routes: `/`), `components/` (`SidebarNav`, `TopBar`, `DashboardShell`,
  `ActiveSearchCard`, `StatusStageReference`).
- **Data note:** all content is static, sourced directly from CONTEXT.md — there is no backend/service
  wired up yet (see [`../../services/README.md`](../../services/README.md)).
- **Run locally:**
  ```bash
  npm install
  npm run dev
  ```
- **Verify:** `npm run typecheck` (TypeScript strict, no build step configured yet).
