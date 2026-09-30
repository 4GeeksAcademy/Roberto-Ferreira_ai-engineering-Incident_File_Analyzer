from __future__ import annotations

import io
import csv
import sys
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from analyzer_core import analyze_csv, results_csv  # noqa: E402

app = FastAPI(title="Incident Analyzer API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
last_summary: dict | None = None


@app.get("/")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "incident-analyzer-api"}


@app.post("/api/incidents/analyze")
async def analyze_incidents(file: UploadFile = File(...)) -> dict:
    global last_summary
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a CSV file.")
    content = await file.read()
    if not content.strip():
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")
    try:
        summary = analyze_csv(io.StringIO(content.decode("utf-8")))
    except (UnicodeError, csv.Error, ValueError) as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    last_summary = summary
    return summary


@app.get("/api/incidents/results/export")
async def export_results() -> Response:
    if last_summary is None:
        raise HTTPException(status_code=404, detail="No analysis has been run yet.")
    return Response(
        content=results_csv(last_summary),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=results.csv"},
    )
