NEXT ACTION FOR HUMAN: review `handoff/round_1.md` (26-case failure digest re-scored against your corrected gold) and hand me the build agent's **round-1 patch** as `round_1.zip`. I will then run `scripts/check_patch_surface.py round_1.zip`, apply it, run prompt hygiene + the full test suite, commit as `tuning round 1 patch`, and start round 2. Nothing else is pending on my side.

Phase: D, round 1 (dev reclassification -> rebuild -> re-score -> digest)   Branch/sha: `b2/build` @ `0a6fcca`   Date: 2026-11-04

## 1. What the human changed (committed as-is)

Commit `30eb348` — 4 files, committed verbatim, no edits by me:

- `cases/src/dev-15.yaml`: `class: out_of_scope -> clear`, `gold_should_escalate: false -> true`, `gold_escalation_codes: [] -> [E1_NO_OBLIGATION]`, `rationale` rewritten (argues the empty register is a positive claim needing a human, and cites `guide/annotation-guide.md` §8 placing E1 inside `clear`).
- `config/splits.yaml`: dev = `{clear: 15, conflicting: 5, out_of_scope: 4, adversarial: 2}`.
- `DECISIONS.md`: +2 signed lines.
- `cases/CHANGELOG.md`: new.

`dev-16` … `dev-19` were deliberately left untouched.

## 2. Rebuild and validation — green

```
$ .venv/Scripts/python.exe scripts/build_cases.py        -> exit 0  compiled 26 dev and 30 test cases
$ .venv/Scripts/python.exe scripts/validate_cases.py     -> exit 0  valid: 26 dev, 30 test, 0 shared source documents
```

(No `--strict`, as instructed.) Rebuilt `cases/dev.json` confirms 26 cases, classes `{clear: 15, conflicting: 5, out_of_scope: 4, adversarial: 2}`, and `dev-15` = `clear` / `gold_should_escalate=True` / `[E1_NO_OBLIGATION]` / `gold_obligations: []`.

- Held-out gold untouched: `sha256(cases/test.json)` = `c3e147bb20d90071a9c32c09ee5618e14b61a7516bb8dd9c2a1e20cf8db564ea` = `cases/FROZEN.sha256`, byte-for-byte (hash only, file not opened for content).
- `validate_cases.py` rule `gold_should_escalate == bool(gold_escalation_codes)` now holds for dev-15.
- Only the 1 E1 positive exists in dev after this change (dev-15); dev has no E2/E3 besides the 5 constructed E2 conflicting cases and 1 E3.

## 3. Re-score: `failure_digest.py` cannot do it, so the run was replayed offline

- `scripts/failure_digest.py` **does not re-score**. It reads the stored `metrics.json` (line 17), `cases.csv` (line 22) and the case snapshots embedded in `details.json` (lines 23/24/31) — all written against the pre-reclassification gold. Digesting the original run dir would have published stale numbers for exactly dev-15.
- `run_eval.py` has **no in-place mode**: `run_eval.py:101` always mints a fresh `run_dir=out/run_<split>_<stamp>`, and there is no `--rescore` flag (argparse at `run_eval.py:24-25`).
- Therefore the original run was **replayed offline** and re-scored by `run_eval`'s own scoring path (`agent.scoring.score` + `agent.metrics.aggregate`), which is the only tool-faithful way to get corrected numbers:

```
$ (no GEMINI_API_KEY / GROQ_API_KEY in the shell)
$ .venv/Scripts/python.exe run_eval.py --split dev --scratch   -> exit 0
  completed 26 cases; output: eval_results/scratch/run_dev_20261104T002625424993Z
```

`mode` is recorded as **`replay`**, not `live`. Zero HTTP: `run_agent(live=False)` is cache-only, a miss would have exited 3 (`run_eval.py:205`), and no API keys were loaded, so a live call could not have succeeded anyway.

## 4. Disclosure: one cache entry was re-keyed (dev-15 transaction latency)

The pure replay first failed: `CacheMiss(7f06388a…, case=dev-15, seq=transaction)`. Two independent causes, both diagnosed before touching anything:

1. `run_eval.py:144` keys the `transaction` record on `sha256(canonical(case))` over the **whole** case dict, so a gold-only edit invalidates it — even though the agent-facing request is unchanged.
2. `run_eval.py:69` does `json.loads(path.read_text())` with **no encoding**, i.e. locale `cp1252` here, not UTF-8. The rebuilt `cases/dev.json` contains 4 non-ASCII bytes (the `§` in dev-15's new rationale), so a UTF-8 read and run_eval's read produce **different case dicts** and therefore different hashes. My first seed attempt used UTF-8 and landed on the wrong key; that mis-keyed file was deleted.

Resolution: re-keyed dev-15's `transaction` entry at the key the run actually computes, carrying over the **live run's measured latency of 73,578 ms**. The old entry's request was verified to match, and the case diff was verified to touch only `['class', 'gold_escalation_codes', 'gold_should_escalate', 'rationale']` — no `document_id`, `intake_party` or `business_context`, so the agent-facing request is provably identical and the measured latency still applies. No scoring code, gold file, prompt, or committed artifact was modified; `cache/scratch/` is gitignored.

**Latent fragility (observed, not fixed):** `run_eval.py:69` reading a UTF-8 JSON file with the locale encoding means `case_sha256` and all `transaction` keys depend on the machine's ANSI code page. I did not change it — adding `encoding='utf-8'` would re-key every transaction entry and destroy replayability for this round.

## 5. Verification: the replay reproduced the live run exactly

Row-by-row diff of `cases.csv` (baseline `run_dev_20261103T222510405942Z` vs re-scored `run_dev_20261104T002625424993Z`):

- **Only dev-15 changed substantively**: `class out_of_scope -> clear`, `escalation_correct True -> False`.
- Every other row differs solely in `git_sha`, `case_sha256`, `mode` (expected: those are run-level provenance fields).
- `error_class` distribution identical in both: `VALIDATION_ERROR` 9, blank 13, `LOOP_EXHAUSTED` 3, `SCHEMA_FAIL` 1.
- `exception` True 23/26 in both; `schema_valid` True 22/26 in both.

## 6. Corrected metrics (re-scored vs live baseline)

| metric | live baseline | re-scored |
|---|---|---|
| `escalation_recall` | 0.833 (5/6) | **0.714 (5/7)** [0.359, 0.918] |
| `false_escalation` | 0.600 (12/20) | **0.632 (12/19)** [0.410, 0.809] |
| `mode` | live | replay |
| all other aggregates (13 of 16 keys) | — | unchanged |

Unchanged and still baseline: `obligation_recall` 0.146 (6/41), `exception_rate` 0.885 (23/26), `grounded_rate` 1.000 (7/7), `schema_valid` 22/26, `cost` mean $0.00538/case, `retrieval_score` min −1.0 / mean 0.528 / max 0.709.

Deviation is exactly what the reclassification implies: dev-15 became a seventh escalation positive, and the model returned `escalated: false, escalation_codes: []` where gold now demands `E1_NO_OBLIGATION` — so it is a miss, not a pass.

## 7. The four genuine E4 failures (by case id)

| case id | class | error_class |
|---|---|---|
| `dev-06` | clear | `LOOP_EXHAUSTED` |
| `dev-08` | clear | `LOOP_EXHAUSTED` |
| `dev-12` | clear | `LOOP_EXHAUSTED` |
| `dev-24` | conflicting | `SCHEMA_FAIL` |

These are the 4 `schema_valid=false` cases. The 9 `VALIDATION_ERROR` labels are intermediate tool-argument hiccups the agent recovered from (`run_eval.py:163` promotes the first trace error to the case), which is why `exception_rate` is 0.885 while only 4 cases are terminal execution failures.

## 8. The E1 finding that round 1 should be built around

`dev-15` has `retrieval_score = -1.0` and the provisional `e1_floor` in `config/thresholds.yaml` is also **`-1.0`**. The engine emits `E1_NO_OBLIGATION` only when the retrieval score falls *under* the floor (`agent/engine.py:48`), so `-1.0 < -1.0` is false and **E1 can never fire for this case**. dev-15 is not a prompt failure — it is structurally unreachable at the current provisional floor. Calibration is what fixes it, and per your instruction I did **not** run `scripts/calibrate_floors.py`; thresholds remain `provisional-dev-only` with `calibration_sha256: null`.

## 9. Artifacts and pushes

- `handoff/round_1.md` — full failure digest (66,375 B, under the 100,000 B cap, no truncation), from `run_dev_20261104T002625424993Z`.
- `eval_results/rounds/dev_round_1_summary.md` — aggregate metrics, delta table, E4 list, class breakdown.
- Commits pushed to `origin/b2/build`: `30eb348` (human's 4 files) and `0a6fcca` (`cases/dev.json` rebuild + the two round-1 artifacts). `pre-push guard passed: no protected paths in outgoing history` for both.
- Not committed (as before): `eval_results/case_validation.json`, `eval_results/dev_run_log.jsonl` (validator/log artefacts), and everything under `eval_results/scratch/` (gitignored).
- No protected path was touched: `cases/src/` (except the human's own dev-15), `guide/`, `prompts/`, `config/tool_descriptions.yaml`, `agent/scoring.py`, `agent/metrics.py`, `config/targets*`, `eval_results/targets.md` are all untouched; no force push, no tag moved or deleted.

## 10. Not done, deliberately

- `scripts/calibrate_floors.py` — deferred to Phase E until after the last tuning round, per instruction. It would now find 1 E1 positive instead of 0.
- No live API call of any kind this round.
- `cases/test.json` not opened for content; hash-verified only.
- No patch applied — round 1 stops at the digest, waiting for `round_1.zip`.

## 11. Open question for you (not acted on)

Phase C §9 noted that all five zero-obligation dev cases (`dev-15` … `dev-19`) carry rationales describing exactly what the guide calls E1. You reclassified **only dev-15**. `dev-16` … `dev-19` remain `out_of_scope` with `gold_should_escalate: false` and `[]`, so under your ruling their empty registers do *not* escalate. That leaves dev with exactly one E1 positive, which is thin for an E1 floor sweep. If that asymmetry is intentional, no action needed; if not, it is a gold edit for a later round — I will not touch it without your word.
