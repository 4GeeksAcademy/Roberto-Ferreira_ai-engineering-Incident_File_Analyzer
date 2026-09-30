import unittest

from agents.talent_ops_agent.agent import TalentOpsAgent


class TalentOpsAgentTest(unittest.TestCase):
    def test_agent_summary_counts_pipeline_data(self):
        payload = {
            "position": "Executive Assistant",
            "location": "Medellín",
            "candidates": [
                {"name": "Ana Gomez", "status": "received", "stage": "pending", "notes_count": 0},
                {"name": "Luis Ruiz", "status": "in_progress", "stage": "personal_interview", "notes_count": 2},
                {"name": "Maria Vega", "status": "discarded", "stage": "review", "notes_count": 1},
            ],
        }

        result = TalentOpsAgent().run(payload)

        self.assertEqual(result["total_candidates"], 3)
        self.assertEqual(result["status_counts"]["received"], 1)
        self.assertEqual(result["status_counts"]["in_progress"], 1)
        self.assertEqual(result["status_counts"]["discarded"], 1)
        self.assertEqual(result["stage_counts"]["personal_interview"], 1)
        self.assertIn("Review new applicants", result["recommendations"][0])
        self.assertIn("Ana Gomez", result["flags"]["candidates_missing_notes"])

    def test_agent_handles_empty_pipeline(self):
        result = TalentOpsAgent().run({"position": "Executive Assistant", "location": "Medellín", "candidates": []})

        self.assertEqual(result["total_candidates"], 0)
        self.assertEqual(result["status_counts"], {})
        self.assertEqual(result["stage_counts"], {})
        self.assertIn("Pipeline looks healthy", result["recommendations"][0])


if __name__ == "__main__":
    unittest.main()
