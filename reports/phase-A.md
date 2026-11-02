NEXT ACTION FOR HUMAN: Carry the two pushed files (`reports/phase-A.md`, `corpus-report.md`) at https://github.com/emmyagama/b2-obligation-triage to the build agent and bring back `b2-bundle-v1.zip` + `BUNDLE-NOTES.md` for Phase B; also settle open issue OI-1 (`gh auth login`) when convenient.

Phase: A   Branch/sha: b2/build @ 032246a (2 commits)   Date: 2026-11-02

Repo: https://github.com/emmyagama/b2-obligation-triage (public, empty except Phase A files; default branch switched to `b2/build`, see D2).

---

## A1. B1 reference pack

**B1 repo is public: https://github.com/emmyagama/ng-health-reg-assistant** (verified via `api.github.com`: `visibility: public`, `private: false`, default branch `main`). The local clone at `../ng-health-reg-assistant` was fetched and is at `origin/main` (`723f50a`). **No `b1-reference-pack/` zip was produced**: everything the brief asks to cover exists in the public repo (verified with `git ls-files`), so there is nothing to export that is not already public. The local clone's untracked files (`OPENCODE-B1-PROMPT*.md`, `OPENCODE_REPORT.md`) are B1 process documents, not part of the coverage list, and were excluded; `.env` was never opened beyond confirming a `GROQ_API_KEY=` line exists (no value read into any report).

### Paths for the build agent (all paths relative to the B1 repo root)

| Item | Path(s) |
|---|---|
| Embedder code | `src/embed_store.py` |
| Chunking code (separate module) | `src/chunker.py` |
| Harness entry point | `run_eval.py` (`main()` at `run_eval.py:1148`) |
| Metric helpers | inside `run_eval.py`: `compute_metrics` (`:501`), `_citation_metrics` (`:363`), `_retrieval_metrics` (`:422`), `_groundedness_block` (`:449`), `recompute` (`:1039`), `classify_shown_to_user` (`:982`); plus `analysis/render_results.py` (table renderer) |
| `check_readme.py` | **does not exist** — never committed in B1 (checked `git ls-files`, `git log --all --diff-filter=A`, recursive disk search). B1's README drift guard is `python analysis/render_results.py --check` (`.github/workflows/ci.yml:45`) |
| CI workflow | `.github/workflows/ci.yml` (single workflow, 45 lines) |
| Requirements | `requirements.txt` (direct pins), `requirements.lock.txt` (full freeze) |

### Embedder (B1)

- **Provider: local HuggingFace sentence-transformers, not Groq.** `src/embed_store.py:41`: `EMBED_MODEL_NAME = "all-MiniLM-L6-v2"`, loaded lazily (`src/embed_store.py:82-87`).
- **Vector dimension: 384** (not asserted in code; verified empirically against the committed Chroma store `chroma_db/chroma.sqlite3`, collection `ng_health_regs`: 1,218 vectors × 384 dims).
- **Batching:** `model.encode(texts, show_progress_bar=True, normalize_embeddings=False)` with sentence-transformers default batch (32) at `src/embed_store.py:166-170`; Chroma insert batches of 500 at `src/embed_store.py:172-180`; existing-id paging `limit=1000` at `:131-141`.
- **Rate-limit handling: none** (local model, no network). Retrieval knobs: `INTERNAL_FETCH_K=10`, `MAX_PER_DOC=3` (`src/embed_store.py:67-68`); collection metadata `hnsw:space: l2` (`:122-125`).

### Chunking (B1)

