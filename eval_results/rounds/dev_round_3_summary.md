# Dev round 3 summary

Live dev run of the applied round-2 patch (`prompts/system_v3.md` + `config/tool_descriptions.yaml`).
**Third and final permitted tuning round.**

- run dir: `eval_results/scratch/run_dev_20261104T120406146271Z`
- split: dev; mode: **live**; prompt_version: **system_v3**
- git_sha: `3cf338068567f469b062318ce8edb4305d971a48` (recorded at run time; the 1-line `agent/evalio.py` UTF-8 fix was uncommitted when this run executed)
- case_sha256: `14c7d0976c8a8b6497fb0f8a743c5481e70cab8f1e3bb5dd18227427c360bf40` (unchanged since round 1 - no gold edit)
- threshold_sha256: `180eae3857a1bcac42c42e5a30fd8f96ddff42b744e57f1d6e3e501fc1e0cb55` (unchanged - no calibration)
- cases: 26; classes: adversarial 2, clear 15, conflicting 5, out_of_scope 4
- comparison baseline: `eval_results/scratch/run_dev_20261104T065517968832Z` (round 2, live)
- replication run: `eval_results/scratch/run_dev_20261104T111659780513Z` (identical config; see section 3)

## 1. Aggregate deltas (round 2 -> round 3)

| metric | round 2 | round 3 | direction |
|---|---|---|---|
| constructed_e2_recall | 0.600 (3/5) | 0.200 (1/5) | worse |
| cost | {"mean_usd": 0.007933336923076923, "n": 26} | {"mean_usd": 0.007924993461538462, "n": 26} | neutral |
| deadline_relative | 0.200 (3/15) | 0.267 (4/15) | better |
| escalation_recall | 0.714 (5/7) | 0.857 (6/7) | better |
| exception_rate | 0.846 (22/26) | 0.885 (23/26) | worse |
| false_escalation | 0.737 (14/19) | 0.789 (15/19) | worse |
| grounded_rate | 1.000 (17/17) | 1.000 (16/16) | unchanged |
| latency | {"n": 26, "p50_ms": 105640.5, "p95_ms": 126035.25} | {"n": 26, "p50_ms": 88570.0, "p95_ms": 121992.75} | neutral |
| obligation_recall | 0.195 (8/41) | 0.220 (9/41) | better |

`grounded_rate` moved 17/17 -> 16/16 (value unchanged at 1.000).

## 2. Terminal E4 failures

- round 2 (n=7): `dev-03` LOOP_EXHAUSTED, `dev-06` LOOP_EXHAUSTED, `dev-08` LOOP_EXHAUSTED, `dev-09` LOOP_EXHAUSTED, `dev-11` LOOP_EXHAUSTED, `dev-14` SCHEMA_FAIL, `dev-21` SCHEMA_FAIL
- round 3 (n=8): `dev-01` SCHEMA_FAIL, `dev-03` SCHEMA_FAIL, `dev-08` SCHEMA_FAIL, `dev-10` SCHEMA_FAIL, `dev-11` LOOP_EXHAUSTED, `dev-16` LOOP_EXHAUSTED, `dev-26` SCHEMA_FAIL, `dev-20` SCHEMA_FAIL

`schema_valid` 19/26 -> 18/26. `error_class` counts:  12, ClauseNotFound 1, LOOP_EXHAUSTED 2, SCHEMA_FAIL 6, VALIDATION_ERROR 5.

## 3. Run-to-run variance (same config, two independent live runs)

The first round-3 invocation completed all 26 cases and wrote `cases.csv`/`metrics.json` but crashed
while serialising `details.json` (`agent/evalio.py:4` wrote without `encoding=`, so Windows used cp1252
and died on U+2215). It was fixed (rule-1) and the run repeated. Both runs used identical config:
`system_v3`, git `3cf3380`, same `case_sha256`, `mode=live`. `cache_hit=0` on all 383 tool calls in the
repeat, i.e. no response reuse - the two runs are independent samples.

| | round 3 (run A, crashed) | round 3 (run B, complete) |
|---|---|---|
| terminal E4 failures | 4 | 8 |
| E4 case ids | dev-01, dev-03, dev-14, dev-20 | dev-01, dev-03, dev-08, dev-10, dev-11, dev-16, dev-26, dev-20 |
| `schema_valid` | 22/26 | 18/26 |
| `escalation_recall` | 0.857 | 0.857 |
| `obligation_recall` | 0.220 | 0.220 |
| `exception_rate` | 1.000 | 0.885 |
| `false_escalation` | 0.737 | 0.789 |

