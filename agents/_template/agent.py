"""Base template for company agents.

Use this pattern when creating a new agent in the repo: define a clear purpose,
provide a small business-oriented interface, and keep the logic easy to test.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class AgentInput:
    """Simple data object for agent input."""

    user_query: str
    context: Dict[str, Any] | None = None


class BaseAgent:
    """Minimal reusable base class for repo agents."""

    def __init__(self, name: str, purpose: str):
        self.name = name
        self.purpose = purpose

    def run(self, payload: AgentInput) -> Dict[str, Any]:
        """Return a structured response from the agent."""
        return {
            "agent": self.name,
            "purpose": self.purpose,
            "query": payload.user_query,
            "context": payload.context or {},
            "result": "Agent template is ready to be customized.",
        }


if __name__ == "__main__":
    example = AgentInput(
        user_query="Summarize the active hiring round.",
        context={"position": "Executive Assistant", "location": "Medellín"},
    )
    print(BaseAgent("demo-agent", "Example company agent").run(example))
