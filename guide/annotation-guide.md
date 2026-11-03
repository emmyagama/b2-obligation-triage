# Annotation guide — obligations from CUAD contracts

**Version:** `1.0.0`
**Status:** `frozen` — issued as `guide-v1.0`. Gold-producing; stamped on every record as `guideline_version` (§11.1).
**Owner and approver:** Emmanuel Agama
**Issued:** 2026-11-02
**Supersedes:** nothing — first issued version.
**Companion file:** `guide/obligation_types.yaml` (the machine-readable list of obligation types). Both files carry the same version number; a mismatch is a build error.
**Basis:** `corpus-report.md` (Phase A, 2026-11-02) — CUAD v1, 510 contracts, 41 labelled categories.
**Change control:** §11.

This guide is the normative rulebook for obligation annotation on this corpus. It binds annotators and the automated pass alike. Where an annotator's judgement and this guide disagree, this guide wins; where the guide is silent, the annotator escalates (§8).

---

## 1. What this guide decides, and what it does not

The guide answers five questions and nothing else:

1. Which of the 41 CUAD categories can produce an obligation (§3).
2. When a piece of contract text is one obligation and when it is two (§4).
3. Who owes it — `provider`, `customer`, `both`, `unclear` (§5).
4. What deadline it carries — `absolute`, `relative`, `recurring`, `none` (§6).
5. When a human has to look at it — `E1`, `E2`, `E3` — and how hard it was — difficulty 1–3 (§7, §8, §9).

Out of scope: whether the contract is good or bad, whether a term is enforceable, and legal advice of any kind. We label duties, not opinions.

### 1.1 Two numbers to keep in mind

From `corpus-report.md` (§5, §6):

- **Expiration Date** is labelled in 413 of 510 contracts and **Effective Date** in 390 of 510. So roughly one contract in five has no stated effective or expiry date. Every relative deadline anchored to those fields will be unresolvable in those contracts. That is a known, expected source of `E3` — not an annotator failure (§6.4).
- **`test.json` (102 contracts) is a clean, disjoint split** of the same 510 contracts with byte-identical `context` strings (§2, §8 of the report). It is the sealed held-out set (D7, §11.3 rule 4): no annotation, no examples, no tuning against it. Everything else = 408 contracts for pilot and iteration.

---

## 2. The one sentence rule

> An obligation is a duty that one identified party owes: to do something, to refrain from something, or to pay something. One duty, one party, one obligation. If we cannot say **who** owes it and **what** they must do, it is not an obligation.

---

## 3. Which categories count as obligations

### 3.1 The inclusion test

A CUAD category is **included** (`include: true`) when a clause of that type normally imposes, on an identified party, a duty to **do**, **refrain**, **pay**, **notify**, **permit**, or **account**. It is **excluded** (`include: false`) when the clause is only descriptive: it names, dates, defines, allocates a forum, sets up mechanics, or grants a bare permission with no corresponding duty.

Three deliberate calls:

- **Consequence and risk terms are included.** Liability caps, uncapped liability, liquidated damages and warranty periods are included even though nobody "performs" them. A cap is a duty of restraint on the party who would otherwise claim more; a liquidated-damages clause is a payment duty triggered by breach. The corpus requires this: `corpus-report.md` §7 shows **Cap On Liability + Uncapped Liability labelled together in 111 contracts**, and conflict review is impossible if both sides of that pair are excluded (D2).
- **Qualifiers of a licence are excluded and folded in.** "Perpetual", "irrevocable", "unlimited use" modify one grant; making each its own obligation would triple-count a single sentence and break §4. They are recorded as `grant_qualifiers` on the `LIC-GRANT` obligation instead (§4.4), and the conflict checker reads them from there (D3).
- **Date and identity fields are excluded but retained as anchors.** Effective Date, Expiration Date, Agreement Date, Parties and Document Name are not obligations, yet relative deadlines depend on them. They stay in the schema as *context fields*, not obligation types.

### 3.2 The table (29 included, 12 excluded)

Codes are stable and never reused. `CUAD n/510` is the number of contracts carrying that label in `CUADv1.json` (report §6) — triage information, not a criterion for inclusion.

