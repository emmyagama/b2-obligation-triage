# CUAD corpus report (facts only)

Generated: 2026-11-02 by Phase A of the B2 handoff. No opinions, no recommendations, no selection judgement — facts about the downloaded files only.

## 0. Provenance

| Fact | Value |
|---|---|
| URL given in brief | `https://github.com/TheAtticusProject/cuad` (HTTP 301 → `https://github.com/The-Atticus-Project/cuad`) |
| Download URL actually used | `https://raw.githubusercontent.com/The-Atticus-Project/cuad/main/data.zip` |
| Why the URL differs | the repository was renamed to `The-Atticus-Project` and the default branch is `main`, not `master`; `.../TheAtticusProject/cuad/raw/master/data.zip` and `.../The-Atticus-Project/cuad/raw/master/data.zip` both return 404 (the latter served a 231,223-byte GitHub HTML page) |
| Date downloaded | 2026-11-02 |
| `data.zip` sha256 | `F8161D18BEA4E9C05E78FA6DDA61C19C846FB8087EA969C172753BC2F45B999A` |
| `data.zip` size | 18,309,308 bytes (ZIP magic `50 4B 03 04`) |
| Local path | `data/cuad/` (gitignored) |
| Other files in the source repository (not in `data.zip`) | `category_descriptions.csv` 8,987 B, `contract_review.png` 324,025 B, `evaluate.py` 7,132 B, `readme.md` 2,140 B, `run.sh` 668 B, `scrape.py` 5,480 B, `train.py` 36,664 B, `utils.py` 24,502 B (listing read 2026-11-02 from `api.github.com/repos/The-Atticus-Project/cuad/contents/`) |

## 1. Directory tree (depth 3, file counts and sizes)

```
data/cuad/
|-- CUADv1.json                    (1 file, 40,128,638 bytes)
|-- data.zip                       (1 file, 18,309,308 bytes)
|-- test.json                      (1 file, 7,378,232 bytes)
`-- train_separate_questions.json  (1 file, 35,065,844 bytes)
```

Extracted tree contains exactly 3 JSON files plus the archive; no subdirectories, no PDFs, no per-contract filenames.

## 2. Data files: format, fields, trimmed sample record

All three files have the same SQuAD-style shape:

```
{"version": "aok_v1.0", "data": [ {"title": str, "paragraphs": [ {"context": str, "qas": [
    {"id": str, "question": str, "is_impossible": bool,
     "answers": [{"text": str, "answer_start": int}]} ]} ]} ] }
```

| File | `version` | records (`data`) | paragraphs | QAs | QAs per record |
|---|---|---|---|---|---|
| `CUADv1.json` | `aok_v1.0` | 510 | 510 | 20,910 | 41 (all records) |
| `test.json` | `aok_v1.0` | 102 | 102 | 4,182 | 41 (all records) |
| `train_separate_questions.json` | `aok_v1.0` | 408 | 408 | 22,450 | 37–160 (several questions per category) |

Top-level field names: `version`, `data`. Record fields: `title`, `paragraphs`. Paragraph fields: `context`, `qas`. QA fields: `id`, `question`, `is_impossible`, `answers`. Answer fields: `text`, `answer_start`.

Title sets: `CUADv1.json` titles = `train_separate_questions.json` ∪ `test.json` (408 + 102 = 510, intersection 0). For every title present in more than one file the `context` strings are byte-identical (510/510 identical, 0 differing).

### Trimmed sample records (contract text ≤ 500 characters)

**`CUADv1.json`** — title: `LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT`, 1 paragraph, 41 QAs; first QA id `LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT__Document Name`, question `Highlight the parts (if any) of this contract related to "Document Name" that should be reviewed by a lawyer. Details: The name of the contract`, answer `{"text": "DISTRIBUTOR AGREEMENT", "answer_start": 44}`; `context[:500]`:

```
EXHIBIT 10.6

                              DISTRIBUTOR AGREEMENT

         THIS  DISTRIBUTOR  AGREEMENT (the  "Agreement")  is made by and between Electric City Corp.,  a Delaware  corporation  ("Company")  and Electric City of Illinois LLC ("Distributor") this 7th day of September, 1999.

                                    RECITALS

         A. The  Company's  Business.  The Company is  presently  engaged in the business  of selling an energy  efficiency  device,  which is  referred to as an 
