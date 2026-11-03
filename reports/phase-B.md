NEXT ACTION FOR HUMAN: Annotate from `annotation/workspace/` (40 files, local to this repo checkout) and carry this report to the build agent for two rulings — (1) the 80 MB Chroma store held local under the brief's 25 MB threshold, (2) the taxonomy-loader boolean vs guide 0/1 mismatch (open issue B-1) — and confirm the embedding weights hash below against the Hugging Face original before any live run.

Phase: B (resumed after OpenCode stopped mid-phase; completed by the Arena execution agent)   Branch/sha: `arena/18088414-b2-obligation-triage` @ base `0922477` ("commit mid Phase B") + the Phase B completion commit containing this report   Date: 2026-11-03

Repo note: the brief names branch `b2/build`; this session is bound to the Arena session branch above, which started from the same commit `0922477` that OpenCode pushed to `b2/build`. Everything described here is pushed to the session branch.

---

## Where OpenCode stopped (state found at resume)

OpenCode's single squashed commit `0922477` already contained: the unpacked bundle v1, `adapters/b1_embedder.py` (correct against the `agent/embed.py` contract: 384-dim, `embed` + `embed_batch`, `normalize_embeddings=False` as in B1), `config/model.yaml` pointing at the adapter with the pinned LLM (`openai/gpt-oss-120b`, temperature 0, seed 42), `config/pricing.yaml` filled from Phase A, the built corpus (40 documents in `corpus/documents/`, `corpus/selection.json`, `db/b2.sqlite` with 40 `corpus_documents` rows and 2,075 `clause_labels` rows), and the human-filled guide/taxonomy. Missing at resume: embeddings (`corpus/embeddings/` absent, `corpus_version: unbuilt`), the annotation workspace, `reports/phase-B.md`, and any Phase B entries in `INTEGRATION-LOG.md`. Nothing in the found state was discarded; Phase B was completed from that commit.

## Commands run (with exit codes)

| Command | Exit | Result |
|---|---|---|
| `make setup` | 0 | venv created on Python 3.11.2; `requirements.txt` installed (run twice: once before, once after a sandbox restore dropped the ignored `.venv`; both exit 0) |
| `make test` (first run, found state) | 1 | `2 failed, 50 passed` — the two copytree-based engine tests; fixed per rule 1 (see `INTEGRATION-LOG.md`), after which the same tests pass individually and in the full suite |
| `.venv/bin/python -m pip install -r requirements-embedding.txt` | 0 | `sentence-transformers==6.1.0` + torch stack installed locally (sandbox-only; not a repo change) |
| adapter smoke test (offline, `B2_OFFLINE=1`, local weights) | 0 | 384-dim unit-norm vectors; paraphrase cosine 0.89 vs unrelated 0.17; batch == single (max diff 0.0); deterministic on repeat |
| `python scripts/build_corpus.py --cuad-dir data/cuad --n 40` | — | **Not re-run.** The corpus was already built and committed by OpenCode and verified read-only here: 40 picks, 2,075 label spans, `swaps: []`, conflict candidates 18/18 (minimum 14, shortfall 0). The gitignored raw CUAD download (`data/cuad/`) is not present in this sandbox (see "Access OpenCode had that this agent does not"), so a from-scratch rebuild cannot be replayed here; chunking over the committed corpus reproduces the build agent's independently verified 14,903 chunks exactly, which cross-validates the committed selection and offsets |
| `python scripts/build_embeddings.py` (offline; `HF_HUB_OFFLINE=1`, local model path) | 0 | `embedded 14903 chunks, dimension 384`; `corpus/embeddings/manifest.json` written; `config/model.yaml` `corpus_version` updated locally (held from the push, see below) |
| `python scripts/make_annotation_workspace.py` | 0 | `wrote 40 annotation workspace files` (run twice; regenerated identically after the sandbox restore) |
| `make test` (final) | 0 | `52 passed` and `prompt hygiene passed` |
| Chroma re-verification (post-restore) | 0 | store loads 14,903 chunks × 384 dims; content digest equals manifest `1a0f089d6fe42953c1dcc827c71d2b1df65fee364608706eab9d0feac070b2a2` |
| `python scripts/pre_push_guard.py` | 0 | see the completion commit's push record (run immediately before push) |

## The 40 contracts (from `corpus/selection.json`)

