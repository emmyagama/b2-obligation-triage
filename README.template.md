# B2: contract-obligation triage

B2 is an evaluation prototype for extracting obligations and deadlines from CUAD-style commercial contracts, grounding extracted quotes in the source, and routing ambiguity or conflict to human review. It is not legal advice and is not ready for unsupervised use.

> **Privacy and safety warning**
> The live CLI sends contract text to the configured model provider. The released evaluation below replays cached responses; it does not establish accuracy, confidentiality or data-handling behaviour for the live provider path. Do not use it on confidential, privileged or regulated contracts without authorization and a privacy review. Human reviewers, not the model, decide escalations. Protection controls (offline replay, cache identity, source-slice grounding, freeze and guard checks) reduce accidental network use and drift, but they do not remove provider or privacy risk.

> **At a glance**
> - **What works:** deterministic offline replay; cache identity and freeze/guard checks; source-slice quote grounding on extracted quotes (narrow check); escalation recall {{ escalation_recall_point }}.
> - **What failed:** exception rate {{ exception_rate_point }}; obligation recall {{ obligation_recall_point }}; false escalation {{ false_escalation_point }}; relative deadline capture {{ deadline_relative_point }}; constructed E2 exception rate {{ constructed_e2_exception_rate_point }}; E2-code recall {{ constructed_e2_recall_point }}; latency p50/p95 {{ latency_short }}; mean live cost {{ cost }}.
> - **What this does not establish:** live CLI/provider accuracy or confidentiality; natural-conflict performance; legal correctness; performance outside this 30-case test-only run; clause-location quality; Nigerian or Gulf law claims. Human review is still pending.

## Disclosures and limits
- CUAD consists of US commercial contracts; findings are illustrative, not claims about Nigerian or Gulf law.
- CUAD clause-category labels are available to the agent, so clause location is not evaluated.
- The selected contract groups are project-defined title buckets, not an official CUAD family taxonomy.
- Emmanuel authors the additional obligations and deadlines under the [annotation guide](guide/annotation-guide.md), frozen at `guide-v1.0`.
- A human sweep found no genuine E2 conflict among the 40 selected contracts.
- All 14 E2 cases (5 dev, 9 test) are constructed composites assembled from real clauses, with pairs and gold chosen by a human; they are not natural-conflict samples.
- Planned split: dev 26 (14 clear, 5 conflicting, 5 out-of-scope, 2 adversarial); test 30 (12, 9, 5, 4), total 56.
- The 30-case test run is test-only and uses cached provider responses; it is the only released held-out evaluation here.

## Held-out results
Exception rate: {{ exception_rate }}.
Absolute deadline capture: {{ deadline_absolute }}.
Relative deadline capture: {{ deadline_relative }}.
Obligation recall: {{ obligation_recall }}.
Escalation recall: {{ escalation_recall }}; false escalation: {{ false_escalation }}; grounded quote rate: {{ grounded_rate }}.
Latency p50/p95: {{ latency }}; live cost: {{ cost }} (rounded to four decimal places).
Constructed E2 cases: {{ constructed_e2_cases }}; exception rate: {{ constructed_e2_exception_rate }}; E2-code recall: {{ constructed_e2_recall }}. These are reported separately and do not estimate natural-conflict performance.

All proportion metrics require numerator, denominator and Wilson 95% range. The 100% grounded-quote result means each extracted quote was found in the source after whitespace normalisation; it does not establish that the quote supports the obligation or that the obligation is correct.

## Scope and methods
Cuts: {{ cuts }}. Dev/test source-document overlap: {{ document_overlap }}. Tuning: {{ tuning_history }}. Live test runs executed: {{ test_run_count }}.

## Failure taxonomy and honest failures
{{ falsification }}

{{ failure_taxonomy }}

## Human review
Pending: three real reviewers and 20 sampled escalations, planned for v1.0.1. Human reviewers, not the model, decide escalated issues. Dates that cannot be resolved without guessing remain unresolved and are escalated.

## Offline reproduction
{{ offline_reproduction }}

The checkout currently tracks 10,479 response files under `cache/llm/`. `CACHE-ARTIFACT.md` documents a versioned compressed artifact with a SHA-256 checksum, exact download and verification steps, and a clean-clone replay. The artifact is not yet published; the tracked files remain the current replay source.

## Measurement definitions
An exception is any failed per-case check or recorded error. Obligations match on type and owed-by, with no more than one unmatched extra per case. A deadline must match in kind and, where gold has a resolved date, within one day; when gold is unresolved the output must also remain unresolved. `none` is captured as a kind. Quotes are grounded when present in the source after collapsing whitespace only. Recall denominators are gold obligations or gold deadlines; grounded rate uses extracted quotes; escalation rates use gold-positive or gold-negative cases respectively. Constructed E2-code recall is the fraction of constructed conflicting cases with human E2 gold for which the output contains E2. Wilson ranges apply to proportions, not continuous latency or cost. A small relative-deadline denominator produces a wide interval and cannot support a precise comparison.

The E1 and E5 floors and their provenance are in `config/thresholds.yaml` and `eval_results/threshold_calibration.md`. E5 is applied after model output. The E1 precheck uses the human-authored taxonomy and cached query embeddings. Default-escalating types are routed conservatively for review; a candidate pair is not by itself proof of a conflict.

## Safety and scope
Human reviewers, not the model, decide escalated issues. The system is not legal advice. Dates that cannot be resolved without guessing remain unresolved and are escalated. End-to-end latency is unavailable for a partially resumed live case unless its earlier complete measurement exists; it is excluded from the latency denominator. Model prices must be configured before live calls and are captured in cache metadata. Local embeddings are assumed to have no per-call API charge.
