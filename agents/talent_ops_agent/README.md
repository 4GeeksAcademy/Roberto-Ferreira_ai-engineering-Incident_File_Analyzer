# Talent Ops Agent

A practical AI agent for the Brasaland hiring pipeline.

## Purpose

This agent helps people operations teams understand the current candidate pipeline by summarizing stage
progress, highlighting risk areas, and proposing the next operational move.

## Inputs

The agent accepts a structured payload such as:

- `position`
- `location`
- `candidates` with `name`, `status`, `stage`, and `notes_count`
- `company` context

## Output

It returns:

- total candidates,
- counts by status and stage,
- risk flags,
- and recommended next actions.

## Example

```python
from agents.talent_ops_agent.agent import TalentOpsAgent

agent = TalentOpsAgent()
result = agent.run({
    "position": "Executive Assistant",
    "location": "Medellín",
    "candidates": [
        {"name": "Ana Gomez", "status": "received", "stage": "pending", "notes_count": 0},
        {"name": "Luis Ruiz", "status": "in_progress", "stage": "personal_interview", "notes_count": 2},
    ],
})
```

## Why it matters

This is a real, reusable example of an AI agent that solves a specific operational need rather than
being a scaffold with no behavior.
