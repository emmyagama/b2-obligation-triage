# B2 prototype - offline synthetic demonstration

**Demonstration only. Not an evaluation. No quality claims. Live evaluation
remains disabled and unavailable.**

## What this is

A deterministic end-to-end run of the B2 baseline pipeline over fictional
documents inside a temporary workspace:

lean index build -> retrieval precheck -> tool-calling engine ->
jsonschema/quote-grounding/deadline validation -> sqlite decisions ->
scoring against synthetic gold -> baseline Wilson metrics.

The model response is **scripted by this script** and served from a local
demo cache through the baseline's real offline cache path (a cache miss
raises; no socket is ever opened). All artifacts are written to a
workspace outside the repository.

## What this is not

- No provider calls, no credentials, no network. `B2_OFFLINE=1` is set
  before the baseline package is imported, so its socket-level guard is
  active for the whole run.
- No held-out (test) cases, no CUAD content, no private material, no
  local run caches or databases.
- Not an evaluation result: n=3 synthetic cases authored inside this
  demo. The printed numbers are plumbing evidence, not performance.
- Not a claim of defect-free software. Review findings and known gaps
  stay in the local phase reports and are not published on this branch.

## Run

```text
python prototype/run_demo.py --workdir <dir>
python -m pytest -q prototype/test_demo.py
```

Expected: exit status 0, a line `DEMO_OK cases=3 exceptions=0
provider_calls=0`, and a machine-readable report at
`<dir>/out/report.json` (plus `metrics.json` and `summary.md`).

## Real baseline code vs demo stand-ins

Real, unmodified baseline code:

- lean index format, checksums and cosine search (`agent/lean_index.py`)
- human taxonomy from `guide/obligation_types.yaml` (`agent/taxonomy.py`)
- baseline prompt text `prompts/system_v3.md`
- tool loop, JSON-schema validation, verbatim quote grounding, absolute /
  relative deadline verification (`agent/engine.py`, `agent/validate.py`)
- deadline resolution (`agent/deadlines.py`) and escalation floors from
  `config/thresholds.yaml` (e5 = 0.65, provenance `uncalibrated-fallback`)
- intake idempotency, sqlite schema, decisions/escalations
  (`agent/intake.py`, `db/schema.sql`)
- scoring (`agent/scoring.py`) and Wilson metrics (`agent/metrics.py`)
- offline cache semantics (`agent/cache.py`) and the `B2_OFFLINE`
  socket guard (`agent/__init__.py`)

Deliberate demo stand-ins (labelled in every output):

- model response: fabricated here as `scripted-offline-response`; the
  baseline production model name is never claimed as having run
- embedder: demo-local deterministic blake2b hash vectors (64 dims), NOT
  the baseline MiniLM/Gemini embedder - retrieval scores are illustrative
- documents, cases and gold: fictional, authored in this file
- pricing: zero placeholder - no spend exists in this demo
- split label: `demonstration`, mode `offline-scripted`

## Files

- `run_demo.py` - CLI demonstration (see its module docstring)
- `test_demo.py` - three offline tests (no credentials, no network)
- `README.md` - this file

## Limitations

- Tiny synthetic sample; retrieval scores depend on the demo embedder.
- Baseline thresholds keep their `uncalibrated-fallback` provenance; this
  demo neither calibrates nor validates them.
- Draft v1.1 live-runner controls are deliberately not part of this
  branch. Live evaluation would require a separately approved protocol
  with commitment, budget and identity binding; none exists here.
- The frozen baseline paths (`agent/`, `scripts/`, `guide/`, `cases/`,
  `eval_results/`, `README.md`, `config/`, `prompts/`) are untouched.
  The root README is byte-verified by `check_readme.py` against rendered
  evaluation results, so prototype presentation lives in this directory.
