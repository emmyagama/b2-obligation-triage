NEXT ACTION FOR HUMAN: Review §5.1 — the test-gold exposure is accepted and the embargo is restored at the tip — then the calibration result recorded below once the 26-case dev run finishes.

Phase: C (pre-flight + calibration attempt)   Branch/sha: `b2/build` @ `37ef1d6`   Date: 2026-11-03

## 1. Phases A and B — verified complete

- `reports/phase-A.md`, `reports/phase-B.md`, `reports/phase-B-addendum.md`, `reports/lean-migration.md`, `corpus-report.md` all present and committed; `INTEGRATION-LOG.md` present (74 lines).
- `corpus/selection.json`: 40 picks; conflict coverage `before 18 / after 18 / minimum 14 / shortfall 0` (candidates, not adjudications).
- `db/b2.sqlite` (read-only): 46 `corpus_documents` (40 base + 1 dev adversarial + 5 dev composites), 2,753 `clause_labels`.
- Lean index `corpus/embeddings/manifest.json`: format `b2-lean-v1`, 19,445 chunks, 384 dims, `corpus_version sha256:f31c766c…` matches `config/model.yaml`.
- `cases/dev.json` = 26 cases, `config/splits.yaml` dev/test = 26/30.
- Deviations/gaps: `annotation/workspace/` exists but holds **0 of 40** files (gitignored, lost with the sandbox; regenerate with `python scripts/make_annotation_workspace.py` — not needed for calibration). No tags exist yet (§4).

## 2. Case build and strict validation — green

```
$ .venv/Scripts/python.exe scripts/build_cases.py          -> exit 0  compiled 26 dev and 30 test cases
$ .venv/Scripts/python.exe scripts/validate_cases.py --strict -> exit 0  valid: 26 dev, 30 test, 0 shared source documents
```

- No `--replace-commitment` used (forbidden and unnecessary): `sha256(cases/test.json)` = `c3e147bb20d90071a9c32c09ee5618e14b61a7516bb8dd9c2a1e20cf8db564ea` = `cases/FROZEN.sha256` = `HEAD:cases/FROZEN.sha256`.
- `cases/dev.json` shows ` M` in `git status` only as a `core.autocrlf` stat artefact; bytes are identical to `HEAD` (verified: both `b0157522…`, `git diff --exit-code` = 0).
- Untracked artefact of the validator: `eval_results/case_validation.json` (`{"dev_cases":26,"test_cases":30,"document_overlap":0,"strict":true}`); it is guard-protected, left uncommitted.

## 3. Test synthetic shard + freeze — already built, re-frozen, hashes match

- Shard present, so **no rebuild** of `make_composite --split test` / `make_adversarial --split test` / `build_embeddings --split test` was needed: 13 documents, `corpus/synthetic_test/manifest.json`, `index/{chunks.json 1,249,581 B, vectors.npy 6,700,160 B, manifest.json}`, `embed_cache/` 4,921 entries, `db/test_docs.sqlite` 856,064 B.
- `$ .venv/Scripts/python.exe scripts/freeze_test_synthetics.py` -> exit 0, `synthetic commitment: 6d8fd4dbda70011438812a16f3f7d65fe891f4a5482c44bc2d034a668ef8bdc6`, equal to `cases/FROZEN-SYNTHETIC.sha256` and to `HEAD:cases/FROZEN-SYNTHETIC.sha256`.
- Nothing embargoed was added: `corpus/synthetic_test/`, `db/test_docs.sqlite`, `cases/test.json`, `cache/llm/` remain untracked and absent from `origin/b2/build`.

## 4. Pre-flight gates

| Gate | Status |
|---|---|
| `build_cases` + `validate_cases --strict` | pass (§2) |
| `eval_results/targets.md` committed | pass (`0990933`) |
| `python scripts/prompt_hygiene.py` | pass after rule-1 fix (§6) |
| `py -3.11 scripts/venv.py test` (= `make test`) | pass: `60 passed, 1 skipped` + `prompt hygiene passed`, exit 0 |
| tag `guide-v1.0` | **missing** — `freeze_check.py` exit 1 (`refs/tags/guide-v1.0`); `run_eval.py --live` hard-requires it |
| tag `targets-v1` | **missing** (must be tagged before the first live run) |
| `scripts/pre_push_guard.py` | **fails** — see §5 |
| live smoke `run_eval.py --split dev --live --scratch --limit 2` | **not run** — no `GROQ_API_KEY` |
| calibration on full 26 dev | **blocked** — needs a completed 26-case dev run |

## 5. INTEGRITY INCIDENT — brief §0.9, stopping here

`git ls-remote origin refs/heads/b2/build` = `37ef1d6` = local `HEAD`, and `git merge-base --is-ancestor 2f42a21 origin/b2/build` = 0, so the following are **on the remote right now**:

- `cases/src/test-01.yaml` … `test-30.yaml` (the complete held-out gold: classes, `gold_obligations`, exact `clause_ref` offsets, deadlines, escalation codes, conflict pairs) — added by `2f42a21` "Add files via upload" (Emmanuel Agama, 2026-11-03 14:18 +0100), i.e. the GitHub web UI bypasses the `.gitignore` embargo added in `032246a`.
- `cases/TEST-NOTES.md` — added by `67bab1e` (14:20 +0100); contains the per-case gold-obligation table, the nine composite pair commands, the 13 synthetic ids and the split counts.

Not exposed (verified against `git ls-tree -r origin/b2/build`): `cases/test.json`, `cache/llm/`, any `eval_results/` test output, `corpus/synthetic_test/`, `db/test_docs.sqlite`. Only `cases/FROZEN.sha256` (hash) went out early, as intended.

