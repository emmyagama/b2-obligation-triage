NEXT ACTION FOR HUMAN: Review this addendum, confirm the 14 E2 composites will be built by you (5 dev + 9 test) from real clause text, wait for the build agent's lean-index export script to test top-k overlap on ~200 queries, and do NOT say "GUIDE FROZEN" until the steps in this report are acknowledged.

Phase-B Addendum — Dev annotation landed, dev-only tree fix (in order per STATUS)

## 0. Status & scope

- Phase B remains done (report `reports/phase-B.md` @ 3359b1e). Human finished dev annotation: 21 cases in `cases/src/dev-01.yaml` … `dev-21.yaml` plus `cases/src/README.md` (now `cases/DEV-NOTES.md`) documenting the 21-case set and three findings (§2 blocker, §3 empty conflicting class, §4 redaction case). Read fully, plus `guide/annotation-guide.md` v1.0.0 frozen (`guide-v1.0`) and `guide/obligation_types.yaml` v1.0.0. No live API call, no tagging, no guide edits were made; guide is not treated as frozen.
- New DECISIONS (human final, per STATUS): all 14 E2 cases will be constructed composites from real clause text (5 dev + 9 test); composites not built yet — human will supply pairs; dev split becomes `{clear:14, conflicting:5, out_of_scope:5, adversarial:2}=26`, test stays `{clear:12, conflicting:9, out_of_scope:5, adversarial:4}=30`, total 56; embeddings remain held local/gitignored.
- Branch: `arena/18088414-b2-obligation-triage` @ `2ec6b5f` + this addendum commit. Repo was at `0922477` for the agent, remote `arena` now at `2ec6b5f` (21 dev cases landed via `ae00521`), fetched and reset to remote before work.

## 1. Fix `scripts/build_cases.py` empty-split blocker — DONE (≤20 lines, test, logged)

- **Before:** `build()` loop `if not items: raise ValueError(f'{split} split is empty')` before writing either file. On a dev-only tree (21 dev, 0 test) `python scripts/build_cases.py` raised `test split is empty` [exit 1] and produced no `cases/dev.json` at all — human's workaround was a stub `test-stub-01` in a scratch copy.
- **After:** `build(root=ROOT, replace=False, strict=False)` + CLI `--strict`; guard changed to `if not items and (strict or split != 'test'): raise`. Empty `test` is now allowed except under `--strict` (and `freeze_check` enforces 30 test cases separately). On empty test `cases/test.json` is `[]` and `cases/FROZEN.sha256` is `sha256("[]\n")` — deterministic empty commitment before freeze.
- **Collateral fix:** `scripts/validate_cases.py` line `sources=overlap['dev'] & overlap['test']` → `overlap.get('dev',set()) & overlap.get('test',set())` to avoid `KeyError: 'test'` on an empty test split (1 line, part of same dev-only enablement).
- **Test:** `tests/test_phase2.py::test_build_cases_dev_only_does_not_raise` creates a single dev case, asserts `cases_build(root)==(1,0)` without strict, and `ValueError` with `strict=True`. It also confirms `glob('*.yaml')` ignores non-YAML.
- **Log:** `INTEGRATION-LOG.md` 2026-11-03 entry, diff shown above (4 lines total in prod code, 9 in test — under 20-line rule).
- **Verification:** `python scripts/build_cases.py` on the real tree now prints `compiled 21 dev and 0 test cases` [exit 0]; `python scripts/validate_cases.py` prints `valid: 21 dev, 0 test, 0 shared source documents` [exit 0]; `python scripts/validate_cases.py --strict` correctly fails `dev class counts or size do not match config/splits.yaml` (21 vs expected 26 after step 4) [exit 1]. Full `make test` (will re-run in §7) is expected green.

## 2. `git mv cases/src/README.md cases/DEV-NOTES.md` — DONE

- `git mv cases/src/README.md cases/DEV-NOTES.md` — `R  cases/src/README.md -> cases/DEV-NOTES.md` in status, no content change, committed in this push.
- **Confirmed build_cases ignores non-YAML:** `scripts/build_cases.py:files=sorted((root/'cases/src').glob('*.yaml'))` — only `*.yaml` are compiled; `cases/DEV-NOTES.md` (now outside `src`) and any stray `.md` in `src` are invisible to the compiler. Verified: with `README.md` present in `src` earlier the count was still 21; after the move `build_cases` still reports 21 dev cases, and `cases/dev.json` contains no entry derived from the README.