| CUAD category | Include | Code | Name | Deadline | Esc |
|---|---|---|---|---|---|
| Document Name | no | `EXC-DOC-NAME` | Document name / exhibit label | none | 0 |
| Parties | no | `EXC-PARTIES` | Parties identification | none | 0 |
| Agreement Date | no | `EXC-DATE-AGREEMENT` | Agreement (signature) date | none | 0 |
| Effective Date | no | `EXC-DATE-EFFECTIVE` | Effective date (anchor field) | none | 0 |
| Expiration Date | no | `EXC-DATE-EXPIRY` | Expiration date (anchor field) | none | 0 |
| Renewal Term | no | `EXC-TERM-RENEWAL` | Renewal-term mechanics | none | 0 |
| Notice Period To Terminate Renewal | **yes** | `TRM-RENEWAL-NOTICE` | Notice to prevent renewal | relative | **1** |
| Governing Law | no | `EXC-GOVERNING-LAW` | Governing law / forum | none | 0 |
| Most Favored Nation | **yes** | `PRC-MFN` | Most-favoured-nation commitment | recurring | **1** |
| Non-Compete | **yes** | `COV-NON-COMPETE` | Non-compete restriction | relative | 0 |
| Exclusivity | **yes** | `COV-EXCLUSIVITY` | Exclusivity / exclusive dealing | relative | 0 |
| No-Solicit Of Customers | **yes** | `COV-NO-SOLICIT-CUSTOMER` | No-solicitation of customers | relative | 0 |
| Competitive Restriction Exception | no | `EXC-COMPETITIVE-EXCEPTION` | Carve-out to a competitive restriction | none | 0 |
| No-Solicit Of Employees | **yes** | `COV-NO-SOLICIT-EMPLOYEE` | No-solicitation of employees | relative | 0 |
| Non-Disparagement | **yes** | `COV-NON-DISPARAGEMENT` | Non-disparagement | relative | 0 |
| Termination For Convenience | **yes** | `TRM-CONVENIENCE` | Termination for convenience | relative | **1** |
| Rofr/Rofo/Rofn | **yes** | `TRM-ROFR-ROFO-ROFN` | Right of first refusal / offer / negotiation | relative | **1** |
| Change Of Control | **yes** | `CTL-CHANGE-OF-CONTROL` | Change-of-control notice / consent | none | **1** |
| Anti-Assignment | **yes** | `CTL-NO-ASSIGNMENT` | No assignment without consent | none | 0 |
| Revenue/Profit Sharing | **yes** | `PAY-REVENUE-SHARE` | Revenue / profit sharing | recurring | **1** |
| Price Restrictions | **yes** | `PAY-PRICE-RESTRICTION` | Price restriction (floor / cap / resale) | recurring | **1** |
| Minimum Commitment | **yes** | `PUR-MINIMUM-COMMITMENT` | Minimum purchase commitment | recurring | **1** |
| Volume Restriction | **yes** | `PUR-VOLUME-RESTRICTION` | Volume restriction | recurring | **1** |
| Ip Ownership Assignment | **yes** | `IP-OWNERSHIP-ASSIGNMENT` | IP ownership assignment | none | 0 |
| Joint Ip Ownership | no | `EXC-IP-JOINT` | Joint IP ownership (allocation) | none | 0 |
| License Grant | **yes** | `LIC-GRANT` | Licence grant (with qualifiers) | none | 0 |
| Non-Transferable License | **yes** | `LIC-NO-TRANSFER` | Non-transferable licence | none | 0 |
| Affiliate License-Licensor | **yes** | `LIC-AFFILIATE-PROVIDER` | Affiliate licence — licensor side | none | 0 |
| Affiliate License-Licensee | **yes** | `LIC-AFFILIATE-CUSTOMER` | Affiliate licence — licensee side | none | 0 |
| Unlimited/All-You-Can-Eat-License | no | `EXC-LICENCE-UNLIMITED` | Unlimited-use licence qualifier | none | 0 |
| Irrevocable Or Perpetual License | no | `EXC-LICENCE-IRREVOCABLE` | Irrevocable / perpetual qualifier | none | 0 |
| Source Code Escrow | **yes** | `LIC-SOURCE-ESCROW` | Source code escrow | recurring | **1** |
| Post-Termination Services | **yes** | `SVC-POST-TERMINATION` | Post-termination / transition services | relative | 0 |
| Audit Rights | **yes** | `CTL-AUDIT-RIGHT` | Audit / inspection rights | recurring | **1** |
| Uncapped Liability | **yes** | `LIA-UNCAPPED` | Uncapped liability / no-cap carve-outs | none | **1** |
| Cap On Liability | **yes** | `LIA-CAP` | Liability cap | none | **1** |
| Liquidated Damages | **yes** | `LIA-LIQUIDATED-DAMAGES` | Liquidated damages | relative | **1** |
| Warranty Duration | **yes** | `WAR-DURATION` | Warranty period | relative | 0 |
| Insurance | **yes** | `INS-COVERAGE` | Insurance to be maintained | recurring | 0 |
| Covenant Not To Sue | **yes** | `COV-NO-SUE` | Covenant not to sue | relative | 0 |
| Third Party Beneficiary | no | `EXC-THIRD-PARTY` | Third-party beneficiary | none | 0 |

