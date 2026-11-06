NEXT ACTION FOR HUMAN: send the **README text and docs for Phase G** (step 1: "Receive README text and docs from the human (from the build agent). Commit."). Phase F is complete — the single held-out live run is valid, the artefacts are released, and the offline replay reproduced `summary_test.md` **byte-identically**. Per the brief I stop here and start nothing in Phase G without your input.

Phase: F (complete)   Branch/sha: `b2/build` @ `22b63c5`   Date: 2026-11-06

## 1. The freeze run

```
$ B2_OFFLINE unset, GEMINI_API_KEY loaded from repo .env
$ python run_eval.py --split test --live --rpm 4        -> exit 0, "completed 30 cases"
   run dir: eval_results/run_test_20261106T015359777023Z
   wall time ~39 min (01:54 -> 02:33 UTC), 10,479 entries in cache/llm (+329 new)
```

**Deviation from the brief's literal command, already sanctioned:** the brief says `--split all --live`, but `run_eval.py:57` rejects `live` unless the split is exactly `test` (the guard is original from bundle v1 and no test pins `--split all`). You chose **`--split test --live`**, which is also what Phase F's replay and validity rules are written against. `--rpm 4` was the safe value; no rate-limit exit (4) and no `CacheMiss` (3) occurred, so neither the `--resume` path nor the stop-and-report path was needed.

**Validity (brief line 155: exit 0 with zero dead-lettered cases):**

| check | result |
|---|---|
| exit code | 0 |
| cases | 30 / 30 |
| dead-lettered (`E6_TOOL_FAILURE`) | **0** |
| `eval_results/test_run_log.jsonl` | `started` → `completed`, `valid: true`, `mode: live`, `cases: 30`, `case_sha256: ea702983…` |
| `run_metadata.json` | `mode: live`, `split: test`, `git_sha: d6456ae`, `prompt_version: system_v3`, `threshold_sha256: c591ea9a…` |

`case_sha256` equals `FROZEN.sha256` and `threshold_sha256` equals `sha256(config/thresholds.yaml)`, both re-verified after the run. `run_eval.py:31-35` now refuses any further live run, so the freeze is one-way.

## 2. Held-out results (as committed)

From `eval_results/summary_test.md` (Wilson 95%):

| Metric | Result |
|---|---|
| exception_rate | 96.7% (29/30; 83.3%–99.4%) |
| escalation_recall | 77.8% (7/9; 45.3%–93.7%) |
| false_escalation | 81.0% (17/21; 60.0%–92.3%) |
| obligation_recall | 26.8% (11/41; 15.7%–41.9%) |
| grounded_rate | **100.0%** (38/38; 90.8%–100.0%) |
| deadline_relative | 20.0% (1/5; 3.6%–62.4%) |
| deadline_recurring | 16.7% (3/18) |
| deadline_none | 5.6% (1/18) |
| deadline_absolute | not measurable (0 denominator) |

Constructed E2 cases: 9; their exception rate 100.0% (9/9), code recall 33.3% (3/9). Latency p50 / p95 **74 656 / 120 603 ms** (n=30); mean cost **0.007870434333333332 USD** (n=30), total **0.2361 USD**. `mode` is `live`.

These are the numbers the build agent documents; I have not interpreted or optimised against them, and no threshold, prompt, guide or gold may change in response to them (`run_eval.py:31-35` and the `code-frozen` tag enforce that — a change requires a v1.1 re-baseline).

## 3. Artefacts released (commit `7416b24`)

`.gitignore` embargo lines removed, then committed: `cases/src/test-*.yaml` (30), `cases/test.json`, `cache/llm/` (10,479 files, 90.8 MB), `eval_results/` (`run_test_20261106T015359777023Z/` incl. `details.json`, `cases.csv`, `run.sqlite`; plus `summary_test.md`, `metrics_test.json`, `cost_latency.csv`, `deadline_breakdown.csv`, `drift.csv`, `run_test_*.csv`, `test_run_log.jsonl`), `handoff/post_freeze_test_digest.md`, `.gitignore`.

Two scope decisions worth your eye:

- **The synthetic test shard went out too.** The brief's list does not name it, but 13 of the 30 held-out cases (`test-13`…`test-21`, `test-27`…`test-30`) resolve to `corpus/synthetic_test/documents/`, and `run_eval.py:95` raises `case document missing` without them, while `merge_test` (`agent/synthetic.py:20-32`) silently returns `False` without `db/test_docs.sqlite` and changes retrieval. Both `.gitignore` blocks are stamped *"embargoed until valid test run"* — now satisfied — so `corpus/synthetic_test/{documents,index,manifest.json}` and `db/test_docs.sqlite` are committed (**~12 MB**). `embed_cache/` (41 MB) and `db/test_docs.sqlite-*` stay local, as does `cases/TEST-NOTES.md`, which is not in your release list and is protected by `pre_push_guard.py`.
- **Left untracked, unchanged:** `eval_results/case_validation.json`, `eval_results/dev_run_log.jsonl` (pre-existing, not in the release list).

