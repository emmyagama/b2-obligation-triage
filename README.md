# B2: contract-obligation triage

B2 is an evaluation prototype for extracting obligations and deadlines from CUAD-style commercial contracts, grounding extracted quotes in the source, and routing ambiguity or conflict to human review. It is not legal advice and is not ready for unsupervised use.

> **Privacy and safety warning**
> The live CLI sends contract text to the configured model provider. The released evaluation below replays cached responses; it does not establish accuracy, confidentiality or data-handling behaviour for the live provider path. Do not use it on confidential, privileged or regulated contracts without authorization and a privacy review. Human reviewers, not the model, decide escalations. Protection controls (offline replay, cache identity, source-slice grounding, freeze and guard checks) reduce accidental network use and drift, but they do not remove provider or privacy risk.

> **At a glance**
> - **What works:** deterministic offline replay; cache identity and freeze/guard checks; source-slice quote grounding on extracted quotes (narrow check); escalation recall 77.8% (7/9).
> - **What failed:** exception rate 96.7% (29/30); obligation recall 26.8% (11/41); false escalation 81.0% (17/21); relative deadline capture 20.0% (1/5); constructed E2 exception rate 100.0% (9/9); E2-code recall 33.3% (3/9); latency p50/p95 74.7 / 120.6 s (n=30); mean live cost $0.0079 per transaction, n=30.
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
Exception rate: 96.7% (29/30; Wilson 95% 83.3%–99.4%).
Absolute deadline capture: not measurable (0 denominator).
Relative deadline capture: 20.0% (1/5; Wilson 95% 3.6%–62.4%).
Obligation recall: 26.8% (11/41; Wilson 95% 15.7%–41.9%).
Escalation recall: 77.8% (7/9; Wilson 95% 45.3%–93.7%); false escalation: 81.0% (17/21; Wilson 95% 60.0%–92.3%); grounded quote rate: 100.0% (38/38; Wilson 95% 90.8%–100.0%).
Latency p50/p95: 74656.0 / 120603.0 ms (n=30); live cost: $0.0079 per transaction, n=30 (rounded to four decimal places).
Constructed E2 cases: 9; exception rate: 100.0% (9/9; Wilson 95% 70.1%–100.0%); E2-code recall: 33.3% (3/9; Wilson 95% 12.1%–64.6%). These are reported separately and do not estimate natural-conflict performance.

All proportion metrics require numerator, denominator and Wilson 95% range. The 100% grounded-quote result means each extracted quote was found in the source after whitespace normalisation; it does not establish that the quote supports the obligation or that the obligation is correct.

## Scope and methods
Cuts: none instructed. Dev/test source-document overlap: 0. Tuning: not yet recorded. Live test runs executed: 1.

## Failure taxonomy and honest failures
The design is wrong, not the model. A suspected cause is missing or ambiguous effective-date labels in contracts with relative deadlines; this requires investigation.

Pending post-freeze documentation.

## Human review
Pending: three real reviewers and 20 sampled escalations, planned for v1.0.1. Human reviewers, not the model, decide escalated issues. Dates that cannot be resolved without guessing remain unresolved and are escalated.

## Offline reproduction
Run `python run_eval.py --split test` with the released cache; then run `python check_readme.py`. No API key or network is required. For the versioned compressed cache artifact and clean-clone verification, see `CACHE-ARTIFACT.md`.

The checkout currently tracks 10,479 response files under `cache/llm/`. `CACHE-ARTIFACT.md` documents a versioned compressed artifact with a SHA-256 checksum, exact download and verification steps, and a clean-clone replay. The artifact is not yet published; the tracked files remain the current replay source.

## Measurement definitions
An exception is any failed per-case check or recorded error. Obligations match on type and owed-by, with no more than one unmatched extra per case. A deadline must match in kind and, where gold has a resolved date, within one day; when gold is unresolved the output must also remain unresolved. `none` is captured as a kind. Quotes are grounded when present in the source after collapsing whitespace only. Recall denominators are gold obligations or gold deadlines; grounded rate uses extracted quotes; escalation rates use gold-positive or gold-negative cases respectively. Constructed E2-code recall is the fraction of constructed conflicting cases with human E2 gold for which the output contains E2. Wilson ranges apply to proportions, not continuous latency or cost. A small relative-deadline denominator produces a wide interval and cannot support a precise comparison.

The E1 and E5 floors and their provenance are in `config/thresholds.yaml` and `eval_results/threshold_calibration.md`. E5 is applied after model output. The E1 precheck uses the human-authored taxonomy and cached query embeddings. Default-escalating types are routed conservatively for review; a candidate pair is not by itself proof of a conflict.

## Safety and scope
Human reviewers, not the model, decide escalated issues. The system is not legal advice. Dates that cannot be resolved without guessing remain unresolved and are escalated. End-to-end latency is unavailable for a partially resumed live case unless its earlier complete measurement exists; it is excluded from the latency denominator. Model prices must be configured before live calls and are captured in cache metadata. Local embeddings are assumed to have no per-call API charge.