```

**`test.json`** — title: `LohaCompanyltd_20191209_F-1_EX-10.16_11917878_EX-10.16_Supply Agreement`, 1 paragraph, 41 QAs; first QA id `..._Supply Agreement__Document Name`, answer `{"text": "SUPPLY CONTRACT", "answer_start": 14}`; `context[:500]`:

```
Exhibit 10.16 SUPPLY CONTRACT Contract No: Date: The buyer/End-User: Shenzhen LOHAS Supply Chain Management Co., Ltd. ADD: Tel No. : Fax No. : The seller: ADD: The Contract is concluded and signed by the Buyer and Seller on , in Hong Kong. 1. General provisions 1.1 This is a framework agreement, the terms and conditions are applied to all purchase orders which signed by this agreement (hereinafter referred to as the "order"). 1.2 If the provisions of the agreement are inconsistent with the order
```

**`train_separate_questions.json`** — title: `LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT`, 1 paragraph, 68 QAs; first QA id `..._DISTRIBUTOR AGREEMENT__Document Name_0`; question and answer identical to the `CUADv1.json` entry above; `context[:500]` identical to the `CUADv1.json` sample.

## 3. Exact category strings (41), as they appear

The category string appears inside the double quotes of every question (`related to "<category>"`) and as the QA-id suffix after `__`. The 41 strings are identical in all three files (union = 41; no file-specific strings). Order as it appears in the first contract of `CUADv1.json`:

1. Document Name
2. Parties
3. Agreement Date
4. Effective Date
5. Expiration Date
6. Renewal Term
7. Notice Period To Terminate Renewal
8. Governing Law
9. Most Favored Nation
10. Non-Compete
11. Exclusivity
12. No-Solicit Of Customers
13. Competitive Restriction Exception
14. No-Solicit Of Employees
15. Non-Disparagement
16. Termination For Convenience
17. Rofr/Rofo/Rofn
18. Change Of Control
19. Anti-Assignment
20. Revenue/Profit Sharing
21. Price Restrictions
22. Minimum Commitment
23. Volume Restriction
24. Ip Ownership Assignment
25. Joint Ip Ownership
26. License Grant
27. Non-Transferable License
28. Affiliate License-Licensor
29. Affiliate License-Licensee
30. Unlimited/All-You-Can-Eat-License
31. Irrevocable Or Perpetual License
32. Source Code Escrow
33. Post-Termination Services
34. Audit Rights
35. Uncapped Liability
36. Cap On Liability
37. Liquidated Damages
38. Warranty Duration
39. Insurance
40. Covenant Not To Sue
41. Third Party Beneficiary

Question template (identical wording for every category): `Highlight the parts (if any) of this contract related to "<category>" that should be reviewed by a lawyer. Details: <one-line description of the category>`.

## 4. How the title encodes the family

There are no per-contract filenames — a contract's only identifier is the `title` field. Two title shapes occur:

- `COMPANY_MM_DD_YYYY-EX-<id>-<FAMILY NAME>` (e.g. `ACCURAYINC_09_01_2010-EX-10.31-DISTRIBUTOR AGREEMENT`)
- `Company_YYYYMMDD_Form_EX-<id>_<numeric>_EX-<id>_<Family Name>` (e.g. `AgapeAtpCorp_20191202_10-KA_EX-10.1_11911128_EX-10.1_Supply Agreement`)
- free-form, no `EX-` marker (e.g. `MetLife, Inc. - Remarketing Agreement`)

**Derivable rule:** family = the substring after the **last** match of the regular expression `EX-[\w.()]+[-_]` in the title.

Rule statistics over the 510 unique titles:

- parsed: 470 / 510
- not parsed: 40 / 510
- distinct parsed family strings (case-sensitive): 250, of which 200 occur exactly once
- distinct parsed family strings after lower-casing (over all 1,020 records): 238; case variants exist (e.g. `STRATEGIC ALLIANCE AGREEMENT` and `Strategic Alliance Agreement`)
- the parsed string still carries exhibit-id noise in some titles (e.g. `10.1_Development Agreement`, `10.9_Content License Agreement`)

Family strings occurring on 2 or more of the 510 unique titles (count, family string):

```
2  '10.18_Development Agreement'
2  '10.1_Content License Agreement'
6  '10.1_Development Agreement'
4  '10.1_Endorsement Agreement'
2  '10.1_Franchise Agreement1'
2  '10.1_Franchise Agreement3'
3  '10.1_Promotion Agreement'
3  '10.1_Reseller Agreement'
3  '10.1_Sponsorship Agreement'
2  '10.1_Supply Agreement'
2  '10.2_Co-Branding Agreement'
2  '10.2_Content License Agreement'
2  '10.2_Distributor Agreement'
2  '10.4_Co-Branding Agreement'
2  '10.5_License Agreement'
2  '10.5_Trademark License Agreement'
3  '10.9_Content License Agreement'
2  '10_Affiliate Agreement'
10  'AGENCY AGREEMENT'
7  'COLLABORATION AGREEMENT'
2  'CONSTRUCTION AND MAINTENANCE AGREEMENT'
9  'CONSULTING AGREEMENT'
10  'COOPERATION AGREEMENT'
3  'Collaboration Agreement'
2  'Cooperation Agreement'
2  'DEVELOPMENT AGREEMENT'
13  'DISTRIBUTOR AGREEMENT'
9  'ENDORSEMENT AGREEMENT'
6  'FRANCHISE AGREEMENT'
9  'INTELLECTUAL PROPERTY AGREEMENT'
12  'JOINT FILING AGREEMENT'
9  'JOINT VENTURE AGREEMENT'
3  'LICENSE AND HOSTING AGREEMENT'
4  'MAINTENANCE AGREEMENT'
2  'OPERATIONS AND MAINTENANCE AGREEMENT'
12  'OUTSOURCING AGREEMENT'
5  'PROMOTION AGREEMENT'
5  'RESELLER AGREEMENT'
8  'SERVICE AGREEMENT'
3  'SERVICES AGREEMENT'
2  'SERVICING AGREEMENT'
3  'SOFTWARE LICENSE AND MAINTENANCE AGREEMENT'
23  'SPONSORSHIP AGREEMENT'
23  'STRATEGIC ALLIANCE AGREEMENT'
10  'SUPPLY AGREEMENT'
2  'Sponsorship Agreement'
8  'Strategic Alliance Agreement'
3  'TRANSPORTATION CONTRACT'
3  'TRANSPORTATION SERVICES AGREEMENT'
2  'UNCONDITIONAL CAPITAL MAINTENANCE AGREEMENT'
```

(Note: the table is case-sensitive; `Collaboration Agreement`, `Cooperation Agreement`, `Sponsorship Agreement` and `Strategic Alliance Agreement` are separate raw strings from their upper-case twins. The full machine-generated list of all 250 parsed strings with counts was produced by the Phase A analysis script.)

The remaining 200 parsed family strings occur exactly once each.

25 sample titles where the rule yields nothing (40 in total):

```
PACIRA PHARMACEUTICALS, INC. - A_R STRATEGIC LICENSING, DISTRIBUTION AND MARKETING AGREEMENT
MetLife, Inc. - Remarketing Agreement
IntegrityFunds_20200121_485BPOS_EX-99.E UNDR CONTR_11948727_EX-99.E UNDR CONTR_Service Agreement
MSCIINC_02_28_2008-EX-10.10-
Zounds Hearing, Inc. - MANUFACTURING DESIGN MARKETING AGREEMENT
Principal Life Insurance Company - Broker Dealer Marketing and Servicing Agreement
FEDERATEDGOVERNMENTINCOMESECURITIESINC_04_28_2020-EX-99.SERV AGREE-SERVICES AGREEMENT_SECONDAMENDMENT
Antares Pharma, Inc. - Manufacturing Agreement
ELECTRAMECCANICA VEHICLES CORP. - Manufacturing Agreement
Columbia Laboratories, (Bermuda) Ltd. - AMEND NO. 2 TO MANUFACTURING AND SUPPLY AGREEMENT
NUVEEN - REMARKETING AGREEMENT
SightLife Surgical, Inc. - STRATEGIC SALES _ MARKETING AGREEMENT
VIVINT SOLAR, INC. - NON-COMPETITION AGREEMENT
FEDERATEDGOVERNMENTINCOMESECURITIESINC_04_28_2020-EX-99.SERV AGREE-SERVICES AGREEMENT
Magenta Therapeutics, Inc. - Master Development and Manufacturing Agreement
WESTERN COPPER - NON-COMPETITION AGREEMENT
LECLANCHÉ S.A. - JOINT DEVELOPMENT AND MARKETING AGREEMENT
HEMISPHERX - Sales, Marketing, Distribution, and Supply Agreement
Sonos, Inc. - Manufacturing Agreement
VAPOTHERM, INC. - Manufacturing and Supply Agreement
GWG HOLDINGS, INC. - ORDERLY MARKETING AGREEMENT
XACCT Technologies, Inc.SUPPORT AND MAINTENANCE AGREEMENT
Apollo Endosurgery - Manufacturing and Supply Agreement
Quaker Chemical Corporation - NON COMPETITION AND NON SOLICITATION AGREEMENT
Array BioPharma Inc. - LICENSE, DEVELOPMENT AND COMMERCIALIZATION AGREEMENT
```

The other 15 unparsed titles include the four `FEDERATEDGOVERNMENTINCOMESECURITIESINC_...` variants, three `ClickstreamCorp/EmeraldHealthBioceuticalsInc/GentechHoldingsInc_..._EX1A-6 MAT CTRCT_...` titles, `ADMA BioManufacturing, LLC -  Amendment #3 to Manufacturing Agreement`, `Apollo Endosurgery`-style `Company - <family>` titles without `EX-`, and `Cerus Corporation - FIRST AMEND TO SUPPLY AND MANUFACTURING AGREEMENT`.

