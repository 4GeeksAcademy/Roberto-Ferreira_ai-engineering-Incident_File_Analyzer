import csv
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from analyzer_core import analyze_csv  # noqa: E402
from services.api import main  # noqa: E402


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(main.app)
        cls.dataset = ROOT / "incidents-brasaland.csv"

    def setUp(self):
        main.last_summary = None

    def test_export_before_analysis(self):
        response = self.client.get("/api/incidents/results/export")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "No analysis has been run yet.")

    def test_empty_and_non_csv_uploads(self):
        empty = self.client.post(
            "/api/incidents/analyze", files={"file": ("empty.csv", b"")}
        )
        self.assertEqual(empty.status_code, 400)
        self.assertEqual(empty.json()["detail"], "The uploaded file is empty.")

        non_csv = self.client.post(
            "/api/incidents/analyze", files={"file": ("data.txt", b"anything")}
        )
        self.assertEqual(non_csv.status_code, 400)
        self.assertEqual(non_csv.json()["detail"], "Upload a CSV file.")

    def test_invalid_encoding_and_missing_columns(self):
        encoding = self.client.post(
            "/api/incidents/analyze", files={"file": ("data.csv", b"\xff")}
        )
        self.assertEqual(encoding.status_code, 422)
        self.assertIn("utf-8", encoding.json()["detail"].lower())

        missing = self.client.post(
            "/api/incidents/analyze",
            files={"file": ("data.csv", b"incident_id,category,status\n1,EQUIPMENT,OPEN\n")},
        )
        self.assertEqual(missing.status_code, 422)
        self.assertIn("Missing required columns", missing.json()["detail"])

    def test_official_dataset_json_parity_and_export(self):
        payload = self.dataset.read_bytes()
        response = self.client.post(
            "/api/incidents/analyze",
            files={"file": ("incidents-brasaland.csv", payload, "text/csv")},
        )
        self.assertEqual(response.status_code, 200)
        summary = response.json()
        with self.dataset.open(encoding="utf-8", newline="") as stream:
            expected = analyze_csv(stream)
        # JSON object keys are strings, while the Python summary uses integer
        # satisfaction scores as distribution keys.
        expected_json = json.loads(json.dumps(expected))
        self.assertEqual(summary, expected_json)
        self.assertEqual(summary["total_records"], 100)
        self.assertEqual(summary["valid_records"], 96)
        self.assertEqual(summary["invalid_records"], 4)
        self.assertEqual(summary["average_satisfaction"], 3.46)

        export = self.client.get("/api/incidents/results/export")
        self.assertEqual(export.status_code, 200)
        self.assertEqual(export.headers["content-type"], "text/csv; charset=utf-8")
        self.assertIn("attachment; filename=results.csv", export.headers["content-disposition"])
        rows = list(csv.DictReader(io.StringIO(export.text)))
        self.assertEqual(rows[0], {"metric": "total_records", "value": "100"})
        self.assertTrue(any(row["metric"] == "average_satisfaction" and row["value"] == "3.46" for row in rows))

    def test_cors_for_backoffice_origin(self):
        response = self.client.options(
            "/api/incidents/analyze",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["access-control-allow-origin"], "http://localhost:3000")


if __name__ == "__main__":
    unittest.main()
