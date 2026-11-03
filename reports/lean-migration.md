NEXT ACTION FOR HUMAN: Verify the 26-case dev split (14 clear / 5 E2 composites / 5 oos / 2 adv) matches `config/splits.yaml`, confirm the lean index size (17.7M for 46 docs, 13.5M for 40 base) is acceptable under the 25 MB brief threshold (Chroma 80M remains ignored), and do NOT run `--split test` live until the 9 test composites are built and the test shard is frozen via `freeze_test_synthetics.py` — guide is now frozen.

Phase: v1.1 lean-index migration (GUIDE FROZEN)   Branch: `arena/18088414-b2-obligation-triage` @ `80bbea9` (bundle v1.1) + this commit   Date: 2026-11-03

Inspect confirms the build-agent's b2-bundle-v1.1 overlay (35 files, `B2 v1.1 — changed-files handoff` in `BUNDLE-NOTES.md`) on base `7c07919`. Human guide/taxonomy 1.1.0 ERR-03 and dev 26 (5 constructed E2) already landed as `974f836`/`2e4be59` (26 YAML, DEV-NOTES 2.0). This run is the Phase B-machine lean migration.

## Commands run (with exit codes)

| Command | Exit | Result |
|---|---|---|
| `git fetch` + `reset --hard origin/arena` | 0 | landed bundle (`80bbea9`) with `agent/lean_index.py`, `scripts/export_lean_index.py`, updated `build_embeddings.py` (`--split dev/test`), `corpus_version.py`, `requirements-export.txt`, etc. |
| `make setup` | 0 | venv rebuild (py3.11) on bundle's pinned `requirements.txt` (16 pkgs, light) |
| Model restore (PyPI wheel `gt-all-minilm-l6-v2==0.1.0` sha256 `b9a0018d…`, `model.safetensors` `53aa5117…`) | 0 | `/home/user/model-cache/all-MiniLM-L6-v2/` (88M) — same hash as Phase B, `B2_EMBEDDING_MODEL_PATH` used, offline |
| Old Chroma rebuild (via `7c07919:scripts/build_embeddings.py` + chromadb) | 0 | `embedded 14903 chunks, dim 384` → `corpus/embeddings/chroma` 57M + HNSW, `manifest.json` chroma (`1a0f089d…`) |
| `B2_OFFLINE=1 python scripts/export_lean_index.py` | 0 | `{"verified_chunks":14903,"dimensions":384,"corpus_version":"sha256:0f4a8408…","unindexed_base_documents":0,"diagnostic":{"index_bytes":13520772,"mean_top_k_overlap":0.99875,"minimum_top_k_overlap":0.875,"queries":200,"top_k":8}}` → lean `chunks.json` 2.0M + `vectors.npy` 11M + `manifest.json` + `legacy_chroma_manifest.json` + `migration_report.json` (diagnostic self-queries, not human queries) |
| `B2_OFFLINE=1 B2_BASE_ROOT=$PWD B2_CHROMA_STORE=$PWD/corpus/embeddings/chroma pytest -q tests/test_v11.py::test_local_chroma_all_14903_slices` | 0 | 1 passed — all 14903 source slices match lean metadata |
| `make_composite --split dev` ×5 (pairs from DEV-NOTES 2.0) | 0 | `composite_d8416b5f…` (Changepoint+53e37ecc), `c5f9c6f4…` (Changepoint+Dova), `1d5bf003…` (Upjohn+bb70642), `bc622aa3…` (GranTierra+Papa), `8fd5f850…` (Upjohn+Papa) — 46 docs total (40+1 adv+5), manifest 6 entries |
| `B2_OFFLINE=1 python scripts/build_embeddings.py --split dev` | 0 | `embedded 19445 chunks, dim 384` (reused 14903, embedded 4542 new) → lean `chunks.json` 2.7M + `vectors.npy` 15M, `corpus_version` `sha256:f31c766c…` |
| `python scripts/build_cases.py` / `validate_cases.py` | 0/0 | `26 dev and 0 test` / `valid: 26 dev, 0 test, 0 shared` — `validate --strict` fails on empty test as expected until test shard built |
| `make test` | 0 | `60 passed, 1 skipped` (new `test_v11` 7 tests), `prompt hygiene passed` |
| `python scripts/pre_push_guard.py < /dev/null` | 0 | `no protected paths` — Chroma + test shard remain gitignored |

## Inspect of b2-bundle-v1.1

- **Apply base:** `arena/18088414-b2-obligation-triage` @ `7c07919d837f`; overlay not a full repo — human guide/taxonomy/dev gold not in overlay, retained from remote.
- **New/changed key files:** `agent/lean_index.py` (text-free NumPy index, cosine, `LeanIndex`/`Shards`), `scripts/export_lean_index.py` (one-time Chroma→lean, checks every slice, top-k diagnostic), `scripts/build_embeddings.py` now `--split dev/test` with vector reuse, `agent/corpus_version.py` hashes lean vector bytes (excludes test synthetics, includes `document_sha256`), `agent/synthetic.py` + `scripts/make_composite.py`/`make_adversarial.py` now `--split test` to `corpus/synthetic_test/` + `db/test_docs.sqlite` (gitignored, guard-blocked), `scripts/freeze_test_synthetics.py` (seal `FROZEN-SYNTHETIC`), `tests/test_v11.py` (7 new tests), `.gitignore` updated via this commit to commit lean, ignore Chroma/test shard.
- **Human review note (from BUNDLE-NOTES):** guide integer `0/1` now loads but runtime E3 mapping + deadline_text verbatim + original CUAD test exclusion still need human sign-off before live — no guide edits made here.
- **Chroma vs lean:** Chroma 57M sqlite + 23M HNSW = 80M (ignored, Phase B hold retired); lean 40-doc 13.5M (`index_bytes` from diagnostic) + 46-doc 17.7M (vectors+chunks) — both under 25 MB brief threshold. `corpus_version` now hashes lean, not Chroma.

