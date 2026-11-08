# b2cli

Local, SQLite-backed post-signature contract-obligation triage on top of the
frozen B2 engine. It is a research prototype: it is **not legal advice**, and
escalated items require a human reviewer.

## What it does

Given a plain-text contract, `b2cli` runs the same pipeline used in the
evaluation (chunking, retrieval, grounded tool-calling agent, deadline
resolution, validation, escalation routing) and writes a JSON report plus
SQLite rows. It is for contracts you supply yourself. Such text has **no
expert clause labels**, so the category-filtered E1 precheck is disabled; E1
("no obligations found") is applied after the model loop when zero obligations
are recorded.

This path has **no accuracy claim**. Measured numbers in the top-level README
come from the annotated CUAD-based test split, not from arbitrary user
contracts.

## Install

```
pip install -r requirements.txt
```

Python 3.11. Offline replay needs no provider package. Live mode needs
`requests` (already in requirements). The optional B1 sentence-transformer
embedder is used only if its adapter imports; otherwise a deterministic hash
embedder (`b2cli-hash-384d`) is used, which retrieves worse than the evaluated
pipeline and is labelled as such in the report.

## Usage

```
python -m b2cli --contract ./contract.txt --party customer --ref MY-2026-01
```

Options:

| flag | meaning |
|---|---|
| `--contract` | UTF-8 text file (cp1252 fallback), max 2 MB |
| `--party` | `provider`, `customer`, `licensee`, `licensor`, `other` |
| `--ref` | external reference; also the idempotency key |
| `--context` | optional business context |
| `--db` | SQLite path (default `b2cli_data/b2.sqlite`) |
| `--cache-dir` | response cache (default `b2cli_data/cache`) |
| `--out` | report directory (default `b2cli_data/out`) |
| `--live` | enable real provider calls |
| `--acknowledge-live` | required with `--live`; accepts transmission of the text |
| `--env-file` | optional `KEY=VALUE` file with provider credentials |
| `--max-cost-usd` | hard spend cap for live calls |
| `--max-requests` | hard request cap for live calls |
| `--version` | print the CLI version |

### Offline (default)

Responses are read from the cache. A miss exits `3` and no socket is opened
(`B2_OFFLINE` is enforced at import time). Re-running the same `--ref` with the
same contract returns the original run and makes no further model calls.

### Live (explicit opt-in)

```
python -m b2cli --live --acknowledge-live --env-file ../.env \
    --max-cost-usd 1 --max-requests 12 \
    --contract ./fictional-pilot.txt --party customer --ref SMOKE-1
```

Live mode sends the contract text to the configured LLM provider. Do not use a
confidential contract unless you accept that transmission. Keys are read from
`GEMINI_API_KEY` (Gemini models) or `GROQ_API_KEY`; values are never printed.
USD estimates use `config/pricing.yaml`; missing pricing re-prices as unknown
rather than guessed.

## Exit codes

| code | meaning |
|---|---|
| 0 | run completed (including escalated/failed case routed to a queue) |
| 1 | usage, privacy refusal, missing key, or unexpected error |
| 2 | missing required arguments |
| 3 | offline cache miss (no network attempt) |
| 4 | live budget cap reached |
| 5 | refused path (inside a tracked baseline directory) |

## Outputs

`report.json` contains the decision, obligations with deadlines (absolute,
relative, recurring, none), escalation codes and queues, run status, cost and
request counts, the embedder label and a retrieval note. The SQLite database is
the same schema as the evaluation; you can query `decisions`, `obligations`,
`obligation_deadlines`, `escalations` and `tool_calls` (audit trace).

State defaults to `b2cli_data/`, which is gitignored.
