# B2: contract-obligation triage

B2 is an auditable research prototype for extracting contractual obligations from contract text and routing ambiguous or high-risk items to human review. It includes a tool-calling LLM pipeline, a human-authored obligation taxonomy, quote-grounding and deadline checks, escalation routing, an offline evaluation harness, and a local CLI for unlabelled contracts.

**Research prototype, not a validated legal service.** This repository is not legal advice, has not been validated for production or legal practice, and must not be used as the sole basis for a legal decision. The historical evaluation below reports substantial failures, and human review remains pending. Live CLI use is opt-in and sends contract text to the configured provider.

> **Privacy and safety warning**
> The live CLI sends contract text to the configured model provider. The released evaluation below replays cached responses; it does not establish accuracy, confidentiality or data-handling behaviour for the live provider path. Do not use it on confidential, privileged or regulated contracts without authorization and a privacy review. Human reviewers, not the model, decide escalations. Protection controls (offline replay, cache identity, source-slice grounding, freeze and guard checks) reduce accidental network use and drift, but they do not remove provider or privacy risk.

> **At a glance**
> - **What works:** deterministic offline replay; cache identity and freeze/guard checks; source-slice quote grounding on extracted quotes (narrow check); escalation recall 77.8% (7/9).
> - **What failed:** exception rate 96.7% (29/30); obligation recall 26.8% (11/41); false escalation 81.0% (17/21); relative deadline capture 20.0% (1/5); constructed E2 exception rate 100.0% (9/9); E2-code recall 33.3% (3/9); latency p50/p95 74.7 / 120.6 s (n=30); mean live cost $0.0079 per transaction, n=30.
> - **What this does not establish:** live CLI/provider accuracy or confidentiality; natural-conflict performance; legal correctness; performance outside this 30-case test-only run; clause-location quality; Nigerian or Gulf law claims. Human review is still pending.

## Try the fictional offline demo

```text
python prototype/run_demo.py --workdir <dir>
```

See [prototype/README.md](prototype/README.md). The demo uses fictional documents and scripted offline responses in a workspace outside the repository. It makes no provider calls and is a functionality demonstration only: **not an accuracy evaluation**.

## Disclosures and limits

- CUAD consists of US commercial contracts; findings are illustrative, not claims about Nigerian or Gulf law.
- CUAD clause-category labels are available to the agent, so clause location is not evaluated.
- The selected contract groups are project-defined title buckets, not an official CUAD family taxonomy.
- Emmanuel authors the additional obligations and deadlines under the [annotation guide](guide/annotation-guide.md), frozen at `guide-v1.0`.
- A human sweep found no genuine E2 conflict among the 40 selected contracts.
- All 14 E2 cases (5 dev, 9 test) are constructed composites assembled from real clauses, with pairs and gold chosen by a human; they are not natural-conflict samples.
- The final split was 26 dev cases (15 clear, 5 conflicting, 4 out-of-scope, 2 adversarial) and 30 test cases (12 clear, 9 conflicting, 5 out-of-scope, 4 adversarial), total 56.
- The 30-case test run is test-only and uses cached provider responses; it is the only released held-out evaluation here.

**The held-out set was not fully blind.** Test annotations were exposed in public repository history before the run, and the then-current Arena branch tip still tracked test annotations and notes before freeze. The exposure was accepted and documented in [DECISIONS.md](DECISIONS.md). The held-out commitment was re-signed at human direction after dev live runs and before the held-out run, as recorded in [the Phase E report](reports/phase-E.md). These facts do not establish that held-out content was used for tuning, but limit claims of independence. The selection's exclusion of the original CUAD test contracts has not been independently established.

## Historical held-out evaluation (frozen baseline)

The results below are the historical evaluation of the frozen baseline on the annotated CUAD-based test split. They are not results for the newer local user-contract CLI described below.

