NEXT ACTION FOR HUMAN: send **`TEST FROZEN`** when `cases/test.json` and `cases/src/test-*.yaml` are complete and `scripts/validate_cases.py --strict` passes. That exact message is the gate for Phase E step 2 (`build_cases.py --split test` → commit + tag `test-frozen` → `freeze_check.py --split test` → tag `code-frozen`); calibration is done and nothing else is blocking.

Phase: E (step 1 complete)   Branch/sha: `b2/build` @ pending commit   Date: 2026-11-04

## 1. What ran

```
$ python scripts/reconstruct_details.py --run <B> --diff --out recon_B.json   -> 26/26 identical, exit 0
$ python scripts/reconstruct_details.py --run <B> --lean                       -> recon_B_lean.json
$ python scripts/reconstruct_details.py --run <A> --lean                       -> A/details.reconstructed.json (87,693 B, 0 gaps)
$ python scripts/calibrate_floors.py --run <A dir> --run <B dir>               -> exit 0
$ git check-ignore eval_results/scratch/<runA>/details.reconstructed.json      -> .gitignore:21 eval_results/scratch/
$ pytest -q -k "calibration or heldout_digest"                                 -> 2 passed
```

Calibration consumed round 3 only (`system_v3`, both runs): **run A** `run_dev_20261104T111659780513Z` (reconstructed), **run B** `run_dev_20261104T120406146271Z` (as written). No round 1/2 data was used, per your directive.

## 2. Thresholds written

`config/thresholds.yaml` (provenance labels are required to be non-`provisional` by `run_eval.py:83`):

| key | value | provenance | basis |
|---|---|---|---|
| `e1.value` | **-0.9999999999999999** | `uncalibrated-fallback` | `math.nextafter(-1.0, inf)` — smallest float above the minimum observed retrieval score; 1 distinct gold positive (dev-15) |
| `e5.value` | **0.65** | `uncalibrated-fallback` | no swept floor met false escalation ≤ 0.20 → spec fallback |
| `calibration_sha256` | `c8fe42a9…795cf2d` | — | sha256 of `eval_results/threshold_calibration.md`; re-verified `match: True` (freeze_check line 31) |

**E1** (`threshold_calibration.md` § E1): the sweep is one row above -1.0 (recall 1.000, false escalation 0.000) and then monotonically worse, so the floor sits just above -1.0. This is a *fallback*, not a sweep: one positive case cannot support a calibration, which is why the label is `uncalibrated-fallback` rather than `dev-sweep` (the 13-positive test fixture still exercises the `dev-sweep` path — `tests/test_engine.py:174` passes).

**E5** (§ E5): the sweep is **flat** — all four floors give pooled recall 1.000 / false escalation 0.789, because no case has a minimum confidence in (0, 0.80): 3 cases sit at 0 and 49 at ≥ 0.85. False escalation is driven by escalation codes (E2/E3/E4), not the confidence floor, so 0.65 is carried as the documented fallback rather than as a tuned value.

Per-run and pooled (both are printed in the report):

| | pooled (n=52) | run A | run B |
|---|---:|---:|---:|
| false escalation at every floor | 0.789 | 0.737 | 0.842 |
| recall at every floor | 1.000 | 1.000 | 1.000 |

Two caveats are recorded in the report itself: pooled n=52 is the **same 26 cases twice, not independent draws**, and run-to-run variance on the identical config (E4 4 vs 8, `schema_valid` 22 vs 18, `exception_rate` 1.000 vs 0.885, `deadline_relative` 0.067 vs 0.267, `false_escalation` 0.737 vs 0.789) **exceeds most round-to-round deltas**, so every figure above is dev-only and noisy.

## 3. Run A reconstruction — provenance

Per your instruction there is **no** `details.json` for run A. `scripts/reconstruct_details.py --lean` wrote `eval_results/scratch/run_dev_20261104T111659780513Z/details.reconstructed.json` (`"reconstructed": true`, 26 rows, only the four fields `calibrate_floors.py` reads).

- **Proof before use:** the same script run against **run B** was diffed against B's real `details.json` — **all 26 rows identical** on `case`, `retrieval_score`, `args`, `decision.escalation_codes`, 0 gaps, exit 0. (The earlier full-mode reconstruction of B was byte-identical at 159,628 bytes.) Any mismatch would have stopped me and been reported; there was none.
- **Cross-checks on A:** 26 rows, 0 gaps; rows without `args` = `dev-01, dev-03, dev-14, dev-20` = exactly A's four `schema_valid=False` cases.
- **Unrecoverable:** turn-1 `metadata.created_at` and `system_fingerprint` for all 25 runs — run B overwrote those cache entries at the shared turn-1 request key and `tool_calls` stores no per-call timestamp. Neither is read by calibration.
- **Consumer audit (your confirmation requirement):** only `scripts/failure_digest.py:17` and `scripts/calibrate_floors.py:9` read `details.json` anywhere in the tree; `check_readme.py` → `scripts/render_readme.py` reads `run_metadata.json` and metrics only; `freeze_check.py` has no `details` reference; round summaries are prose. The digest was already run against run B for round 3. Nothing reads A's `details.json`.
- A's file lives under `eval_results/scratch/`, which `.gitignore:21` covers, so it stays **local** and is regenerable from the committed script — consistent with the brief's "scratch will not be committed".

## 4. Gate status for steps 2–4 (not started)

- `freeze_check.py` prerequisites already satisfied: calibration report hash matches, no `provisional` provenance. It will still **fail** until `code-frozen` and `guide-v1.0` tags + held-out artifacts exist (lines 23, 11–22) — that is step 3, after `TEST FROZEN`.
- `eval_results/test_run_log.jsonl` has no valid completed entry (calibration-before-test ordering preserved).
- No held-out file, guide, prompt, score or gold was touched.

## 5. Artifacts

- `config/thresholds.yaml`, `eval_results/threshold_calibration.md` — Phase E step 1 outputs (committed).
- `scripts/reconstruct_details.py` (243 lines), `scripts/calibrate_floors.py` (146 lines) — both >20-line, human-directed, logged in `INTEGRATION-LOG.md`.
- `INTEGRATION-LOG.md` — reconstruction + calibration entry.
- Run artifacts stay local under `eval_results/scratch/` (gitignored); `eval_results/case_validation.json` and `eval_results/dev_run_log.jsonl` are pre-existing untracked files left untouched.
