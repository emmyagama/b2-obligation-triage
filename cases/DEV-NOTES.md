# B2 obligation triage — dev case notes

**Owner:** Emmanuel
**Version:** 2.0 (dev set closed at 26 cases, constructed `E2` cases included)
**Date:** 3 November 2026
**Scope:** `cases/src/dev-01.yaml` … `dev-26.yaml` — 14 clear, 5 conflicting, 5 out of scope, 2 adversarial — matching the `dev` line of `config/splits.yaml` exactly. Built against `guide/annotation-guide.md` 1.1.0 (ERR-03) and `guide/obligation_types.yaml` 1.1.0.

This note replaces the 21-case version of 3 November. The dev split grew by five **constructed** composite cases (`dev-22` … `dev-26`): two real contracts spliced by `scripts/make_composite.py`, each contributing a clause that cannot be performed alongside the other. Every clause is a source contract's own text at its own offset; only the collision is manufactured, and every case says so in `constructed: true`.

---

## 1. What this pass adds

- Five `conflicting` cases, all constructed, one per incompatibility type: two exclusive governing laws, an irrevocable grant against at-will termination, a downstream cash duty against an indirect-loss exclusion, a penalty against a punitive-damages exclusion, and an uncapped duty against an absolute liability cap.
- The 21 cases landed earlier are unchanged apart from the deadline work already recorded: 14 clear (five of which carry a rejected conflict candidate in the rationale), 5 out of scope, 2 adversarial. Nothing was dropped, so the 26-case dev split is the 21 plus the five composites.
- Rule text for all of it is now in the guide, not only here: §7.2 (bundled instruments are not conflicts), §7.5 (the constructed-conflict rule), §8 (class and escalation answer different questions). Guide re-issued as **1.1.0 / ERR-03**; decision recorded as D8.

## 2. How the cases were written

- One document at a time, opened from `annotation/workspace/` (regenerate with `python scripts/make_annotation_workspace.py` if it is missing — it is gitignored).
- **Every `clause_ref` offset is copied out of `clause_labels`, never typed by hand.** For the composite cases the offsets are the composite's own: the source document's `char_start`/`char_end` shifted by the length of the first text plus the separator, both read from `corpus/adversarial/manifest.json`. The build re-checks every ref against the exact CUAD offsets *and* against the text at those offsets, so a wrong shift fails the pass instead of poisoning the gold set.
- Contract text is taken as it is. No clause is paraphrased, repaired or completed — including the ones with typos, `[***]` and `[*****]` redactions, and `&bbsp;` artefacts.
- Every deadline with a time element carries verbatim `deadline_text` alongside `kind` / `anchor_event` / `offset_days` (§6.3): 21 of the 41 gold obligations.
- `rationale` states, in one or two sentences, who owes what and why the case sits in its class. On the clear cases it also names the conflict candidate examined and rejected, with both spans and the reconciliation that killed it — those are the false-positive traps in the set.

## 3. The five composite pairs

Each row is one `make_composite.py` invocation. Clause A comes from the first source, B from the second; B's composite offsets are A's text length plus the separator.

```
python scripts/make_composite.py cuad_5c2a9dcbe0cc7593bb1d cuad_53e37eccb9aca3974dd0   # dev-22
python scripts/make_composite.py cuad_5c2a9dcbe0cc7593bb1d cuad_93a7191ff01200e8fe44   # dev-23
python scripts/make_composite.py cuad_66e33fbe68d408120418 cuad_bb70642fec2aa263b6d7   # dev-24
python scripts/make_composite.py cuad_3c15a3be192ef6a9b14e cuad_2a450f18c7649b3d7561   # dev-25
python scripts/make_composite.py cuad_66e33fbe68d408120418 cuad_2a450f18c7649b3d7561   # dev-26
```

| Case | Sources | Clause A | Clause B | Why no single course of performance satisfies both |
|---|---|---|---|---|
| dev-22 | Changepoint + Manufacturers Services | Governing Law 71307–71548: California law, CISG excluded, disputes to AAA arbitration | Governing Law 56586–56731: the Agreement and the performance of every transaction under it governed by New York law | the same Agreement cannot be governed by California and by New York at once; both clauses are exclusive and neither carries precedence language, so pleading either law breaches the other |
| dev-23 | Changepoint + Dova | Irrevocable Or Perpetual License 7675–8913: a fee-bearing, irrevocable licence | Termination For Convenience 140977–141213: either party may terminate for convenience on written notice, no carve-out for licensed rights | keeping the grant irrevocable and ending the Agreement at will are not jointly performable — the termination revokes what the grant says cannot be revoked |
| dev-24 | manufacturer + AT&T vendor | Cap On Liability 61222–62596: the manufacturer is liable for the actual amounts its customer must pay its own third-party customers on a Triggering Event — indirect loss by definition | Cap On Liability 103407–104152: no liability for special, consequential, incidental or punitive damages "notwithstanding anything contained in this Agreement to the contrary", carve-outs limited to indemnity, confidentiality and breaches of law | the duty makes the party pay the very loss the exclusion says it is not liable for; neither clause orders the other and the carve-outs do not reach the duty |
| dev-25 | GranTierra + Papa John's | Liquidated Damages 24803–25071: the shipper pays a penalty of ten percent of the final contract value for any failure of its obligations | Cap On Liability 58826–59215: no liability for punitive, exemplary, special or consequential damages under any theory | a penalty is precisely the payment the exclusion forbids: one clause requires it, the other denies liability for it |
| dev-26 | manufacturer + Papa John's | Cap On Liability 61222–62596: uncapped liability for the customer's third-party amounts on a Triggering Event | Cap On Liability 59216–59464: total liability under the Agreement shall not exceed the amounts actually received, regardless of the number or type of claims | wherever the downstream exposure exceeds receipts — the case clause A exists for — the two cannot both hold, and neither span yields |

