# Dev round 2 summary

Live dev run of the applied round-1 patch (`prompts/system_v2.md` + `config/tool_descriptions.yaml`).

- run dir: `eval_results/scratch/run_dev_20261104T065517968832Z`
- split: dev; mode: **live**; prompt_version: **system_v2**
- git_sha: `99dd9f1c972edc513ddc9e867b8c924b13660d46` (round 1 was `30eb348f828a72532ad6ed1e4e5f50347e921e22`)
- case_sha256: `14c7d0976c8a8b6497fb0f8a743c5481e70cab8f1e3bb5dd18227427c360bf40` (unchanged from round 1 - no gold edit)
- threshold_sha256: `180eae3857a1bcac42c42e5a30fd8f96ddff42b744e57f1d6e3e501fc1e0cb55` (unchanged - no calibration)
- cases: 26; classes: adversarial 2, clear 15, conflicting 5, out_of_scope 4
- comparison baseline: `run_dev_20261104T002625424993Z` (round 1 re-scored against corrected gold, mode=replay)

## Aggregate deltas (round 1 -> round 2)

| metric | round 1 | round 2 | direction |
|---|---|---|---|
| constructed_e2_exception_rate | 1.000 (5/5) | 0.800 (4/5) | better |
| constructed_e2_recall | 0.200 (1/5) | 0.600 (3/5) | better |
| cost | {"mean_usd": 0.005383806923076922, "n": 26} | {"mean_usd": 0.007933336923076923, "n": 26} | neutral |
| deadline_none | 0.053 (1/19) | 0.105 (2/19) | better |
| deadline_relative | 0.267 (4/15) | 0.200 (3/15) | worse |
| exception_rate | 0.885 (23/26) | 0.846 (22/26) | better |
| false_escalation | 0.632 (12/19) | 0.737 (14/19) | worse |
| grounded_rate | 1.000 (7/7) | 1.000 (17/17) | better |
| latency | {"n": 26, "p50_ms": 82828.0, "p95_ms": 121492.0} | {"n": 26, "p50_ms": 105640.5, "p95_ms": 126035.25} | neutral |
| obligation_recall | 0.146 (6/41) | 0.195 (8/41) | better |

Unchanged: 5 of 16 aggregate keys (`escalation_recall`, `obligation_recall` denominator, cost n, and the deterministic `retrieval_score` distribution).

## Terminal E4 failures

- round 1 (n=4): `dev-06` LOOP_EXHAUSTED, `dev-08` LOOP_EXHAUSTED, `dev-12` LOOP_EXHAUSTED, `dev-24` SCHEMA_FAIL
- round 2 (n=7): `dev-03` LOOP_EXHAUSTED, `dev-06` LOOP_EXHAUSTED, `dev-08` LOOP_EXHAUSTED, `dev-09` LOOP_EXHAUSTED, `dev-11` LOOP_EXHAUSTED, `dev-14` SCHEMA_FAIL, `dev-21` SCHEMA_FAIL

**E4 went from 4 to 7** (`schema_valid` 22/26 -> 19/26). `LOOP_EXHAUSTED` 3 -> 5, `SCHEMA_FAIL` 1 -> 2.
`dev-12` and `dev-24` were fixed; `dev-03`, `dev-09`, `dev-11`, `dev-14`, `dev-21` are new.

## Deterministic note

`retrieval_score` is produced by `retrieval_precheck` (`agent/engine.py:33-46`), which embeds the
frozen taxonomy's category queries and searches the committed index. It is prompt- and
model-independent, so it is byte-identical to round 1 by construction (all 26 cases match).
`engine.py:47` emits E1 only when `score < e1_floor`; dev-15 scores exactly `-1.0` against a
provisional floor of `-1.0`, so E1 remains unreachable until Phase E calibration.

## Aggregate metrics