## 5. Per-contract character counts (the `context` field)

| File | n | min | median | max | mean | total |
|---|---|---|---|---|---|---|
| `CUADv1.json` | 510 | 645 | 33,143 | 338,211 | 52,563 | 26,807,133 |
| `test.json` | 102 | 645 | 25,657 | 300,768 | 46,848 | 4,778,515 |
| `train_separate_questions.json` | 408 | 1,081 | 35,960 | 338,211 | 53,991 | 22,028,618 |

Contracts with a non-empty label (at least one answer with non-blank `text`) for the date categories:

| File | Effective Date | Expiration Date |
|---|---|---|
| `CUADv1.json` | 390 / 510 | 413 / 510 |
| `test.json` | 70 / 102 | 78 / 102 |
| `train_separate_questions.json` | 363 / 408 | 384 / 408 |

## 6. Label count per category

Counts are `contracts (or questions, for the train file) with ≥1 non-empty answer` / `total questions for that category`.

### `CUADv1.json` (denominator 510 for every category)

| Category | Non-empty / total |
|---|---|
| Affiliate License-Licensee | 59 / 510 |
| Affiliate License-Licensor | 23 / 510 |
| Agreement Date | 470 / 510 |
| Anti-Assignment | 374 / 510 |
| Audit Rights | 214 / 510 |
| Cap On Liability | 275 / 510 |
| Change Of Control | 121 / 510 |
| Competitive Restriction Exception | 76 / 510 |
| Covenant Not To Sue | 100 / 510 |
| Document Name | 510 / 510 |
| Effective Date | 390 / 510 |
| Exclusivity | 180 / 510 |
| Expiration Date | 413 / 510 |
| Governing Law | 437 / 510 |
| Insurance | 166 / 510 |
| Ip Ownership Assignment | 124 / 510 |
| Irrevocable Or Perpetual License | 70 / 510 |
| Joint Ip Ownership | 46 / 510 |
| License Grant | 255 / 510 |
| Liquidated Damages | 61 / 510 |
| Minimum Commitment | 165 / 510 |
| Most Favored Nation | 28 / 510 |
| No-Solicit Of Customers | 34 / 510 |
| No-Solicit Of Employees | 59 / 510 |
| Non-Compete | 119 / 510 |
| Non-Disparagement | 38 / 510 |
| Non-Transferable License | 138 / 510 |
| Notice Period To Terminate Renewal | 111 / 510 |
| Parties | 509 / 510 |
| Post-Termination Services | 182 / 510 |
| Price Restrictions | 15 / 510 |
| Renewal Term | 176 / 510 |
| Revenue/Profit Sharing | 166 / 510 |
| Rofr/Rofo/Rofn | 85 / 510 |
| Source Code Escrow | 13 / 510 |
| Termination For Convenience | 183 / 510 |
| Third Party Beneficiary | 32 / 510 |
| Uncapped Liability | 111 / 510 |
| Unlimited/All-You-Can-Eat-License | 17 / 510 |
| Volume Restriction | 82 / 510 |
| Warranty Duration | 75 / 510 |

