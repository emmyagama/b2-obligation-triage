NEXT ACTION FOR HUMAN: **Phase D is finished — 3 of 3 permitted rounds are used, so tuning stops here regardless of result (per `ROUND_2_NOTES.md`).** Please authorize me to start **Phase E**: run `scripts/calibrate_floors.py` (the one activity you told me to hold until now), regenerate `config/thresholds.yaml`, run `scripts/freeze_check.py`, tag `code-frozen`, then execute the held-out `--split test` live run and write `reports/phase-E.md`. Two things need your call first: (1) whole-repo `prompt_hygiene.py` is still red on the standing `handoff/round_1.md` identifier findings — do I keep reporting it red through freeze, or finally exempt those paths? (2) Phase E's calibration report will *consume dev results from all three rounds*, and the run-to-run variance below is larger than most round-to-round deltas, so say whether you want a single pooled calibration or a variance-aware one. Nothing else is blocking.

Phase: D, round 3 (final)   Branch/sha: `b2/build` @ `3cf3380`   Date: 2026-11-04

## 1. What ran

```
$ run_eval.py --split dev --live --scratch --limit 2 --rpm 4  -> exit 0  (bad key: 2x HTTPError, discarded)
$ run_eval.py --split dev --live --scratch --limit 2 --rpm 4  -> exit 0  (clean; run_dev_20261104T111200943209Z)
$ run_eval.py --split dev --live --scratch --rpm 4            -> exit 1  (crash, details.json 0 bytes)
$   ... evalio.py encoding fix, suite 60 passed/1 skipped ...
$ run_eval.py --split dev --live --scratch --rpm 4            -> exit 0  -> run_dev_20261104T120406146271Z
```

Official round-3 result: **`eval_results/scratch/run_dev_20261104T120406146271Z`** — `mode=live`, `prompt_version=system_v3`, `git_sha=3cf3380`, `case_sha256=14c7d097…`, `threshold_sha256=180eae38…` (both unchanged), 26/26 cases, 37.5 min.

Patch applied before running: `check_patch_surface.py` → `patch surface passed`; all three patch files pass the scanner's own predicates; suite `60 passed, 1 skipped`.

## 2. Round 2 → round 3

| metric | round 2 | round 3 | direction |
|---|---|---|---|
| `escalation_recall` | 0.714 (5/7) | **0.857 (6/7)** | better |
| `obligation_recall` | 0.195 (8/41) | **0.220 (9/41)** | better |
| `deadline_relative` | 0.200 (3/15) | **0.267 (4/15)** | better |
| `grounded_rate` | 1.000 (17/17) | 1.000 (16/16) | unchanged |
| `constructed_e2_recall` | 0.600 (3/5) | **0.200 (1/5)** | worse |
| `exception_rate` | 0.846 (22/26) | **0.885 (23/26)** | worse |
| `false_escalation` | 0.737 (14/19) | **0.789 (15/19)** | worse |
| terminal E4 failures | 7 | **8** | worse |
| `schema_valid` | 19/26 | **18/26** | worse |

Round-3 E4 by case id (n=8): `dev-01`, `dev-03`, `dev-08`, `dev-10`, `dev-11`, `dev-16`, `dev-20`, `dev-26`.

Cost mean $0.00792/case (**$0.2060** total); p50 88.6 s, p95 122.0 s.

## 3. Run-to-run variance — the headline finding

The first round-3 invocation completed all 26 cases, then crashed writing `details.json`. Its `cases.csv` and `metrics.json` are valid, so it is usable as a **replication sample of the identical config** (`system_v3`, `git 3cf3380`, same `case_sha256`, `mode=live`). `cache_hit=0` on all 383 tool calls in the repeat, so the two runs are genuinely independent samples, not a replay.

| | run A (crashed) | run B (complete) |
|---|---|---|
| terminal E4 failures | **4** | **8** |
| E4 case ids | `dev-01`, `dev-03`, `dev-14`, `dev-20` | `dev-01`, `dev-03`, `dev-08`, `dev-10`, `dev-11`, `dev-16`, `dev-20`, `dev-26` |
| `schema_valid` | 22/26 | 18/26 |
| `escalation_recall` | 0.857 (6/7) | 0.857 (6/7) |
| `obligation_recall` | 0.220 (9/41) | 0.220 (9/41) |
| `constructed_e2_recall` | 0.200 (1/5) | 0.200 (1/5) |
| `exception_rate` | **1.000 (26/26)** | 0.885 (23/26) |
| `false_escalation` | 0.737 (14/19) | 0.789 (15/19) |
| `deadline_relative` | **0.067 (1/15)** | 0.267 (4/15) |
| `grounded_rate` | 1.000 (22/22) | 1.000 (16/16) |