**14 of 26 cases differ on decision fields** (`escalation_correct`, `schema_valid`, `obligations_found`,
`deadlines_captured`, `exception`, `predicted_e2`) between the two runs: dev-06, dev-07, dev-08, dev-09, dev-10, dev-11, dev-12, dev-14, dev-16, dev-18, dev-19, dev-24, dev-25, dev-26.

Run A is reported for variance only: it has no `details.json`, so it cannot be digested by
`failure_digest.py`. Run B is the artifact-complete round-3 result. **The two runs disagree by more
than the round-to-round deltas being compared, so single-run metric movements in this phase are
within run-to-run noise for most metrics.**

## 4. Deterministic note

`retrieval_score` remains prompt-independent (`retrieval_precheck`, `agent/engine.py:33-46`) and is
identical to rounds 1 and 2. `engine.py:47` emits E1 only on `score < e1_floor`; dev-15 still scores
exactly `-1.0` against a provisional `-1.0`, so E1 remains unreachable until Phase E calibration.

## 5. Aggregate metrics

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
    "numerator": 1,
    "value": 0.2,
    "wilson_95": [
      0.03622410863243014,
      0.6244653702374747
    ]
  },
  "cost": {
    "mean_usd": 0.007924993461538462,
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
    "numerator": 4,
    "value": 0.26666666666666666,
    "wilson_95": [
      0.10897453325692374,
      0.5195043405598057
    ]
  },
  "escalation_recall": {
    "denominator": 7,
    "numerator": 6,
    "value": 0.8571428571428571,
    "wilson_95": [
      0.4868721707256811,
      0.9743203756552565
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
    "numerator": 15,
    "value": 0.7894736842105263,
    "wilson_95": [
      0.5666572155618583,
      0.9149232336708375
    ]
  },
  "grounded_rate": {
    "denominator": 16,
    "numerator": 16,
    "value": 1.0,
    "wilson_95": [
      0.8063923194655637,
      1
    ]
  },
  "latency": {
    "n": 26,
    "p50_ms": 88570.0,
    "p95_ms": 121992.75
  },
  "mode": "live",
  "obligation_recall": {
    "denominator": 41,
    "numerator": 9,
    "value": 0.21951219512195122,
    "wilson_95": [
      0.12003174778217568,
      0.3670500598822617
    ]
  },
  "split": "dev"
}
```

## 6. Class breakdown

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
    "mean_usd": 0.005104494999999999,
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
    "numerator": 2,
    "value": 1.0,
    "wilson_95": [
      0.34238022750665303,
      1
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
    "n": 2,
    "p50_ms": 38125.0,
    "p95_ms": 72437.5
  },
  "obligation_recall": {
    "denominator": 6,
    "numerator": 1,
    "value": 0.16666666666666666,
    "wilson_95": [
      0.030053369748306635,
      0.5635028221864702
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
    "mean_usd": 0.008040308,
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
    "numerator": 11,
    "value": 0.8461538461538461,
    "wilson_95": [
      0.5776536898051745,
      0.9567418216419186
    ]
  },
  "grounded_rate": {
    "denominator": 8,
    "numerator": 8,
    "value": 1.0,
    "wilson_95": [
      0.6755924351161198,
      1
    ]
  },
  "latency": {
    "n": 15,
    "p50_ms": 87562.0,
    "p95_ms": 123159.29999999999
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
    "numerator": 1,
    "value": 0.2,
    "wilson_95": [
      0.03622410863243014,
      0.6244653702374747
    ]
  },
  "cost": {
    "mean_usd": 0.008360096000000001,
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
    "numerator": 1,
    "value": 0.3333333333333333,
    "wilson_95": [
      0.06149194472039621,
      0.7923403991979522
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
    "numerator": 1,
    "value": 0.5,
    "wilson_95": [
      0.09453120573423074,
      0.9054687942657693
    ]
  },
  "escalation_recall": {
    "denominator": 5,
    "numerator": 5,
    "value": 1.0,
    "wilson_95": [
      0.5655175352168251,
      1
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
    "denominator": 4,
    "numerator": 4,
    "value": 1.0,
    "wilson_95": [
      0.5101091635454027,
      1
    ]
  },
  "latency": {
    "n": 5,
    "p50_ms": 95562.0,
    "p95_ms": 116050.4
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
    "mean_usd": 0.008358935,
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
    "numerator": 2,
    "value": 0.5,
    "wilson_95": [
      0.15003898915214947,
      0.8499610108478506
    ]
  },
  "false_escalation": {
    "denominator": 4,
    "numerator": 2,
    "value": 0.5,
    "wilson_95": [
      0.15003898915214947,
      0.8499610108478506
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
    "p50_ms": 119172.0,
    "p95_ms": 121807.65
  },
  "obligation_recall": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  }
}
```