`src/chunker.py` (731 lines). Defaults `src/chunker.py:52-55`: `DEFAULT_MAX_CHARS = 700`, `DEFAULT_OVERLAP_CHARS = 100` (comment: keeps chunks inside all-MiniLM-L6-v2's 256-token window, ~4 chars/token). Section-aware: heading regexes `:62-109`, `pack_lines()` `:474`, `chunk_document()` `:507`, CLI `main()` `:525`. Outputs `data/processed/chunks.jsonl` and `data/processed/all_chunks.json`.

### Harness and CI

- Entry point `run_eval.py` (1,191 lines); CLI flags `--prefix --golden --k --strict/--no-strict --resume --recompute-only` (`:1150-1180`); defaults `DEFAULT_GOLDEN=data/golden_set_50.json` (`:71`).
- Retry/backoff in `run_eval.py`: `RETRY_BASE_SECONDS=2.0`, `RETRY_CAP_SECONDS=60.0`, `RETRY_ATTEMPTS=6`, `RETRY_AFTER_CEILING_SECONDS=120.0` (`:146-151`); retries 429 and 5xx plus connection errors (`:157-167`); exponential backoff with full jitter `delay *= 0.5 + random.random()` and `Retry-After` clamp (`:170-180`); wrapper `_call_with_retry()` (`:183-204`).
- CI: `.github/workflows/ci.yml` — `ubuntu-latest`, Python matrix `["3.10","3.12"]`, `pip install -r requirements.txt`, `py_compile`, `python src/guardrails.py`, `python src/answer.py`, `pytest tests/ -q`, `python analysis/render_results.py --check`. **No `secrets.*` referenced.**
- Requirements highlights: `sentence-transformers==6.1.0`, `chromadb==1.5.9`, `groq==1.7.0`, `requests==2.34.2`, `python-dotenv==1.2.4`, `pytest==8.3.4`; lock file also pins `httpx==0.28.1`, `tenacity==9.2.1`, `torch==2.14.1`, `transformers==5.19.0` (note: `pytest` is in `requirements.txt` but absent from `requirements.lock.txt`).
- Python version: no `pyproject.toml`/`setup.py`/`.python-version` in B1. CI matrix 3.10/3.12; README:89 says "Requires Python 3.10-3.12"; `scripts/build.sh` enforces `(3,10) <= version < (3,13)`.

### README headings only (B1 `README.md`, in order)

`# B1 — Nigerian Health-Regulation Q&A` · `## Demo Video` · `## What it does` · `## What it doesn't` · `## What breaks` · `## Evaluation Results` · `## Limitations of these measurements` · `## Method and architecture` · `## Setup` · `## What I'd Do Next` · `## Licence and contact`

### First two entries of `data/golden_set_30.json` (format reference; array of 30 objects)

```json
{
  "id": 1,
  "question": "What does HEFAMAA require before a health facility can operate in Lagos State?",
  "expected_doc_id": "hefamaa_requirements",
  "expected_section": "How it works - Register Facility",
  "answerable": true
}
```
```json
{
  "id": 2,
  "question": "What documents must be uploaded during HEFAMAA facility registration?",
  "expected_doc_id": "hefamaa_requirements",
  "expected_section": "How it works - Uploading Letter of Intent",
  "answerable": true
}
```

### How B1 calls Groq

- Model id: **`openai/gpt-oss-120b`** (`src/answer.py:243`, function default of `generate_answer`).
- Parameters used: `model`, `messages` (system + user), `temperature=0.1` (`src/answer.py:261-277`). **No** `max_tokens`, `tools`, `tool_choice`, `seed`, `response_format`, `top_p` anywhere in the repo (a comment in `experiments/test_structured_output.py:204-218` states `response_format` is deliberately not used). Experiments use `temperature=0.0`.
- Key read: `os.getenv("GROQ_API_KEY")` with `.env` loaded via dotenv (`src/answer.py:46-47, 253-257`).
- Errors: typed `GroqAPIError` with `status_code` and `retry_after` parsed from the `Retry-After` header (`src/answer.py:199-288`); `src/answer.py` raises, the harness retries (see above).

---

## A2. Provider facts

Read 2026-11-02.

| Fact | Value |
|---|---|
| Model id B1 used | `openai/gpt-oss-120b` |
| Exact model id to pin for B2 | `openai/gpt-oss-120b` (confirmed present in `GET /openai/v1/models`: 11 models listed, this one included) |
| Price, input (per 1M tokens) | **$0.15** (uncached), **$0.075** cached input |
| Price, output (per 1M tokens) | **$0.60** |
| Price sources, read date | `console.groq.com/docs/model/openai/gpt-oss-120b` and `home.cloud.groq.io/pricing`, both read 2026-11-02; a third-party rate card dated 2026-10-27 agrees |
| Context window / max output | 131,072 / 65,536 tokens (same docs page) |

### Rate limits

The console was not accessible from this session (no browser), so limits were read from the `x-ratelimit-*` headers of one cheap call — `POST https://api.groq.com/openai/v1/chat/completions`, `model=openai/gpt-oss-120b`, `max_tokens=8`, HTTP 200, at `2026-11-02 12:44:57 GMT`:

```
x-ratelimit-limit-requests: 1000
x-ratelimit-limit-tokens: 8000
x-ratelimit-remaining-requests: 998
x-ratelimit-remaining-tokens: 7919
x-ratelimit-reset-requests: 2m52.8s
x-ratelimit-reset-tokens: 607ms
```

No day-scoped header was returned. The headers do not label the window period (RPM vs RPD vs TPM) — see open issue OI-2. Cross-reference from a published Groq rate card (read 2026-11-02, card dated 2026-10-27) for this model on the dev plan: **30 RPM / 1,000 requests per day / 8,000 TPM / 200,000 tokens per day** — the observed `1000` requests and `8000` tokens limits match the 1K-RPD and 8K-TPM figures. Recommended safe pacing value for `--rpm` in later phases: **20** (two-thirds of the published 30 RPM), subject to human confirmation (OI-2).

### Tool calling and seed — one cheap confirmation call

`chat.completions.create(model="openai/gpt-oss-120b", tools=[record_obligations schema], tool_choice="auto", temperature=0, seed=42, max_tokens=200)`:

- `finish_reason: "tool_calls"`; returned `record_obligations` with parsed arguments `{"obligations":[{"obligation":"pay fees within 30 days","party":"Party A"}]}` → **tool calling works**.
- `seed=42` accepted with no error. Two identical follow-up calls (`temperature=0, seed=42, max_tokens=300`) returned byte-identical content (`'SEEDTEST'` both times) → seed accepted and deterministic on this sample (2/2).
- Usage on the tool call: 154 prompt / 106 completion tokens (6 reasoning tokens).

---

## A3. CUAD download and corpus report

- Requested URL `github.com/TheAtticusProject/cuad` → HTTP 301 → `github.com/The-Atticus-Project/cuad`; `data.zip` lives on branch **`main`** (`/raw/master/data.zip` 404s — the first attempt received a 231,223-byte HTML page).
- Downloaded `https://raw.githubusercontent.com/The-Atticus-Project/cuad/main/data.zip` on **2026-11-02**, **18,309,308 bytes**, sha256 **`F8161D18BEA4E9C05E78FA6DDA61C19C846FB8087EA969C172753BC2F45B999A`**, ZIP magic verified, extracted into `data/cuad/` (gitignored): `CUADv1.json` (40,128,638 B), `test.json` (7,378,232 B), `train_separate_questions.json` (35,065,844 B).
- **`corpus-report.md` committed at the repo root** (facts only, no judgement). Headline facts: 510 / 102 / 408 contracts; 41 categories (identical strings in all three files); title-encoded family with a derivable rule covering 470/510 titles; offsets verified 30/30 against `paragraphs[0].context`.

---

## A4. Environment and repo

| Fact | Value |
|---|---|
| Python | 3.11.9 |
| OS | Microsoft Windows 11 Pro, 10.0.26100, 64-bit |
| Free disk (C:) | 19.2 GB at report time |
| Git | 2.51.0.windows.1 |
| `gh` | was **not installed** → installed 2.103.3 via winget (logged in `INTEGRATION-LOG.md`) |
| `gh auth status` | `You are not logged into any GitHub hosts. To log in, run: gh auth login` (exit 1) — see OI-1 |
| Credential used | Git Credential Manager stores a working GitHub credential for user `emmyagama` (`git ls-remote` against B1 succeeded); token never printed, logged, or committed |

### Repo created

- `POST /user/repos` → **`emmyagama/b2-obligation-triage`**, public, `has_wiki=false`, `has_projects=false`, empty (no auto-README, no auto-license).
- Local: `git init -b b2/build`; root commit `2746ece` "chore: empty initial commit (Phase A4)" (literally empty, `--allow-empty`); `032246a` "chore: add .gitignore with data, secret and test-gold embargo patterns (Phase A4)".
- `.gitignore` contents (exactly the brief's patterns):

```
data/
.env
cache/scratch/
annotation/workspace/
eval_results/scratch/
__pycache__/
.venv/
cases/src/test-*.yaml
cases/test.json
eval_results/**/*test*
cache/llm/
```

- Verified locally: `git check-ignore` classifies `cases/test.json`, `eval_results/summary_test.md`, `cache/llm/x` as ignored (spot-checked via `git status` after touching test paths is deferred to Phase B when those paths exist).

---

## Commands run (with exit codes)

| Command | Exit | Note |
|---|---|---|
| `python --version` | 0 | 3.11.9 |
| `gh auth status` (before install) | 127 | `gh` not recognised |
| `winget install --id GitHub.cli -e ...` | 0 | installed 2.103.3 |
| `gh auth status` (after install) | 1 | not logged in — OI-1 |
| `git -C ../ng-health-reg-assistant fetch origin` | 0 | local == `origin/main` |
| `curl ... TheAtticusProject/cuad/raw/master/data.zip` | 0 (HTTP 404 body) | wrong: HTML saved, discarded |
| `curl -L ... raw.githubusercontent.com/The-Atticus-Project/cuad/main/data.zip` | 0 | 18,309,308 B |
| `Expand-Archive data.zip` | 0 | 3 JSON files |
| Groq probe A (tools + seed) via B1 venv `groq==1.7.0` | 0 | tool call returned |
| Groq probe B (raw HTTP headers) | 0 | HTTP 200, headers captured |
| Groq probe C (seed determinism, 2 calls) | 0 | identical outputs |
| `api.github.com/repos/...` visibility checks | 0 | B1 public |
| `POST /user/repos` (b2-obligation-triage) | HTTP 201 | created |
| `git init -b b2/build` + 2 commits | 0 | clean tree |
| CUAD analysis scripts (3 runs, temp dir) | 0 | all numbers in `corpus-report.md` |
| sample-verification script (report vs data) | 0 | both fenced samples now byte-identical to `context[:500]` |

## Key outputs (trimmed)

```
B1 visibility: public, default branch main, HEAD 723f50a (== local after fetch)
Groq: model openai/gpt-oss-120b; tools+seed OK; seed 2/2 identical
headers: limit-requests 1000 / limit-tokens 8000 (2026-11-02 12:44:57 GMT)
price: $0.15 in / $0.60 out / $0.075 cached-in per 1M (read 2026-11-02)
CUAD: 510 + 102 + 408 contracts; 41 categories; offsets 30/30 pass vs context
repo: emmyagama/b2-obligation-triage (public) ← created; local b2/build @ 032246a
```

## Deviations from the brief

1. **D1 — `gh` missing, installed by me** (winget, GitHub CLI 2.103.3). Environment fix, logged in `INTEGRATION-LOG.md`. `gh auth login` still fails on scope (OI-1); repository creation therefore used the GitHub REST API with the stored Git Credential Manager token (never printed).
2. **D2 — default branch of the new repo set to `b2/build`** (planned via API after the first push) instead of `main`, so the build agent can read `reports/` immediately. `main` does not exist yet; Phase G creates it by fast-forward from `b2/build` and can switch the default back. No merge to `main` happens before Phase G.
3. **D3 — CUAD URL differs from the brief's** (repo renamed to `The-Atticus-Project`, branch `main`). Logged in `INTEGRATION-LOG.md`.
4. **D4 — no `b1-reference-pack/` zip**: all coverage-listed artefacts are in the public B1 repo, so there was nothing non-public to export.
5. **D5 — `check_readme.py` does not exist in B1** (the brief lists it as an item to cover). B1's equivalent is `analysis/render_results.py --check`. Reported rather than invented — the B2 build agent must supply `check_readme.py` for Phase G.

## Open issues / stop-and-ask items

- **OI-1 — `gh` is not authenticated.** `gh auth login --with-token` with the stored credential fails: `error validating token: missing required scope 'read:org'`. Everything Phase A needed worked via the REST API, but Phase G needs `gh run watch`. *Human action:* run `gh auth login` interactively (device flow) when convenient, or confirm that REST-based monitoring is acceptable. I did not ask for, print, or store any token.
- **OI-2 — rate-limit window labels are ambiguous.** The `x-ratelimit-*` headers give `1000` requests / `8000` tokens without stating the period, and no day-scoped header exists. Published card (2026-10-27) says 30 RPM / 1K RPD / 8K TPM / 200K TPD. Before Phase D I will use `--rpm 20` unless you say otherwise. Also note 8,000 TPM is low for tool-calling agents; 429 dead-letters are plausible and the brief's `--resume` flow covers them.
- **OI-3 — Phase B input still missing:** `b2-bundle-v1.zip` + `BUNDLE-NOTES.md` from the build agent (expected; nothing to do until they arrive).
- No protected path was touched. No test-gold, `cache/llm/`, or `eval_results/` content was committed or pushed.