Split: **29 included / 12 excluded.** Deadline defaults: **12 relative, 8 recurring, 9 none, 0 absolute.** Escalating by default: **14**.

> **On "0 absolute":** no category defaults to `absolute`, because obligations are nearly always anchored to an event ("within 30 days of delivery") or repeat. `absolute` remains a valid value and is assigned per instance when the clause names a fixed calendar date ("Closing shall occur on 15 March 2026") — see D6, §6.2.

### 3.3 Why each exclusion is excluded

| Excluded category | Why it is not an obligation | What we do with it instead |
|---|---|---|
| Document Name, Parties | Names and identifiers. Nobody owes anything. | Context fields. `Parties` feeds the provider/customer mapping (§5). |
| Agreement Date, Effective Date, Expiration Date | Dates, not duties. | Anchor fields for relative and recurring deadlines (§6). |
| Renewal Term | Describes automatic renewal mechanics. The only duty in that neighbourhood is the notice that stops renewal — and that has its own category. | Anchor (`renewal date`), nothing else. |
| Governing Law | Chooses a forum and a law. No performance. | Context field; may be cited in a conflict note, never as an obligation. |
| Competitive Restriction Exception | A carve-out from a restriction. It narrows a duty, it does not create one. | `exceptions` field on the `COV-NON-COMPETE` / `COV-EXCLUSIVITY` obligation. |
| Joint Ip Ownership | Allocates ownership between the parties (often "each owns an undivided interest and may exploit it"). An allocation, not a duty. If a sentence in it does state a duty (consent, accounting, registration), that sentence is labelled under `IP-OWNERSHIP-ASSIGNMENT`. | Folded; cross-reference `IP-OWNERSHIP-ASSIGNMENT`. |
| Unlimited/All-You-Can-Eat-License, Irrevocable Or Perpetual License | Qualities of one licence grant. Splitting them out double-counts the grant. | `grant_qualifiers: [perpetual, irrevocable, unlimited, ...]` on `LIC-GRANT`. The perpetual/irrevocable qualifier is what the conflict checker uses against `TRM-CONVENIENCE` (§7.3). |
| Third Party Beneficiary | Confers a right on someone who is not a party. No duty runs between provider and customer — and `owed_by` has no value for "a third party". | Context field. If the clause also restricts the parties (e.g. "this section may not be amended without X's consent"), label that restriction under `CTL-NO-ASSIGNMENT` or leave it to `E3`. |

### 3.4 Included, but with a trap

Two included types routinely produce **zero** obligations in practice. An included type can still yield `E1`; inclusion is not a promise that a duty exists.

- **`TRM-CONVENIENCE`** — "Either party may terminate for convenience" is a *permission*. The only duty is the notice the terminating party must give. If no notice requirement and no other duty is stated, emit no obligation and escalate `E1`.
- **`TRM-ROFR-ROFO-ROFN`** — a right of first refusal is a right held by one party and a duty on the other (to offer first). Record the duty (on the grantor), not the right.

---

## 4. One obligation or two

### 4.1 The base rule

> **One clause × one duty × one party = one obligation.** A clause that binds both parties is **two** obligations.

Two different duties in one sentence are two obligations even when they share a subject. Two parties sharing one indivisible duty are **one** obligation with `owed_by: both` (§5.4).

### 4.2 Split when — any one of these is true

1. **Different party.** "Licensor shall deliver the Software and Licensee shall pay the Fees." → 2 (one `provider`, one `customer`).
2. **`each party` / `either party` mutual duty.** "Each party shall keep the other's Confidential Information confidential." → 2, one filed `provider`, one `customer`, same span. This is the explicit rule: *a clause binding both parties is two obligations.*
3. **Different required act.** "Supplier shall deliver the Equipment and shall train Customer's staff." → 2. Delivery and training are separately completable; one can be done and the other not.
4. **Different deadline.** "Supplier shall deliver 100 units by 1 March 2026 and 200 units by 1 May 2026." → 2.
5. **Different trigger or condition.** "Provider shall notify Customer of a Security Incident; Provider shall notify Customer of any Change of Control." → 2. Different events, separately missable.
6. **Different obligation type.** "Supplier shall comply with applicable law and shall maintain the insurance required by Schedule 3." → 2 (a compliance duty and an `INS-COVERAGE` duty).

### 4.3 Do **not** split (these stay one obligation)

