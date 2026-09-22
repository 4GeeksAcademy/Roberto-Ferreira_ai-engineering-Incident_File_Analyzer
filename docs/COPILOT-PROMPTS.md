# Copilot Agent Prompt Set: Incident File Analyzer

Phased, declarative prompts for the VS Code Copilot agent. Each prompt states expected outcomes, authoritative sources, deliverables, constraints, and out-of-scope work. Technical values (field names, categories, statuses, expected results) are never restated here; they come from `CONTEXT-company.md`.

## How to use

1. Save the project README as `docs/PROJECT-BRIEF.md` in the fork, and confirm `CONTEXT-company.md` and `incidents-COMPANY.csv` are in the repo so the agent can inspect them.
2. Run the prompts in order, each in a fresh agent session.
3. Do not start the next phase until the current phase's report passes its gate.
4. Commit after every gate so a later phase can be rolled back cleanly.
5. Paste each final report back for review before moving on.

| Phase | Focus | Gate |
|-------|-------|------|
| 0 | Context and architecture (no feature code) | CONTEXT rules confirmed; shared-module location approved |
| 1 | Shared logic and `analyze.py` | Every metric matches CONTEXT; console screenshot taken |
| 2 | Backend endpoints | API JSON matches script; every error case verified |
| 3 | Backoffice page | Real file uploaded; numbers match; UI screenshot taken |
| 4 | Audit and PR readiness | Checklist evidenced; PR draft ready |

---

## Phase 0: Context and Architecture (no feature code)

```
# PHASE 0 — PROJECT CONTEXT AND ARCHITECTURE

## Expected outcome
The repository ends this phase with (a) a persistent instructions file that
every later agent session inherits, and (b) an architecture decision document
that settles where shared analysis logic lives. No feature code exists at the
end of this phase.

## Authoritative sources (inspect before writing anything)
- docs/PROJECT-BRIEF.md — defines what must be delivered and how it is evaluated
- CONTEXT-company.md — defines exact CSV field names, required fields, valid
  categories, allowed statuses, and expected output values
- incidents-COMPANY.csv — the 100-record test file (locate it in the repo)
- The monorepo itself: root layout, scripts/, services/api/, uis/backoffice/,
  package/dependency manifests, existing conventions, existing tests, README files

## Deliverables
1. .github/copilot-instructions.md containing:
   - the project purpose in a few sentences
   - the standing rules block below, verbatim
   - the exact CSV field names, valid categories, allowed statuses, and expected
     values, transcribed from CONTEXT-company.md (or a precise pointer to the
     file where transcription would risk drift)
   - the target folder structure: scripts/analyze.py, scripts/incidents-COMPANY.csv,
     services/api/, uis/backoffice/
2. docs/ARCHITECTURE-DECISION.md containing:
   - the technology stack actually found in services/api and uis/backoffice
     (framework, language, package manager, test runner), each backed by a file path
   - the recommended location and import strategy for a single shared analysis
     module that both scripts/analyze.py and the API can import without any
     duplicated logic, with the alternatives considered and the reason for the pick
   - how "last analysis" state is held for the export endpoint
   - open questions or ambiguities found in the brief or CONTEXT
3. A restatement of the CONTEXT rules (fields, categories, statuses, what makes
   a record invalid, how the satisfaction average is defined, and every expected
   value) so the human can confirm the agent read them correctly.

## Standing rules (to be embedded in the instructions file)
- Requirements, evaluation criteria, and screenshots define WHAT must be delivered.
- Repository instructions and approved prior artifacts define project context.
- Source code, configuration, dependencies, tests, and verified runtime behavior
  define technical facts. Important claims are verified against the repository.
- Uncertainty is reported explicitly; guesses are never presented as facts.
- Field names, categories, statuses, and expected values come only from
  CONTEXT-company.md; nothing generic is substituted.
- Validation and analysis logic exists in exactly one shared module; the script
  and the API both consume it.
- Invalid records are counted, classified by reason, and reported, never silently dropped.
- Work stays inside the phase currently being executed.

## Constraints and scope boundaries
- Existing repository files remain untouched except for the two deliverables above.
- The architecture decision is a recommendation awaiting human approval.

## Must not
- Write analysis logic, endpoints, UI components, or tests.
- Install dependencies or modify manifests.
- Assume a stack, path, or value that was not verified in the repository.

## Final report
- Files created, with paths
- The restated CONTEXT rules and expected values
- Stack facts discovered, each with its source file
- Ambiguities and questions for the human
- Confirmation that no feature code was written
```

**Gate:** confirm the restated CONTEXT rules match your file and approve the shared-module location.

---

## Phase 1: Shared Logic and the Analysis Script

