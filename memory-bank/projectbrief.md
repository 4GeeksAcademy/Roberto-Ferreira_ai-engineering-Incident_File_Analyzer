# Project Brief

Source of truth: [CONTEXT.md](../CONTEXT.md)

## Business description

Brasaland is a grilled-food restaurant chain with 14 locations across Colombia and Florida. This
project is owned by the **Brasaland Digital** team, the company's internal technology unit that builds
operational tools for hiring, people operations, and daily restaurant support.

## Problem statement

Ashley Turner, People Manager, can no longer manage the **Executive Assistant** hiring process in a
shared Google Sheet. The data set is too large for a spreadsheet workflow, multiple people edit the same
file at the same time, and a save conflict already destroyed candidate data. The company needs a shared
source of truth that keeps candidate status, notes, and progression organized.

## Project objective

Build a **Talent Pipeline Tracker** so recruiters can:

- See all candidates at a glance: name, position, status, and stage.
- Filter by status and stage and search by name or email without reloading the page.
- Open a candidate's detail view and adjust status or stage as decisions evolve.
- Add internal interview notes and remove obsolete notes when needed.
- Register candidates coming from non-standard channels and fix incorrect data quickly.

## Core stakeholders

- **Ashley Turner** — People Manager; operational owner of the hiring process.
- **Nicolás Park** — CTO; sponsor for the tooling and delivery priority.
- **Brasaland Digital** — internal engineering team delivering the product.
- **Recruiters and interviewers** — end users who need clear pipeline visibility.

## Active hiring context

| Field    | Value                                                                             |
| -------- | ---------------------------------------------------------------------------------- |
| Position | Executive Assistant                                                                |
| Company  | Brasaland                                                                         |
| Location | Corporate headquarters, Medellín                                                 |
| Profile  | Executive support experience, calendar and travel management, professional English |

## Non-negotiable product rules

- Raw API values such as `in_progress` or `personal_interview` must never be rendered in the UI.
- Notes are visible only inside the candidate detail view.
- The create/register form must include every field required by the API contract.
- The app must avoid destructive spreadsheet behavior by making updates explicit and traceable.

## Success definition

The milestone is accepted when the repository includes:

- a working candidate-tracking frontend,
- a documented memory bank with company context and decisions,
- a real reusable AI agent or skill implementation,
- and a clean shared pattern for future project modules.