- **Lists of synonyms or examples of a single prohibition.** "Licensee shall not sublicense, assign, transfer or otherwise dispose of the Software." → 1 `LIC-NO-TRANSFER`.
- **The same verb, same party, same deadline, several objects.** "Supplier shall comply with the Data Protection Law and the Export Control Laws." → 1 (compliance duty, two objects). Split only if a distinct deadline, remedy or condition attaches to one object.
- **Exceptions and carve-outs.** These go in `exceptions` on the duty they narrow, not into separate records — this is where the excluded `EXC-COMPETITIVE-EXCEPTION` category lands.
- **Efforts standards, purposes and consequences of the same duty.** "shall use commercially reasonable efforts to …" is a qualifier on the duty (`efforts_standard: commercially_reasonable`), not a second duty. A liquidated-damages figure attached to a delivery duty is recorded on the duty as `consequence` *and* as a separate `LIA-LIQUIDATED-DAMAGES` payment obligation only if it is drafted as a stand-alone payment obligation payable by an identified party.
- **Recitals, definitions, purpose statements, headings.** → zero obligations; escalate `E1` only if a reviewer would expect a duty there.
- **Scope qualifiers of a grant** (§3.3).

### 4.4 Worked examples

| Span (illustrative, invented) | Obligations | Why |
|---|---|---|
| "Licensor hereby grants Licensee a perpetual, irrevocable, worldwide, royalty-free licence to use the Software." | **1** — `LIC-GRANT`, `owed_by: provider`, `grant_qualifiers: [perpetual, irrevocable, worldwide, royalty_free]` | One grant, one grantor. Qualifiers are attributes. |
| "Licensor grants the licence in Section 2.1 and Licensee shall pay the Fees within 30 days of each invoice." | **2** — `LIC-GRANT` (provider) + a `PAY-*` payment duty (customer, recurring) | Different parties, different acts. |
| "Either party may terminate this Agreement on sixty (60) days' written notice." | **2** — one `TRM-CONVENIENCE` obligation filed `provider`, one filed `customer`, both `relative`, deadline "60 days before the termination date" | Text binds both parties ⇒ two. |
| "The parties shall jointly appoint an independent expert to resolve the dispute." | **1** — `owed_by: both` | Indivisible joint act; neither party can perform it alone. |
| "The parties shall each bear their own costs." | **2** | Two separate duties that happen to be symmetrical. |
| "Supplier shall maintain the insurance specified in Schedule 3 and shall provide certificates of insurance annually." | **2** — both `INS-COVERAGE`, one `relative`/`none`, one `recurring` | Different acts, different deadlines. |
| "This Agreement shall automatically renew for successive one-year terms unless either party notifies the other at least 90 days before the end of the then-current term." | **2** — `TRM-RENEWAL-NOTICE`, one per party, `relative` | Two parties, two duties. `EXC-TERM-RENEWAL` produces nothing. |
| "Customer may not disclose Confidential Information, and shall return it on termination." | **2** — confidentiality duty (`none` if no period stated) and return duty (`relative`, anchored to termination) | Different acts and deadline types. |

### 4.5 What is required to score a consequence

A consequence (penalty, damages, termination right, price adjustment) can only be scored if the obligation it attaches to is **pinned to text**. Each obligation record therefore carries:

- `span_start`, `span_end` — character offsets into `paragraphs[0].context`, plus `quote` verbatim.
- `code`, `owed_by`, `deadline_behaviour`, `deadline_text` (verbatim), `anchor` (+ `anchor_resolved`), `escalation`, `difficulty`.

Validation is mandatory and cheap: `context[span_start:span_end] == quote`. `corpus-report.md` §8 confirms this holds for CUAD answers (30/30 offsets pass; `context` strings are byte-identical across all three files). An obligation whose span fails that slice check is rejected, not repaired by hand.

---

## 5. Party mapping (`owed_by`)

### 5.1 The mapping

**Licensor = `provider`. Licensee = `customer`.** Then, by role in the exchange (not by the word used):

| `owed_by` | Roles |
|---|---|
| `provider` | licensor, seller, supplier, vendor, service provider, contractor, developer, consultant, lessor, disclosing party (of know-how/software), assignor of IP |
| `customer` | licensee, buyer, purchaser, customer, client, end user, recipient, distributor, reseller, lessee, receiving party |
| `both` | a single indivisible joint duty (see §5.4) |
| `unclear` | cannot be determined from the contract text (see §5.5) |

### 5.2 Map the duty, not the party name

`owed_by` is decided **per obligation**, not per contract. In a cross-licence, the same company is `provider` under one obligation and `customer` under the next. Distributors and resellers are `customer`: they buy/receive from the provider in this contract even though they resell downstream. If a contract has no licence at all (supply, consulting, sponsorship), `provider` = the side that supplies or performs, `customer` = the side that pays or receives.

### 5.3 `owed_by` is who must perform, not who benefits

A liability cap benefits one party and restrains the other. Record the **restrained** party (the one who cannot claim above the cap) as the one who owes the duty of restraint. Where a cap is mutual, `owed_by: both`.

