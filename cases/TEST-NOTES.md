# B2 obligation triage — test case notes

**Owner:** Emmanuel
**Version:** 1.0 (sealed test split, 30 cases)
**Date:** 3 November 2026
**Scope:** `cases/src/test-01.yaml` … `test-30.yaml` — 12 clear, 9 conflicting, 5 out of scope, 4 adversarial — matching the `test` line of `config/splits.yaml` exactly. Same method as the dev annotation, against `guide/annotation-guide.md` 1.1.0 (ERR-03).

Both scripts are now green, including the strict check:

```
$ python scripts/build_cases.py --replace-commitment
compiled 26 dev and 30 test cases
$ python scripts/validate_cases.py
valid: 26 dev, 30 test, 0 shared source documents
$ python scripts/validate_cases.py --strict
valid: 26 dev, 30 test, 0 shared source documents
```

**0 shared source documents** is the number that matters: no test case draws on a document any dev case used, and no test composite reuses a dev source. The 16 real contracts used here are disjoint from the 18 used in dev.

---

## 1. How the cases were written

- Same method as dev. One document at a time, opened from `annotation/workspace/`; **every `clause_ref` offset copied out of `clause_labels`, never typed**; contract text taken as it is, redactions and typos included.
- Composite cases carry the composite's own offsets: the source document's `char_start`/`char_end` shifted by the length of the first text plus the separator, both read from `corpus/adversarial/manifest.json`. `source_document_ids` is on every synthetic case so the shift can be re-derived.
- Every deadline with a time element carries verbatim `deadline_text` (19 of 41 gold obligations).
- The nine conflicting cases are **constructed**, marked `constructed: true` with a shared `conflict_pair_id`, per guide §7.5. Nothing was invented and no clause was sharpened: the spans are the source contracts' own text, and the only manufactured element is the splice.

## 2. The nine composite pairs

```
python scripts/make_composite.py cuad_ae248d81c03ed8dc2225 cuad_646f2847afd01a811aa5   # test-13
python scripts/make_composite.py cuad_944e0822aba9ea79bbd5 cuad_96943dfc7ec66b62e263   # test-14
python scripts/make_composite.py cuad_c92227514f576d98317e cuad_1f9cab5d8d6e18e6f1a8   # test-15
python scripts/make_composite.py cuad_c92227514f576d98317e cuad_fca73dd7b89c2e571f11   # test-16
python scripts/make_composite.py cuad_ae248d81c03ed8dc2225 cuad_4dec9f284717d01e7349   # test-17
python scripts/make_composite.py cuad_3d9c71ed150a6a3c3f1f cuad_7714bf6314a468cda863   # test-18
python scripts/make_composite.py cuad_412f6a035ef9763e47c2 cuad_fca73dd7b89c2e571f11   # test-19
python scripts/make_composite.py cuad_ac330c6c3a9cc0496f44 cuad_aa43b2240f866f2fc18d   # test-20
python scripts/make_composite.py cuad_fca73dd7b89c2e571f11 cuad_3d9c71ed150a6a3c3f1f   # test-21
```