Exception rate: 96.7% (29/30; Wilson 95% 83.3%–99.4%).
Absolute deadline capture: not measurable (0 denominator).
Relative deadline capture: 20.0% (1/5; Wilson 95% 3.6%–62.4%).
Obligation recall: 26.8% (11/41; Wilson 95% 15.7%–41.9%).
Escalation recall: 77.8% (7/9; Wilson 95% 45.3%–93.7%); false escalation: 81.0% (17/21; Wilson 95% 60.0%–92.3%); grounded quote rate: 100.0% (38/38; Wilson 95% 90.8%–100.0%).
Latency p50/p95: 74656.0 / 120603.0 ms (n=30); live cost: $0.0079 per transaction, n=30.
Constructed E2 cases: 9; exception rate: 100.0% (9/9; Wilson 95% 70.1%–100.0%); E2-code recall: 33.3% (3/9; Wilson 95% 12.1%–64.6%). These are reported separately and do not estimate natural-conflict performance.

Proportion intervals are Wilson 95%; latency and cost report sample counts instead. See [the test metrics](eval_results/metrics_test.json) for recurring and no-deadline breakdowns. Relative-deadline results have a small denominator and a wide interval. A completed valid run means the execution completed without dead-lettered cases; it does not mean the performance targets were met. The 100% grounded-quote result means each extracted quote was found in the source after whitespace normalisation; it does not establish that the quote supports the obligation or that the obligation is correct.

## Scope and methods

Cuts: none instructed. Dev/test source-document overlap: 0. Live test runs executed: 1. The held-out run used `gemini-3.5-flash-lite` and `system_v3`; the human selected a test-only live run instead of the original all-splits command. See [Phase F](reports/phase-F.md).

Dev exception history, from the committed round summaries: [round one](eval_results/rounds/dev_round_1_summary.md), 88.5% (23/26; Wilson 95% 71.0%-96.0%); [round two](eval_results/rounds/dev_round_2_summary.md), 84.6% (22/26; 66.5%-93.8%); [round three](eval_results/rounds/dev_round_3_summary.md), 88.5% (23/26; 71.0%-96.0%). Round one was a cached re-score after a human dev reclassification; the later rounds were live. The same-config round-three run A had 100.0% exceptions (26/26; Wilson 95% 87.1%-100.0%) but crashed during detail serialization; the artifact-complete run B is the round-three result above. This variability means small round-to-round movements should not be treated as reliable gains. The frozen baseline was not tuned on the held-out results. A separately versioned CLI candidate was later developed using dev cases; it is not the frozen baseline and has no held-out result.

The E1 and E5 floors are both documented fallbacks, not well-supported calibrations: E1 had one distinct dev positive, and no E5 candidate met the false-escalation constraint. The pooled calibration observations repeat the same dev cases and are not independent cases. See [threshold calibration](eval_results/threshold_calibration.md).

## Failure taxonomy and honest failures

The [prespecified falsification rule](eval_results/targets.md) triggers if exception rate exceeds 35% or relative deadline capture falls below 55%. Both conditions triggered on the held-out run.

The design is wrong, not the model. A suspected cause is missing or ambiguous effective-date labels in contracts with relative deadlines; this requires investigation.

- **Incomplete duty extraction:** obligations and their deadlines were often missed or did not match the human annotation. A grounded quotation alone does not establish that the selected duty, type or party is correct.
- **Escalation errors:** unnecessary escalations were common. The runtime can add review routing for default-priority types or unresolved fields, while the model can also flag ambiguity or conflict; the aggregate does not attribute every false escalation to a single cause.
- **Terminal and recovered tool failures:** some cases ended in schema failure or exhausted the turn limit; other cases recovered from tool errors. The prespecified exception measure counts recorded errors even if a later call succeeds, so it is not a count of terminal failures alone.
- **Constructed conflicts:** conflict-code detection was limited, and all constructed-conflict cases had exceptions. These stitched examples do not measure the frequency or detection rate of naturally occurring conflicts.
- **Grounding is necessary but insufficient:** every extracted quotation counted by the grounding metric appeared in the source after whitespace normalization. The metric excludes cases that produced no quotation and does not verify legal interpretation, completeness, role or deadline.

## Human review

Pending: three real reviewers and 20 sampled escalations, planned for v1.0.1. No review agreement is claimed. Human reviewers, not the model, decide escalated issues. Dates that cannot be resolved without guessing remain unresolved and are escalated.