### 5.4 `both` is narrow

Use `both` **only** when the duty is genuinely indivisible — one act that requires both parties ("the parties shall jointly appoint…", "the parties shall enter into a novation in the agreed form") — or when the drafting imposes a single duty on the parties collectively with no way to attribute shares (D4).

**Never** use `both` as a shortcut for "it binds each party". That case is two obligations, one `provider` and one `customer` (§4.2 rule 2). This is the single most likely place for annotators to drift, so it carries its own check in the pilot.

### 5.5 `unclear`

Use `unclear` when the text genuinely does not say: a passive construction with an unnamed actor ("notice shall be given within 30 days"), a duty on an affiliate or subcontractor that is not a signatory, a duty on "the receiving party" where roles swap across clauses, or two readings that survive a careful re-read. If you resolve it by inference from context and you are confident, use the resolved value and note the inference; if the inference is doing real work, escalate `E3` **and** use `unclear`.

`intake_party` (the wider upstream schema enum) is untouched by this: `owed_by` is the narrower gold enum `provider | customer | both | unclear`.

---

## 6. Deadlines

### 6.1 The four values

| Value | Means | Example (invented) | What we store |
|---|---|---|---|
| `absolute` | A single deadline fixed on the calendar, not computed from anything. | "Closing shall occur on 15 March 2026." | `deadline_text`, `due_date: 2026-03-15`, `anchor: null` |
| `relative` | A single deadline computed from an anchor event or date. | "45 days counted from the effective date" | `deadline_text`, `anchor: effective_date`, `anchor_offset_days: 45`, `due_date` (only if resolvable) |
| `recurring` | A duty that repeats each period or per instance. | "due each quarter, on day 15" | `deadline_text`, `period: quarterly`, `anchor_offset_days: 15`, `due_date: null` |
| `none` | No time element at all. | "Provider shall keep the Confidential Information secret." | `deadline_text: null` |

### 6.2 Priority when a clause fits two

1. **Recurring beats relative** if the trigger happens more than once, even though each instance has its own computed date. "Pay each invoice within 30 days" is `recurring`, not `relative`; the 30 days goes in `deadline_text`, the repeat in `period`.
2. **Absolute beats relative** only when the date is literally written on the calendar *and* the duty happens once. "File the application by 31 December 2026" is `absolute`, even though the agreement has an effective date.
3. If neither, and there is no time element, `none`.

The `deadline_behaviour` in `obligation_types.yaml` is a **default prior**, not a straitjacket: it states what that type usually is, drives consistency checks and sampling, and is overridden per instance when the clause differs. An override must be recorded (`deadline_behaviour_override: true`) so we can see which defaults are wrong.

### 6.3 Anchors

Allowed anchors: contract fields (`effective_date`, `expiration_date`, `agreement_date`, `renewal_date`), events in the contract (`delivery`, `acceptance`, `invoice_date`, `receipt`, `termination_notice`, `termination`, `breach`, `change_of_control`), or `unresolved`.

Rules:
- Store the anchor **and** the offset. Never store only a computed date — a wrong anchor then becomes invisible.
- Verbatim `deadline_text` is mandatory whenever any time language exists ("within thirty (30) days", "promptly", "as soon as reasonably practicable"). Do not paraphrase.
- "Promptly", "as soon as practicable", "commercially reasonable efforts" are **not** deadlines. Record `deadline_behaviour: none` with `time_standard: promptly` and note it in `notes`.

### 6.4 When the anchor cannot be resolved

This is expected, not exceptional: `corpus-report.md` shows Effective Date missing in 120/510 contracts and Expiration Date in 97/510.

> If the anchor is not stated in the contract text, keep `deadline_behaviour: relative`, set `anchor: unresolved`, `anchor_resolved: false`, leave `due_date: null`, and escalate **`E3`**. Do **not** drop the obligation, and do **not** guess a date from context outside the contract.

A deadline that is only resolvable by reading a second clause elsewhere in the contract is fine (resolve it), but record `anchor_clause_ref` so the resolution is auditable — and mark difficulty 2 (§9).

---

## 7. Genuine conflict (`E2`)

### 7.1 Definition

> **A genuine conflict is two clauses that cannot both be performed** — two duties, or a duty and a term modifying it, that no single course of conduct can satisfy at the same time, for the same party, in the same period.

Four conditions, all required:

1. **Two operative spans** — both in the operative text, not recitals or purpose clauses.
2. **Same subject matter and same party** — the incompatibility must bite on one party's behaviour.
3. **Overlapping scope** — same object, same people, same time window. A restriction during the term and one after it do not overlap.
4. **No reconciliation available** — nothing in the contract orders them: "subject to", "notwithstanding", "except as provided in", "to the extent permitted by", schedule-precedence language, specific-over-general structure, or a carve-out that makes both satisfiable.

