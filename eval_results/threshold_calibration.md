# Threshold calibration

Dev only; n=52 across 2 runs is noisy. E1 uses gold E1 labels; E5 uses gold escalation and other retained codes. Ties: higher recall, then lower false escalation, then lower floor.

## Sources

- `eval_results/scratch/run_dev_20261104T111659780513Z` — reconstructed from run.sqlite (`details.reconstructed.json`, `"reconstructed": true`); n=26.
- `eval_results/scratch/run_dev_20261104T120406146271Z` — run `details.json` as written; n=26.

Run A has no usable `details.json` (0 bytes: the harness crashed writing it), so it is reconstructed by `scripts/reconstruct_details.py --lean`, whose output carries `"reconstructed": true` and only the fields this script reads.
The same reconstruction was first run against run B and diffed against B's real `details.json`: **all 26 rows identical** on `case`, `retrieval_score`, `args` and `decision.escalation_codes` (0 gaps). That diff is the provenance proof for run A.
Unrecoverable in run A: the turn-1 `metadata` of every run — `created_at` and `system_fingerprint` (25 runs each). Run B overwrote those cache entries because turn-1 requests are identical across runs, and `tool_calls` stores no per-call timestamp. Neither field is read by this script.
Nothing else in Phase E reads run A's `details.json`: `check_readme.py` (repo root) goes through `scripts/render_readme.py`, which reads `run_metadata.json` and metrics only; `scripts/freeze_check.py` has no `details` reference; the round summaries are prose; and of the whole tree only `scripts/failure_digest.py:17` and this script read `details.json` (the digest was already run against run B for round 3).

## E1

| Floor | Recall | False escalation |
|---:|---:|---:|
| -2.0 | 0.000 | 0.000 |
| -0.9999999999999999 | 1.000 | 0.000 |
| 0.43850000000000006 | 1.000 | 0.080 |
| 0.5013000000000001 | 1.000 | 0.120 |
| 0.5057000000000001 | 1.000 | 0.200 |
| 0.5206000000000001 | 1.000 | 0.240 |
| 0.5339000000000002 | 1.000 | 0.280 |
| 0.5459000000000002 | 1.000 | 0.360 |
| 0.5542000000000001 | 1.000 | 0.400 |
| 0.5572000000000001 | 1.000 | 0.440 |
| 0.5957000000000001 | 1.000 | 0.560 |
| 0.6149000000000001 | 1.000 | 0.600 |
| 0.6185000000000002 | 1.000 | 0.640 |
| 0.6233000000000001 | 1.000 | 0.680 |
| 0.6263000000000001 | 1.000 | 0.720 |
| 0.6575000000000001 | 1.000 | 0.760 |
| 0.6846000000000001 | 1.000 | 0.880 |
| 0.6931000000000002 | 1.000 | 0.920 |
| 0.7085000000000001 | 1.000 | 1.000 |

Selected E1: -0.9999999999999999. The sweep steps the floor to `math.nextafter(score, inf)`, i.e. the smallest float above each observed score, and the selected value is the smallest float above the minimum observed score (-1); E1 fires only when retrieval returns nothing better.
Provenance: uncalibrated-fallback — gold carries 1 distinct E1 positive case(s) (dev-15), so this floor rests on a single example (retrieval score -1) and is not a sweep-based calibration.

## E5

### Pooled (2 runs, n=52)

| Floor | Recall | False escalation |
|---:|---:|---:|
| 0.50 | 1.000 | 0.789 |
| 0.60 | 1.000 | 0.789 |
| 0.70 | 1.000 | 0.789 |
| 0.80 | 1.000 | 0.789 |

Selected E5: 0.65 (uncalibrated-fallback).

No swept floor satisfies false escalation <= 0.20, so the spec fallback 0.65 applies. The sweep is flat: no case has a minimum confidence between 0 and 0.80 (3 case(s) sit at 0 and are caught by every floor, 49 sit at or above 0.85 and are caught by none), so all four floors give identical predictions. False escalation is driven by escalation codes (E2/E3/E4), not by the confidence floor.

### eval_results/scratch/run_dev_20261104T111659780513Z

| Floor | Recall | False escalation |
|---:|---:|---:|
| 0.50 | 1.000 | 0.737 |
| 0.60 | 1.000 | 0.737 |
| 0.70 | 1.000 | 0.737 |
| 0.80 | 1.000 | 0.737 |

E5 for this run alone: 0.65 (uncalibrated-fallback); E1 for this run alone: -0.9999999999999999.

### eval_results/scratch/run_dev_20261104T120406146271Z

| Floor | Recall | False escalation |
|---:|---:|---:|
| 0.50 | 1.000 | 0.842 |
| 0.60 | 1.000 | 0.842 |
| 0.70 | 1.000 | 0.842 |
| 0.80 | 1.000 | 0.842 |

E5 for this run alone: 0.65 (uncalibrated-fallback); E1 for this run alone: -0.9999999999999999.

Per-run and pooled tables use the selected pooled E1 floor so they describe the configuration being frozen.

## Independence of the pooled sample

The pooled n=52 is the same 26 dev cases observed once per run, not independent draws: the same case contributes 2 times, so the pooled figures are not 2x the evidence.
Run-to-run variance on the identical config (`system_v3`, git `3cf3380`) exceeds most round-to-round deltas — E4 4 vs 8, `schema_valid` 22 vs 18, `exception_rate` 1.000 vs 0.885, `deadline_relative` 0.067 vs 0.267, `false_escalation` 0.737 vs 0.789. Treat every figure above as dev-only and noisy.
