# Tech Context

This file captures the verified project architecture and implementation choices for the Brasaland
Talent Pipeline Tracker and related company repo structures.

## Repository layout

- `uis/` contains the user-facing product experiences: `website/`, `backoffice/`, and the main
  `talent-pipeline-tracker/` app.
- `agents/` is where AI assistants live. The repo includes a general template and a concrete agent for
  candidate pipeline support.
- `skills/` holds reusable capabilities such as research and analysis; template and real examples live
  here.
- `packages/shared/` is the repository's shared library boundary for reusable domain modules and types.
- `services/` remains a documentation-only placeholder because the backend API is external to this repo.

## Verified technical stack

### Frontend stack

- Next.js 15.4.6 with App Router
- React 19 and React DOM 19
- TypeScript 5.8.3 in strict mode
- `npm run typecheck` via `tsc --noEmit`
- `npm run build` via Next.js production build

### AI and reusable code stack

- Python 3 standard library for simple agent logic and tests
- Node.js built-in test runner for validating shared JS modules
- Domain-facing shared helpers are kept in `packages/shared/` so they can be reused by future UIs or agents

## Architecture notes

### Candidate-tracker app

The main app under `uis/talent-pipeline-tracker/` follows a simple app-router structure:

- `/` — candidate list view
- `/candidates/new` — create candidate form
- `/candidates/[id]` — detail and notes view
- `/candidates/[id]/edit` — edit page

Shared patterns include:

- typed API access in `lib/api-client.ts` and `lib/records.ts`
- human-readable status/stage mapping in domain type files
- reusable form logic in `components/candidate-form.tsx`

### Agent design pattern

Agents in this repo should do one of two things:

1. make the hiring workflow more actionable for recruiters,
2. encapsulate a repeatable decision-making pattern that other tools can reuse.

The concrete agent in `agents/talent-ops-agent/` follows this pattern by summarizing pipeline health,
flagging candidates needing attention, and generating next-step recommendations.

### Shared module design pattern

The shared package at `packages/shared/` is a place for low-level, reusable logic that is not app-specific.
This includes:

- candidate status/stage label mapping,
- domain-level helper functions,
- future schema definitions or metadata utilities.

## API contract constraints

The API contract must not be changed. The following values are treated as canonical:

- status: `received`, `in_progress`, `selected`, `discarded`
- stage: `pending`, `review`, `personal_interview`, `technical_interview`, `offer_presented`

Human-friendly labels must be rendered in the UI instead of raw API values.

## Constraints and risks

- No backend service is implemented in this repo; the generated app depends on the centrally deployed mock API.
- `NEXT_PUBLIC_API_URL` must be configured in the local environment for runtime API usage.
- The project remains intentionally lightweight and documentation-first until the real service contract is available.
- Shared code must remain compact, explicit, and easy to test.

## Decision log

- Use a repo-level memory bank as the source of truth for product and architecture context.
- Keep the app UI decoupled from raw API strings by mapping them to labels in one layer.
- Keep agent and skill implementations small but reusable; avoid empty templates.
- Prefer direct, documented shared modules over hidden logic scattered across apps.