## Offline reproduction

Run `python run_eval.py --split test` with the released cache; then run `python check_readme.py`. No API key or network is required. For the versioned compressed cache artifact and clean-clone verification, see `CACHE-ARTIFACT.md`.

Set `B2_OFFLINE=1` explicitly for replay. The Phase F report records a fresh Windows clone replay with that setting, no API keys and a byte-identical test summary. The host network itself was not disabled. The released test synthetic shard and response cache are required for reproduction; see [Phase F](reports/phase-F.md).

The checkout currently tracks 10,479 response files under `cache/llm/`. `CACHE-ARTIFACT.md` documents a versioned compressed artifact with a SHA-256 checksum, exact download and verification steps, and a clean-clone replay. The artifact is not yet published; the tracked files remain the current replay source.

## Local user-contract CLI (v0.1.1; separate from the historical evaluation)

`b2cli` is an optional local tool for post-signature triage of your own contract text. It is a newer, separately versioned path for unlabelled user contracts. It reuses the same engine, validation, deadline logic and escalation routing as the frozen baseline, but it has **no accuracy claim**: the historical results in this README come from the annotated CUAD-based test split, not from this unlabelled-input path.

python -m b2cli --contract ./contract.txt --party customer --ref MY-2026-01

The default is offline replay: responses are read from `b2cli_data/cache`, and a cache miss exits 3 without opening a socket. Live mode is opt-in (`--live --acknowledge-live`), sends the contract text to the configured provider, requires a key in the environment (or `--env-file`), and enforces `--max-requests` before every HTTP attempt (retries included) plus a `--max-cost-usd` conservative worst-case reservation per attempt. The reported cost is an estimate from provider-reported usage, not provider billing, and only a provider-side quota is authoritative. User documents carry no expert clause labels, so the category-filtered E1 precheck is disabled for this path and E1 is applied after the model loop when zero obligations are recorded. Without the optional B1 embedding package a deterministic hash embedder (`b2cli-hash-384d`) is used, so retrieval quality is lower than in the evaluated pipeline. The SQLite database, cache and `report.json` default to the untracked `b2cli_data/` directory. Escalated items require human review; this tool does not provide legal advice.

## Later development status (not a held-out result)

After the historical evaluation, a separately versioned CLI candidate was developed using dev cases; the frozen baseline itself was not tuned on held-out results. The final candidate-v2 live dev run completed 19/26 cases and missed the primary quality targets. The remaining cases were not run because the authorized attempt cap was reached. Candidate v2 is not the published CLI and is not a fresh held-out result. Earlier offline replay figures were development diagnostics, not live performance. The published CLI remains v0.1.1.

## Measurement definitions

An exception is any failed per-case check or recorded error, including a recovered tool error; it is not simply a count of terminal failures. Obligations match on type and owed-by, with no more than one unmatched extra per case. A deadline must match in kind and, where gold has a resolved date, within one day; when gold is unresolved the output must also remain unresolved. `none` is captured as a kind. Quotes are grounded when present in the source after collapsing whitespace only. Recall denominators are gold obligations or gold deadlines; grounded rate uses extracted quotes; escalation rates use gold-positive or gold-negative cases respectively. Constructed E2-code recall is the fraction of constructed conflicting cases with human E2 gold for which the output contains E2.

The E1 precheck uses the human-authored taxonomy and cached query embeddings. E5 is applied after model output. Default-escalating types are routed conservatively for review; a candidate pair is not by itself proof of a conflict. Human reviewers, not the model, decide escalated issues. Unresolved dates remain unresolved rather than guessed. End-to-end latency is unavailable for a partially resumed live case unless an earlier complete measurement exists. Cost uses recorded live-run metadata; local embeddings are assumed to have no per-call API charge.

## Safety and scope

Human reviewers, not the model, decide escalated issues. The system is not legal advice. Dates that cannot be resolved without guessing remain unresolved and are escalated. Model prices must be configured before live calls and are captured in cache metadata. Local embeddings are assumed to have no per-call API charge.