### `test.json` (denominator 102 for every category)

| Category | Non-empty / total |
|---|---|
| Affiliate License-Licensee | 12 / 102 |
| Affiliate License-Licensor | 6 / 102 |
| Agreement Date | 93 / 102 |
| Anti-Assignment | 72 / 102 |
| Audit Rights | 38 / 102 |
| Cap On Liability | 44 / 102 |
| Change Of Control | 26 / 102 |
| Competitive Restriction Exception | 16 / 102 |
| Covenant Not To Sue | 24 / 102 |
| Document Name | 102 / 102 |
| Effective Date | 70 / 102 |
| Exclusivity | 33 / 102 |
| Expiration Date | 78 / 102 |
| Governing Law | 83 / 102 |
| Insurance | 32 / 102 |
| Ip Ownership Assignment | 23 / 102 |
| Irrevocable Or Perpetual License | 13 / 102 |
| Joint Ip Ownership | 7 / 102 |
| License Grant | 50 / 102 |
| Liquidated Damages | 14 / 102 |
| Minimum Commitment | 32 / 102 |
| Most Favored Nation | 3 / 102 |
| No-Solicit Of Customers | 7 / 102 |
| No-Solicit Of Employees | 10 / 102 |
| Non-Compete | 23 / 102 |
| Non-Disparagement | 7 / 102 |
| Non-Transferable License | 22 / 102 |
| Notice Period To Terminate Renewal | 16 / 102 |
| Parties | 102 / 102 |
| Post-Termination Services | 29 / 102 |
| Price Restrictions | 0 / 102 |
| Renewal Term | 26 / 102 |
| Revenue/Profit Sharing | 35 / 102 |
| Rofr/Rofo/Rofn | 17 / 102 |
| Source Code Escrow | 1 / 102 |
| Termination For Convenience | 29 / 102 |
| Third Party Beneficiary | 6 / 102 |
| Uncapped Liability | 13 / 102 |
| Unlimited/All-You-Can-Eat-License | 3 / 102 |
| Volume Restriction | 17 / 102 |
| Warranty Duration | 10 / 102 |