### 7.2 What is *not* a conflict

- **Two clauses that coexist with different content.** A $1M general cap plus uncapped liability for IP infringement is not a conflict; the carve-out makes them compatible. Most of CUAD's 111 `Cap + Uncapped` co-occurrences are exactly this.
- **Different parties.** A duty on each party to indemnify the other is not a conflict.
- **One clause stricter than the other**, where the stricter one can be obeyed without breaking the looser one.
- **Gap or silence.** Clause A imposes a duty, and the contract says nothing else. Silence is not a conflict — at most an `E3` if the gap makes the duty unworkable.
- **Co-occurrence.** CUAD is multi-label; two labels in one contract is normal. Report §7's counts are **candidates for checking, not conflicts found.**
- **Two readings of one clause.** Intra-clause incompatibility is `E3` ambiguity, not `E2`. `E2` needs two spans.

### 7.3 Pairs to check (from the corpus, report §7)

| Pair | Contracts with both labels | Genuine conflict only if… |
|---|---|---|
| `LIA-CAP` + `LIA-UNCAPPED` | 111 / 510 | the same liability, for the same party, is capped and expressly uncapped, with no carve-out exempting it |
| `EXC-LICENCE-IRREVOCABLE` (qualifier on `LIC-GRANT`) + `TRM-CONVENIENCE` | 40 / 510 | the licence is perpetual/irrevocable and the licensor may terminate for convenience without a carve-out for the licensed rights |
| `COV-NON-COMPETE` + `COV-EXCLUSIVITY` | 68 / 510 | one clause requires the party to deal exclusively with X while the other forbids dealing in that market at all, and no exception category reconciles them |

Any other conflicting pair may be flagged — these three are the ones the corpus says occur often enough to justify a standing checklist.

### 7.4 Evidence required for `E2`

Both spans (offsets + verbatim), the party, the duty each imposes, one sentence on **why no single course of conduct satisfies both**, and the reconciliation attempted and rejected. Attach the same `conflict_pair_id` to both obligation records. `E2` is a property of the **pair**, so it appears on both halves.

---

## 8. When to escalate

Escalation is a **defect class**, not a difficulty rating. One primary code per obligation (per pair for `E2`); secondary observations go in `notes`.

### 8.1 The three codes

| Code | Name | Use when | Evidence required | Do **not** use for |
|---|---|---|---|---|
| **E1** | **No obligation** | The span or category under examination yields **zero** duties: a bare permission, a recital, a definition, a remedy with no duty attached, or an empty/absent clause. A null is a positive claim and must be confirmed by a human. | The quote or the searched category; which categories were checked; the reason it is not a duty (permission / description / definition / allocation / absence). | Getting out of a hard call. "I could not decide" is `E3`, not `E1`. |
| **E2** | **Conflict** | Two operative clauses cannot both be performed (§7). | Both spans, both duties, one party, the failed reconciliation attempt. | Two clauses that merely differ; intra-clause tension; a strict-plus-loose pair. |
| **E3** | **Conditional or ambiguous** | The duty's existence, party, scope, object or deadline anchor cannot be settled from the contract text: an unresolved anchor, an undefined term that changes the duty, two surviving readings, a condition whose satisfaction decides whether a duty exists at all, or an unattributable actor. | The ambiguous text verbatim; the competing readings; which resolution would change the label; the specific field left null. | Routine conditionality (below). Ordinary drafting complexity. Length. |

### 8.2 Routine conditionality is **not** `E3`

This is the biggest false-positive risk. "Payment due within 30 days of invoice", "if Customer requests transition services, Provider shall provide them", "escrow releases on Provider insolvency" — all conditional, all normal, all resolvable from the contract **without judgement**. Those are difficulty 2, not escalations.

Escalate only when the condition changes **whether a duty exists / who owes it / what it covers**, and the contract does not tell you.

### 8.3 Precedence

If more than one code applies to one record: **`E2` > `E1` > `E3`**. Note the others in `notes`. Do not stack codes on one record — stacked codes destroy the agreement statistics.

### 8.4 Escalate by default

`escalates_by_default: 1` in `obligation_types.yaml` (14 of the 29 included types) means: *queue every instance of this type for human confirmation even when the automated pass is confident*, because the type is defined by a threshold, a comparison, or a schedule that goes wrong often — MFN, revenue share, price restrictions, minimum commitment, volume restriction, liquidated damages, caps and uncapped liability, change of control, ROFR/ROFO/ROFN, escrow, audit, renewal notice, termination for convenience (D5).

