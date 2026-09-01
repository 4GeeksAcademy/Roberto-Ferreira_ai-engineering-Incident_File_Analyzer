# Project Brief

Source of truth: [CONTEXT.md](../CONTEXT.md)

## Business description

Brasaland is a grilled-food restaurant chain with 14 locations across Colombia and Florida. This
project is owned by the **Brasaland Digital** team, the company's internal technology unit that builds
tools for operational teams.

## The problem

Ashley Turner (People Manager) can no longer run the **Executive Assistant** hiring process in a shared
Google Sheet: over a hundred applications, three people editing the file simultaneously, and a save
conflict that already destroyed the data of two candidates.

## Project objective

Build a **Talent Pipeline Tracker** — a candidate management web app — so recruiters can:

- See all candidates at a glance (name, position, status, stage).
- Filter by status and stage, and search by name or email, without a page reload.
- Open a candidate's detail view and update their status or stage.
- Add internal notes after calls/interviews, and delete notes that are no longer needed.
- Register candidates who apply through other channels, and correct bad data.

## Active search context (current hiring req used to validate the tool)

| Field    | Value                                                                              |
| -------- | ----------------------------------------------------------------------------------- |
| Position | Executive Assistant                                                                 |
| Company  | Brasaland                                                                            |
| Location | Corporate headquarters, Medellín                                                    |
| Profile  | Executive support experience, calendar and travel management, professional English  |

## Non-negotiable product rules (from CONTEXT.md)

- Raw API values (e.g. `in_progress`, `personal_interview`) must never be shown in the UI — always use
  the human-readable labels.
- Notes are visible only inside the candidate detail view.
- The registration/create form must include every field required by the API.