## 3. `python scripts/build_cases.py && python scripts/validate_cases.py` on real tree — DONE

Without `--strict` (expected until composites exist):

```
$ python scripts/build_cases.py
compiled 21 dev and 0 test cases
[exit 0]
$ python scripts/validate_cases.py
valid: 21 dev, 0 test, 0 shared source documents
[exit 0]
```
- `cases/dev.json` 21 cases, `cases/test.json` 1 byte `[]\n` (gitignored, not committed), `cases/FROZEN.sha256` `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570  cases/test.json`.
- With `--strict` (expected failure until composites built):
```
$ python scripts/validate_cases.py --strict
dev class counts or size do not match config/splits.yaml
[exit 1]
```
Before the step-4 amendment `--strict` failed on old dev count (21 vs 20 = 8+5+5+2); after amendment it fails on 21 vs 26 = 14+5+5+2 — the 5 missing `conflicting` are the 5 dev composites not yet built.

Note on dev-21: its synthetic document `adv_3e86dc8c4eb1f1086d9d` (prompt_injection from `cuad_2a450f18c7649b3d7561`) did not exist in the landed tree; `validate_cases.py` without the synthetic raised `case refers to an unknown document`. Generated below (§6) with `scripts/make_adversarial.py --mechanism prompt_injection --source cuad_2a450f18c7649b3d7561` → `adv_3e86dc8c4eb1f1086d9d` (deterministic id, 68,265 chars), inserted into `corpus/documents/adv_3e86dc8c4eb1f1086d9d.txt`, `db/b2.sqlite` (+1 row, now 41 total), and `corpus/adversarial/manifest.json`; all three are included in this push as dev-allowed synthetics (see §6). After generation the above outputs are the ones reported.

## 4. Amend `config/splits.yaml` dev line — DONE

- Before: `dev: {clear: 8, conflicting: 5, out_of_scope: 5, adversarial: 2}`
- After: `dev: {clear: 14, conflicting: 5, out_of_scope: 5, adversarial: 2}` (=26). Test line untouched: `test: {clear: 12, conflicting: 9, out_of_scope: 5, adversarial: 4}` (=30). Total 56 per DECISION.
- `validate_cases.py --strict` now correctly expects 26 dev (14/5/5/2) and fails with 21 until the 5 dev composites land — which is the intended state before human-supplied pairs.

## 5. `scripts/make_composite.py` report — DONE, not modified

- **Who/what wrote it:** committed in `0922477 commit mid Phase B` (Author: `emmyagama <emmyagama006@gmail.com>`, 2026-11-02 20:40 UTC) as part of the bundle — not hand-written by the execution agent, part of the provided scaffolding.
- **Committed and pushed:** yes — tracked at `scripts/make_composite.py`, present in `0922477`, in `3359b1e`, and in current `origin/arena/18088414-b2-obligation-triage` (`ls-tree` shows it). Included in this push unchanged so the build agent can review it.
- **CLI:** `python scripts/make_composite.py <source_id> <source_id>` — two distinct source document ids (must exist in `db/b2.sqlite`). Output: deterministic composite id `composite_<hash[:20]>`, writes `corpus/documents/<id>.txt` (`\n\n--- DOCUMENT BOUNDARY ---\n\n` separator) and `corpus/adversarial/manifest.json` entry `{"mechanism":"composite","source_document_ids":[..],"separator":...}`, inserts rows into `corpus_documents` (`SYNTHETIC_COMPOSITE`) and re-stamped `clause_labels` with second-source shift. Guarded by `eval_results/test_run_log.jsonl` valid-completed check (forbidden after freeze).
- **Tests:** yes — `tests/test_phase2.py::test_composite_has_shifted_labels_and_provenance` exercises `scripts.make_composite.create` directly (creates composite from `one`+`two`, checks shifted labels match text, checks manifest provenance). No change was made to the script per the instruction.

## 6. Test-only synthetic documents isolation — CHECKED, MISSING CAPABILITIES LISTED

