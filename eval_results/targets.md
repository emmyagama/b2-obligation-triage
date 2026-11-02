# Targets

Written before the first run.

| Metric | Target | Floor | Measured on |
|---|---|---|---|
| **Exception rate** | ≤ 20% | ≤ 30% | 30 held-out |
| Obligation recall (gold matched) | ≥ 0.80 | ≥ 0.65 | 30 held-out |
| **Deadline capture, absolute** | ≥ 0.85 | ≥ 0.75 | held-out, absolute cases |
| **Deadline capture, relative** | ≥ 0.70 | ≥ 0.55 | held-out, relative cases |
| Escalation recall | ≥ 0.85 | ≥ 0.70 | ~15 held-out that should escalate |
| False escalation | ≤ 0.20 | ≤ 0.30 | ~15 that should not |
| Grounded quote rate | ≥ 0.95 | ≥ 0.90 | all extracted |
| p50 / p95 latency | ≤ 10 s / ≤ 20 s | ≤ 25 s | all runs |
| Cost per transaction | ≤ $0.03 | ≤ $0.06 | live run only |

**Relative deadline capture is deliberately the lowest target and the most interesting number.** It is the one that requires the anchor-date tool, and it is where the build will fail first. Publishing a 0.70 next to a 0.85 is more credible than publishing 0.85 twice.


### 7.2 Falsification, written now

If held-out exception rate exceeds 35%, or relative deadline capture falls below 0.55, **the design is wrong, not the model.** Publish that sentence with the number and name the most likely cause: CUAD's Effective Date label is missing or ambiguous in the contracts where relative obligations concentrate. The build still ships, with the failure documented — that is the entire point of the taxonomy.

