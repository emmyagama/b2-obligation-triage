# Dev round 1 summary

Re-score of the baseline live dev run against the corrected gold (dev-15 reclassification).

- run dir: `eval_results/scratch/run_dev_20261104T002625424993Z`
- split: dev; mode: **replay** (cache-served replay of the live run; zero API calls)
- git_sha: `30eb348f828a72532ad6ed1e4e5f50347e921e22` (baseline run was `0560b18a1b04f6eb781abde366ed8b7bc7a4f9e5`)
- case_sha256: `14c7d0976c8a8b6497fb0f8a743c5481e70cab8f1e3bb5dd18227427c360bf40` (baseline was `b0157522a63712f82384be38ebf4ab7dbb5fc0881ee4228111ac626b37b983cc`)
- prompt_version: system_v1; threshold_sha256: `180eae3857a1bcac42c42e5a30fd8f96ddff42b744e57f1d6e3e501fc1e0cb55`
- cases: 26; classes: adversarial 2, clear 15, conflicting 5, out_of_scope 4

## Why re-scored

The human reclassified `dev-15` `out_of_scope` -> `clear` and set `gold_should_escalate: true`
with `gold_escalation_codes: [E1_NO_OBLIGATION]` (signed in `DECISIONS.md`, commit `30eb348`).
`failure_digest.py` cannot re-score: it reads the stored `metrics.json`, `cases.csv` and the case
snapshots inside `details.json`, all of which were written against the pre-reclassification gold.
`run_eval.py` has no in-place re-score either (`run_eval.py:101` always writes a fresh run dir),
so the existing run was replayed offline from `cache/scratch` and re-scored by `run_eval`'s own
scoring path. Outputs are byte-identical to the live run - the only per-case difference is dev-15.

## Deltas vs the live baseline

| metric | live baseline | re-scored |
|---|---|---|
| escalation_recall | 0.833 (5/6) | 0.714 (5/7) |
| false_escalation | 0.600 (12/20) | 0.632 (12/19) |
| mode | live | replay |

All other aggregate metrics are unchanged. Per case, `dev-15` moved
`escalation_correct: True -> False` (the model did not escalate; gold now requires E1).

## Terminal E4 failures (n=4)

- `dev-06` (clear) - `LOOP_EXHAUSTED`
- `dev-08` (clear) - `LOOP_EXHAUSTED`
- `dev-12` (clear) - `LOOP_EXHAUSTED`
- `dev-24` (conflicting) - `SCHEMA_FAIL`

The 9 `VALIDATION_ERROR` labels are intermediate tool-argument hiccups the agent recovered from
(`run_eval.py:163` promotes the first trace error to the case), which is why `exception_rate` is
0.885 (23/26) even though only 4 cases are genuine terminal execution failures.

## Aggregate metrics

```json
{
  "constructed_e2_cases": 5,
  "constructed_e2_exception_rate": {
    "denominator": 5,
    "numerator": 5,
    "value": 1.0,
    "wilson_95": [
      0.5655175352168251,
      1
    ]
  },
  "constructed_e2_recall": {
    "denominator": 5,
    "numerator": 1,
    "value": 0.2,
    "wilson_95": [
      0.03622410863243014,
      0.6244653702374747
    ]
  },
  "cost": {
    "mean_usd": 0.005383806923076922,
    "n": 26
  },
  "deadline_absolute": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_none": {
    "denominator": 19,
    "numerator": 1,
    "value": 0.05263157894736842,
    "wilson_95": [
      0.009351994062300362,
      0.24638731166898786
    ]
  },
  "deadline_recurring": {
    "denominator": 7,
    "numerator": 1,
    "value": 0.14285714285714285,
    "wilson_95": [
      0.02567962434474355,
      0.5131278292743189
    ]
  },
  "deadline_relative": {
    "denominator": 15,
    "numerator": 4,
    "value": 0.26666666666666666,
    "wilson_95": [
      0.10897453325692374,
      0.5195043405598057
    ]
  },
  "escalation_recall": {
    "denominator": 7,
    "numerator": 5,
    "value": 0.7142857142857143,
    "wilson_95": [
      0.35893445183261935,
      0.9177810759959433
    ]
  },
  "exception_rate": {
    "denominator": 26,
    "numerator": 23,
    "value": 0.8846153846153846,
    "wilson_95": [
      0.7102409678828635,
      0.9599675537638938
    ]
  },
  "false_escalation": {
    "denominator": 19,
    "numerator": 12,
    "value": 0.631578947368421,
    "wilson_95": [
      0.41039533164803066,
      0.8085048725486492
    ]
  },
  "grounded_rate": {
    "denominator": 7,
    "numerator": 7,
    "value": 1.0,
    "wilson_95": [
      0.6456695649333126,
      1
    ]
  },
  "latency": {
    "n": 26,
    "p50_ms": 82828.0,
    "p95_ms": 121492.0
  },
  "mode": "replay",
  "obligation_recall": {
    "denominator": 41,
    "numerator": 6,
    "value": 0.14634146341463414,
    "wilson_95": [
      0.0688424814129593,
      0.28443458042480957
    ]
  },
  "split": "dev"
}
```

## Class breakdown

