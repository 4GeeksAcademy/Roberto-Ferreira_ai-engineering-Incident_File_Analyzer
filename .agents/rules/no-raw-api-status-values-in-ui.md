# Rule: Never render raw API `status`/`stage` values in the UI

## Scope classification

**File-pattern-based.** This rule activates whenever an agent creates or edits a file matching:

```
uis/talent-pipeline-tracker/app/**
uis/talent-pipeline-tracker/components/**
```

It does not apply outside those paths (e.g. it does not apply to `lib/records.ts`, which is allowed to
carry the raw API values internally).

## Condition

Applies whenever the change renders, displays, or otherwise exposes a candidate record's `status` or
`stage` field to the user (JSX text, alt text, aria-labels, `title` attributes, etc.).

## Rule

- Never render the raw API value (`received`, `in_progress`, `selected`, `discarded`, `pending`,
  `review`, `personal_interview`, `technical_interview`, `offer_presented`) directly in the UI.
- Always resolve the value through the existing lookup maps `STATUS_LABELS` / `STAGE_LABELS` exported
  from `uis/talent-pipeline-tracker/types/records.ts` before displaying it.
- If a new status/stage value is introduced, add it to `RECORD_STATUSES`/`RECORD_STAGES` **and** its
  corresponding label entry in the same commit — do not render a value that has no label mapping.

## Rationale

This is a non-negotiable acceptance criterion from [`CONTEXT.md`](../../CONTEXT.md): "Raw API values
(`in_progress`, `personal_interview`, etc.) must never be visible in the interface. Always use the labels
from this table." It is also called out explicitly in
[`memory-bank/techContext.md`](../../memory-bank/techContext.md) as a verified project constraint. This
rule does not override or contradict [`AGENTS.md`](../../AGENTS.md); it operates one level more specific,
inside the scope AGENTS.md already treats as sensitive (`lib/api-client.ts` and `lib/records.ts` require
developer confirmation to change — this rule protects the UI layer that consumes them).

## Example

```tsx
// ❌ Wrong — raw API value leaks into the UI
<span>{candidate.status}</span>

// ✅ Correct — resolved through the label map
<span>{STATUS_LABELS[candidate.status]}</span>
```