### `train_separate_questions.json` (denominator = questions for that category)

| Category | Non-empty / total |
|---|---|
| Affiliate License-Licensee | 88 / 449 |
| Affiliate License-Licensor | 49 / 440 |
| Agreement Date | 383 / 414 |
| Anti-Assignment | 517 / 623 |
| Audit Rights | 538 / 770 |
| Cap On Liability | 554 / 731 |
| Change Of Control | 191 / 504 |
| Competitive Restriction Exception | 98 / 446 |
| Covenant Not To Sue | 129 / 461 |
| Document Name | 419 / 419 |
| Effective Date | 363 / 451 |
| Exclusivity | 332 / 593 |
| Expiration Date | 384 / 457 |
| Governing Law | 374 / 428 |
| Insurance | 443 / 717 |
| Ip Ownership Assignment | 257 / 564 |
| Irrevocable Or Perpetual License | 142 / 493 |
| Joint Ip Ownership | 101 / 470 |
| License Grant | 642 / 845 |
| Liquidated Damages | 98 / 459 |
| Minimum Commitment | 336 / 611 |
| Most Favored Nation | 35 / 418 |
| No-Solicit Of Customers | 43 / 424 |
| No-Solicit Of Employees | 73 / 432 |
| Non-Compete | 200 / 512 |
| Non-Disparagement | 53 / 430 |
| Non-Transferable License | 255 / 547 |
| Notice Period To Terminate Renewal | 104 / 417 |
| Parties | 2,011 / 2,012 |
| Post-Termination Services | 368 / 623 |
| Price Restrictions | 27 / 420 |
| Renewal Term | 179 / 437 |
| Revenue/Profit Sharing | 331 / 608 |
| Rofr/Rofo/Rofn | 299 / 639 |
| Source Code Escrow | 61 / 457 |
| Termination For Convenience | 205 / 459 |
| Third Party Beneficiary | 28 / 410 |
| Uncapped Liability | 151 / 461 |
| Unlimited/All-You-Can-Eat-License | 26 / 420 |
| Volume Restriction | 136 / 479 |
| Warranty Duration | 157 / 500 |