Selection rule (per the selector): longest per project-defined title bucket, then second-longest in priority order; conflict-candidate coverage checked against a minimum of 14, with swaps only of second picks. Result: **conflict candidates before 18, after 18, shortfall 0; swaps: none.** Conflict candidates are label co-occurrences, not adjudicated conflicts. Families below are the project-defined title buckets, not official CUAD families.

| # | Document ID | Family (bucket) | Chars | Title (truncated) |
|---|---|---|---|---|
| 1 | `cuad_a0e14c30056968d88209` | licence | 272,018 | Array BioPharma Inc. - LICENSE, DEVELOPMENT AND COMMERCIALIZATION AGREEMENT |
| 2 | `cuad_08636f6df2840b29991a` | maintenance | 233,248 | AzulSa_20170303_F-1A_EX-10.3_9943903_EX-10.3_Maintenance Agreement |
| 3 | `cuad_5dad919074219d103fb8` | distribution | 175,770 | ZogenixInc_20190509_10-Q_EX-10.2_11663313_EX-10.2_Distributor Agreement |
| 4 | `cuad_1bc91c6dfb434b456f99` | development | 291,873 | PhasebioPharmaceuticalsInc_20200330_10-K_EX-10.21_12086810_EX-10.21 |
| 5 | `cuad_66e33fbe68d408120418` | supply | 225,094 | UpjohnInc_20200121_10-12G_EX-2.6_11948692_EX-2.6_Manufacturing Agreement |
| 6 | `cuad_298ded523eb4fd77600d` | service | 289,615 | VerizonAbsLlc_20200123_8-K_EX-10.4_11952335_EX-10.4_Service Agreement |
| 7 | `cuad_96943dfc7ec66b62e263` | manufacturing | 109,219 | Sonos, Inc. - Manufacturing Agreement |
| 8 | `cuad_c92227514f576d98317e` | franchise | 300,768 | GOOSEHEADINSURANCE,INC_04_02_2018-EX-10.6-Franchise Agreement |
| 9 | `cuad_53e37eccb9aca3974dd0` | outsourcing | 338,211 | MANUFACTURERSSERVICESLTD_06_05_2000-EX-10.14-OUTSOURCING AGREEMENT |
| 10 | `cuad_4dec9f284717d01e7349` | consulting | 33,425 | SLINGERBAGINC_05_27_2020-EX-10.7-CONSULTING AGREEMENT |
| 11 | `cuad_412f6a035ef9763e47c2` | agency | 221,382 | Monsanto Company - SECOND A_R EXCLUSIVE AGENCY AND MARKETING AGREEMENT |
| 12 | `cuad_7c7b9fab0f2daf6004b0` | collaboration | 335,282 | CERES,INC_01_25_2012-EX-10.20-Collaboration Agreement |
| 13 | `cuad_aa43b2240f866f2fc18d` | cooperation | 76,425 | IDREAMSKYTECHNOLOGYLTD_07_03_2014-EX-10.39-Cooperation Agreement |
| 14 | `cuad_2a450f18c7649b3d7561` | endorsement | 68,204 | PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement |
| 15 | `cuad_ae248d81c03ed8dc2225` | intellectual_property | 155,463 | FIDELITYNATIONALINFORMATIONSERVICES,INC_08_05_2009-EX-10.3-INTELLECTUAL |
| 16 | `cuad_cdbbcb9c511d8f86fe50` | joint_filing | 5,879 | ONEMAINHOLDINGS,INC_02_20_2020-EX-99.D-JOINT FILING AGREEMENT |
| 17 | `cuad_c1d38c5a7a05b88b6c21` | joint_venture | 95,181 | TRANSPHORM,INC_02_14_2020-EX-10.12(1)-JOINT VENTURE AGREEMENT |
| 18 | `cuad_93a7191ff01200e8fe44` | promotion | 175,580 | DovaPharmaceuticalsInc_20181108_10-Q_EX-10.2_11414857_EX-10.2_Promotion |
| 19 | `cuad_b1fe09126a4d0b840349` | reseller | 117,478 | LOYALTYPOINTINC_11_16_2004-EX-10.2-RESELLER AGREEMENT |
| 20 | `cuad_c7256920fc58b74bbd37` | sponsorship | 96,662 | IPAYMENT,INC_05_14_2007-EX-10.1-SPONSORSHIP AGREEMENT |
| 21 | `cuad_1f9cab5d8d6e18e6f1a8` | strategic_alliance | 122,054 | MOELIS_CO_03_24_2014-EX-10.19-STRATEGIC ALLIANCE AGREEMENT |
| 22 | `cuad_3c15a3be192ef6a9b14e` | transportation | 229,670 | GRANTIERRAENERGYINC_05_07_2012-EX-10.6-TRANSPORTATION CONTRACT |
| 23 | `cuad_646f2847afd01a811aa5` | marketing | 52,106 | XpresspaGroupInc_20190401_10-K_EX-10.28_11599457_EX-10.28_Marketing |
| 24 | `cuad_a08094c0e438a7a9c7e5` | branding | 114,759 | InvendaCorp_20000828_S-1A_EX-10.2_2588206_EX-10.2_Co-Branding Agreement |
| 25 | `cuad_c72abcf3341f1ecf6365` | other | 148,691 | HEALTHGATEDATACORP_11_24_1999-EX-10.1-HOSTING AND MANAGEMENT AGREEMENT |
| 26 | `cuad_5c2a9dcbe0cc7593bb1d` | licence | 161,066 | CHANGEPOINTCORP_03_08_2000-EX-10.6-LICENSE AND HOSTING AGREEMENT |
| 27 | `cuad_bb70642fec2aa263b6d7` | maintenance | 228,943 | AtnInternationalInc_20191108_10-Q_EX-10.1_11878541_EX-10.1_Maintenance |
| 28 | `cuad_424083274037f63d7530` | distribution | 89,484 | ACCURAYINC_09_01_2010-EX-10.31-DISTRIBUTOR AGREEMENT |
| 29 | `cuad_8535780896bd997df598` | development | 266,213 | RevolutionMedicinesInc_20200117_S-1_EX-10.1_11948417_EX-10.1_Development |
| 30 | `cuad_ac330c6c3a9cc0496f44` | supply | 188,674 | BELLICUMPHARMACEUTICALS,INC_05_07_2019-EX-10.1-Supply Agreement |
| 31 | `cuad_fca73dd7b89c2e571f11` | service | 112,910 | ReynoldsConsumerProductsInc_20200121_S-1A_EX-10.22_11948918_EX-10.22 |
| 32 | `cuad_871f14e107390dae4b35` | manufacturing | 106,786 | Antares Pharma, Inc. - Manufacturing Agreement |
| 33 | `cuad_7714bf6314a468cda863` | franchise | 249,359 | MRSFIELDSORIGINALCOOKIESINC_01_29_1998-EX-10-FRANCHISE AGREEMENT |
| 34 | `cuad_3d9c71ed150a6a3c3f1f` | outsourcing | 159,336 | OFGBANCORP_03_28_2007-EX-10.23-OUTSOURCING AGREEMENT |
| 35 | `cuad_7d139ce53ee5a9dbf8d5` | consulting | 29,749 | CORALGOLDRESOURCES,LTD_05_28_2020-EX-4.1-CONSULTING AGREEMENT |
| 36 | `cuad_052975b81f9779a680c0` | agency | 161,626 | BONTONSTORESINC_04_20_2018-EX-99.3-AGENCY AGREEMENT |
| 37 | `cuad_03a1e0f461f5359c5502` | collaboration | 209,067 | BERKELEYLIGHTS,INC_06_26_2020-EX-10.12-COLLABORATION AGREEMENT |
| 38 | `cuad_2ef7ad1e760173ae3b0f` | cooperation | 59,532 | MEETGROUP,INC_06_29_2017-EX-10.1-COOPERATION AGREEMENT |
| 39 | `cuad_d39bf71d3da2729aca84` | endorsement | 48,410 | NakedBrandGroupInc_20150731_POS AM (on S-1)_EX-10.75_9196027_EX-10.75 |
| 40 | `cuad_944e0822aba9ea79bbd5` | intellectual_property | 127,205 | ZEBRATECHNOLOGIESCORP_04_16_2014-EX-10.1-INTELLECTUAL PROPERTY AGREEMENT |

