# AGENTS.md

This file is the enforceable protocol for any coding agent (human-directed or autonomous) working in
this repository. It applies to every session, in every folder, unless a more specific `AGENTS.md` or
`.agents/rules/*.md` file overrides it for its own subtree.

## 1. Required reading before starting any session

Before making any change, an agent MUST read, in this order:

1. [`CONTEXT.md`](./CONTEXT.md) — the company briefing (business domain, constraints, acceptance rules).
2. [`memory-bank/projectbrief.md`](./memory-bank/projectbrief.md) — business description, objective, problem solved.
3. [`memory-bank/techContext.md`](./memory-bank/techContext.md) — verified tech stack, architecture, constraints.
4. [`memory-bank/progress.md`](./memory-bank/progress.md) — current state of development and open next steps.

If any of these four files is missing, stop and flag it instead of proceeding on assumptions.

## 2. Mandatory workflow before any commit

Every change set MUST go through these steps, in order, before it is committed:

1. **Re-read [`memory-bank/progress.md`](./memory-bank/progress.md)** to confirm the change doesn't
   duplicate or contradict already-recorded state.
2. **Make the change in the smallest relevant scope** (the specific app/service/folder owning the
   change) — do not spread edits across unrelated top-level folders in the same change set.
3. **Run the checks that exist for the touched project** (e.g. `npm run typecheck` and/or `npm run build`
   inside `uis/talent-pipeline-tracker` for frontend changes; the relevant test/lint command for any
   other project that defines one). If no check script exists for that project, state that explicitly
   instead of skipping silently.
4. **Update [`memory-bank/progress.md`](./memory-bank/progress.md)** to reflect exactly what changed,
   what was verified, and what remains — only mark something done if it was actually verified in this
   session.
5. **Commit with a message describing the verified change**, then push only after the developer has
   confirmed the diff (see Section 3 for exceptions requiring explicit confirmation first).

## 3. Files and folders requiring explicit developer confirmation before modification

The agent MUST NOT modify the following without the developer explicitly confirming it first, because
they define shared/company-wide context, external contracts, or destructive/irreversible operations:

| Path | Why it's protected |
| --- | --- |
| [`CONTEXT.md`](./CONTEXT.md) / [`CONTEXT.es.md`](./CONTEXT.es.md) | Single source of truth for the company; changing it silently would invalidate every other file derived from it (memory-bank, app copy, domain rules). |
| `memory-bank/` (all files) | Persistent cross-session state; must only change as a deliberate, reviewed step (see Section 2), never as a side effect of an unrelated task. |
| `packages/shared/` | Shared types (`@repo/shared-types`) consumed (or intended to be consumed) by multiple apps — a change here can silently break other projects. |
| `docker-compose.yml` (root, once created) | Orchestrates the whole local stack (`services/`, databases, containers) per the repo's own README convention — a bad edit affects every service at once. |
| `.github/` (workflows, `copilot-instructions.md`) | CI/CD and agent-facing configuration; changes here affect automation and every future agent session, not just the current task. |
| `uis/talent-pipeline-tracker/lib/api-client.ts` and `lib/records.ts` | Encode the mock API contract described in CONTEXT.md ("no adaptation required"); changing the contract here without confirmation risks silently breaking API compatibility. |
| Any `.env`, `.env.local`, or secret/credential file | Runtime configuration and secrets must never be created, overwritten, or committed without explicit developer sign-off. |
| `.git/` history rewrites (force-push, reset --hard, amending pushed commits) | Irreversible for a shared branch (`main`); always ask first. |

Any other file not listed here may be edited freely as part of a well-scoped task, following the workflow
in Section 2.