## 7. Conflict-prone pairs

Count of contracts in which **both** categories of the pair have at least one non-empty answer:

| Pair | `CUADv1.json` (510) | `test.json` (102) | `train_separate_questions.json` (408) |
|---|---|---|---|
| Cap On Liability + Uncapped Liability | 111 | 13 | 98 |
| Irrevocable Or Perpetual License + Termination For Convenience | 40 | 7 | 33 |
| Non-Compete + Exclusivity | 68 | 15 | 53 |

## 8. Offset verification (30 random labelled answers)

Method: seed `20261102`; 30 answers sampled uniformly from all answers with non-blank `text` across the three files; for each answer, `text[answer_start : answer_start + len(text)] == text` was evaluated against every candidate full-text source in which the same title occurs — the `context` field of that title in `CUADv1.json`, `test.json`, and `train_separate_questions.json`. `find(text)` was also recorded.

Results:

| Candidate source | Pass / applicable |
|---|---|
| Same-file `context` (the file the answer came from) | 30 / 30 |
| `CUADv1.json` `context` | 30 / 30 |
| `test.json` `context` (title present in 6 of the 30 samples) | 6 / 6 |
| `train_separate_questions.json` `context` (title present in 24 of the 30 samples) | 24 / 24 |
| Any candidate source | 30 / 30 |

Additional fact: for all 510 titles the `context` string is byte-identical wherever the title appears (510 identical, 0 differing), so all candidate sources agree.

Conclusion supported by the data: `answer_start` is a character offset into `paragraphs[0].context` of the same record (Python string slicing, no re-normalisation). The build agent can index `context[answer_start : answer_start + len(answer)]` directly.