Total corpus text: 6,482,417 characters across the 40 documents. DB check: `corpus_documents` = 40 rows, `clause_labels` = 2,075 rows — matching the selector output. Annotation workspace: `annotation/workspace/` in this repo checkout, **40 files** (one per document; gitignored, so present locally, not in the push). Repo sizes: `corpus/documents/` + `corpus/selection.json` ≈ 6.5 MB, `db/` 1.2 MB, `annotation/workspace/` ≈ 1.0 MB, `corpus/embeddings/` ≈ 80 MB (local only, see below).

## Embeddings and the 25 MB threshold (brief step B5 stop-and-report)

The store was built successfully and verified, but `corpus/embeddings/` is **83,530,382 bytes (~80 MB)**, over the brief's 25 MB threshold, so per the brief this was stopped and reported to the human in session, with the investigation the human requested:

- Anatomy: `chroma/chroma.sqlite3` ≈ 59 MB (Chroma full-text index ≈ 27 MB, stored chunk texts/metadata ≈ 23 MB, insert queue ≈ 3 MB, indexes/remainder) + HNSW `data_level0.bin` ≈ 23 MB (the raw 14,903 × 384 float32 vectors = 22.9 MB). Chunk texts total only 7.0 MB; the store format, not the corpus, dominates. Gzipped, the whole store is ≈ 46 MB; the largest single file (≈ 57 MB) is under GitHub's 100 MB limit.
- Reductions tested on copies and rejected: `VACUUM` gains nothing (freelist 0). Deleting the full-text index shrinks the sqlite file to ≈ 26 MB but Chroma then fails to load the store (`Error finding id`, reproduced), so there is no safe post-hoc strip without changing the build agent's store design.
- Chunk-size scaling (computed, not rebuilt): 1,000 chars → 11,111 chunks (≈ 62 MB estimated), 1,400 → 8,587 (≈ 48 MB), 2,000 → 6,769 (≈ 38 MB). Even 2,000 chars misses 25 MB because stored text/FTS dominate, and beyond ~1,000 chars chunks exceed the model's 256-token window (700 chars ≈ 175 tokens, the B1 rationale), silently truncating embeddings. A dimension change means a different model. Any of these is a design change for the build agent, not an execution-agent fix.

