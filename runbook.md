# Incident and escalation runbook (draft: integration incomplete)

Never render a legal conclusion. Preserve evidence and involve a person when necessary.

| Path | Symptom | Detection | Action | Owner |
|---|---|---|---|---|
| Repeated LLM 429 | Model unavailable | Rate-limit responses after retries | Exponential backoff with jitter, maximum three attempts; dead-letter and E6; preserve request safely; retry only after service recovery | Engineering queue |
| No obligation-bearing clause above floor | No usable result | Calibrated precheck | E1; send empty retrieval and context to legal-ops, do not fabricate | Legal-ops queue |
| Conflicting clauses | Possible incompatible duties | Model flags pair plus default-escalation cross-check | E2; attach both passages; human adjudicates | Legal-ops queue |
| Two invalid terminal calls | No validated result | Boundary validation errors | E4; preserve raw tool calls; investigate schema or model output | Engineering queue |
| Duplicate intake | Repeated request | Matching idempotency key and request hash | Return original run ID, do not call the model; reject same key with changed request | Maintainer |
| Mid-transaction database error | Decision cannot be persisted | Transaction exception | Roll back all decision children; inspect and retry safely | Engineering queue |
| Missing relative anchor | Deadline cannot be resolved | Anchor absent or ambiguous | E3; retain verbatim deadline text and evidence; human resolves | Legal-ops queue |

Additional: low-confidence E5 routes to legal-ops. An exhausted tool routes E6 to engineering; no terminal call by turn limit routes E4. Cache misses in replay are hard failures, not permission to contact an API.