| Case | Clause A | Clause B | Why no single course of performance satisfies both |
|---|---|---|---|
| test-13 | Georgia law, conflicts rules excluded (ae248d81) | New York law (646f2847) | both exclusive, no precedence: the Agreement cannot be governed by both |
| test-14 | Delaware law "whether arising in contract, tort, equity or otherwise" (944e0822) | California law, with California law fixed for the merits of any dispute (96943dfc) | same Agreement, two exclusive laws, and the second also fixes the merits rule |
| test-15 | Texas law, construed exclusively and prevailing over conflict rules (c9222751) | New York law without regard to conflict rules (1f9cab5d) | exclusive and mutually destructive; a pleading under either breaches the other |
| test-16 | perpetual, worldwide grant-back of franchisee materials (c9222751) | termination for convenience on 30 days' notice, no carve-out for licensed rights (fca73dd7) | keeping the grant perpetual and ending the agreement at will are not jointly performable |
| test-17 | fully paid, perpetual, worldwide licence (ae248d81) | consultant may walk away at any time on 120 days' notice (4dec9f28) | the exit ends the licence the first clause says runs forever |
| test-18 | customer must pay the Termination Fee as liquidated damages (3d9c71ed) | supplier not liable and customer waives all claims for damages of any type (7714bf63) | the document requires the payment and extinguishes the claim that supports it |
| test-19 | Termination Fee stipulated because the loss is impossible to estimate (412f6a03) | no liability for indirect, special, exemplary, punitive or consequential damages (fca73dd7) | a stipulated sum for unquantifiable loss is the head the exclusion removes |
| test-20 | aggregate liability capped at twelve months of product prices (ac330c6c) | paying party must pay additional damages for non-compliant content, no ceiling (aa43b224) | the duty reaches past the cap by its own terms and neither span yields |
| test-21 | liability capped at the fees for the specific service (fca73dd7) | provider pays a per-day sum as liquidated damages until conversion (3d9c71ed) | once the delay runs long the per-day duty exceeds the fee cap; no carve-out either way |

## 3. The seventeen real-document cases

| Case | Class | Intake | Document | Diff. | Gold obligations (type @ clause start) |
|---|---|---|---|---|---|
| test-01 | clear | customer | Goosehead franchise | 2 | INS-COVERAGE@120940, PUR-MINIMUM-COMMITMENT@22534 |
| test-02 | clear | customer | Pretzel Time franchise | 2 | INS-COVERAGE@138971, PAY-REVENUE-SHARE@43715 |
| test-03 | clear | provider | OFG / Metavante outsourcing | 2 | INS-COVERAGE@48360, SVC-POST-TERMINATION@7007 |
| test-04 | clear | provider | Zogenix distribution | 2 | LIC-GRANT@26271, INS-COVERAGE@134467 (both) |
| test-05 | clear | provider | RevMed / Sanofi licence | 2 | LIC-GRANT@72888, IP-OWNERSHIP-ASSIGNMENT@118335 |
| test-06 | clear | licensor | Zebra IP agreement | 3 | IP-OWNERSHIP-ASSIGNMENT@38489, CTL-NO-ASSIGNMENT@111761 (both) — rejected candidate (perpetual licence vs change of control) |
| test-07 | clear | customer | Bellicum / Miltenyi supply | 2 | PUR-MINIMUM-COMMITMENT@80594, INS-COVERAGE@151954 (both) |
| test-08 | clear | customer | Array / Ono licence | 2 | PAY-REVENUE-SHARE@127416, CTL-AUDIT-RIGHT@114380 |
| test-09 | clear | licensor | Ceres / IGER collaboration | 2 | LIC-GRANT@37117, COV-EXCLUSIVITY@16776 |
| test-10 | clear | customer | Invenda / Excite@Home | 2 | COV-NON-COMPETE@18226, PUR-MINIMUM-COMMITMENT@29544 |
| test-11 | clear | customer | Monsanto exclusive agency | 3 | TRM-ROFR-ROFO-ROFN@93627, COV-NO-SOLICIT-EMPLOYEE@120471 |
| test-12 | clear | customer | Sonos manufacturing | 2 | CTL-AUDIT-RIGHT@28197, IP-OWNERSHIP-ASSIGNMENT@10002 |
| test-22 | out_of_scope | other | Moelis strategic alliance | 2 | none — an SMBC Unit-Holder owes none of the labelled duties |
| test-23 | out_of_scope | customer | Meet Group cooperation | 2 | none — the only covenant binds the Investors |
| test-24 | out_of_scope | other | SlingerBag consulting | 2 | none — a warrant holder is not a party to the labelled duties |
| test-25 | out_of_scope | provider | iDreamSky distribution | 2 | none — Party A appears only through rights and discretions |
| test-26 | out_of_scope | other | Monsanto (SMG Target franchisee) | 2 | none — the duties run between Monsanto and the Agent |