```json
{
  "constructed_e2_cases": 5,
  "constructed_e2_exception_rate": {
    "denominator": 5,
    "numerator": 4,
    "value": 0.8,
    "wilson_95": [
      0.37553462976252533,
      0.9637758913675698
    ]
  },
  "constructed_e2_recall": {
    "denominator": 5,
    "numerator": 3,
    "value": 0.6,
    "wilson_95": [
      0.2307242812760128,
      0.882379225767352
    ]
  },
  "cost": {
    "mean_usd": 0.007933336923076923,
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
    "numerator": 2,
    "value": 0.10526315789473684,
    "wilson_95": [
      0.02935856029887013,
      0.31394082711109006
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
    "numerator": 3,
    "value": 0.2,
    "wilson_95": [
      0.07047549346981563,
      0.45185448715169363
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
    "numerator": 22,
    "value": 0.8461538461538461,
    "wilson_95": [
      0.6646880067178652,
      0.9384996627642165
    ]
  },
  "false_escalation": {
    "denominator": 19,
    "numerator": 14,
    "value": 0.7368421052631579,
    "wilson_95": [
      0.5120844910218489,
      0.8819358765321748
    ]
  },
  "grounded_rate": {
    "denominator": 17,
    "numerator": 17,
    "value": 1.0,
    "wilson_95": [
      0.8156818649911483,
      1
    ]
  },
  "latency": {
    "n": 26,
    "p50_ms": 105640.5,
    "p95_ms": 126035.25
  },
  "mode": "live",
  "obligation_recall": {
    "denominator": 41,
    "numerator": 8,
    "value": 0.1951219512195122,
    "wilson_95": [
      0.10234437385158025,
      0.3401358518706343
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
    "mean_usd": 0.00770103,
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
    "p50_ms": 60937.5,
    "p95_ms": 115781.25
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
    "mean_usd": 0.008111494666666667,
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
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      0,
      0.22809537235419838
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
    "numerator": 3,
    "value": 0.2727272727272727,
    "wilson_95": [
      0.09746059290024889,
      0.5656453011761291
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
    "numerator": 12,
    "value": 0.9230769230769231,
    "wilson_95": [
      0.6668604907890041,
      0.9862895787574435
    ]
  },
  "grounded_rate": {
    "denominator": 10,
    "numerator": 10,
    "value": 1.0,
    "wilson_95": [
      0.7224672001371107,
      0.9999999999999999
    ]
  },
  "latency": {
    "n": 15,
    "p50_ms": 119171.0,
    "p95_ms": 131078.09999999998
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
    "numerator": 4,
    "value": 0.8,
    "wilson_95": [
      0.37553462976252533,
      0.9637758913675698
    ]
  },
  "constructed_e2_recall": {
    "denominator": 5,
    "numerator": 3,
    "value": 0.6,
    "wilson_95": [
      0.2307242812760128,
      0.882379225767352
    ]
  },
  "cost": {
    "mean_usd": 0.008578391999999999,
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
    "numerator": 2,
    "value": 0.6666666666666666,
    "wilson_95": [
      0.2076596008020477,
      0.9385080552796037
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
    "numerator": 4,
    "value": 0.8,
    "wilson_95": [
      0.37553462976252533,
      0.9637758913675698
    ]
  },
  "false_escalation": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "grounded_rate": {
    "denominator": 5,
    "numerator": 5,
    "value": 1.0,
    "wilson_95": [
      0.5655175352168251,
      1
    ]
  },
  "latency": {
    "n": 5,
    "p50_ms": 105969.0,
    "p95_ms": 119912.2
  },
  "obligation_recall": {
    "denominator": 5,
    "numerator": 2,
    "value": 0.4,
    "wilson_95": [
      0.11762077423264783,
      0.769275718723987
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
    "mean_usd": 0.0065750800000000005,
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
    "denominator": 2,
    "numerator": 2,
    "value": 1.0,
    "wilson_95": [
      0.34238022750665303,
      1
    ]
  },
  "latency": {
    "n": 4,
    "p50_ms": 97195.5,
    "p95_ms": 105291.0
  },
  "obligation_recall": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  }
}
```