`python scripts/pre_push_guard.py` → `pre-push guard passed: valid completed live run recorded` (it now takes the `valid_log()` branch at line 14, which runs `freeze_check` and skips the embargo checks).

## 4. Reproducibility check — the headline property

```
$ git clone <local repo>  C:\...\Temp\opencode\b2-replay-clone     -> HEAD 22b63c5, tags code-frozen/guide-v1.0/targets-v1/test-frozen
$ py -3.11 scripts\venv.py setup                                   -> exit 0 (Python 3.11.9, requirements.txt)
$ (no GROQ_API_KEY, no GEMINI_API_KEY, B2_OFFLINE=1)
  python run_eval.py --split test --out <clone>/replay_out         -> exit 0, "completed 30 cases", 44.3 s
```

**Diff result: BYTE-IDENTICAL.**

```
committed sha : 7f7af0c6dd83a7726dd5831e81a1938c705850574400a19a7e243ad03b83ab12
replayed  sha : 7f7af0c6dd83a7726dd5831e81a1938c705850574400a19a7e243ad03b83ab12
BYTE-IDENTICAL : True        (1031 bytes both, 24 CRLF both)
```

`metrics_test.json` is also equal on **every** key except `mode` (`live` → `replay`) — the one difference `run_eval.py:181` is designed to record. Latency and cost reproduce because `run_eval.py:166-168` takes them from cached response metadata, not from replay timing or current pricing.

Network was not disabled (I cannot do that on this host); `B2_OFFLINE=1` makes `agent/cache.py:33` refuse HTTP, and the run carried no API keys, so the replay was provably cache-only.

### The one fix this gate forced (commit `22b63c5`, rule-1, 5 lines, logged)

The first clone failed in 2.3 s with `freeze check failed: held-out hash mismatch`. `freeze_check.py:11` hashes `cases/test.json` **raw bytes** against `FROZEN.sha256` (which hashes the local **LF** bytes), but `core.autocrlf=true` checks it out as **CRLF**. The mirror image sits at `freeze_check.py:31`: `calibration_sha256` hashes the **CRLF** working copy of `eval_results/threshold_calibration.md` while the index held **LF**, so a Linux clone would have failed there instead. Both are exactly the "checksummed artefacts" `.gitattributes` exists for and neither was listed, so the gate could never have passed off the machine that built it. Fix: `cases/test.json -text`, `eval_results/threshold_calibration.md -text`, plus a renormalize so the index carries the CRLF bytes the committed hash matches. Re-verified in a fresh clone: `test.json == FROZEN` ✓, `calibration report == calibration_sha256` ✓, `freeze check passed` ✓. Content bytes of both files are unchanged; no protected path, no scoring, threshold, guide, prompt or gold change.

## 5. Post-freeze digest

```
$ python scripts/failure_digest.py --run eval_results/run_test_20261106T015359777023Z \
      --out handoff/post_freeze_test_digest.md --post-freeze     -> exit 0, "digest written"
```

`permitted()` accepted it because the split is `test`, `--post-freeze` was set, `freeze_check` passed and a valid live completed entry for these exact case bytes exists. The digest carries aggregate metrics, per-class breakdowns and per-failing-case gold/got/trace (capped at 100,000 characters) for the build agent's documentation only.

## 6. Artifacts

- Commits: `7416b24` (release), `22b63c5` (`.gitattributes` rule-1 fix). Both pushed with the Phase F report.
- `eval_results/test_run_log.jsonl` — the frozen `started` + `completed/valid` pair; it is what makes `run_eval.py:31-35` refuse a second live run and what `pre_push_guard.py:14` keys on.
- `handoff/post_freeze_test_digest.md` — post-freeze failure digest.
- `reports/phase-F.md` (this file), `INTEGRATION-LOG.md` — embargo-lift entry and the `.gitattributes` entry.
- Still local: `cases/TEST-NOTES.md`, `corpus/synthetic_test/embed_cache/`, `db/test_docs.sqlite-*`, `eval_results/scratch/`, `eval_results/case_validation.json`, `eval_results/dev_run_log.jsonl`.
- Temp (not in the repo): `C:\Users\DELL\AppData\Local\Temp\opencode\b2-replay-clone` — the verification clone, safe to delete.

## 7. Known latent defects, deliberately unfixed

- **Locale codec reads** (`run_eval.py:69`, `build_cases.py`) still produce `Â§` mojibake in `cases/dev.json` and in `test-17`'s rationale inside `cases/test.json`; `build_cases.py`'s digest is locale-dependent. Unfixed because any edit to those files breaks `FROZEN.sha256` / the `code-frozen` tag after the freeze.
- **`eval_results/threshold_calibration.md` must remain CRLF forever** — its committed hash is over CRLF bytes. The new `.gitattributes` rule now guarantees that on every platform; do not "normalize" it.
