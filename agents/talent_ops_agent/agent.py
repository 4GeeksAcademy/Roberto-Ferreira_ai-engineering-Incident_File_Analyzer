"""Talent pipeline operations agent.

This agent provides a realistic but lightweight candidate pipeline summary for the
Brasaland hiring workflow. It is intentionally small, testable, and reusable.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List


class TalentOpsAgent:
    """Summarizes pipeline health and suggests next actions for recruiters."""

    def __init__(self, name: str = "talent-ops-agent") -> None:
        self.name = name

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        position = payload.get("position", "Unknown role")
        location = payload.get("location", "Unknown location")
        candidates = payload.get("candidates", [])

        status_counts = Counter()
        stage_counts = Counter()
        blocked = []
        notes_waiting = []

        for candidate in candidates:
            status = str(candidate.get("status", "received")).strip()
            stage = str(candidate.get("stage", "pending")).strip()
            name = candidate.get("name", "Unnamed candidate")

            status_counts[status] += 1
            stage_counts[stage] += 1

            if status == "discarded":
                blocked.append(name)

            if int(candidate.get("notes_count", 0) or 0) == 0:
                notes_waiting.append(name)

        recommendations = []
        if status_counts.get("received", 0) > 0:
            recommendations.append("Review new applicants for screening and first-contact follow-up.")
        if stage_counts.get("personal_interview", 0) > 0:
            recommendations.append("Schedule or confirm the next interviews for candidates in personal interview stage.")
        if blocked:
            recommendations.append("Check rejected candidates and confirm no data was accidentally discarded.")
        if notes_waiting:
            recommendations.append("Add interview notes for candidates with no recorded notes yet.")

        if not recommendations:
            recommendations.append("Pipeline looks healthy; continue monitoring the current hiring funnel.")

        return {
            "agent": self.name,
            "position": position,
            "location": location,
            "total_candidates": len(candidates),
            "status_counts": dict(status_counts),
            "stage_counts": dict(stage_counts),
            "flags": {
                "blocked_candidates": blocked,
                "candidates_missing_notes": notes_waiting,
            },
            "recommendations": recommendations,
        }


if __name__ == "__main__":
    sample = {
        "position": "Executive Assistant",
        "location": "Medellín",
        "candidates": [
            {"name": "Ana Gomez", "status": "received", "stage": "pending", "notes_count": 0},
            {"name": "Luis Ruiz", "status": "in_progress", "stage": "personal_interview", "notes_count": 2},
            {"name": "Maria Vega", "status": "discarded", "stage": "review", "notes_count": 1},
        ],
    }
    print(TalentOpsAgent().run(sample))
