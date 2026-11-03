# B2: contract-obligation triage

## Disclosures
CUAD consists of US commercial contracts; findings are illustrative, not claims about Nigerian or Gulf law. CUAD labels clause categories; Emmanuel authors the additional obligations and deadlines under the [annotation guide](guide/annotation-guide.md), frozen at `guide-v1.0`. CUAD labels are available to the agent, so clause location is not evaluated. The selected contract groups are project-defined title buckets, not an official CUAD family taxonomy. Not legal advice. A human sweep found no genuine E2 conflict among the 40 selected contracts. All 14 E2 cases (5 dev, 9 test) are constructed composites assembled from real clauses, with pairs and gold chosen by a human; they are not natural-conflict samples.

Planned split: dev 26 (14 clear, 5 conflicting, 5 out-of-scope, 2 adversarial); test 30 (12, 9, 5, 4), total 56.

## Held-out results
Exception rate: {{ exception_rate }}.
Absolute deadline capture: {{ deadline_absolute }}.
Relative deadline capture: {{ deadline_relative }}.
Obligation recall: {{ obligation_recall }}.
Escalation recall: {{ escalation_recall }}; false escalation: {{ false_escalation }}; grounded quote rate: {{ grounded_rate }}.
Latency p50/p95: {{ latency }}; live cost per transaction: {{ cost }}.
Constructed E2 cases: {{ constructed_e2_cases }}; exception rate: {{ constructed_e2_exception_rate }}; E2-code recall: {{ constructed_e2_recall }}. These are reported separately and do not estimate natural-conflict performance.

All proportion metrics require numerator, denominator and Wilson 95% range.

## Scope and methods
Cuts: {{ cuts }}. Dev/test source-document overlap: {{ document_overlap }}. Tuning: {{ tuning_history }}. Live test runs executed: {{ test_run_count }}.

## Failure taxonomy and honest failures
{{ falsification }}

{{ failure_taxonomy }}

## Human review
Pending: three real reviewers and 20 sampled escalations, planned for v1.0.1.

## Offline reproduction
{{ offline_reproduction }}

## Measurement definitions
An exception is any failed per-case check or recorded error. Obligations match on type and owed-by, with no more than one unmatched extra per case. A deadline must match in kind and, where gold has a resolved date, within one day; when gold is unresolved the output must also remain unresolved. `none` is captured as a kind. Quotes are grounded when present in the source after collapsing whitespace only. Recall denominators are gold obligations or gold deadlines; grounded rate uses extracted quotes; escalation rates use gold-positive or gold-negative cases respectively. Constructed E2-code recall is the fraction of constructed conflicting cases with human E2 gold for which the output contains E2. Wilson ranges apply to proportions, not continuous latency or cost. A small relative-deadline denominator produces a wide interval and cannot support a precise comparison.

The E1 and E5 floors and their provenance are in `config/thresholds.yaml` and `eval_results/threshold_calibration.md`. E5 is applied after model output. The E1 precheck uses the human-authored taxonomy and cached query embeddings. Default-escalating types are routed conservatively for review; a candidate pair is not by itself proof of a conflict.

## Safety and scope
Human reviewers, not the model, decide escalated issues. The system is not legal advice. Dates that cannot be resolved without guessing remain unresolved and are escalated. End-to-end latency is unavailable for a partially resumed live case unless its earlier complete measurement exists; it is excluded from the latency denominator. Model prices must be configured before live calls and are captured in cache metadata. Local embeddings are assumed to have no per-call API charge.