It does not block the pass and it does not make `E3` mandatory; it sets review priority. Priority order when capacity is limited: (1) `LIA-*` and `TRM-*`, (2) `PAY-*` and `PUR-*`, (3) everything else.

---

## 9. Difficulty (1–3)

Difficulty is **how much work it took**, per obligation. It is orthogonal to escalation: a trivial clause can be `E2`, and a hard clause can be perfectly clean.

| Score | Name | The obligation qualifies if… |
|---|---|---|
| **1** | Trivial | One party, one duty, one sentence, explicit modal ("shall" / "shall not"). Deadline absolute or absent, or the anchor is stated in the same sentence. No conditions, no exceptions, no cross-references, `owed_by` obvious without a role table, no conflict candidate. |
| **2** | Ordinary | Needs one step of resolution: an anchor from another clause or a document field (Effective Date, invoice date); one routine condition or exception that does not change whether the duty exists; two parties in the span that split cleanly; a role that needs the §5 table; or a deadline that needs computing. |
| **3** | Hard | Any of: the duty's existence depends on a condition that cannot be resolved; competing readings survive; the anchor is unresolved; the party is unattributable; the span mixes several duties and the split itself is the judgement; the clause is drafted as a right and the annotator must decide whether a duty exists at all; or there is a conflict candidate. |

Rules:
- Difficulty is assigned **per obligation**, never per contract or per category.
- **Every `E2` pair and every `E3` obligation is at least difficulty 2**; in practice most are 3. Every difficulty-3 obligation carries a note saying which criterion fired.
- **A difficulty-3 obligation must be escalated** (`E2` or `E3`) unless the only driver is span length — in which case say so in `notes`.
- Pilot sampling must include **≥25 % difficulty-3**, or the hard cases never get examined before the production run.

---

## 10. Record shape (so the guide and the build agree)

One obligation record:

```
obligation_id, contract_id (CUAD title), category (exact CUAD string), code,
owed_by, obligation_class, span_start, span_end, quote,
deadline_behaviour, deadline_text, anchor, anchor_offset_days, anchor_resolved, due_date,
period, grant_qualifiers[], exceptions[], consequence_ref,
escalation, difficulty, annotator, guideline_version, notes
```

Category strings are used **exactly** as they appear in CUAD (report §3 — all 41 identical across the three files, no normalisation, no case changes). An obligation's `category` is the CUAD label that surfaced the span; its `code` is our obligation type. The mapping between them lives in `obligation_types.yaml` and is total: every obligation's `code` has `include: true` in the YAML, no exceptions.

`guideline_version` on every record reads `1.0.0`. A record stamped with any other value is not gold.

---

## 11. Change control

### 11.1 Status values

`status` is a single value, carried in `meta.status` in the YAML and in the header line of this file. Two values are gold-producing and only these two may be stamped on a record:

| Status | Means | Who may set it | Version shape |
|---|---|---|---|
| `frozen` | Issued and closed to text change. Gold-producing. Stamped on every record as `guideline_version`. | Emmanuel only | `1.0.0` and up, no suffix |
| `amended` | A frozen guide that has since had an errata-driven bump. Records produced before the bump are disclosed as pre-bump. | Emmanuel only | `x.y.z` with a changelog row |

Any version carrying a suffix (`-rc` or otherwise) is pre-issue and is **never** gold.

### 11.2 What bumps the version

Version format is `MAJOR.MINOR.PATCH`. Issued versions carry no suffix. Every bump gets a §13 changelog row, and both files carry the new number in the same commit.

| Edit class | Examples | Bump |
|---|---|---|
| **PATCH** — wording only, no behaviour change | typos, broken cross-references, clearer phrasing that cannot change a label, added non-normative examples | `1.0.0` → `1.0.1` |
| **MINOR** — rule or schema addition, nothing existing redefined | changing one type's `include` / `deadline_behaviour` / `escalates_by_default`, adding a `code`, adding a conflict pair, adding a field | `1.0.1` → `1.1.0` |
| **MAJOR** — semantic change that invalidates earlier labels | redefining `both`, changing the one-vs-two rule, renaming or reusing a `code`, changing what `include` means | `1.1.0` → `2.0.0` |
| **RE-ISSUE** | a new guide replacing this one | status returns to `frozen` under the new number, tag `guide-v<MAJOR>.<MINOR>` |

Two points that matter in practice:

- **The guide is frozen; the run is gated.** This document is closed to text change at `1.0.0`. What remains gated is the *run*: no production run begins until the pilot, the double annotation and the agreement targets (§11.3 rules 4–6) are met and recorded. Issuing the guide does not certify a run.
- **`MAJOR` is not drama.** Codes are stable identifiers: renaming `COV-NO-SUE` is a MAJOR bump even if the rule reads the same, because every previously labelled record would point at a code that no longer means what it meant.