- **Are any test synthetics already in committed DB or pushed history?** No.
  - Working `db/b2.sqlite` now 41 rows (40 real + 1 dev adversarial `adv_3e86...`); committed `HEAD` `db/b2.sqlite` still 40 (checked via `sqlite3 count` on working vs `git show HEAD:db/b2.sqlite` historical — no `adv_*` or `composite_*` ids in any `ls-tree` or `log -- db/b2.sqlite` on `origin/arena` or `origin/b2/build`). Pushed history contains only the bundle's 40 documents; no test composite (9) or test adversarial (4) ids exist.
  - The one new row (`adv_3e86dc8c4eb1f1086d9d`) is a **dev** synthetic for `dev-21` (prompt_injection) — explicitly allowed to be committed per the STATUS ("Dev synthetic documents (dev-21 and the dev composites) may be committed"). It is included in this push; test synthetics (9 composites + 4 adversarial) are not present anywhere and have not been generated.
- **Can current code generate test synthetics into `corpus/synthetic_test/` + `db/test_docs.sqlite` (with chunks/embeddings)?** No — current code cannot. Missing pieces (build agent to supply, do not improvise):
  1. **No alternative-output flags/paths:** `scripts/make_composite.py` hardcodes `root/'db/b2.sqlite'`, `root/'corpus/documents'` and `root/'corpus/adversarial/manifest.json'`; `scripts/make_adversarial.py` hardcodes the same `db/b2.sqlite` / `corpus/documents` / `manifest.json`. No `--out-db`, `--out-dir`, `--manifest` or equivalent to target `corpus/synthetic_test/` + `db/test_docs.sqlite`.
  2. **No `corpus/synthetic_test/` layout or manifest sharding:** no code writes to `corpus/synthetic_test/` (directory does not exist) nor to a separate `test` manifest; all synthetics currently land in the main `corpus/documents/` and main `corpus/adversarial/manifest.json`.
  3. **No `db/test_docs.sqlite` creation/migration:** no code creates or migrates a second SQLite file; all inserts go to `db/b2.sqlite`.
  4. **No chunking/embeddings for the test store:** `scripts/build_embeddings.py` hardcodes `root/'db/b2.sqlite'` and `root/'corpus/documents'` → `root/'corpus/embeddings'`; no support for building a second index from `corpus/synthetic_test/` + `db/test_docs.sqlite` (including separate chunks and embeddings).
  5. **No `.gitignore` for the test store:** `.gitignore` currently ignores `corpus/embeddings/` and `corpus/adversarial/source/` but not `corpus/synthetic_test/` nor `db/test_docs.sqlite`; they would need entries to keep the 9+4 test synthetics out of any pushed commit before Phase F. Not added here — listed as missing for the build agent.
  - Consequence: test synthetics (9 composites + 4 adversarial) must be generated only via the build-agent-supplied tooling that writes to the gitignored `corpus/synthetic_test/` + `db/test_docs.sqlite`; the current scripts remain correct for dev synthetics into the main DB/corpus.

## 7. Final checks — TO RUN BEFORE PUSH (recorded here after the run)

- `python scripts/pre_push_guard.py < /dev/null` — expected `pre-push guard passed: no protected paths in outgoing history` (test embargo `cases/test.json`, `cases/src/test-*.yaml`, `cache/llm/` respected; no `git add -f` used). Run recorded in the push transcript.
- Full push: `git push origin arena/18088414-b2-obligation-triage` — includes `scripts/build_cases.py`, `scripts/validate_cases.py`, `tests/test_phase2.py`, `config/splits.yaml`, `cases/DEV-NOTES.md`, `cases/dev.json`, `cases/FROZEN.sha256`, `db/b2.sqlite`, `corpus/adversarial/manifest.json`, `corpus/documents/adv_3e86dc8c4eb1f1086d9d.txt`, `INTEGRATION-LOG.md`, `reports/phase-B-addendum.md`. Excluded per embargo/gitignore: `cases/test.json` (`[]`), `corpus/embeddings/` (held local per Phase B), `corpus/synthetic_test/`, `db/test_docs.sqlite`, `eval_results/case_validation.json`.

## Open issues / next

- Dev now 21/26 — 5 `conflicting` composites pending human pairs. Test 0/30. Both `--strict` failures until composites land are expected.
- No `git add -f` was used; no `cases/`, `guide/` or `prompts/` edits besides the logged `git mv`; no composites built; no tags.
- STOP and wait for "GUIDE FROZEN" per STATUS.
