import io
from pathlib import Path
import unittest

from analyzer_core import analyze_csv, analyze_rows


class AnalyzerCoreTests(unittest.TestCase):
    DATASET = Path(__file__).resolve().parents[1] / "incidents-brasaland.csv"

    def test_official_dataset_matches_context(self):
        with self.DATASET.open(encoding="utf-8", newline="") as stream:
            summary = analyze_csv(stream)

        self.assertEqual(summary["total_records"], 100)
        self.assertEqual(summary["valid_records"], 96)
        self.assertEqual(summary["invalid_records"], 4)
        self.assertEqual(
            summary["category_breakdown"],
            {
                "CUSTOMER_COMPLAINT": 29,
                "EQUIPMENT": 17,
                "SUPPLY": 22,
                "FOOD_QUALITY": 19,
                "STAFF": 9,
            },
        )
        self.assertEqual(summary["status_breakdown"], {"OPEN": 32, "CLOSED": 50, "DISCARDED": 14})
        self.assertEqual(
            summary["invalid_by_reason"],
            {
                "closed_without_satisfaction_score": 1,
                "empty_or_too_short_description": 1,
                "missing_or_invalid_category": 1,
                "missing_or_invalid_location_id": 1,
            },
        )
        self.assertEqual(summary["satisfaction_distribution"], {1: 4, 2: 6, 3: 12, 4: 19, 5: 9})
        self.assertAlmostEqual(summary["average_satisfaction"], 3.46, places=2)

    def test_valid_rows_and_satisfaction_metrics(self):
        rows = [
            {
                "incident_id": "BRS-000001",
                "date": "2026-01-01",
                "location_id": "COL-01",
                "category": "EQUIPMENT",
                "description": "Freezer stopped working",
                "status": "CLOSED",
                "customer_id": "",
                "satisfaction_score": "4",
                "reporter_id": "MGR-01",
            },
            {
                "incident_id": "BRS-000002",
                "date": "2026-01-02",
                "location_id": "FLA-04",
                "category": "STAFF",
                "description": "Schedule conflict reported",
                "status": "OPEN",
                "customer_id": "",
                "satisfaction_score": "",
                "reporter_id": "MGR-02",
            },
        ]

        summary = analyze_rows(rows)

        self.assertEqual(summary["total_records"], 2)
        self.assertEqual(summary["valid_records"], 2)
        self.assertEqual(summary["invalid_records"], 0)
        self.assertEqual(summary["satisfaction_distribution"], {4: 1})
        self.assertEqual(summary["average_satisfaction"], 4.0)

    def test_context_invalid_reason_counts(self):
        rows = [
            {
                "incident_id": "BRS-000001",
                "date": "2026-01-01",
                "location_id": "",
                "category": "EQUIPMENT",
                "description": "Valid description",
                "status": "OPEN",
                "reporter_id": "MGR-01",
            },
            {
                "incident_id": "BRS-000002",
                "date": "2026-01-02",
                "location_id": "COL-01",
                "category": "UNKNOWN",
                "description": "Valid description",
                "status": "OPEN",
                "reporter_id": "MGR-01",
            },
            {
                "incident_id": "BRS-000003",
                "date": "2026-01-03",
                "location_id": "COL-01",
                "category": "SUPPLY",
                "description": "bad",
                "status": "OPEN",
                "reporter_id": "MGR-01",
            },
            {
                "incident_id": "BRS-000004",
                "date": "2026-01-04",
                "location_id": "COL-01",
                "category": "STAFF",
                "description": "Valid description",
                "status": "CLOSED",
                "reporter_id": "MGR-01",
            },
        ]

        summary = analyze_rows(rows)

        self.assertEqual(summary["invalid_records"], 4)
        self.assertEqual(
            summary["invalid_by_reason"],
            {
                "closed_without_satisfaction_score": 1,
                "empty_or_too_short_description": 1,
                "missing_or_invalid_category": 1,
                "missing_or_invalid_location_id": 1,
            },
        )

    def test_csv_rejects_missing_required_columns(self):
        with self.assertRaisesRegex(ValueError, "Missing required columns: date"):
            analyze_csv(io.StringIO("incident_id,category,status\n1,EQUIPMENT,OPEN\n"))

    def test_empty_csv_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "empty or has no header"):
            analyze_csv(io.StringIO(""))

    def test_schema_documentation_is_rejected_with_clear_message(self):
        with self.assertRaisesRegex(ValueError, "schema/documentation"):
            analyze_csv(io.StringIO("CSV Structure\nFilename: incidents.csv\n"))

    def test_header_bom_and_whitespace_are_normalized(self):
        csv_text = (
            "\ufeff incident_id , date, location_id, category, description, status, reporter_id\n"
            "BRS-1,2026-01-01,COL-01,EQUIPMENT,Freezer stopped,OPEN,MGR-01\n"
        )
        summary = analyze_csv(io.StringIO(csv_text))
        self.assertEqual(summary["valid_records"], 1)

    def test_invalid_status_and_score_are_classified(self):
        row = {
            "incident_id": "BRS-000001",
            "date": "2026-01-01",
            "location_id": "COL-01",
            "category": "EQUIPMENT",
            "description": "Valid description",
            "status": "UNKNOWN",
            "satisfaction_score": "9",
            "reporter_id": "MGR-01",
        }
        summary = analyze_rows([row])
        self.assertEqual(summary["invalid_records"], 1)
        self.assertIn("invalid_status:UNKNOWN", summary["invalid_by_reason"])
        self.assertIn("satisfaction_score_out_of_range", summary["invalid_by_reason"])


if __name__ == "__main__":
    unittest.main()