```
# PHASE 1 — SHARED ANALYSIS MODULE AND analyze.py

## Expected outcome
A single shared analysis module exists, along with scripts/analyze.py that
consumes it. Running `python analyze.py incidents-COMPANY.csv` on the 100-record
file produces output whose values match the expected values in
CONTEXT-company.md exactly.

## Authoritative sources
- .github/copilot-instructions.md and docs/ARCHITECTURE-DECISION.md (approved
  location and import strategy for the shared module)
- CONTEXT-company.md — field names, required fields, valid categories, allowed
  statuses, expected values
- docs/PROJECT-BRIEF.md — the Phase 1 section and the Script evaluation criteria
- incidents-COMPANY.csv — the real input for verification

## Expected behavior of the shared module
- Loads a CSV and evaluates every record against the CONTEXT rules.
- A record is invalid when it lacks at least one required field or holds a value
  outside the allowed statuses or categories. Each invalid record carries its
  reason(s), and results include counts by reason type.
- Metrics are computed on valid records only: valid and invalid totals reported
  separately, category breakdown, status breakdown, and the average satisfaction
  index over closed cases that have a recorded score (using the CONTEXT's
  definition of "closed" and its score field).
- Output is a plain, serializable data structure with no console or web concerns.
- Reading strategy remains sound for a production file that could reach one
  million rows; the choice (native or pandas) is justified in the report.

## Expected behavior of scripts/analyze.py
- Accepts the CSV path as a command-line argument and runs without code changes.
- Prints a readable console summary with separators, clear labels, and aligned
  values, covering all five required metrics and the invalid-record detail.
- Ends by asking `Export results to CSV? [y / n]`; on `y`, writes results.csv
  with one row per metric; on `n`, exits cleanly.
- Missing file, unreadable file, and missing required columns produce clear
  messages and a non-zero exit.

## Deliverables
- The shared module at the approved location
- scripts/analyze.py
- Automated tests asserting the CONTEXT's expected values against the real
  100-record file, plus edge cases (missing field, out-of-range status, out-of-range
  category, closed case without score, empty file)
- Final report

## Constraints
- Test expectations are derived from CONTEXT-company.md, never from the code's own output.
- If the computed results differ from the CONTEXT's expected values, the difference
  is reported with the records responsible; the logic is not bent to force a match
  and the expected values are not edited.
- The CSV serialization used for results.csv is a reusable function so the future
  export endpoint can share it.

## Must not
- Touch services/api or uis/backoffice.
- Duplicate validation or metric logic inside analyze.py.
- Send record contents to any external service (the data is sensitive).
- Guess an ambiguous rule silently; ambiguities are listed in the report.

## Final report
- Files created or changed
- A side-by-side table: each metric, expected value (with CONTEXT source), actual value, match yes/no
- Test command and its result
- The exact console output from the run on the 100-record file
- Reading strategy chosen and why
- Ambiguities, deviations, or unverified assumptions
```

**Gate:** every metric matches CONTEXT. Take the console screenshot for the PR now.

---

## Phase 2: Backend API

```
# PHASE 2 — BACKEND ENDPOINTS

## Expected outcome
services/api exposes two working endpoints that use the shared analysis module
from Phase 1, and the JSON returned for the 100-record file carries the same
values as the script's output.

## Authoritative sources
- .github/copilot-instructions.md, docs/ARCHITECTURE-DECISION.md
- docs/PROJECT-BRIEF.md — the Backend section and Backend evaluation criteria
- The shared module, its tests, and the CSV serializer from Phase 1
- The existing services/api code, conventions, and dependency manifests
- CONTEXT-company.md and incidents-COMPANY.csv

## Expected behavior
- POST /api/incidents/analyze accepts a CSV as multipart/form-data, runs the
  shared analysis, stores it as the "last analysis", and returns the summary as
  JSON covering: valid and invalid totals, invalid counts by reason, category
  breakdown, status breakdown, and average satisfaction.
- GET /api/incidents/results/export returns the last analysis as a downloadable
  CSV with the same row structure as the script's results.csv, produced by the
  shared serializer.
- Input problems return appropriate HTTP status codes with descriptive messages:
  empty file, non-CSV or unreadable content, missing required columns, and export
  requested before any analysis exists.
- A browser running the backoffice dev server can call both endpoints (cross-origin
  access configured to match repository conventions).

## Deliverables
- Endpoint implementation following the existing services/api structure
- Automated tests for success, each error case, and JSON-versus-script parity on
  the 100-record file
- Brief API usage notes (in the existing docs location, or a short README section)
- Final report

## Constraints
- The endpoint layer contains no validation or metric logic of its own; it
  delegates to the shared module.
- Dependencies are added only when required, and each addition is listed in the report.
- The existing project conventions (routing, error format, config) are followed.

## Must not
- Modify shared logic or the script's behavior; a needed change is reported as a
  finding instead.
- Touch uis/backoffice.
- Persist uploaded customer data to disk or logs beyond what the last-analysis
  summary requires.

## Final report
- Files created or changed
- Endpoint contract: method, path, request, success response example, and each
  error case with status code and message
- Test command and its result
- Evidence of parity: the API's JSON values next to the script's expected values
- Anything unverified, including how the server was started and exercised
```

