#!/usr/bin/env python3
"""Run incident CSV analysis from the command line."""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from analyzer_core import analyze_csv, results_csv


def print_summary(summary: dict, source_name: str) -> None:
    print("=" * 60)
    print("  BRASALAND — INCIDENT REPORT ANALYSIS")
    print(f"  Source file: {source_name}")
    print("=" * 60)
    print(f"\nTOTAL RECORDS IN FILE .......... {summary['total_records']}")
    print(f"  ├─ Valid records ................ {summary['valid_records']}")
    print(f"  └─ Invalid / incomplete .......... {summary['invalid_records']}")

    print("\nINVALID RECORDS BREAKDOWN")
    invalid_labels = {
        "missing_or_invalid_location_id": "Missing location_id",
        "missing_or_invalid_category": "Invalid or missing category",
        "empty_or_too_short_description": "Empty description",
        "missing_reporter_id": "Missing reporter_id",
        "closed_without_satisfaction_score": "Closed case, no score",
        "satisfaction_score_out_of_range": "Satisfaction score out of range",
    }
    for label in (
        "missing_or_invalid_location_id",
        "missing_or_invalid_category",
        "empty_or_too_short_description",
        "missing_reporter_id",
        "closed_without_satisfaction_score",
        "satisfaction_score_out_of_range",
    ):
        value = summary["invalid_by_reason"].get(label, 0)
        if value:
            print(f"  {invalid_labels[label]:<35} {value}")

    print("\nBREAKDOWN BY CATEGORY (valid records)")
    for label, value in summary["category_breakdown"].items():
        total = summary["valid_records"] or 1
        print(f"  {label:<28} {value:>3} ({value / total * 100:.1f}%)")

    print("\nBREAKDOWN BY STATUS (valid records)")
    for label, value in summary["status_breakdown"].items():
        total = summary["valid_records"] or 1
        print(f"  {label:<28} {value:>3} ({value / total * 100:.1f}%)")

    print("\nSATISFACTION INDEX (closed cases)")
    closed_count = summary["status_breakdown"].get("CLOSED", 0)
    print(f"  Scored cases: {summary['satisfaction_sample_size']} of {closed_count}")
    average = summary["average_satisfaction"]
    print(f"  Average score: {average:.2f} / 5.00" if average is not None else "  Average score: n/a")
    for score, value in summary["satisfaction_distribution"].items():
        print(f"  ├─ Score {score} ...................... {value}")
    print("=" * 60)


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze a company incident CSV")
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()
    try:
        with args.csv_path.open(newline="", encoding="utf-8") as stream:
            summary = analyze_csv(stream)
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print_summary(summary, args.csv_path.name)
    try:
        answer = input("Export results to CSV? [y / n] ").strip().lower()
    except EOFError:
        answer = "n"
    if answer == "y":
        Path("results.csv").write_text(results_csv(summary), encoding="utf-8", newline="")
        print("Results exported to results.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
