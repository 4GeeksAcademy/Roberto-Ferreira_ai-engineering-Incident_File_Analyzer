# Backend Architecture Proposal

## Evidence basis

This repository is the only authority for business and product decisions in
this proposal: `CONTEXT.md`, the top-level and `services/` guidance, and the
Talent Pipeline Tracker's existing API client and record types. External
FastAPI references below are used only to research framework conventions; they
are not authoritative sources for Brasaland requirements. The repository does
not yet define authentication roles, candidate retention rules, a database
technology, or a concurrency policy, so those are explicitly left as decisions
to validate before implementation.

The current tracker consumes a centrally deployed, course-shared mock API.
This proposal describes the structure of a future Brasaland-owned service; it
does not propose changing the current service in this milestone. Its recruiting
module must preserve the tracker’s documented record, note, status, stage, and
pagination contract when that future service is introduced.

## Scope and decision

Brasaland Digital should introduce one centralized FastAPI application at
`services/api/`, using a **layered modular monolith**. It is a deliberately
small starting point: the Talent Pipeline Tracker is the immediate consumer,
but the same service can later host the locations, menu, and orders modules
identified in the company context. This follows the repository convention that
`services/` holds the company's centralized API and avoids premature
microservices.

The first module should be `recruiting`. Ashley Turner's urgent workflow has
more than one hundred Executive Assistant applications and three simultaneous
editors. The critical flows are finding candidates by name or email, changing
their status and stage, correcting application data, and keeping an auditable
set of internal interview notes. A layered design separates HTTP concerns from
the rules that protect those workflows and from database access. In particular,
it provides a single place to validate valid stage/status values and to ensure
that note deletion and candidate updates are handled consistently rather than
being implemented differently in each endpoint.

This is not MVC: FastAPI routes are HTTP adapters, not controllers that own
business rules. It is also not serverless or a microservice suite. Brasaland's
current scope is one internal tool with a small expected module set; one
deployable service keeps authentication, migrations, observability, and shared
data access coherent while the product is still evolving.

## Proposed layout

```text
services/
  api/
    app/
      main.py                    # application creation and router inclusion
      core/
        config.py                # validated settings and environment access
        security.py              # authentication and authorization primitives
      api/
        deps.py                  # request-scoped shared dependencies
        v1/
          router.py              # version-1 router aggregation
          recruiting.py          # recruiting HTTP endpoints
          branches.py            # future branch HTTP endpoints
          menu.py                # future menu HTTP endpoints
          orders.py              # future order HTTP endpoints
      domains/
        recruiting/
          schemas.py             # request/response validation contracts
          service.py             # candidate and note use cases
          repository.py          # persistence queries and mutations
          models.py              # candidate and note persistence models
        branches/
        menu/
        orders/
      db/
        session.py               # engine, sessions, and transaction boundary
        base.py                  # model registration for migrations
    tests/
      api/
      domains/
```

The primary separation criterion is **business domain**, not technical type:
candidate records and their notes live together because notes only make sense
within a candidate review. Within each domain, schemas define the external API
contract, services coordinate business rules, repositories isolate persistence,
and models represent stored data. Shared cross-cutting concerns stay in `core`,
`api/deps.py`, and `db` so domains do not reach into each other's storage or
configuration details.

`recruiting` should remain independent from future `branches`, `menu`, and
`orders` modules. This matters because candidate privacy, retention, and HR
permissions differ from restaurant ordering and branch operations, even though
all are Brasaland systems. Shared facilities such as configuration, identity,
logging, and database sessions may be reused; business services and
repositories should not be reused across domains.

## Router organization

The app should expose a versioned API namespace, such as `/api/v1`, with the
version router aggregating domain routers. The recruiting router owns the
candidate-record collection, an individual candidate record, a candidate's
workflow transition, and the nested notes collection. The current Next.js
client already calls the equivalent operations: list records, fetch one,
create, replace, update status/stage, list notes, add a note, and delete a
note. The backend should retain those responsibilities under the recruiting
router rather than spreading them through a generic notes router.