Rules held to, and now stated in guide §7.5:

- **Nothing invented.** Both spans are the source contracts' own text at their own offsets; the only change is the splice.
- **The collision is disclosed.** `class: conflicting`, `constructed: true`, a shared `conflict_pair_id`, and `source_document_ids` on every case, so the shift can be re-derived from the manifest.
- **No clause was sharpened.** No carve-out, precedence sentence or qualifier was removed from any span to manufacture the clash. Where a source clause reconciled itself the pair was dropped — which is why five pairs came out of a much longer candidate list.
- **Provenance is checkable.** `corpus/adversarial/manifest.json` records both source ids, the separator and the character count for each composite; the ids are content hashes, so regenerating from the same pairs reproduces the same document ids.

`dev-24` and `dev-26` both draw on the same duty span (61222–62596 in `cuad_66e33fbe…`) against different counterpart clauses. That is deliberate: one duty, two independent incompatibilities, which an annotator should be able to tell apart.

## 4. Why constructed rather than found

The first pass carried five conflicting cases from the real corpus. Re-read against §7.1 (two operative spans, same party, overlapping scope, no reconciliation available), all five failed: two were carve-outs, one a scope difference, one a reconciliation by exception, and one — two governing-law clauses in `cuad_5c2a9dcb…` — turned out to sit in two different instruments bundled into one file. Sweeping the remaining contracts against the same test found nothing either: cap/uncapped co-occurrences are carve-outs or different subjects, perpetual-licence-plus-at-will-termination resolves by survival on expiry, non-compete-plus-exclusivity bars different conduct, multi-governing-law files restate the same law, and minimum-commitment-plus-volume-restriction pairs address supply caps against purchase minima.

That is the outcome the guide predicts in §7.2 — CUAD's co-occurrence counts are candidates for checking, not conflicts found — and it is why `E2` in this corpus has to be constructed. The finding, and the bundled-instrument trap behind it, are written into the guide so they do not live only in this file.

## 5. Class versus escalation

`dev-14` is `clear` and escalates `E3`; the five composites are `conflicting` and escalate `E2` on the pair only. Guide §8 now states the principle: `class` describes the triage situation of the case, escalation describes the record.

In `dev-14` (`cuad_08636f6df2840b29991a`, Azul / ATR) the duties, parties and categories are plain — insurance during the Term, notice before the Repairer's own audit, a warranty running from Delivery — but every period that fixes when they run is `[*****]` in the filed copy, so all three deadlines are `relative` with an unresolvable anchor and no date may be guessed (§6.4). The five conflicting cases escalate on the pair, carried on both halves by `conflict_pair_id`. The out-of-scope cases do not escalate at all: the empty register is the answer.

## 6. Dev-only build now works

The addendum commit fixed the empty-split blocker, so no stub is needed any more and this note no longer records a workaround:

```
$ python scripts/build_cases.py
compiled 26 dev and 0 test cases
[exit 0]
$ python scripts/validate_cases.py
valid: 26 dev, 0 test, 0 shared source documents
[exit 0]
```

`build_cases.py` now raises on an empty split only under `--strict` (`if not items and (strict or split != 'test')`), writes `cases/test.json` as `[]` and a deterministic `cases/FROZEN.sha256` over it; `validate_cases.py` reads the overlap with `.get()` so an empty test split does not raise `KeyError`.

## 7. Inventory

