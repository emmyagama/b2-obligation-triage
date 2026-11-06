# Evaluation: test

Proportion intervals are Wilson 95%; intervals are not used for latency or cost.

| Metric | Result |
|---|---|
| exception_rate | 96.7% (29/30; Wilson 95% 83.3%–99.4%) |
| deadline_absolute | not measurable (0 denominator) |
| deadline_relative | 20.0% (1/5; Wilson 95% 3.6%–62.4%) |
| obligation_recall | 26.8% (11/41; Wilson 95% 15.7%–41.9%) |
| escalation_recall | 77.8% (7/9; Wilson 95% 45.3%–93.7%) |
| false_escalation | 81.0% (17/21; Wilson 95% 60.0%–92.3%) |
| grounded_rate | 100.0% (38/38; Wilson 95% 90.8%–100.0%) |
| deadline_recurring | 16.7% (3/18; Wilson 95% 5.8%–39.2%) |
| deadline_none | 5.6% (1/18; Wilson 95% 1.0%–25.8%) |

Constructed E2 cases: 9.
Constructed E2 exception rate: 100.0% (9/9; Wilson 95% 70.1%–100.0%).
Constructed E2 code recall: 33.3% (3/9; Wilson 95% 12.1%–64.6%).

Latency p50 / p95: 74656.0 / 120603.0 ms (n=30).
Mean cost: 0.007870434333333332 USD (n=30).

Small samples yield wide intervals; do not treat relative-deadline results as precise.
