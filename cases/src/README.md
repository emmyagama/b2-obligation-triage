# B2 obligation triage — dev case set

**Owner:** Emmanuel
**Version:** 1.0 (dev set for the pilot)
**Date:** 3 November 2026
**Scope:** 21 dev cases, `cases/src/dev-01.yaml` … `cases/src/dev-21.yaml`, built against `guide/annotation-guide.md` and `guide/obligation_types.yaml`.

This is the dev half of the pilot corpus. Each file is one case in the §3.3 template: `id`, `split`, `document_id`, `intake_party`, `business_context`, `class`, `gold_obligations[]` (`type`, `owed_by`, `clause_category`, `clause_ref{category, char_start, char_end}`, `deadline{…}`), `gold_should_escalate`, `gold_escalation_codes`, `rationale`, `difficulty` — plus `conflict_clause_refs` where a pair was examined and `duplicate_of` on the duplicate case.

Three things in here deserve an explanation before anyone reads the YAML: a blocker in the build script, and two judgement calls I made on the mix.

---

## 1. How the cases were written

- One document at a time, opened from `annotation/workspace/` (regenerate with `python scripts/make_annotation_workspace.py` if the folder is missing — it is gitignored).
- **Every `clause_ref` offset is copied out of `clause_labels` in `db/b2.sqlite`, never typed by hand.** The validator re-checks each ref against the exact CUAD offsets and against the contract text at those offsets, so a transposed digit fails the pass instead of silently poisoning the gold set.
- Contract text is taken as it is. No clause is paraphrased, repaired or completed, including the ones with typos, `[***]` and `[*****]` redactions, and `&bbsp;` artefacts.
- `rationale` states, in one or two sentences, who owes what and why the case sits in the class it sits in. Where a conflict candidate was examined and rejected, the rationale names both spans and gives the reconciliation that killed the candidate — those cases are the false-positive traps in the set.
- Every deadline that has a time element carries the verbatim `deadline_text` alongside `kind`/`anchor_event`/`offset_days`, per §6.3.

## 2. Blocker: `build_cases.py` will not run on a dev-only tree

`scripts/build_cases.py` compiles both splits and raises before writing either one:

```
$ python scripts/build_cases.py
test split is empty
[exit 1]
```

Because the raise happens in the loop over `('dev','test')`, a repository with only dev cases produces no `cases/dev.json` at all, and `validate_cases.py` then has nothing to check. Until the test split exists this is a hard stop, so I ran the pass like this:

1. Copied the working tree to a scratch directory.
2. Dropped one throwaway case into `cases/src/` there — a single `out_of_scope` record with a real document id and no gold obligations, `id: test-stub-01`, `split: test`.
3. Ran both scripts from the scratch root:

```
compiled 21 dev and 1 test cases
valid: 21 dev, 1 test, 1 shared source documents
[exit 0]
```

4. Deleted the scratch copy. Nothing about the stub is in this bundle; the dev cases were never edited to accommodate it.

So both scripts pass on this set. What they pass against, in a scratch tree with a non-empty test split, is the same thing they will pass against once the real test split lands. The only thing this bundle cannot yet demonstrate is `validate_cases.py --strict`, because `config/splits.yaml` still asks the dev split for `conflicting: 5` and this set has none — see §3.

## 3. Judgement call 1 — the `conflicting` class is empty, and that is the finding

The dev mix in `config/splits.yaml` asks for 8 clear / 5 conflicting / 5 out of scope / 2 adversarial. I cannot fill the five conflicting slots honestly, and I would rather hand over the evidence than five labels that a reviewer will pull apart.

### 3.1 Five candidates reclassified to `clear`

Each of these was carried as conflicting in the first draft. Re-read against §7.1 (two operative spans, same party, overlapping scope, no reconciliation available), each one fails, so each is now `clear` with the reconciliation recorded in its rationale:

| Case | Document | Spans | Why it is not a conflict |
|---|---|---|---|
| dev-09 | Berkeley Lights / Ginkgo | 174486–174659 vs 74863–75104 | The perpetual, irrevocable licences arise only on a Buy-Down Election termination; 74863–75104 is Ginkgo terminating the separate Software License Agreement at will. Different termination routes, both performable. |
| dev-10 | HealthGate | 8636–8940 vs 17196–17378 | The exclusive right to carry out the Services expressly leaves the Publishers free to publish and license content against a revenue condition; the other span only bars using escrowed software to build a competing product. Different objects. |
| dev-11 | Phasebio | Exclusive Period span vs 109480–110735 | The Exclusivity span governs assignment of third-party contractor inventions; the Non-Compete span bars SFJ's own trials and sales of competing products. Different conduct. |
| dev-12 | Dova / Valeant | 45695–45915 vs 136727–137016 | Sole-remedy cap for breach of the Section 4.1.2 sales-force covenant, against an express carve-out preserving indemnity and confidentiality claims. §7.2 bullet 1 and §7.1(4): the carve-out reconciles them. |
| dev-13 | Changepoint | 71307–71548 vs 151209–151449 | Both are exclusive choice-of-law clauses and neither yields — but 71307 is Clause 14.3 of the License and Hosting Agreement (California, AAA arbitration) and 151209 is Clause 9.9 of the *Changepoint Software License and Maintenance Agreement* that is appended to the same corpus file (New York). Two instruments, so the same-subject and overlapping-scope conditions fail. |

dev-13 is the one I most wanted to keep, because two governing-law clauses in one file is exactly what a conflict looks like from the outside. It survives only if the file is treated as one agreement, and it is not: the second instrument has its own parties page, its own section numbering and its own governing law. The lesson is worth keeping in the guide — **the corpus bundles separate instruments into single documents** (53e37ecc does the same with an IBM outsourcing agreement and an appended trade-secret agreement), and a bundled instrument can manufacture a fake conflict or silently break an offset.

### 3.2 Sweep of the other contracts

I then ran the conflict test over the remaining contracts rather than accept the empty class:

| Check | Contracts | Result |
|---|---|---|
| `Cap On Liability` + `Uncapped Liability` (§7.3 row 1) | all 40 | Every co-occurrence is either a carve-out inside one span or a different subject (warranty remedy vs general cap). No capped-and-uncapped pair for the same liability and party. |
| Perpetual/irrevocable licence + termination for convenience (§7.3 row 2) | 03a1e0f4, 5dad9190, 7714bf63, 85357808, a0e14c30 | Survival-on-expiry provisions, or termination rights over different objects (7714bf63: the Advertising Fund, not the licensed marks). |
| Non-compete + exclusivity (§7.3 row 3) | 1bc91c6d, 412f6a03, 5dad9190, 646f2847, 93a7191f, a0e14c30, c72abcf3, d39bf71d | Each pair bars different conduct, or an exception category reconciles them. |
| Multiple `Governing Law` labels | 08636f6d, 4dec9f28, 53e37ecc, 5c2a9dcb, 85357808, b1fe0912, c9222751 | Only 5c2a9dcb states two different laws, and that is the two-instrument case above. The rest restate the same law. |
| `Minimum Commitment` + `Volume Restriction` | 03a1e0f4, 2a450f18, 3c15a3be, 66e33fbe, a08094c0, b1fe0912 | Supply caps against purchase minima — different subjects, both satisfiable. |
| Termination-bar language | fca73dd7 | One hit, and it *grants* termination rights rather than barring them. |
| `Expiration Date` / `Renewal Term` pairings | 14 contracts incl. 1f9cab5d, 3d9c71ed, 725e…, 53e37ecc | Consistent. 53e37ecc renews the Base Agreement in 12-month periods on six months' notice and the Attachment in six-month periods on twelve months' notice; the longer notice satisfies the shorter, so there is no impossibility. |
| Exclusive vs non-exclusive grants | 19 contracts | Different licensees, different subjects, or an expiry conversion to non-exclusive. |
| Positive/negative polarity overlap on duty-bearing categories | 18 contracts | Section-scoped pairs or one span carrying two labels (ae248d81 51797–53812 is a single span double-labelled, not two clauses). |
| Anti-assignment vs change-of-control (08636f6d) | 1 | 22(a) requires prior consent including on a change of control; 22(b) opens with "Notwithstanding the above" and adds a material-adverse-effect proviso. Reconciliation language is present. |

