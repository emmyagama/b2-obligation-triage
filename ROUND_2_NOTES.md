# Round 2 digest — proposed final dev tuning patch

## Scope and activation

This patch is based on the dev-only Round 2 digest and summary on `b2/build` at `0eb470aa4400`. It adds `prompts/system_v3.md`, updates only `config/tool_descriptions.yaml`, and contains this note. The next dev evaluation is the third and final permitted round. No gold, thresholds, scorer, guide, runtime code, corpus, model or held-out data is changed here.

The harness currently selects `system_v2` in `config/model.yaml`; the permitted tuning ZIP cannot modify that file. Applying the patch alone does not activate the new prompt. Emmanuel must authorize OpenCode to make the minimal operational `prompt_version: system_v3` change, as was done for the previous round, before any next run. Record the prompt version and commit in run metadata. Do not calibrate thresholds during the tuning round or alter scoring after seeing results.

## Important integrity incident — action before proceeding

The current public tip of the separate Arena branch, commit `37ef1d6b68de`, still tracks 30 held-out case YAML files under `cases/src/test-*.yaml` and `cases/TEST-NOTES.md`. I checked path names only and did not open their contents. The `b2/build` tip does not track those files. The previous decisions record accepted historical exposure, but these files remain accessible at a current branch tip, not merely in history. Emmanuel/OpenCode must decide containment immediately and remove them from the public branch tip using an ordinary forward commit if authorized; do not force-push. Historical exposure and any accepted limitations remain, and this is not a fully blind held-out set. The current pre-push guard checks the test YAML pattern but does not explicitly protect `cases/TEST-NOTES.md`; the ignore rule alone does not block force-add. Fixing the guard is outside this tuning patch and needs a separate authorized change. Do not proceed to freeze on the assumption the embargo is intact.

## Round 2 observations

The case and threshold hashes were unchanged. Round 1 was an offline replay of a prior live baseline after human reclassification; Round 2 was live. Exception rate fell from 23/26 (88.5%) to 22/26 (84.6%). Obligation recall rose from 6/41 to 8/41; constructed E2-code recall rose from 1/5 to 3/5. Those gains are small-sample observations, not evidence of a reliable improvement; E2 cases are constructed and cannot estimate natural-conflict performance. Meanwhile relative-deadline capture fell from 4/15 to 3/15, false escalation rose from 12/19 to 14/19, and terminal E4 failures rose from 4 to 7, including five turn-limit failures. The stop rule's literal no-gain condition was not met, so this final round is proposed, not a claim that the change was successful overall.

## Changes and hypotheses

- **Harder turn budget:** ask for a small set of distinct searches early, parallel category calls where supported, and a terminal submission by the sixth model turn with room for one repair. A terminal call is required rather than spending the last turn on another lookup. Expected effect: fewer loop-exhaustion failures; the tradeoff is potentially less coverage, which the next dev run must measure.
- **Schema and evidence discipline:** distinguish the singular search argument from unsupported alternatives; use exact categories and identifiers from evidence; preserve quotation case and punctuation; list required terminal and per-obligation fields; on validation error fix the reported issue and retry. Expected effect: fewer avoidable validation errors and lost decisions, without changing validation rules.
- **Preserve general safeguards:** keep substantive review of all supported duties, party mapping, deadline kinds, unresolved anchors and the four E2 conflict conditions. The tool description changes reiterate the existing schemas; no case-specific examples or copied text are included.

These are hypotheses, not measured improvements. Prompts cannot expose the precheck evidence that is only logged, make the system-owned E1 code directly available to the model, prevent automatic E3 routing by the runtime, or resolve an intrinsically ambiguous anchor. Under the present provisional floor, an exact minimum score does not trigger E1 because the comparison is strict. Calibration remains a separate, once-only post-tuning activity. The exception metric intentionally includes recovered tool errors under the existing implementation; do not change that definition after observing results.

Some dev labels may merit human review for joint-party treatment and time classification; no corrections or proposed gold are supplied. If the next round reaches the limit, stop tuning regardless of results and report the outcome honestly. Do not claim readiness for a held-out run until the embargo incident and all freeze gates have been addressed.

## Verification

The patch is limited to the allowed paths and contains no contract excerpts or concrete case/document identifiers. The targeted prompt/tool hygiene check uses the available original corpus and current dev identifiers; it does not inspect held-out content. Whole-repository hygiene is already blocked by identifier-bearing dev digests and the decisions log; the earlier digest encoding issue was repaired by OpenCode, but these existing scanner conflicts remain. No live model or API call, held-out content access, calibration or scoring change was made here.