**Gate:** curl or the API docs show the JSON matching the script, and every error case behaves as described.

---

## Phase 3: Frontend

```
# PHASE 3 — BACKOFFICE INCIDENT ANALYSIS PAGE

## Expected outcome
uis/backoffice contains an incident analysis page reachable from the application
menu. A user uploads the CSV in the browser, sees the analysis on screen, is told
about invalid records, and can download the results as CSV without using a terminal.

## Authoritative sources
- .github/copilot-instructions.md, docs/ARCHITECTURE-DECISION.md
- docs/PROJECT-BRIEF.md — the Frontend section and Frontend evaluation criteria
- The API contract in the Phase 2 report and the running endpoints
- The existing uis/backoffice code: routing, menu, layout, components, styling
  conventions, API-calling patterns, configuration for the backend base URL
- CONTEXT-company.md for category and status labels as they must appear

## Expected behavior
- A menu entry leads to the page, consistent with existing navigation.
- File upload works by drag and drop and/or a file selector, sends the CSV to
  POST /api/incidents/analyze, and shows loading and error states with the API's
  descriptive messages.
- The results appear in clearly separated sections: general metrics (valid,
  invalid, total), category breakdown, status breakdown, and the average
  satisfaction index.
- When invalid records exist, an understandable notice states how many there are
  and how many of each reason type.
- A download button retrieves the CSV from GET /api/incidents/results/export.
- The page reads clearly with the real 100-record file loaded.

## Deliverables
- Page, upload component, results components, and menu wiring, following the
  existing backoffice conventions
- Automated tests where the repository already has a frontend test setup
- Final report

## Constraints
- Displayed values come from the API response only; no metric is recomputed in the browser.
- Backend base URL comes from configuration following existing repo conventions.
- Visual style follows the existing backoffice design.

## Must not
- Modify shared analysis logic, the script, or backend endpoints. If the API
  contract blocks the UI, the issue is reported rather than patched.
- Add UI libraries without necessity, or without listing them in the report.
- Store uploaded data in browser storage.

## Final report
- Files created or changed
- How to run backend and frontend together, and the exact steps to reproduce the
  page with the 100-record file
- What was verified in a running browser versus only by reading code
- Any contract mismatches or unresolved items
```

**Gate:** upload the real file, check the numbers against Phase 1, and take the UI screenshot for the PR.

---

## Phase 4: Audit and PR Readiness

```
# PHASE 4 — CROSS-CUTTING AUDIT AND PR PREPARATION

## Expected outcome
The repository state satisfies every evaluation criterion in the brief, with
evidence, and a pull request description is ready for the human to submit.

## Authoritative sources
- docs/PROJECT-BRIEF.md — the "What we will evaluate" section and the submission structure
- CONTEXT-company.md — expected values
- The whole repository as it stands after Phases 1–3, its tests, and actual runtime behavior

## Deliverables
1. An evaluation-criteria checklist. Each criterion (Script, Backend, Frontend,
   Cross-cutting) is marked met, partially met, or not met, with file paths or
   command output as evidence.
2. A verification that the folder structure matches the submission layout
   (scripts/, services/api/, uis/backoffice/, test CSV in scripts/).
3. Proof that validation and analysis logic exists once: a search showing no
   duplicated logic in the script, API, or UI.
4. A full test run across all layers, with results.
5. A short run guide (how to run the script, API, and UI) in the appropriate README.
6. A draft PR description with clearly marked placeholders where the human
   attaches the console screenshot and the web-interface screenshot.

## Constraints
- Changes are limited to defects found by the audit, README run instructions,
  and the PR draft. Each change is listed with its reason.
- Findings that need a design decision are reported instead of fixed.

## Must not
- Add features, refactor working code, or change expected values.
- Push, open the pull request, or merge anything.
- Mark a criterion as met without evidence.

## Final report
- The completed checklist
- Defects found and fixed, and defects found but deferred
- Test results
- The PR description draft
- Remaining risks or unverified areas
```

---

## Notes

- If an agent asks a clarifying question in Phases 1 to 3, answer it from `CONTEXT-company.md` and do not let it guess. That is the source-of-truth rule working as intended.
- Treat any report that claims a match without a side-by-side table of expected versus actual values as unverified, and send it back.
