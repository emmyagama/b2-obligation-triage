NEXT ACTION FOR HUMAN: review `handoff/round_2.md` (the live system_v2 failure digest) and hand me the build agent's **round-2 patch** as `round_2.zip`; I will run `scripts/check_patch_surface.py round_2.zip`, apply it, re-run hygiene + the full suite, and commit `tuning round 2 patch`. Round 2 improved recall and E2 detection but **regressed on terminal failures (E4 4 -> 7) and false escalation (0.632 -> 0.737)** — decide whether you want the next patch to prioritise those over further recall gains. Nothing else is pending on my side.

Phase: D, round 2 (apply round-1 patch -> live dev run -> digest)   Branch/sha: `b2/build` @ `99dd9f1`   Date: 2026-11-04

## 1. What ran

```
$ (GEMINI_API_KEY loaded from .env, B2_OFFLINE unset)
$ run_eval.py --split dev --live --scratch --limit 2 --rpm 4   -> exit 0   smoke, prompt_version=system_v2, 2/2 schema_valid, 0 errors
$ run_eval.py --split dev --live --scratch --rpm 4             -> exit 0   26/26 cases, 43.2 min
  output: eval_results/scratch/run_dev_20261104T065517968832Z
```

Provenance from `run_metadata.json`: `mode=live`, `prompt_version=system_v2`, `git_sha=99dd9f1`, `case_sha256=14c7d097…` (unchanged — no gold edit), `threshold_sha256=180eae38…` (unchanged — no calibration).

The round-1 patch was applied and verified before this run: `check_patch_surface.py` → `patch surface passed`; the three patch files pass the hygiene scanner's own predicates; suite `60 passed, 1 skipped`.

## 2. Wins under `system_v2`

| metric | round 1 (re-scored) | round 2 |
|---|---|---|
| `obligation_recall` | 0.146 (6/41) | **0.195 (8/41)** |
| `constructed_e2_recall` | 0.200 (1/5) | **0.600 (3/5)** |
| `constructed_e2_exception_rate` | 1.000 (5/5) | **0.800 (4/5)** |
| `grounded_rate` | 1.000 (7/7) | **1.000 (17/17)** — 17 grounded obligations vs 7 |
| `exception_rate` | 0.885 (23/26) | **0.846 (22/26)** |
| `deadline_none` | 0.053 (1/19) | **0.105 (2/19)** |

The patch's "report each supported duty" and "E2 conflict conditions" hypotheses both moved in the intended direction; grounded obligations more than doubled while staying fully grounded.

## 3. Regressions

| metric | round 1 | round 2 |
|---|---|---|
| **E4 terminal failures** | **4** | **7** |
| `schema_valid` | 22/26 | **19/26** |
| `false_escalation` | 0.632 (12/19) | **0.737 (14/19)** |
| `deadline_relative` | 0.267 (4/15) | **0.200 (3/15)** |
| cost (mean/case) | $0.00538 | $0.00793 (+47%) |
| latency p50 | 82.8 s | 105.6 s |

`escalation_recall` is unchanged at 0.714 (5/7).

**Round 2 E4 failures by case id (n=7):**

| case id | class | error_class |
|---|---|---|
| `dev-03` | clear | `LOOP_EXHAUSTED` |
| `dev-06` | clear | `LOOP_EXHAUSTED` |
| `dev-08` | clear | `LOOP_EXHAUSTED` |
| `dev-09` | clear | `LOOP_EXHAUSTED` |
| `dev-11` | clear | `LOOP_EXHAUSTED` |
| `dev-14` | clear | `SCHEMA_FAIL` |
| `dev-21` | adversarial | `SCHEMA_FAIL` |

Round 1's four were `dev-06`, `dev-08`, `dev-12`, `dev-24`. **Fixed:** `dev-12`, `dev-24`. **New:** `dev-03`, `dev-09`, `dev-11`, `dev-14`, `dev-21`. The turn budget (`max_turns: 8`) is being consumed faster under the longer system_v2 prompt plus expanded tool descriptions — five of seven are `LOOP_EXHAUSTED`, i.e. no terminal `record_obligations` before the limit.

## 4. Unchanged, and why

- `retrieval_score` is **byte-identical across all 26 cases** (min −1.000 / mean 0.528 / max 0.709). This is correct, not a cache artefact: `retrieval_precheck` (`agent/engine.py:33-46`) embeds the *frozen taxonomy's* category queries and searches the committed index, so it is prompt- and model-independent by construction.
- `dev-15` is still `escalation_correct: false` with `retrieval_score = -1.0` against a provisional `e1_floor` of `-1.0`. `engine.py:47` fires E1 only on `score < floor`, so E1 remains structurally unreachable until Phase E calibration. I did **not** run `calibrate_floors.py`; `threshold_sha256` is unchanged and `calibration_sha256` is still null.
- No gold, guide, scorer, threshold or held-out path was touched.

## 5. Cost

26 live cases, ~1,007,909 input / 13,346 output tokens, **$0.2063 total** (vs $0.14 in round 1 — the system_v2 prompt is 3,601 chars vs 947, and turn counts rose). 0 HTTP failures; all `gemini-3.5-flash-lite`.

## 6. Standing issues (unchanged)

- **Whole-repo `prompt_hygiene.py` is still red**, now cleanly: it reports `identifier pattern in handoff\round_1.md` (the 33 `CUAD_…` ids in the tool traces) and would next report `document or case id in DECISIONS.md (matched 'dev-15')`. Per your instruction only the cp1252 encoding defect was fixed (digests now write UTF-8); no scanner path was exempted. Round 2's digest is valid UTF-8.
- `scripts/freeze_check.py` still lacks the `code-frozen` tag and a calibration report — Phase E, deliberately deferred until after the last tuning round.
- Held-out exposure remains accepted and disclosed (`DECISIONS.md`).

## 7. Artifacts

- `handoff/round_2.md` — live system_v2 failure digest (78,588 B, UTF-8, no truncation).
- `eval_results/rounds/dev_round_2_summary.md` — delta table, E4 lists, class breakdown.
- Run artifacts stay local under `eval_results/scratch/` (gitignored).