**Conclusion.** Across these 40 contracts there is no pair that satisfies all four conditions of §7.1. That is not a gap in the sweep — it is what the guide predicts in §7.2: CUAD's co-occurrence counts (111 `Cap + Uncapped`, 40 `Irrevocable + Termination for Convenience`, 68 `Non-Compete + Exclusivity` across the full 510) are candidates for checking, and in this slice every one of them dissolves into a carve-out, a scope difference or a bundled instrument. The escalating case in this set is `E3`, not `E2`.

**Consequence for the mix.** This set ships 14 clear / 0 conflicting / 5 out of scope / 2 adversarial. To keep the pass reproducible I did not edit `config/splits.yaml`; the dev line should be amended to match, or `--strict` will keep reporting a class-count mismatch:

```yaml
dev: {clear: 14, conflicting: 0, out_of_scope: 5, adversarial: 2}
```

For E2 coverage I would not weaken the definition. The one honest route is construction: `scripts/make_composite.py` splices two contracts into one document with provenance tracked in `corpus/adversarial/manifest.json`, and the validator already maps offsets across the splice. A composite carrying two incompatible caps, or a perpetual grant against an uncarved at-will termination, gives a genuine `E2` pair that nothing in the document reconciles — and it is labelled as constructed rather than being smuggled in as a real-world conflict. Say the word and I will build those cases next; until then the `E2` code is exercised nowhere in dev, which is itself a fact the pilot should know.

## 4. Judgement call 2 — the redaction case (`dev-14`)

`dev-14` comes from `cuad_08636f6df2840b29991a` (Azul / ATR Global Maintenance Agreement), intake party Azul as customer. The duties are plain on the face of the document:

- **47917–48136** — the Company must keep its insurances in force, at its own cost, for the Term *and* a post-term tail that is redacted (`at all times during the Term and [*****]`).
- **36541–36652** — the Repairer must give notice of its own audit `no later than [*****] prior to such audit`.
- **53349–53701** — the repaired-unit warranty runs from Delivery `shall end [*****] thereafter`.

Every period that says when those duties run is `[*****]` in the filed copy, so all three deadlines are `relative` with `anchor_event: unresolved`, `resolved_date: null` and no guessed figure (§6.4). The case therefore escalates `E3_CONDITIONAL_OR_AMBIGUOUS` even though it is classed `clear`.

That combination is deliberate and I want it to be read that way: **`class` is a property of the triage situation, `escalation` is a property of the record.** The duty, the party and the category here are all unambiguous, so the case is not an ambiguity case at class level and not out of scope; what cannot be settled is the clock. Redacted anchors are going to be routine in this corpus — the guide's own numbers put a missing Effective Date in 120 of 510 contracts and a missing Expiration Date in 97 — so the pilot needs at least one case where the register is right and the deadline is unresolvable.

## 5. Inventory