```mermaid
flowchart LR
  UI[Talent Pipeline Tracker] --> API[/api/v1]
  API --> Recruiting[recruiting router]
  API --> Branches[branches router - future]
  API --> Menu[menu router - future]
  API --> Orders[orders router - future]
  Recruiting --> CandidateService[candidate and notes services]
  CandidateService --> RecruitingRepository[recruiting repository]
  RecruitingRepository --> Database[(database)]
```

Search, status, and stage filters should be query parameters on the recruiting
collection, so filtering happens on the server as application volume grows.
The list response should preserve pagination metadata (`total`, `page`, and
`limit`), matching the interface currently defined by the frontend. Candidate
transition handling should validate the documented `received`, `in_progress`,
`selected`, and `discarded` statuses and the five recruiting stages; the UI can
continue to translate these API values into human-readable labels.

## FastAPI conventions researched

The proposal follows the official FastAPI documentation, **"Bigger
Applications - Multiple Files"** (FastAPI Docs,
https://fastapi.tiangolo.com/tutorial/bigger-applications/). Its use of
`APIRouter`, router inclusion from the application entry point, and shared
dependencies informs `api/v1/router.py`, the domain routers, and `api/deps.py`.

It also follows the structure demonstrated by the official **FastAPI
Full-Stack Template** (FastAPI GitHub organization,
https://github.com/fastapi/full-stack-fastapi-template): configuration is kept
outside route handlers, schemas are distinct from ORM models, and API routes
are grouped independently from CRUD/persistence concerns. This repository does
not need to copy that template wholesale. The proposed `domains/<domain>/`
layout combines each business capability's schema, service, repository, and
models, which is easier to navigate while Brasaland has only a few modules.

## Frontend and backend coexistence

The Talent Pipeline Tracker in `uis/talent-pipeline-tracker/` and the FastAPI
application are separate deployable systems. The frontend's API client already
uses `NEXT_PUBLIC_API_URL` and JSON requests; the backend should publish a
versioned OpenAPI contract that mirrors its record, note, error, and paginated
response shapes. Contract changes must be versioned or coordinated, because
the frontend uses the record fields and `ApiResult` shape directly.

In development and production, the backend must configure FastAPI CORS with an
explicit allow-list of the deployed tracker origin(s), permitted methods, and
headers. It must not use a wildcard origin when credentials or authenticated HR
operations are enabled. Browser access should be restricted to the Next.js UI,
while service-to-service access is authenticated separately.

Environment variables belong to the system that consumes them. The Next.js app
may expose only non-secret `NEXT_PUBLIC_*` values such as the API base URL.
Backend variables, including database URLs, signing keys, credentials, allowed
origins, and runtime environment, must be read and validated in
`app/core/config.py` and never be placed in frontend-prefixed variables or
committed configuration files. Each system should provide its own documented
example environment file with placeholder values.

## Risks and Points of Attention

1. If route handlers directly query and mutate database models, validation of
   candidate transitions and permissions will drift across create, edit, and
   status-update flows. For a process already harmed by concurrent spreadsheet
   edits, inconsistent updates would recreate lost or misleading candidate
   state in a more opaque form.
2. If candidates and notes are not kept in a recruiting boundary, a generic
   cross-domain notes implementation could expose internal interview comments
   through unrelated systems or make privacy and retention controls difficult
   to enforce.
3. If the UI calls an unversioned, undocumented API, small response changes can
   break the tracker’s list, detail, and note views without a clear migration
   path. The risk rises as Brasaland adds menu, branch, and order capabilities.
4. If CORS and environment ownership are treated as an afterthought, local
   development will fail across the separate origins, or secrets may be exposed
   by accidentally placing them in `NEXT_PUBLIC_*` variables.

## Next architectural checkpoint

Before implementation, Brasaland should confirm authentication roles for People
Managers and recruiters, candidate-data retention requirements, and whether
concurrent edits require optimistic locking or an audit history. Those choices
belong in the recruiting domain service and persistence design, not in the
frontend alone.