### 11.3 Rules

1. **Version format** `MAJOR.MINOR.PATCH`. This file is `1.0.0`. The YAML carries the same version in `meta.version`.
2. **Issue and freeze.** Issued as `guide-v1.0` on 2026-11-02 with D1–D7 resolved (§12). The text does not change during a run. Run gate: no production run begins until the pilot of 40 contracts is double-annotated and adjudicated and the targets in rule 6 are met.
3. **Errors after issue** are handled by an errata log and a **version bump**, never by silently editing rules: log the error class, bump `PATCH` (clarification) or `MINOR` (rule change), re-run the affected slice, and **disclose** that the slice was re-run. Nothing is ever edited in the held-out set after results are seen — that is the one non-negotiable rule.
4. **Held-out discipline.** `test.json`'s 102 contracts are sealed (report §2: disjoint titles, byte-identical context). No development, no examples, no tuning against them.
5. **Double annotation.** ≥10 % of the pilot, stratified so all 29 included codes and all escalation codes appear at least twice.
6. **Agreement targets.** Held for the pilot; revised only by errata (§11.2 PATCH) once the pilot reports: `owed_by` agreement ≥ 0.80; span overlap F1 ≥ 0.85; obligation-count agreement within ±1 per contract ≥ 0.85; escalation-code κ ≥ 0.70. Report the numbers even when they miss.
7. **Adjudication.** Emmanuel adjudicates; the adjudicated record is gold; the disagreement itself is kept, because the disagreement pattern is what identifies a badly written rule.
8. **Per-clause traceability.** Because CUAD spans are verified character offsets (report §8), every gold obligation must survive `context[span_start:span_end] == quote` on build. Failing records are rejected, and rejection rate is a reported metric.
9. **Derived numbers travel together.** The counts in §3.2 (29/12, 12 relative / 8 recurring / 9 none, 14 escalating) are also in `meta.counts` and `summary` in the YAML. Any content edit updates all of them in the same commit, or the pair is inconsistent.

---

## 12. Decisions of record

Resolved at issue; these bind the guide.

| ID | Decision | Resolution as issued |
|---|---|---|
| **D1** | Rights as obligations | A right is an obligation only where it implies a duty on the other party (ROFR ⇒ duty to offer). A bare permission yields no obligation and is escalated `E1`. Governs `TRM-CONVENIENCE`, `TRM-ROFR-ROFO-ROFN` (§3.4). |
| **D2** | Liability caps and uncapped liability | In scope, as `risk_allocation` types (§3.1). They are the corpus's most frequent conflict pair (111 contracts); excluding them makes `E2` undetectable there. Accepted consequence: `owed_by` for a cap is the restrained party (§5.3). |
| **D3** | Licence qualifiers | Folded into `LIC-GRANT` as `grant_qualifiers`, never counted as separate obligations (§3.3, §4.4). The perpetual-vs-termination conflict is detected from the qualifier field (§7.3). |
| **D4** | Meaning of `both` | `both` is reserved for indivisible joint duties. Drafting that binds each party separately is two obligations, `provider` and `customer` (§4.2 rule 2, §5.4). |
| **D5** | Default escalations | All 14 types with `escalates_by_default: 1` stand. Review priority: `LIA-*` and `TRM-*`, then `PAY-*` and `PUR-*`, then the rest (§8.4). If review capacity is constrained, the cut order is `CTL-AUDIT-RIGHT`, `TRM-CONVENIENCE`, `LIC-SOURCE-ESCROW`, `CTL-CHANGE-OF-CONTROL`. |
| **D6** | Empty `absolute` default | Retained: no type defaults to `absolute`; `absolute` is assigned per instance when a fixed calendar date is stated (§3.2 note, §6.2). |
| **D7** | Held-out set | `test.json` (102 contracts, disjoint, byte-identical context) is the sealed held-out set (§11.3 rule 4). |

---

## 13. Changelog

| Version | Date | Change |
|---|---|---|
| `1.0.0` | 2026-11-02 | Issued and frozen as `guide-v1.0`. D1–D7 resolved and recorded (§12). No rule, type, code or count changed from the reviewed text: 29 included / 12 excluded of 41 CUAD categories; 12 relative / 8 recurring / 9 none; 14 escalating by default. |

---

## 14. Approval

| | |
|---|---|
| Owner and approver | Emmanuel Agama |
| Date | 2026-11-02 |
| Next review | After the pilot reports (§11.3 rules 4–6) |

*End of guide, version `1.0.0`. Companion taxonomy: `guide/obligation_types.yaml`, version `1.0.0`.*