This is the condition the brief calls an integrity incident, so I stopped instead of proceeding to calibration. `pre_push_guard.py` correctly blocks every push (`protected paths tracked before freeze: cases/src/test-01.yaml, …`), so nothing further can be pushed until you decide. Note `cases/TEST-NOTES.md` is **not** covered by any `.gitignore` pattern, so the guard will not catch it even after the YAMLs are untracked.

Your options (I did not act on any of them): (a) accept and document the disclosure (the reader is the build agent you already share the repo with); (b) make the repository private; (c) author a fresh, never-pushed held-out split and re-seal `FROZEN.sha256` — permissible right now because `eval_results/dev_run_log.jsonl` does not exist (no dev live run has started); (d) remove the files from history — requires `git push --force`, which brief §0.5 forbids.

### 5.1 Human decision (2026-11-03, this session): purge if possible, else accept

**A full purge is not possible, so the exposure is accepted.** Reasons: the files sit in `2f42a21`, reachable from `origin/b2/build`, `origin/HEAD` and `origin/arena/18088414-b2-obligation-triage`, so removing them from GitHub means rewriting every reachable commit and `git push --force`, which brief §0.5 forbids; and even a rewrite would not be *entire* — GitHub keeps unreachable objects addressable by SHA until GC, and any clone made before today (the build agent reads this repo) keeps its own copy.

Actions taken to make the acceptance operative:

- `git rm --cached` on `cases/src/test-01.yaml` … `test-30.yaml` and `cases/TEST-NOTES.md` — index only; all 31 files remain byte-identical on disk and are still compiled by `build_cases.py`. `.gitignore` now also lists `cases/TEST-NOTES.md`.
- `python scripts/pre_push_guard.py` passes again, so the embargo is enforced for every future push, and the files disappear from the branch tip when this report is pushed.
- Recorded in `DECISIONS.md`.
- **Residual, accepted:** the gold remains in the pushed history of `b2/build` and `arena/18088414-b2-obligation-triage`, in GitHub's unreachable-object store and in any pre-fix clone. The held-out split is therefore not blind to anyone with repo access; this is disclosed rather than repaired.

## 6. Rule-1 environment fix applied (logged in `INTEGRATION-LOG.md`)

- **File:** `scripts/prompt_hygiene.py`, 3 lines (`read_text()` → `read_text(encoding='utf-8')` at the corpus scan, the `cases/dev.json` read and the prompt/code/doc scan).
- **Reason:** on Windows those reads used the locale codec (`cp1252`) and died with `'charmap' codec can't decode byte 0x81 in position 172`, so `py -3.11 scripts/venv.py test` exited 1 after a green pytest leg. `python -X utf8 scripts/prompt_hygiene.py` passed beforehand, confirming the cause. Scan set, patterns and the "never open test gold" property are unchanged.
- **Verification:** `B2_OFFLINE=1 .venv/Scripts/python.exe scripts/prompt_hygiene.py` → exit 0; full `py -3.11 scripts/venv.py test` → exit 0.

## Commands run (with exit codes)

```
.venv/Scripts/python.exe scripts/build_cases.py                 0
.venv/Scripts/python.exe scripts/validate_cases.py --strict     0
.venv/Scripts/python.exe scripts/freeze_test_synthetics.py      0   (6d8fd4db… == committed)
py -3.11 scripts/venv.py test                                   1 -> 0  (after §6 fix; 60 passed, 1 skipped)
.venv/Scripts/python.exe scripts/prompt_hygiene.py              0   (after §6 fix)
.venv/Scripts/python.exe scripts/pre_push_guard.py              1   (protected paths tracked)
.venv/Scripts/python.exe scripts/freeze_check.py                1   (refs/tags/guide-v1.0 missing)
git ls-remote origin refs/heads/b2/build                         0   (37ef1d6 = HEAD)
```

## Deviations from the brief

- No `--replace-commitment`, no edits under `cases/`, `guide/`, `prompts/`, no force-add of `corpus/synthetic_test/`, `db/test_docs.sqlite`, `cache/llm/` or test results.
- One ≤20-line rule-1 fix to `scripts/prompt_hygiene.py`, logged (§6).
- Brief order is Phase C → Phase D (up to 3 tuning rounds) → Phase E calibration; no `handoff/round_*.md` exists, so tuning has not run. Confirm whether you intend to calibrate straight after the smoke test (skipping D) or run round 1 first.

## Open issues / stop-and-ask items

1. **Integrity incident (§5)** — your decision required; every push is blocked meanwhile.
2. **No API key**: `GROQ_API_KEY` is absent from process/user/machine scope and there is no `.env`, so neither the Phase C smoke test nor the 26-case dev run that `calibrate_floors.py --run` requires can start. Offline replay is not a substitute: `cache/llm/` holds 10,150 entries, **all** `provider=embedder` / `all-MiniLM-L6-v2`, zero LLM responses, so a cache-only dev run would exit 3 (`CacheMiss`).
3. **Tags**: `guide-v1.0` (GUIDE FROZEN is recorded in `INTEGRATION-LOG.md`, but the tag was never created and `reports/lean-migration.md` still lists four BUNDLE-NOTES human-review items "for tag before live") and `targets-v1`. Tell me to create them, or create them yourself.
4. `annotation/workspace/` is empty (§1).
5. Once 1–3 are cleared, the calibration sequence is: `python run_eval.py --split dev --live --scratch --limit 2` (smoke) → `python run_eval.py --split dev --live --scratch --rpm <safe from A2>` (full 26) → `python scripts/calibrate_floors.py --run eval_results/scratch/<run_dir>` → commit `config/thresholds.yaml` + `eval_results/threshold_calibration.md`.