**Human decision (in session):** commit and push everything except the Chroma store and the `corpus_version` bump; keep the store local and gitignored (`.gitignore` entry added with the reason) because the build agent's export script will read it; put this anatomy in this report; close Phase B. Accordingly this push contains **no** `corpus/embeddings/` and `config/model.yaml` still reads `corpus_version: unbuilt` in the repo; the bump (`sha256:cacb1b3f…3d11`) exists only in the local working tree alongside the local store. Until the build agent rules, a fresh clone cannot replay against these embeddings — that is the accepted, disclosed consequence of the hold. The build agent should rule on: store format vs the 25 MB expectation, chunk size/dimension, or accepting ~80 MB.

Embedding model provenance in this sandbox (network cannot reach Hugging Face here): weights came from the PyPI wheel `gt-all-minilm-l6-v2==0.1.0`, which bundles `sentence-transformers/all-MiniLM-L6-v2` for offline use. Wheel sha256 matches the PyPI-published digest (`b9a0018d…a54`); bundled `model.safetensors` sha256 `53aa51172d142c89d9012cce15ae4d6cc0ca6895895114379cacb4fab128d9db`; config is the expected 6-layer/384-hidden/vocab-30522 BertModel. The adapter gained an optional `B2_EMBEDDING_MODEL_PATH` override (default unchanged) to load the exported local copy. **Before any live run, confirm the safetensors hash against the Hugging Face original** (Phase C already requires re-verifying model/price facts); if it differs, the embeddings must be rebuilt — `corpus_version` binding ensures a rebuild, not a silent swap. Full detail in `INTEGRATION-LOG.md`. Note the local weights export did not survive the sandbox restore (below) and must be re-exported from the same verified wheel before any rebuild in this sandbox.

## Prompt hygiene and the guide (protected paths)

Two hygiene failures were found against the filled guide and resolved only with human-authored wording, applied verbatim; a full read-only replica scan confirmed no other files trip the guard:

1. `guide/annotation-guide.md` §6.1 example phrases shared 8-word sequences with two corpus contracts. Human supplied replacement example wording for both rows in session; applied verbatim; file now passes.
2. `guide/obligation_types.yaml` metadata field name (corpus acronym + version digit, 42 occurrences) matched the guard's identifier pattern. No code reads that field and it appears nowhere else. Human selected the exact rename (same name without the digit); applied verbatim.

Final state: `make test` fully green (`52 passed`, `prompt hygiene passed`). These edits are the human's authored changes carried by the execution agent, logged in `INTEGRATION-LOG.md`. No protected file was edited on the execution agent's own initiative, and the guard was not weakened.

## Deviations from the brief

