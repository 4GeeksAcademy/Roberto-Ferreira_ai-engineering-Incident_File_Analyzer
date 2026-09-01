---
name: verify-frontend-typecheck
description: Run and confirm a clean TypeScript strict-mode typecheck for uis/talent-pipeline-tracker before considering any frontend change in this app complete. Use whenever files under uis/talent-pipeline-tracker are added, edited, or removed.
---

# Skill: Verify Frontend Typecheck

## Objective

Confirm that a change made to `uis/talent-pipeline-tracker` compiles cleanly under TypeScript `strict`
mode before the change is considered done, formalizing the check step already required by
[`AGENTS.md`](../../../AGENTS.md) Section 2 ("Run the checks that exist for the touched project").

## When to use

- Any time a file under `uis/talent-pipeline-tracker/**` (app routes, components, lib, types) was
  created, edited, or deleted in the current session.
- Before updating `memory-bank/progress.md` to mark a frontend task as done.

## Inputs

| Input | Description | Where it comes from |
| --- | --- | --- |
| `project_dir` | Path to the Next.js app | `uis/talent-pipeline-tracker` (fixed — this is the only frontend in the repo, verified in `memory-bank/techContext.md`) |
| `command` | The typecheck script | `npm run typecheck`, defined in `uis/talent-pipeline-tracker/package.json` (`"typecheck": "tsc --noEmit"`) |
| `changed_files` | List of files touched in the session that fall under `project_dir` | Derived from the current diff/working tree |

## Steps

1. Confirm `changed_files` includes at least one file under `uis/talent-pipeline-tracker`. If not, this
   skill does not apply — skip it.
2. Run `npm run typecheck` inside `uis/talent-pipeline-tracker`.
3. Capture the exit code and full output.
4. Report the result before proceeding to commit.

## Acceptance criteria (pass/fail, objectively checkable)

- **Pass:** `npm run typecheck` exits with code `0` and prints no `error TS####` lines.
- **Fail:** exit code is non-zero, OR the output contains one or more lines matching `error TS\d+`. On
  fail, the change is NOT considered complete and must not be recorded as done in
  `memory-bank/progress.md`.
- The skill's own report must state the literal exit code and, on failure, quote the first failing
  `error TS####` line — a subjective "looks fine" statement does not satisfy this skill.

## Recurrence in this project

This is not a hypothetical task: `uis/talent-pipeline-tracker/tsconfig.json` sets `"strict": true`, and
`package.json` defines a dedicated `typecheck` script specifically because there is no build/CI step yet
in this repo (`memory-bank/progress.md` notes no CI/test setup exists). Every future change to this app
(new fields on `RecordBase`, new routes, new components) will re-trigger this exact verification step, so
it is documented once here rather than re-derived per session.
