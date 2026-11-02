# Annotation guide — human authoring required

This is a skeleton, not a frozen guide. Emmanuel must supply every annotation judgement before `guide-v1.0` is tagged and before a live run.

## Version and freeze rule
What is the guide version? When and how is it frozen? How are errors handled without editing held-out cases after results?

## Category inclusion
Which CUAD categories are obligation-bearing and which are excluded? Populate `obligation_types.yaml`.

## Unit of annotation
When is one clause one obligation versus multiple obligations? What is required to score a consequence?

## Deadlines
How should absolute, relative, recurring, and no-deadline cases be annotated, including unresolved anchors and verbatim text? Provide examples in the human-authored guide.

## Party and role mapping
The output and gold `owed_by` enum is `provider`, `customer`, `both`, `unclear`. Map licensor to provider and licensee to customer. `intake_party` retains the wider schema enum. How should other role ambiguities be handled?

## Genuine conflict
What evidence distinguishes genuinely incompatible clauses from merely different or compatible clauses?

## Escalation
When should each escalation code be used, and what evidence is necessary?

## Difficulty
Define the difficulty scale and how it is applied.