- **Branch:** work is on the Arena session branch `arena/18088414-b2-obligation-triage` (from `b2/build`'s `0922477`), not `b2/build` itself; the session binding does not permit switching. Merge path to `b2/build`/`main` is the human's call (Phase G merges per the brief).
- **Embeddings not committed** (step B6) and `corpus_version` bump held, per the human's in-session ruling on the 25 MB threshold above. Corpus, DB, selection and workspace (step B5 outputs) are committed/present as specified; `reports/phase-B.md` is this file.
- **`build_corpus.py` not re-run** in this sandbox because the raw CUAD download is not available here (below); the committed corpus was verified instead (counts, offsets via chunk reproduction, 14,903-chunk cross-check against the build agent's independent figure).
- **Rule-1 fixes made** (each logged with diffs in `INTEGRATION-LOG.md`): the two copytree engine tests made hermetic (+4 lines; clean-checkout failures, would also fail CI); `adapters/b1_embedder.py` optional local model path (+4 lines). No other code was changed. `scripts/run_embeddings.py` found in the tree (a network-allowing wrapper by OpenCode) was left untouched and unused; the brief's `scripts/build_embeddings.py` was used.
- **Sandbox restore incident:** the sandbox was restored from a snapshot mid-session, dropping ignored local state (`.venv`, embedding `cache/llm/` entries, the local weights export, `annotation/workspace/`). Tracked files and `corpus/embeddings/` were intact (digest re-verified). Venv rebuilt, workspace regenerated, full tests re-passed. The execution agent did not delete any cache; the loss was environmental and is disclosed here and in the log.

## Access OpenCode had that this agent does not (as requested)

- **Unrestricted network.** OpenCode's Windows machine could reach Hugging Face (model download), `raw.githubusercontent.com` (CUAD), and presumably Groq. This sandbox can reach only `github.com`, `codeload.github.com`, `api.github.com`, `registry.npmjs.org`, `pypi.org`, `files.pythonhosted.org`; Hugging Face, Groq, S3 and raw GitHub content fail at TLS. Consequences handled above: weights sourced via a verified PyPI wheel; no live Groq call was made or attempted in Phase B (none is required until Phase C smoke tests).
- **The raw CUAD data (`data/cuad/`, gitignored)** and the B1 local clone referenced in Phase A are not in this sandbox. Not needed for Phase B completion (corpus already built), but any corpus rebuild or Phase A replay here would need the human to supply `data.zip` (sha256 in `corpus-report.md`).
- **`GROQ_API_KEY`.** Not present in this sandbox and never requested in chat. Phase C's live smoke test and all later live phases need the key supplied in the execution environment (shell/`.env`, never committed) plus Groq network access — or they must run on a machine that has both, as OpenCode's did.
- **`gh` CLI / GitHub auth** are not set up in this sandbox; pushes here use the session's configured git remote. Phase G's `gh run watch` steps need `gh` auth wherever they run.

## Open issues / stop-and-ask items

- **B-1 (blocks Phase C):** taxonomy loader vs guide type mismatch — `agent/taxonomy.py:15` requires a YAML boolean for the escalation-default field; the guide uses `0`/`1` integers throughout, so loading the real taxonomy raises. Human to change guide values to `true`/`false`, or build agent to accept `0`/`1` in the loader. Not fixed here (protected path on one side, build-agent semantics on the other). Detail in `INTEGRATION-LOG.md`.
- **B-2 (blocks committing embeddings/replay):** the 80 MB vs 25 MB ruling for the build agent (anatomy above). The local store and local `corpus_version` are preserved in this checkout for the build agent's export script; do not delete `corpus/embeddings/` locally.
- **B-3 (before any live run):** confirm the embedding weights hash against the Hugging Face original and re-verify Groq model/pricing/limits (Phase A figures were read 2026-11-02); supply `GROQ_API_KEY` + network in the live environment.
- **B-4 (informational):** guide freeze/tag (`guide-v1.0`), targets tag, and case building are Phase C items and were not started; the guide edits recorded above were made before any freeze, at the human's direction, so no frozen artefact is affected.

## Deliverables status for Phase B

- Bundle v1 integrated and committed (`0922477`, by OpenCode) — done before resume.
- `make setup && make test` — **green** (52 passed + prompt hygiene) after the logged rule-1 test fix and the human-worded guide fixes.
- Embedder adapter written, config pointed at it, LLM/temperature/seed pinned, `config/pricing.yaml` filled (Phase A numbers) — done (OpenCode) and verified here.
- Corpus (40 contracts, selection, DB) built and committed — done (OpenCode), verified here; embeddings built and verified — **held local by human decision**; annotation workspace generated — **40 files at `annotation/workspace/` (local; the human annotates from there)**.
- `reports/phase-B.md` (this file) and `INTEGRATION-LOG.md` — in the completion commit. Tag: none (per brief).