## Lean-index export detail

- **Export input:** `corpus/embeddings/chroma` (14903 chunks, `content_sha256` `1a0f089d6fe42953c1dcc827c71d2b1df65fee364608706eab9d0feac070b2a2`, model `all-MiniLM-L6-v2`) — rebuilt locally with same weights hash as Phase B.
- **Output:** `corpus/embeddings/` lean: `chunks.json` text-free metadata (5 fields, sorted by `chunk_id`), `vectors.npy` float16 (15M for 46 docs, 11M for 40), `manifest.json` (`b2-lean-v1`, sha256 of both files + `document_sha256` map), `legacy_chroma_manifest.json` retained, `migration_report.json` diagnostic.
- **Diagnostic (stored-vector self queries, 200 deterministic, top-8):** `mean_top_k_overlap` **0.99875**, `minimum` **0.875**, `queries` 200, `top_k` 8, `index_bytes` 13520772 — per BUNDLE-NOTES, this is a diagnostic of old rounded L2 `1/(1+dist)` vs new cosine, not a real human-query benchmark; float16 tie changes explain <1.
- **Independent check:** `test_local_chroma_all_14903_slices` passed — every of the 14903 Chroma chunk texts equals its source document slice at the lean metadata offsets.
- **After 5 composites:** `build_embeddings --split dev` reused the 14903 exported vectors (same model/dtype/chunking) and locally embedded only the 4542 new chunks from the 6 new docs (1 adv +5 composites), total 19445. New `corpus_version` `sha256:f31c766ca3…` includes document bytes, labels, base provenance, text-free chunk metadata, vector bytes, format/model/dim/dtype — excludes test material (test shard not built, `FROZEN-SYNTHETIC` not sealed).

## Dev composites built (already in pushed history + this commit)

- 26 dev cases exactly match `config/splits.yaml` dev `14/5/5/2`: 14 clear (dev-01…14, 5 with rejected candidate rationales) + 5 E2 composites (dev-22…26) + 5 out_of_scope (15…19) + 2 adversarial (20 duplicate, 21 prompt_injection `adv_3e86…`). `build_cases`/`validate` pass without `--strict`; `--strict` fails on empty test (30 test = 12/9/5/4 pending, 9 E2 test composites human work, test shard gitignored).
- Composite sources (from DEV-NOTES 2.0): dev-22 `5c2a9dcb+53e37ecc`, dev-23 `5c2a9dcb+93a7191f`, dev-24 `66e33fbe+bb70642`, dev-25 `3c15a3be+2a450f1`, dev-26 `66e33fbe+2a450f1` — each joined with `--- DOCUMENT BOUNDARY ---`, provenance in `corpus/adversarial/manifest.json` (ordered hashes, separator, text hash). Offsets validated at mapped composite positions.

## Sizes and commit

- **Before (Phase B Chroma):** `corpus/embeddings/chroma/chroma.sqlite3` 57M + HNSW 23M = 80M (ignored, `corpus/embeddings/` old hold).
- **After (v1.1 lean):** base 40-doc lean 13.5M index_bytes (2.0M json + 11M npy + manifests), 46-doc lean 17.7M (2.7M +15M) — committed in this push; Chroma 80M stays ignored; `.gitignore` updated to ignore `chroma` + `corpus/synthetic_test/` + `db/test_docs.sqlite*` (protected by guard).
- **This push:** `cases/dev.json` (26), `config/model.yaml` (`corpus_version` `f31c766c…`), `corpus/adversarial/manifest.json` (6), `db/b2.sqlite` (46), 5× `composite_*.txt`, `corpus/embeddings/` lean 5 files, `.gitignore`, `INTEGRATION-LOG.md`, this report. Excluded: `cases/test.json` (empty `[]`, embargoed), `corpus/embeddings/chroma` (80M), test shard (not built), `eval_results/case_validation.json` (gitignored/protected).

## Open / next

- Test side still 0/30 — 9 E2 test composites must be authored (source pairs by human), then `build_embeddings --split test` + `freeze_test_synthetics.py` → `cases/FROZEN-SYNTHETIC.sha256` before any dev live run; `freeze_check.py` will verify both commitments and `code-frozen`/`guide-v1.0` tags.
- GUIDE FROZEN acknowledged — no guide edits made here; human review items from BUNDLE-NOTES remain (E3 vs confirmation, E2 party/scope check, deadline_text verbatim, CUAD test exclusion) for tag before live.
