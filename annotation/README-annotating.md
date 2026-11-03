# Annotation desk — human judgement only

Emmanuel chooses source pairs and writes all obligation, deadline, party, escalation, rationale, difficulty and gold judgements. Generated workspaces and synthetic scripts are mechanisms, not suggested answers. CUAD's expert clause labels are inputs, not obligation gold. No genuine E2 conflict was found in the 40 selected contracts; the 14 planned E2 cases are constructed composites from real clauses. Human review must determine whether each constructed pairing meets the guide.

## Cases

Write YAML under `cases/src/`, one case per file or an array. Filenames must begin with `dev-` or `test-`, agreeing with `split`. Fields are `id`, `split`, `document_id`, `intake_party`, optional `business_context`, `class`, `gold_obligations`, `gold_should_escalate`, `gold_escalation_codes`, `rationale` and integer `difficulty`. For a synthetic, supply `source_document_id` or ordered `source_document_ids`, matching its manifest. A composite must have `constructed: true`; each conflicting case must use a composite and include human-authored E2. Other cases may omit `constructed` or set it false.

Each gold obligation has `type`, `owed_by`, `clause_category`, `deadline` and `clause_ref`. A ref has `category`, `char_start`, `char_end` and optional `document_id`; omission means the case document. Offsets are zero-based Python Unicode character offsets, end-exclusive. Source refs on composites are mapped through the recorded boundary; exact labels and slices are checked. `conflict_clause_refs` is an optional list of additional exact refs; at least two distinct refs must appear across it and the gold obligations for a conflicting case. This mechanical check does not decide legal incompatibility.

`deadline.kind` is absolute, relative, recurring or none. `deadline_text` may be a string or null; `resolved_date`, when present, is ISO; `offset_days`, when present, is an integer. Other human-authored deadline metadata may include `anchor_event`, `anchor_resolved` and `period`. The scorer currently assesses kind and resolved date, not deadline text or other metadata. See the handoff for guide/validator implications. `duplicate_of` is for an adversarial exact duplicate referencing an earlier case in the same split, with identical text, party and context; replay reuses the original request.

## Construct and compile

Use `python scripts/make_composite.py --split dev SOURCE_A SOURCE_B` or `--split test` for locally embargoed test composites. Sources must be two different real base documents. The script joins whole documents in the specified order and maps all existing source labels; it creates no gold. The test split writes only under `corpus/synthetic_test/` and `db/test_docs.sqlite`. Use `scripts/make_adversarial.py --split test ...` for test-only mutations. These paths, including provenance and vector indexes, are ignored and guarded before the completed valid held-out run.

Compile with `python scripts/build_cases.py`; dev-only compilation is permitted and creates an empty test artifact locally. `--strict` requires both splits; `python scripts/validate_cases.py --strict` verifies configured counts and exact references. Before publishing any commitment, review the source overlap and class distribution. `cases/FROZEN.sha256` is the only held-out artifact pushed before the completed valid live test run. Never expose held-out gold or test per-case results before freeze. After a valid test run, do not tune.

Non-English mutation needs a supplied excerpt or explicitly selected offline translation adapter; it has no inherited CUAD labels. The optional translation requirements and language model are separately installed by the operator. See `BUNDLE-NOTES.md` for the lean-index build and test-shard steps.