**14 of 26 cases differ on decision fields** (`escalation_correct`, `schema_valid`, `obligations_found`, `deadlines_captured`, `exception`, `predicted_e2`) between two runs of the same configuration: `dev-06`, `dev-07`, `dev-08`, `dev-09`, `dev-10`, `dev-11`, `dev-12`, `dev-14`, `dev-16`, `dev-18`, `dev-19`, `dev-24`, `dev-25`, `dev-26`.

Splitting the metrics by behaviour matters more than the headline:

- **Stable across both runs:** `escalation_recall` 0.857, `obligation_recall` 0.220, `constructed_e2_recall` 0.200. Since both agree and both differ from round 2 (0.714 / 0.195 / 0.600), these three movements are the ones that survive a repeat: escalation +1 case, obligations +1 case, and **constructed E2 recall genuinely regressed 3/5 → 1/5**.
- **Unstable across both runs:** terminal E4 (4 vs 8), `schema_valid` (22 vs 18), `exception_rate` (1.000 vs 0.885), `deadline_relative` (0.067 vs 0.267), `false_escalation` (0.737 vs 0.789). On these, round 2's value sits *inside* the same-config spread — round 2's E4 of 7 lies between 4 and 8, round 2's `deadline_relative` of 0.200 lies between 0.067 and 0.267 — so the round-2 → round-3 movement on them is not distinguishable from noise.

`temperature: 0` and `seed: 42` do not make `gemini-3.5-flash-lite` reproduce, and nothing in the harness retries a case to confirm a result. The individual round numbers in `reports/phase-D-round1.md` and `phase-D-round2.md` should be read with the same caveat. Run A cannot be digested by `failure_digest.py` (its `details.json` is built in memory during the run, not from `run.sqlite`), so run B is the artifact-complete round-3 record.

## 4. Arena containment (your decision, executed)

Per your instruction I removed the held-out gold from the Arena tip with an ordinary forward commit, no force-push:

- `origin/arena/18088414-b2-obligation-triage`: `37ef1d6b` → **`79f1d865`** (fast-forward), deleting `cases/TEST-NOTES.md` + `cases/src/test-01..30.yaml`.
- Verified: **0** held-out paths on the Arena tip and **0** on `b2/build`; the only `cases/` divergence left between the two branches is `CHANGELOG.md`, `dev.json`, `dev-15.yaml` (your re-split).
- History was **not** rewritten: `37ef1d6b` is still an ancestor of `b2/build`, and both branches still reach the old commits. The files therefore remain recoverable from history — this is tip containment only, and the set was never blind (per `DECISIONS.md`).
- Executed in a detached temporary worktree so the main tree was untouched; worktree removed afterwards.
- Guard hardened as authorized: `pre_push_guard.py` now treats `cases/TEST-NOTES.md` as protected (11/11 direct `protected()` checks pass).

## 5. Incidents during this round

- **Harness crash (fixed):** `agent/evalio.py:4` wrote JSON without `encoding=`, so Windows used cp1252 and died on U+2215 — losing `details.json` and 33.5 minutes of a completed run. Same class as the `prompt_hygiene.py` and `failure_digest.py` defects already fixed. One line, logged in `INTEGRATION-LOG.md`.
- **My error:** the first smoke run loaded the API key with an off-by-two substring, so both cases failed `HTTPError`. Discarded; not part of any reported number.
- **Cost:** round 3 spent **$0.3791** across two full live runs (A $0.1731 + B $0.2060) instead of one, plus a 2-case smoke, because of the crash above.
- **GitHub:** two pushes returned transient `500 Internal Server Error` and succeeded on retry; no history or ref was harmed.

## 6. Standing issues (unchanged)

- `prompt_hygiene.py` still red: `identifier pattern in handoff\round_1.md` (33 `CUAD_…` ids in tool traces), and it would next report `document or case id in DECISIONS.md (matched 'dev-15')`. No path exempted, per your earlier instruction.
- No calibration: `threshold_sha256` unchanged across all three rounds; `calibration_sha256` still null; `code-frozen` tag still absent — all Phase E.
- dev-15 still cannot reach E1 (`retrieval_score = -1.0` vs `e1_floor = -1.0`, strict `<` at `engine.py:47`).
- Held-out exposure remains accepted and disclosed.

## 7. Artifacts

- `handoff/round_3.md` — live system_v3 failure digest (81,661 B, UTF-8, no truncation).
- `eval_results/rounds/dev_round_3_summary.md` — deltas, both E4 lists, variance section, class breakdown.
- `INTEGRATION-LOG.md` — evalio encoding fix entry.
- Run artifacts stay local under `eval_results/scratch/` (gitignored).
