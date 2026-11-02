# Decisions and open issues

## Brief resolutions adopted
1. Normalize licensor to provider and licensee to customer for gold/output; intake keeps the wider enum.
2. Gold requires `clause_ref` with category and exact character offsets; the Phase 2 validator must enforce it.
3. E5 routes to legal-ops.
4. Missing terminal call after eight turns becomes E4 and LOOP_EXHAUSTED.
5. Empty intake requires a synthetic document row, to be produced in Phase 2.
6. Publish Wilson 95% intervals for proportions rather than the planning approximations. Wilson intervals do not apply to continuous latency or cost; report sample counts, not a fictitious Wilson interval, for those measures.
7. CUAD category labels are agent inputs: clause location is not evaluated.
8. Emmanuel authors the obligation taxonomy. The loader rejects empty or incomplete included entries.
9. Default to 40 weighted contracts with logged conflict-coverage swaps. Candidate clause pairs are not adjudicated conflicts.
10. Freeze the guide before any live run; tag v1.0.0 after evaluation, with human review pending until v1.0.1.

## Additional implementation decisions
- Gold with an unresolved relative or recurring deadline matches only an unresolved prediction of the same kind; no date is guessed. Matching first maximizes deadline-compatible identity matches before matching remaining identities.
- Default-escalating obligation types are conservatively routed as E3 unless the model flags E2. The conflict-pair cross-check reports candidates and default flags; it cannot decide legal incompatibility.
- The date parser accepts unambiguous explicit ISO and spelled-out month dates; ambiguous numerical dates and unsupported recurring expressions remain unresolved or are rejected rather than guessed. Supported anniversary and explicit effective-date-relative weekly, monthly and quarterly recurrences are computed. Month-end and leap-day arithmetic clamp to the final day of the target month; this is a computational convention, not legal advice.
- Recorded transaction latency is used in replay. A resumed partial case without an earlier complete measurement is marked unavailable rather than reporting replay or partial wall-clock time as full transaction latency.
- Before calibration, the configuration uses clearly marked dev-only provisional floors. Held-out runs reject provisional values. Calibration tie-breaks by highest recall, then lowest false-escalation, then lowest floor.
- Offline fixtures use a fake embedding provider and synthetic examples only; they are not human gold or evidence of real-world performance.

## Phase 2 / integration checkpoints
- B1 uses a local all-MiniLM-L6-v2 model and Chroma; its Nigerian-health acronym expansion is not appropriate for this corpus. OpenCode's adapter must implement the interface in the Phase 2 handoff and preserve caching.
- Verify actual CUAD text, label offsets, filenames and family derivation against OpenCode's corpus report before implementing selection or annotation tooling. Do not infer these structures here.
- Recheck recurrence and date-parser coverage against corpus formats without adding held-out examples to code or prompts; unsupported cases remain escalated. Never infer a legal meaning from an interval convention.

## User-approved Phase 2 deviations from v2.0 specification
- CUAD contains 244 repeated `(document, category, start)` positions with distinct answer text across the full source. On the preliminary 40-contract selection, 22 such positions occur in 16 documents. Emmanuel approved changing the `clause_labels` uniqueness key to `(document_id, category, char_start, char_end)` to retain every distinct CUAD span; the original start-only key could not ingest them verbatim. Exact duplicate full spans, if encountered, are rejected rather than silently dropped.
- CUAD titles do not expose a canonical 25-family taxonomy: the report found 250 raw parsed strings and 40 titles the raw rule does not parse. Emmanuel approved a deterministic, project-defined 25-bucket title normalization with an `other` bucket, fixed precedence and disclosed limitations. These buckets are not CUAD's expert labels or official families. Selection logs both source family string and assigned bucket. Combined-family titles use the first matching priority, which affects representativeness.
- B1's local Chroma/L2 store is reused through the OpenCode adapter. B2 loads a temporary copy of the persisted index for read-only replay because opening Chroma can modify its files; exact squared-L2 distances are evaluated deterministically and mapped to similarity as `1 / (1 + distance)`, with scores rounded to four decimals and ties sorted by chunk ID. E1 calibration must use this score, not B1's prior thresholds. The persisted content digest is verified before use.
- Composite source documents may be assembled without assigning conflict labels; source provenance remains explicit, and the human decides whether the pairing is genuinely conflicting. Exact gold refs remain anchored to the original CUAD span and are checked at the mapped composite offset.
- Reviewer obligation counts are stored with each verdict as structured JSON in `human_reviews.note`; `escalations.human_obligation_count` is populated only when all three reviewers supply the same count. Disagreement or missing counts remain unresolved rather than being averaged into a false consensus.
