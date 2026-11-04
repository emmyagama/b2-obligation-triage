# Round 1 digest — proposed next-round patch

## Status and activation

Based only on the dev digest on `b2/build` (head `b5a3b2c59007`) and its accompanying dev re-score summary. This patch adds `prompts/system_v2.md` and updates `config/tool_descriptions.yaml`; it contains no gold, thresholds, scorer, code, guide, corpus or held-out material. The next run is a new dev-only prompt round, not a re-score of Round 1. Do not change the frozen scoring or calibrate thresholds during the tuning rounds.

**Activation requires a decision:** the harness currently selects `system_v1` in `config/model.yaml`, but the allowed tuning patch surface excludes that file. Merely applying this ZIP will not activate `system_v2`. Emmanuel must explicitly authorize OpenCode to make the minimal operational `prompt_version: system_v2` change, or resolve the versioning/surface conflict another way, before the next run. The patch deliberately does not change `config/model.yaml` or overwrite `system_v1`. Capture the new prompt version and source commit in the next run metadata. This activation change is distinct from changing scoring or thresholds.

The current dev configuration already reflects Emmanuel's reclassification: 15 clear, 5 constructed conflicting, 4 out-of-scope and 2 adversarial, total 26. My earlier message suggesting a present split-count mismatch was incorrect. Preserve the human's existing dev gold and configuration.

## Digest and proposed changes

The re-scored dev replay reports 23/26 exceptions, 6/41 obligation recall, 4/15 relative-deadline capture, and 12/19 false escalation. On five constructed E2 cases, E2-code recall is 1/5; these are constructed, not natural-conflict performance. These are small, dev-only samples, not held-out results. The re-score used a cached replay of the earlier live run after a human gold reclassification, not a new model run. Four cases had terminal E4 failures; the published exception definition also counts trace errors, including intermediate errors that later recovered. Keep that prespecified rule unchanged.

- **Search and tool discipline:** one query string per search, copy the current document identifier only from tool results, inspect exact categories, use multiple distinct tool calls in a turn where available, avoid redundant searches, and reserve a turn for the terminal call. Expected effect: fewer malformed calls and turn-limit failures; no guarantee of provider parallel-call behavior.
- **Evidence and coverage:** inspect operative spans and report each supported relevant duty, rather than terminating empty on thin evidence or discarding a duty because of uncertainty. Match types to the actual text; do not use an unrelated type to fit a schema. Expected effect: improved obligation recall and grounded typing without case-specific hints.
- **Party, time and E2 handling:** emphasize who performs each duty, the narrow joint-party rule, recurring versus relative deadlines, verbatim time/recurrence text, unresolved anchors, and the four conflict conditions. Expected effect: fewer deadline/schema errors and less confusion between a conflict, ordinary conditions and ambiguity.

These are hypotheses, not measured improvements. Prompt/tool changes cannot fix a missing evidence channel, scorer or validator behavior. In particular, the retrieval precheck's evidence is logged, not sent to the model; the model must obtain evidence through tools. The model cannot directly emit system-owned E1, and the provisional E1 floor is not calibrated. The runtime also turns default-review flags and unresolved anchors into E3; prompt wording alone cannot override that behavior. Any change to these mechanisms is outside this tuning patch and requires a separate human decision and re-baseline if warranted.

## Review flags — human decision only

Some dev annotations may merit human review for the joint-party rule, whether recurring language was classified consistently, and how an unresolved anchor relates to escalation. These are flags, not corrected labels or proposed gold. The digest also shows a human-reviewed reclassification; do not undo it or edit any annotation on the model's behalf.

The repository's decisions record a prior exposure of held-out annotations in pushed history, accepted by Emmanuel after removal from branch tips. No held-out content was opened for this patch. This limits any claim of fully blind evaluation and should remain disclosed.

## Verification and handoff

The ZIP contains only paths allowed by `scripts/check_patch_surface.py`. Prompt content is checked against the available original corpus and dev identifiers, with no contract excerpts or case/document IDs deliberately embedded. The current repository's published dev digest under `handoff/` contains a non-UTF-8 byte as well as identifiers and excerpts, and the whole-repo hygiene scanner scans that directory. In a controlled check the scanner failed on decoding; after decoding with replacement it failed on an identifier. A whole-repo hygiene run therefore fails independently of this patch until the digest/scanner handling is resolved. OpenCode should report that conflict and check the new prompt/tool descriptions without weakening protections or concealing the existing digest issue. No API call, live model run, test-case access, threshold tuning or scoring change was performed here.
