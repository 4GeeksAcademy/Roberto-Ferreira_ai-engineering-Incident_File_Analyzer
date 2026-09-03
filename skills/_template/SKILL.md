# Skill template

Use this template when creating a reusable AI capability for the company repo.

## Purpose

A skill should solve a repeatable team problem with a clear input and output contract. It should be
small, practical, and easy to document.

## When to use this skill

Use it when the same workflow appears repeatedly across agents, scripts, or projects, such as:

- research synthesis,
- data cleaning,
- code review,
- prompt orchestration,
- or domain-specific analysis.

## Inputs

Describe the expected inputs clearly. Include:

- the source data or context,
- required parameters,
- output format expectations,
- constraints and edge cases.

## Workflow

1. Validate the input.
2. Transform or analyze the data.
3. Return a structured result.
4. Explain assumptions clearly.

## Output contract

Return a concise, structured result that is easy to consume in downstream code or prompts. For example:

- summary,
- findings,
- recommendations,
- or a normalized data object.

## Example

```text
Input: candidate pipeline summary
Output: status counts, stage counts, risk flags, action recommendations
```

## Quality bar

A good skill is:

- readable,
- deterministic,
- documented,
- and testable.

This template is intentionally simple so the repo can grow without creating empty or vague capability files.