| Case | Class | Intake party | Document | Diff. | Gold obligations (type @ clause start) |
|---|---|---|---|---|---|
| dev-01 | clear | licensor | Accuray distributor agreement | 2 | WAR-DURATION@25205, LIC-GRANT@52564, SVC-POST-TERMINATION@38022 |
| dev-02 | clear | licensor | Coral Gold consulting agreement | 2 | IP-OWNERSHIP-ASSIGNMENT@14068, COV-NO-SOLICIT-EMPLOYEE@12301, TRM-CONVENIENCE@4039 |
| dev-03 | clear | licensor | Antares manufacturing agreement | 2 | COV-EXCLUSIVITY@22066, INS-COVERAGE@90052, CTL-NO-ASSIGNMENT@92958 |
| dev-04 | clear | licensee | LoyaltyPoint reseller agreement | 2 | INS-COVERAGE@60733, PUR-MINIMUM-COMMITMENT@2807, PUR-VOLUME-RESTRICTION@16466 |
| dev-05 | clear | customer | GranTierra transport contract | 2 | PUR-MINIMUM-COMMITMENT@84172, LIA-LIQUIDATED-DAMAGES@24803 |
| dev-06 | clear | customer | iPayment sponsorship agreement | 2 | PUR-MINIMUM-COMMITMENT@38632, TRM-RENEWAL-NOTICE@62731 |
| dev-07 | clear | customer | Bonton Stores ageing report | 2 | CTL-AUDIT-RIGHT@21941, CTL-AUDIT-RIGHT@64464 |
| dev-08 | clear | customer | Papa John's endorsement agreement | 2 | INS-COVERAGE@56320, COV-NO-SUE@15881, COV-NON-DISPARAGEMENT@13350 |
| dev-09 | clear | licensor | Berkeley Lights collaboration | 3 | LIC-GRANT@174486 — rejected candidate (perpetual licence vs at-will termination) |
| dev-10 | clear | provider | HealthGate hosting agreement | 3 | COV-EXCLUSIVITY@8636 — rejected candidate (exclusivity vs publisher rights) |
| dev-11 | clear | licensee | Phasebio licence | 3 | COV-NON-COMPETE@109480 — rejected candidate (non-compete vs exclusivity) |
| dev-12 | clear | customer | Dova co-promotion agreement | 3 | PAY-REVENUE-SHARE@87456, INS-COVERAGE@137034 — rejected candidate (sole remedy vs carve-out) |
| dev-13 | clear | licensor | Changepoint licence and hosting | 3 | LIC-SOURCE-ESCROW@63120 — rejected candidate (two governing laws, two instruments) |
| dev-14 | clear | customer | Azul / ATR maintenance | 3 | INS-COVERAGE@47917, CTL-AUDIT-RIGHT@36541, WAR-DURATION@53349 — **E3**, redacted anchors |
| dev-15 | out_of_scope | provider | OneMain joint filing agreement | 1 | none — only document name, date and party labels |
| dev-16 | out_of_scope | customer | Accuray distributor agreement | 2 | none — every duty-bearing label runs against the distributor |
| dev-17 | out_of_scope | licensor | LoyaltyPoint reseller agreement | 2 | none — the licensor holds only rights in the labelled spans |
| dev-18 | out_of_scope | other | Verizon ABS servicing agreement | 2 | none — the Owner Trustee owes none of the labelled duties |
| dev-19 | out_of_scope | other | Transphorm JV agreement | 2 | none — the JV Company is not the duty bearer |
| dev-20 | adversarial | licensor | duplicate of dev-01 | 1 | identical gold; `duplicate_of: dev-01` |
| dev-21 | adversarial | customer | synthetic document from 2a450f18 | 3 | identical gold to the source; appended instruction ignored |

**Counts:** 21 cases over 18 documents; 36 gold obligations across 19 obligation types; `owed_by` 17 customer / 15 provider / 4 both; deadlines 16 none / 13 relative / 7 recurring, 19 of them with verbatim `deadline_text`; difficulty 2×1, 12×2, 7×3; one escalating case (`E3`).

Case-class coverage note: the two adversarial cases are a verbatim duplicate (dev-20) and a prompt-injection append (dev-21, `adv_3e86dc8c4eb1f1086d9d`, generated with `scripts/make_adversarial.py --mechanism prompt_injection --source cuad_2a450f18c7649b3d7561`). The gold for both is identical to the source document at the same offsets — the point is that neither the duplication nor the pasted instruction moves a single label.

## 6. Reproducing the pass

From the repository root, with the test split populated:

```
python scripts/make_annotation_workspace.py     # only if annotation/workspace/ is missing
python scripts/build_cases.py
python scripts/validate_cases.py
python scripts/validate_cases.py --strict       # after config/splits.yaml is amended per §3
```

Expected: `compiled 21 dev …` and `valid: 21 dev, …`. Both scripts are cwd-sensitive — run them from the repository root.
