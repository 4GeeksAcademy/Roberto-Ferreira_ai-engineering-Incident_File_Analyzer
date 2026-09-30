# Talent Pipeline API

This service provides the mock API required by the Brasaland Talent Pipeline Tracker.

## Purpose

It exposes the same record and note endpoints expected by the frontend app under `uis/talent-pipeline-tracker`.

## Endpoints

- `GET /records`
- `GET /records/:id`
- `POST /records`
- `PUT /records/:id`
- `PATCH /records/:id`
- `GET /records/:id/notes`
- `POST /records/:id/notes`
- `DELETE /records/:id/notes/:noteId`

## Run locally

```bash
cd services/talent-pipeline-api
npm install
npm start
```

The service listens on `http://localhost:4100`.

## Frontend config

Set the app environment to:

```env
NEXT_PUBLIC_API_URL=http://localhost:4100
```
