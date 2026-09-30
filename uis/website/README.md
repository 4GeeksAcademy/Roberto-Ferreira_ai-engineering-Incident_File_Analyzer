# website

Brasaland's public-facing corporate website.

- **Objective:** render the company's public identity (name, industry, locations, HQ) for external
  visitors, sourced from [`CONTEXT.md`](../../CONTEXT.md).
- **Stack:** Next.js 15.4.6 (App Router), React 19.1.0, TypeScript 5.8.3 (strict). Same versions as the
  other apps in `uis/`.
- **Structure:** `app/` (routes: `/`), `components/` (reusable presentational pieces — `SiteHeader`,
  `Hero`, `CompanyHighlights`, `StatCard`, `LocationsSection`, `SiteFooter`).
- **Run locally:**
  ```bash
  npm install
  npm run dev
  ```
- **Verify:** `npm run typecheck` (TypeScript strict, no build step configured yet).