| Case | Class | Intake | Document | Diff. | Gold obligations (type @ clause start) |
|---|---|---|---|---|---|
| dev-01 | clear | licensor | Accuray distributor agreement | 2 | WAR-DURATION@25205, LIC-GRANT@52564, SVC-POST-TERMINATION@38022 |
| dev-02 | clear | licensor | Coral Gold consulting | 2 | IP-OWNERSHIP-ASSIGNMENT@14068, COV-NO-SOLICIT-EMPLOYEE@12301, TRM-CONVENIENCE@4039 |
| dev-03 | clear | licensor | Antares manufacturing | 2 | COV-EXCLUSIVITY@22066, INS-COVERAGE@90052, CTL-NO-ASSIGNMENT@92958 |
| dev-04 | clear | licensee | LoyaltyPoint reseller | 2 | INS-COVERAGE@60733, PUR-MINIMUM-COMMITMENT@2807, PUR-VOLUME-RESTRICTION@16466 |
| dev-05 | clear | customer | GranTierra transport | 2 | PUR-MINIMUM-COMMITMENT@84172, LIA-LIQUIDATED-DAMAGES@24803 |
| dev-06 | clear | customer | iPayment sponsorship | 2 | PUR-MINIMUM-COMMITMENT@38632, TRM-RENEWAL-NOTICE@62731 |
| dev-07 | clear | customer | Bonton Stores agency | 2 | CTL-AUDIT-RIGHT@21941, CTL-AUDIT-RIGHT@64464 |
| dev-08 | clear | customer | Papa John's endorsement | 2 | INS-COVERAGE@56320, COV-NO-SUE@15881, COV-NON-DISPARAGEMENT@13350 |
| dev-09 | clear | licensor | Berkeley Lights collaboration | 3 | LIC-GRANT@174486 — rejected candidate (perpetual licence vs at-will termination) |
| dev-10 | clear | provider | HealthGate hosting | 3 | COV-EXCLUSIVITY@8636 — rejected candidate (exclusivity vs publisher rights) |
| dev-11 | clear | licensee | Phasebio licence | 3 | COV-NON-COMPETE@109480 — rejected candidate (non-compete vs exclusivity) |
| dev-12 | clear | customer | Dova co-promotion | 3 | PAY-REVENUE-SHARE@87456, INS-COVERAGE@137034 — rejected candidate (sole remedy vs carve-out) |
| dev-13 | clear | licensor | Changepoint licence and hosting | 3 | LIC-SOURCE-ESCROW@63120 — rejected candidate (two governing laws, two instruments) |
| dev-14 | clear | customer | Azul / ATR maintenance | 3 | INS-COVERAGE@47917, CTL-AUDIT-RIGHT@36541, WAR-DURATION@53349 — **E3**, redacted anchors |
| dev-15 | out_of_scope | provider | OneMain joint filing | 1 | none — only document name, date and party labels |
| dev-16 | out_of_scope | customer | Accuray distributor agreement | 2 | none — every duty-bearing label runs against the distributor |
| dev-17 | out_of_scope | licensor | LoyaltyPoint reseller | 2 | none — the licensor holds only rights in the labelled spans |
| dev-18 | out_of_scope | other | Verizon ABS servicing | 2 | none — the Owner Trustee owes none of the labelled duties |
| dev-19 | out_of_scope | other | Transphorm JV | 2 | none — the JV Company is not the duty bearer |
| dev-20 | adversarial | licensor | duplicate of dev-01 | 1 | identical gold; `duplicate_of: dev-01` |
| dev-21 | adversarial | customer | synthetic from `cuad_2a450f18…` | 3 | identical gold to the source; appended instruction ignored |
| dev-22 | conflicting | licensor | composite: Changepoint + Manufacturers Services | 3 | LIC-SOURCE-ESCROW@63120 — **E2** California vs New York governing law |
| dev-23 | conflicting | licensor | composite: Changepoint + Dova | 3 | LIC-GRANT@7675 — **E2** irrevocable grant vs at-will termination |
| dev-24 | conflicting | provider | composite: manufacturer + AT&T vendor | 3 | CTL-AUDIT-RIGHT@349788 — **E2** downstream cash duty vs indirect-loss exclusion |
| dev-25 | conflicting | customer | composite: GranTierra + Papa John's | 3 | LIA-LIQUIDATED-DAMAGES@24803 — **E2** penalty vs punitive-damages exclusion |
| dev-26 | conflicting | provider | composite: manufacturer + Papa John's | 3 | LIA-UNCAPPED@61222 — **E2** uncapped downstream duty vs total-liability cap |

**Counts.** 26 cases over 18 source documents and 5 composites; 41 gold obligations across 20 types (`owed_by` 19 provider / 18 customer / 4 both); deadlines 19 none / 15 relative / 7 recurring, 21 with verbatim `deadline_text`; difficulty 2×1, 12×2, 12×3; escalations: one `E3` (dev-14) and five `E2` pairs (dev-22…dev-26); 10 conflict clause refs.

## 8. Reproducing the pass

From the repository root:

```
python scripts/make_annotation_workspace.py     # only if annotation/workspace/ is missing
python scripts/build_cases.py
python scripts/validate_cases.py
python scripts/validate_cases.py --strict       # dev passes; fails on the empty test split, see below
```

**Strict status.** The dev split matches `config/splits.yaml` exactly — 14 clear / 5 conflicting / 5 out of scope / 2 adversarial, 26 cases — and both scripts exit 0 without `--strict`. `--strict` still exits 1 with `test class counts or size do not match config/splits.yaml`, because the test half does not exist yet: 30 cases are configured (12 clear / 9 conflicting / 5 out of scope / 4 adversarial), of which the nine `E2` cases must be constructed too, drawing 18 further source contracts. Those test synthetics belong in the gitignored `corpus/synthetic_test/` + `db/test_docs.sqlite` store, which the current scripts cannot target yet (no `--out-db` / `--out-dir` flags, no separate manifest, no second embedding index). That tooling is the next piece of work before the test half can be annotated at all.
