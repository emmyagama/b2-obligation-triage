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
- Superseding the earlier Chroma/L2 decision: migrate the existing Chroma vectors once from a temporary copy, checking every chunk's text against its source slice. Runtime/CI use text-free NumPy cosine; float16 storage is converted to float32 for comparison, scores rounded to four decimals and ties resolved by chunk ID. The corpus version is SHA-256 over length-framed base document bytes and DB labels, chunk metadata and vector-file bytes, plus chunking parameters, model ID, dimensions and dtype. Test synthetic documents and their shard are excluded; their document SHA-256 is included in request and transaction cache keys. Recalibrate E1 on dev cosine scores; old L2 floors and caches are not interchangeable.
- Composite source documents may be assembled without assigning conflict labels; source provenance remains explicit, and the human decides whether the pairing is genuinely conflicting. Exact gold refs remain anchored to the original CUAD span and are checked at the mapped composite offset.
- Reviewer obligation counts are stored with each verdict as structured JSON in `human_reviews.note`; `escalations.human_obligation_count` is populated only when all three reviewers supply the same count. Disagreement or missing counts remain unresolved rather than being averaged into a false consensus.

## v1.1 construction and measurement
- The human found no genuine E2 conflict in the 40 documents. All 14 E2 cases are constructed composites; human selection, adjudication and gold remain mandatory. Report constructed E2 exception rate and E2-code recall separately, with counts and Wilson intervals; overall metrics remain unchanged.
- Planned dev/test totals are 26/30 (56 combined); test-only synthetic text, provenance, embeddings and DB are embargoed through the completed valid test run.

## Held-out test-gold exposure — accepted (2026-11-03)
- Found by the Phase C pre-flight: all 30 `cases/src/test-*.yaml` and `cases/TEST-NOTES.md` were in pushed commits `2f42a21` and `67bab1e` on `origin/b2/build` (GitHub web upload, which bypasses the `.gitignore` embargo added in `032246a`). Brief §0.9 defines this as an integrity incident; `cases/test.json`, `cache/llm/`, test results and the local test shard were never pushed.
- Emmanuel's instruction: purge it from GitHub entirely if that is possible, otherwise accept and document. A full purge is **not** possible — the files are reachable from `origin/b2/build`, `origin/HEAD` and `origin/arena/18088414-b2-obligation-triage`, so removing them needs a history rewrite plus `git push --force` (forbidden by §0.5), and even then GitHub's unreachable objects and any clone made before the fix keep a copy. The exposure is therefore **accepted**.
- Mitigation applied: the 31 files are untracked from the branch tip (byte-identical on disk, still compiled by `build_cases.py`), `.gitignore` now covers `cases/TEST-NOTES.md`, and `scripts/pre_push_guard.py` passes again so the embargo is enforced on every future push.
- Accepted residue: the gold remains in the pushed history of both branches, in GitHub's unreachable-object store and in pre-fix clones. The held-out split is not blind to anyone with repository access; this is disclosed, not repaired, and no re-seal of `FROZEN.sha256` was performed.

dev-15 reclassified from out_of_scope to clear with E1: the document carries only trivial labels; guide §8 places E1 inside clear cases. Signed: Emmanuel, 4 Nov 2026.

Hygiene scope narrowed to model-facing files after dev results; no prompt or metric affected. Signed: Emmanuel, 4 Nov 2026.