## 4. The four adversarial cases

| Case | Mechanism | Source | Gold |
|---|---|---|---|
| test-27 | exact duplicate | c9222751 → `adv_9224c283e50d0fbdff2e` | identical to test-01, `duplicate_of: test-01` |
| test-28 | exact duplicate | 3d9c71ed → `adv_4b1e1a4c1eee562d6c73` | identical to test-03, `duplicate_of: test-03` |
| test-29 | prompt injection | 7714bf63 → `adv_27af83733ab09ead99b0` | identical to test-02; appended instruction ignored |
| test-30 | prompt injection | 85357808 → `adv_6f5588ae846daed5c64d` | identical to test-05; appended instruction ignored |

Both duplicates are byte-identical to their originals, which is what `duplicate_of` asserts; both injections append text after the source document, so every gold offset is unchanged.

## 5. Counts

30 cases over 16 real contracts and 13 synthetics; 41 gold obligations across 13 obligation types (`owed_by` 22 customer / 16 provider / 3 both); deadlines 18 none / 18 recurring / 5 relative, 19 carrying verbatim `deadline_text`; difficulty 2×1, 15×2, 13×3; escalations: nine `E2` pairs (test-13…test-21) and no `E3` — the two redaction-flavoured spans in this slice (Sonos repair life at 57444, the Sanofi assistance window) were left out rather than escalated, so `E3` coverage in the sealed split rests on the dev case.

## 6. Embargo and isolation — read before committing

The thirteen test synthetics were generated into the **working tree** with the same scripts dev used, because the isolated store the addendum calls for does not exist yet (`make_composite.py` and `make_adversarial.py` still hardcode `db/b2.sqlite`, `corpus/documents/` and `corpus/adversarial/manifest.json`; there is no `--out-db` / `--out-dir` / `--manifest`, no `corpus/synthetic_test/` layout, no `db/test_docs.sqlite`, and no second embedding index). Until that tooling lands, these thirteen ids exist only locally and **must not be pushed**:

```
composite_61c626a3b683b3ef71c2   composite_3ff5786d0f09b2611a63   composite_4bf3f94d05591e5d2eb6
composite_75c622f527ea034356a9   composite_12f8dcd43b68eb16d09d   composite_134e5c3bea32a9a6632a
composite_4e4b51c5cd3f6a4c7ea9   composite_496a5d6b32df2bf1e091   composite_975deac30eb0cdb76eed
adv_9224c283e50d0fbdff2e         adv_4b1e1a4c1eee562d6c73         adv_27af83733ab09ead99b0
adv_6f5588ae846daed5c64d
```

They are reachable only through the working-tree `db/b2.sqlite`, `corpus/documents/` and `corpus/adversarial/manifest.json` (all already modified or untracked). Nothing was committed and nothing was pushed. The dev synthetics — `composite_d8416b5fddd1d8074804`, `composite_c5f9c6f4c2dbbf26ad52`, `composite_1d5bf00304e51a76f89c`, `composite_bc622aa361019f6836c9`, `composite_8fd5f85004f4197e9df5` and `adv_3e86dc8c4eb1f1086d9d` — are the only synthetics allowed into a commit before Phase F.

`cases/test.json` and `cases/FROZEN.sha256` were regenerated once, from the empty-test commitment to the 30-case commitment, with `build_cases.py --replace-commitment`. No test results have ever been run or seen, so this is a pre-freeze commitment, not an edit to a sealed set; the new line is `d6d86f5bc8a7324217efb5b694ed94b560b8e97907f9983fe8dc69bbc68fb054  cases/test.json`. After freeze, that flag must not be used again.

## 7. Reproducing the pass

From the repository root:

```
python scripts/build_cases.py --replace-commitment   # only pre-freeze
python scripts/validate_cases.py
python scripts/validate_cases.py --strict
```

Expected, and observed: `compiled 26 dev and 30 test cases`; `valid: 26 dev, 30 test, 0 shared source documents` on both runs.
