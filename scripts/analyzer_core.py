"""Shared Brasaland incident CSV validation and analysis logic."""
from __future__ import annotations

import csv
import io
from collections import Counter
from dataclasses import dataclass
from statistics import fmean
from typing import Iterable, TextIO

# Brasaland incident context: `.project_requirements/CONTEXT-brasaland.en.md`.
REQUIRED_FIELDS = (
    "incident_id",
    "date",
    "location_id",
    "category",
    "description",
    "status",
    "reporter_id",
)
CATEGORY_FIELD = "category"
STATUS_FIELD = "status"
SATISFACTION_FIELD = "satisfaction_score"
ALLOWED_CATEGORIES: frozenset[str] = frozenset(
    {"CUSTOMER_COMPLAINT", "EQUIPMENT", "SUPPLY", "FOOD_QUALITY", "STAFF"}
)
CATEGORY_ORDER = (
    "CUSTOMER_COMPLAINT",
    "EQUIPMENT",
    "SUPPLY",
    "FOOD_QUALITY",
    "STAFF",
)
ALLOWED_STATUSES: frozenset[str] = frozenset({"OPEN", "CLOSED", "DISCARDED"})
CLOSED_STATUS = "CLOSED"
STATUS_ORDER = ("OPEN", "CLOSED", "DISCARDED")
VALID_LOCATIONS: frozenset[str] = frozenset(
    {f"COL-{number:02d}" for number in range(1, 11)}
    | {f"FLA-{number:02d}" for number in range(1, 5)}
)


@dataclass(frozen=True)
class InvalidRecord:
    row_number: int
    reasons: tuple[str, ...]


def _validation_reasons(row: dict[str, str]) -> list[str]:
    reasons: list[str] = []
    for field in ("incident_id", "date", "status"):
        if not row.get(field, "").strip():
            reasons.append(f"missing_field:{field}")
    if row.get(STATUS_FIELD, "").strip() and row[STATUS_FIELD] not in ALLOWED_STATUSES:
        reasons.append(f"invalid_status:{row[STATUS_FIELD]}")
    if not row.get("location_id", "").strip() or row.get("location_id") not in VALID_LOCATIONS:
        reasons.append("missing_or_invalid_location_id")
    if not row.get(CATEGORY_FIELD, "").strip() or row.get(CATEGORY_FIELD) not in ALLOWED_CATEGORIES:
        reasons.append("missing_or_invalid_category")
    if len(row.get("description", "").strip()) < 5:
        reasons.append("empty_or_too_short_description")
    if not row.get("reporter_id", "").strip():
        reasons.append("missing_reporter_id")
    if row.get(STATUS_FIELD) == CLOSED_STATUS and not row.get(SATISFACTION_FIELD, "").strip():
        reasons.append("closed_without_satisfaction_score")
    if row.get(SATISFACTION_FIELD, "").strip():
        try:
            score = int(row[SATISFACTION_FIELD])
        except ValueError:
            score = 0
        if not 1 <= score <= 5:
            reasons.append("satisfaction_score_out_of_range")
    return reasons


def analyze_rows(rows: Iterable[dict[str, str]]) -> dict:
    invalid_records: list[InvalidRecord] = []
    category_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    satisfaction_values: list[int] = []
    total_records = 0
    for row_number, row in enumerate(rows, start=2):
        total_records += 1
        reasons = _validation_reasons(row)
        if reasons:
            invalid_records.append(InvalidRecord(row_number, tuple(reasons)))
            continue
        category_counts[row[CATEGORY_FIELD]] += 1
        status_counts[row[STATUS_FIELD]] += 1
        if row[STATUS_FIELD] == CLOSED_STATUS:
            satisfaction_values.append(int(row[SATISFACTION_FIELD]))

    reason_counts = Counter(reason for record in invalid_records for reason in record.reasons)
    satisfaction_distribution = dict(
        sorted(Counter(int(value) for value in satisfaction_values).items())
    )
    return {
        "total_records": total_records,
        "valid_records": total_records - len(invalid_records),
        "invalid_records": len(invalid_records),
        "invalid_details": [
            {"row_number": record.row_number, "reasons": list(record.reasons)}
            for record in invalid_records
        ],
        "invalid_by_reason": dict(sorted(reason_counts.items())),
        "category_breakdown": {
            category: category_counts[category]
            for category in CATEGORY_ORDER
            if category_counts[category]
        },
        "status_breakdown": {
            status: status_counts[status] for status in STATUS_ORDER if status_counts[status]
        },
        "average_satisfaction": fmean(satisfaction_values) if satisfaction_values else None,
        "satisfaction_sample_size": len(satisfaction_values),
        "satisfaction_distribution": satisfaction_distribution,
    }


def analyze_csv(stream: TextIO) -> dict:
    reader = csv.DictReader(stream)
    if not reader.fieldnames:
        raise ValueError("CSV is empty or has no header row")
    # Spreadsheet exports may include a UTF-8 BOM or accidental surrounding
    # whitespace in the header. Normalize only the header names so valid files
    # are not rejected for transport/formatting noise.
    reader.fieldnames = [field.lstrip("\ufeff").strip() for field in reader.fieldnames]
    if reader.fieldnames == ["CSV Structure"]:
        raise ValueError(
            "This file contains the CSV schema/documentation, not incident records. "
            "Upload a CSV with the required columns as its first row."
        )
    missing = sorted(set(REQUIRED_FIELDS) - set(reader.fieldnames))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    def normalized_rows():
        for row in reader:
            yield {
                (key.lstrip("\ufeff").strip() if key else key): value
                for key, value in row.items()
            }

    return analyze_rows(normalized_rows())


def results_csv(summary: dict) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(("metric", "value"))
    scalar_keys = (
        "total_records",
        "valid_records",
        "invalid_records",
        "average_satisfaction",
        "satisfaction_sample_size",
    )
    for key in scalar_keys:
        writer.writerow((key, summary[key]))
    for group_key in ("invalid_by_reason", "category_breakdown", "status_breakdown"):
        for label, value in summary[group_key].items():
            writer.writerow((f"{group_key}.{label}", value))
    for label, value in summary["satisfaction_distribution"].items():
        writer.writerow((f"satisfaction_distribution.{label}", value))
    return output.getvalue()