### adversarial
```json
{
  "constructed_e2_cases": 0,
  "constructed_e2_exception_rate": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "constructed_e2_recall": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "cost": {
    "mean_usd": 0.0021343,
    "n": 2
  },
  "deadline_absolute": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_none": {
    "denominator": 3,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      5.551115123125783e-17,
      0.5614970317550454
    ]
  },
  "deadline_recurring": {
    "denominator": 1,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      0,
      0.7934506856227626
    ]
  },
  "deadline_relative": {
    "denominator": 2,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      0,
      0.6576197724933469
    ]
  },
  "escalation_recall": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "exception_rate": {
    "denominator": 2,
    "numerator": 2,
    "value": 1.0,
    "wilson_95": [
      0.34238022750665303,
      1
    ]
  },
  "false_escalation": {
    "denominator": 2,
    "numerator": 1,
    "value": 0.5,
    "wilson_95": [
      0.09453120573423074,
      0.9054687942657693
    ]
  },
  "grounded_rate": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "latency": {
    "n": 2,
    "p50_ms": 37461.0,
    "p95_ms": 71175.9
  },
  "obligation_recall": {
    "denominator": 6,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      2.7755575615628914e-17,
      0.3903342879021653
    ]
  }
}
```

### clear
```json
{
  "constructed_e2_cases": 0,
  "constructed_e2_exception_rate": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "constructed_e2_recall": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "cost": {
    "mean_usd": 0.006236238666666666,
    "n": 15
  },
  "deadline_absolute": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_none": {
    "denominator": 13,
    "numerator": 1,
    "value": 0.07692307692307693,
    "wilson_95": [
      0.013710421242556586,
      0.3331395092109959
    ]
  },
  "deadline_recurring": {
    "denominator": 6,
    "numerator": 1,
    "value": 0.16666666666666666,
    "wilson_95": [
      0.030053369748306635,
      0.5635028221864702
    ]
  },
  "deadline_relative": {
    "denominator": 11,
    "numerator": 4,
    "value": 0.36363636363636365,
    "wilson_95": [
      0.15166471095367573,
      0.6461988254921511
    ]
  },
  "escalation_recall": {
    "denominator": 2,
    "numerator": 1,
    "value": 0.5,
    "wilson_95": [
      0.09453120573423074,
      0.9054687942657693
    ]
  },
  "exception_rate": {
    "denominator": 15,
    "numerator": 15,
    "value": 1.0,
    "wilson_95": [
      0.7961166989641515,
      1
    ]
  },
  "false_escalation": {
    "denominator": 13,
    "numerator": 10,
    "value": 0.7692307692307693,
    "wilson_95": [
      0.49743624053272495,
      0.9182047128150143
    ]
  },
  "grounded_rate": {
    "denominator": 7,
    "numerator": 7,
    "value": 1.0,
    "wilson_95": [
      0.6456695649333126,
      1
    ]
  },
  "latency": {
    "n": 15,
    "p50_ms": 90579.0,
    "p95_ms": 137805.99999999994
  },
  "obligation_recall": {
    "denominator": 30,
    "numerator": 6,
    "value": 0.2,
    "wilson_95": [
      0.0950510717728987,
      0.3730569641314825
    ]
  }
}
```

### conflicting
```json
{
  "constructed_e2_cases": 5,
  "constructed_e2_exception_rate": {
    "denominator": 5,
    "numerator": 5,
    "value": 1.0,
    "wilson_95": [
      0.5655175352168251,
      1
    ]
  },
  "constructed_e2_recall": {
    "denominator": 5,
    "numerator": 1,
    "value": 0.2,
    "wilson_95": [
      0.03622410863243014,
      0.6244653702374747
    ]
  },
  "cost": {
    "mean_usd": 0.005187056,
    "n": 5
  },
  "deadline_absolute": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_none": {
    "denominator": 3,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      5.551115123125783e-17,
      0.5614970317550454
    ]
  },
  "deadline_recurring": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_relative": {
    "denominator": 2,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      0,
      0.6576197724933469
    ]
  },
  "escalation_recall": {
    "denominator": 5,
    "numerator": 4,
    "value": 0.8,
    "wilson_95": [
      0.37553462976252533,
      0.9637758913675698
    ]
  },
  "exception_rate": {
    "denominator": 5,
    "numerator": 5,
    "value": 1.0,
    "wilson_95": [
      0.5655175352168251,
      1
    ]
  },
  "false_escalation": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "grounded_rate": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "latency": {
    "n": 5,
    "p50_ms": 89735.0,
    "p95_ms": 113443.4
  },
  "obligation_recall": {
    "denominator": 5,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      0,
      0.43448246478317476
    ]
  }
}
```

### out_of_scope
```json
{
  "constructed_e2_cases": 0,
  "constructed_e2_exception_rate": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "constructed_e2_recall": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "cost": {
    "mean_usd": 0.00405788,
    "n": 4
  },
  "deadline_absolute": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_none": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_recurring": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_relative": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "escalation_recall": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "exception_rate": {
    "denominator": 4,
    "numerator": 1,
    "value": 0.25,
    "wilson_95": [
      0.04558726080970055,
      0.6993581574175981
    ]
  },
  "false_escalation": {
    "denominator": 4,
    "numerator": 1,
    "value": 0.25,
    "wilson_95": [
      0.04558726080970055,
      0.6993581574175981
    ]
  },
  "grounded_rate": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "latency": {
    "n": 4,
    "p50_ms": 67156.5,
    "p95_ms": 87852.7
  },
  "obligation_recall": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  }
}
```

