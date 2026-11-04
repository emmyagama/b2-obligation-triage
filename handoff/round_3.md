# Failure digest

Split: dev; mode: live; cases: 26

## Aggregate metrics

```json
{
  "constructed_e2_cases": 5,
  "constructed_e2_exception_rate": {
    "denominator": 5,
    "numerator": 4,
    "value": 0.8,
    "wilson_95": [
      0.37553462976252533,
      0.9637758913675698
    ]
  },
  "constructed_e2_recall": {
    "denominator": 5,
    "numerator": 1,
    "value": 0.2,
    "wilson_95": [
      0.03622410863243014,
      0.6244653702374747
    ]
  },
  "cost": {
    "mean_usd": 0.007924993461538462,
    "n": 26
  },
  "deadline_absolute": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_none": {
    "denominator": 19,
    "numerator": 2,
    "value": 0.10526315789473684,
    "wilson_95": [
      0.02935856029887013,
      0.31394082711109006
    ]
  },
  "deadline_recurring": {
    "denominator": 7,
    "numerator": 1,
    "value": 0.14285714285714285,
    "wilson_95": [
      0.02567962434474355,
      0.5131278292743189
    ]
  },
  "deadline_relative": {
    "denominator": 15,
    "numerator": 4,
    "value": 0.26666666666666666,
    "wilson_95": [
      0.10897453325692374,
      0.5195043405598057
    ]
  },
  "escalation_recall": {
    "denominator": 7,
    "numerator": 6,
    "value": 0.8571428571428571,
    "wilson_95": [
      0.4868721707256811,
      0.9743203756552565
    ]
  },
  "exception_rate": {
    "denominator": 26,
    "numerator": 23,
    "value": 0.8846153846153846,
    "wilson_95": [
      0.7102409678828635,
      0.9599675537638938
    ]
  },
  "false_escalation": {
    "denominator": 19,
    "numerator": 15,
    "value": 0.7894736842105263,
    "wilson_95": [
      0.5666572155618583,
      0.9149232336708375
    ]
  },
  "grounded_rate": {
    "denominator": 16,
    "numerator": 16,
    "value": 1.0,
    "wilson_95": [
      0.8063923194655637,
      1
    ]
  },
  "latency": {
    "n": 26,
    "p50_ms": 88570.0,
    "p95_ms": 121992.75
  },
  "mode": "live",
  "obligation_recall": {
    "denominator": 41,
    "numerator": 9,
    "value": 0.21951219512195122,
    "wilson_95": [
      0.12003174778217568,
      0.3670500598822617
    ]
  },
  "split": "dev"
}
```

## Class breakdown

### adversarial
```json
{
  "constructed_e2_cases": 0,
  "constructed_e2_exception_rate": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "constructed_e2_recall": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "cost": {
    "mean_usd": 0.005104494999999999,
    "n": 2
  },
  "deadline_absolute": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_none": {
    "denominator": 3,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      5.551115123125783e-17,
      0.5614970317550454
    ]
  },
  "deadline_recurring": {
    "denominator": 1,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      0,
      0.7934506856227626
    ]
  },
  "deadline_relative": {
    "denominator": 2,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      0,
      0.6576197724933469
    ]
  },
  "escalation_recall": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "exception_rate": {
    "denominator": 2,
    "numerator": 2,
    "value": 1.0,
    "wilson_95": [
      0.34238022750665303,
      1
    ]
  },
  "false_escalation": {
    "denominator": 2,
    "numerator": 2,
    "value": 1.0,
    "wilson_95": [
      0.34238022750665303,
      1
    ]
  },
  "grounded_rate": {
    "denominator": 2,
    "numerator": 2,
    "value": 1.0,
    "wilson_95": [
      0.34238022750665303,
      1
    ]
  },
  "latency": {
    "n": 2,
    "p50_ms": 38125.0,
    "p95_ms": 72437.5
  },
  "obligation_recall": {
    "denominator": 6,
    "numerator": 1,
    "value": 0.16666666666666666,
    "wilson_95": [
      0.030053369748306635,
      0.5635028221864702
    ]
  }
}
```
### clear
```json
{
  "constructed_e2_cases": 0,
  "constructed_e2_exception_rate": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "constructed_e2_recall": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "cost": {
    "mean_usd": 0.008040308,
    "n": 15
  },
  "deadline_absolute": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_none": {
    "denominator": 13,
    "numerator": 1,
    "value": 0.07692307692307693,
    "wilson_95": [
      0.013710421242556586,
      0.3331395092109959
    ]
  },
  "deadline_recurring": {
    "denominator": 6,
    "numerator": 1,
    "value": 0.16666666666666666,
    "wilson_95": [
      0.030053369748306635,
      0.5635028221864702
    ]
  },
  "deadline_relative": {
    "denominator": 11,
    "numerator": 3,
    "value": 0.2727272727272727,
    "wilson_95": [
      0.09746059290024889,
      0.5656453011761291
    ]
  },
  "escalation_recall": {
    "denominator": 2,
    "numerator": 1,
    "value": 0.5,
    "wilson_95": [
      0.09453120573423074,
      0.9054687942657693
    ]
  },
  "exception_rate": {
    "denominator": 15,
    "numerator": 15,
    "value": 1.0,
    "wilson_95": [
      0.7961166989641515,
      1
    ]
  },
  "false_escalation": {
    "denominator": 13,
    "numerator": 11,
    "value": 0.8461538461538461,
    "wilson_95": [
      0.5776536898051745,
      0.9567418216419186
    ]
  },
  "grounded_rate": {
    "denominator": 8,
    "numerator": 8,
    "value": 1.0,
    "wilson_95": [
      0.6755924351161198,
      1
    ]
  },
  "latency": {
    "n": 15,
    "p50_ms": 87562.0,
    "p95_ms": 123159.29999999999
  },
  "obligation_recall": {
    "denominator": 30,
    "numerator": 6,
    "value": 0.2,
    "wilson_95": [
      0.0950510717728987,
      0.3730569641314825
    ]
  }
}
```
### conflicting
```json
{
  "constructed_e2_cases": 5,
  "constructed_e2_exception_rate": {
    "denominator": 5,
    "numerator": 4,
    "value": 0.8,
    "wilson_95": [
      0.37553462976252533,
      0.9637758913675698
    ]
  },
  "constructed_e2_recall": {
    "denominator": 5,
    "numerator": 1,
    "value": 0.2,
    "wilson_95": [
      0.03622410863243014,
      0.6244653702374747
    ]
  },
  "cost": {
    "mean_usd": 0.008360096000000001,
    "n": 5
  },
  "deadline_absolute": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_none": {
    "denominator": 3,
    "numerator": 1,
    "value": 0.3333333333333333,
    "wilson_95": [
      0.06149194472039621,
      0.7923403991979522
    ]
  },
  "deadline_recurring": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_relative": {
    "denominator": 2,
    "numerator": 1,
    "value": 0.5,
    "wilson_95": [
      0.09453120573423074,
      0.9054687942657693
    ]
  },
  "escalation_recall": {
    "denominator": 5,
    "numerator": 5,
    "value": 1.0,
    "wilson_95": [
      0.5655175352168251,
      1
    ]
  },
  "exception_rate": {
    "denominator": 5,
    "numerator": 4,
    "value": 0.8,
    "wilson_95": [
      0.37553462976252533,
      0.9637758913675698
    ]
  },
  "false_escalation": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "grounded_rate": {
    "denominator": 4,
    "numerator": 4,
    "value": 1.0,
    "wilson_95": [
      0.5101091635454027,
      1
    ]
  },
  "latency": {
    "n": 5,
    "p50_ms": 95562.0,
    "p95_ms": 116050.4
  },
  "obligation_recall": {
    "denominator": 5,
    "numerator": 2,
    "value": 0.4,
    "wilson_95": [
      0.11762077423264783,
      0.769275718723987
    ]
  }
}
```
### out_of_scope
```json
{
  "constructed_e2_cases": 0,
  "constructed_e2_exception_rate": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "constructed_e2_recall": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "cost": {
    "mean_usd": 0.008358935,
    "n": 4
  },
  "deadline_absolute": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_none": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_recurring": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_relative": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "escalation_recall": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "exception_rate": {
    "denominator": 4,
    "numerator": 2,
    "value": 0.5,
    "wilson_95": [
      0.15003898915214947,
      0.8499610108478506
    ]
  },
  "false_escalation": {
    "denominator": 4,
    "numerator": 2,
    "value": 0.5,
    "wilson_95": [
      0.15003898915214947,
      0.8499610108478506
    ]
  },
  "grounded_rate": {
    "denominator": 2,
    "numerator": 2,
    "value": 1.0,
    "wilson_95": [
      0.34238022750665303,
      1
    ]
  },
  "latency": {
    "n": 4,
    "p50_ms": 119172.0,
    "p95_ms": 121807.65
  },
  "obligation_recall": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  }
}
```

## Cases

### dev-01 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Warranty Duration", "clause_ref": {"category": "Warranty Duration", "char_end": 25665, "char_start": 25205}, "deadline": {"anchor_event": "installation", "deadline_text": "for a period of one (1) year following Installation of the Products at Customer's facility", "kind": "relative", "offset_days": 365}, "owed_by": "provider", "type": "WAR-DURATION"}, {"clause_category": "License Grant", "clause_ref": {"category": "License Grant", "char_end": 52836, "char_start": 52564}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}, {"clause_category": "Post-Termination Services", "clause_ref": {"category": "Post-Termination Services", "char_end": 38322, "char_start": 38022}, "deadline": {"anchor_event": "last_shipment", "deadline_text": "for a minimum period of 10 years after the last shipment of a System pursuant to this Agreement", "kind": "relative", "offset_days": 3650}, "owed_by": "provider", "type": "SVC-POST-TERMINATION"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"distributor agreement"} | None | retries=0
- 4 search_corpus: {"query":"installation"} | None | retries=0
- 5 search_corpus: {"query":"license"} | None | retries=0
- 6 search_corpus: {"query":"payment"} | None | retries=0
- 7 llm_response: {"turn":2} | None | retries=0
- 8 get_clause: {"category":"Warranty Duration","document_id":"cuad_424083274037f63d7530"} | None | retries=0
- 9 get_clause: {"category":"Cap On Liability","document_id":"cuad_424083274037f63d7530"} | None | retries=0
- 10 get_clause: {"category":"License Grant","document_id":"cuad_424083274037f63d7530"} | None | retries=0
- 11 get_clause: {"category":"Non-Transferable License","document_id":"cuad_424083274037f63d7530"} | None | retries=0
- 12 llm_response: {"turn":3} | None | retries=0
- 13 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Warranty Duration","clause_quote":"Accuray will provide a warranty to each Customer that the Products will be  | VALIDATION_ERROR | retries=0
- 14 llm_response: {"turn":4} | None | retries=0
- 15 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Warranty Duration","clause_quote":"Accuray will provide a warranty to each Customer that the Products will be  | VALIDATION_ERROR | retries=0
Terminal args: null

### dev-02 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Ip Ownership Assignment", "clause_ref": {"category": "Ip Ownership Assignment", "char_end": 14371, "char_start": 14068}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "IP-OWNERSHIP-ASSIGNMENT"}, {"clause_category": "No-Solicit Of Employees", "clause_ref": {"category": "No-Solicit Of Employees", "char_end": 13122, "char_start": 12301}, "deadline": {"anchor_event": "termination", "deadline_text": "during the Term and for a period of one year from the date of expiration or termination", "kind": "relative", "offset_days": 365}, "owed_by": "provider", "type": "COV-NO-SOLICIT-EMPLOYEE"}, {"clause_category": "Termination For Convenience", "clause_ref": {"category": "Termination For Convenience", "char_end": 4399, "char_start": 4039}, "deadline": {"anchor_event": "termination_date", "deadline_text": "prior to the expiry of the Term", "kind": "relative", "offset_days": -90}, "owed_by": "provider", "type": "TRM-CONVENIENCE"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "This Agreement can be terminated at any time prior to the expiry of the Term, as follows: (a) by the Consultant electing to give the Company not less than 3 months prior notice of such termination;", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "provider", "type": "TRM-CONVENIENCE"}, {"clause_quote": "The Consultant covenants, undertakes and agrees with the Company that during the Term and for a period of one year from the date of expiration or termination of this Agreement for any reason whatsoever, it shall not, on its own behalf or on behalf of any person, whether directly or indirectly, in any capacity whatsoever, offer employment to or solicit the employment of or otherwise entice away from the employment of the Company or any of the Affiliated Companies, any individual who is employed or engaged by the Company or any of the Affiliated Companies at the date of expiration or termination of this Agreement or who was employed or engaged by the Company or any of the Affiliated Companies, within the one year period immediately preceding the date of expiration or termination of this Agreement, as applicable.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "provider", "type": "COV-NO-SOLICIT-EMPLOYEE"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"consultant resigns exit planning"} | None | retries=0
- 4 search_corpus: {"query":"termination resign notice"} | None | retries=0
- 5 llm_response: {"turn":2} | None | retries=0
- 6 get_clause: {"category":"Termination For Convenience","document_id":"cuad_7d139ce53ee5a9dbf8d5"} | None | retries=0
- 7 get_clause: {"category":"No-Solicit Of Employees","document_id":"cuad_7d139ce53ee5a9dbf8d5"} | None | retries=0
- 8 llm_response: {"turn":3} | None | retries=0
- 9 search_corpus: {"query":"not less than 3 months prior notice"} | None | retries=0
- 10 llm_response: {"turn":4} | None | retries=0
- 11 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Termination For Convenience","clause_quote":"This Agreement can be terminated at any time prior to the expiry  | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Termination For Convenience", "clause_quote": "This Agreement can be terminated at any time prior to the expiry of the Term, as follows: (a) by the Consultant electing to give the Company not less than 3 months prior notice of such termination;", "confidence": 1, "consequence": null, "deadline": {"anchor_event": "termination", "kind": "relative", "offset_days": -90, "raw_text": "3 months prior notice", "recurring_rule": null, "resolved_date": null}, "description": "The Consultant may terminate the Agreement by giving the Company not less than 3 months prior notice.", "owed_by": "provider", "type": "TRM-CONVENIENCE"}, {"clause_category": "No-Solicit Of Employees", "clause_quote": "The Consultant covenants, undertakes and agrees with the Company that during the Term and for a period of one year from the date of expiration or termination of this Agreement for any reason whatsoever, it shall not, on its own behalf or on behalf of any person, whether directly or indirectly, in any capacity whatsoever, offer employment to or solicit the employment of or otherwise entice away from the employment of the Company or any of the Affiliated Companies, any individual who is employed or engaged by the Company or any of the Affiliated Companies at the date of expiration or termination of this Agreement or who was employed or engaged by the Company or any of the Affiliated Companies, within the o

### dev-03 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Exclusivity", "clause_ref": {"category": "Exclusivity", "char_end": 22377, "char_start": 22066}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "COV-EXCLUSIVITY"}, {"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 90601, "char_start": 90052}, "deadline": {"deadline_text": "for a period of [***] thereafter", "kind": "recurring", "period": "during_term"}, "owed_by": "both", "type": "INS-COVERAGE"}, {"clause_category": "Anti-Assignment", "clause_ref": {"category": "Anti-Assignment", "char_end": 93421, "char_start": 92958}, "deadline": {"kind": "none"}, "owed_by": "both", "type": "CTL-NO-ASSIGNMENT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"license"} | None | retries=0
- 4 search_corpus: {"query":"solicit"} | None | retries=0
- 5 search_corpus: {"query":"compete"} | None | retries=0
- 6 search_corpus: {"query":"audit"} | None | retries=0
- 7 llm_response: {"turn":2} | None | retries=0
- 8 get_clause: {"category":"Exclusivity","document_id":"cuad_871f14e107390dae4b35"} | None | retries=0
- 9 get_clause: {"category":"Audit Rights","document_id":"cuad_871f14e107390dae4b35"} | None | retries=0
- 10 llm_response: {"turn":3} | None | retries=0
- 11 search_corpus: {"query":"indemnif"} | None | retries=0
- 12 search_corpus: {"query":"insurance"} | None | retries=0
- 13 search_corpus: {"query":"covenant"} | None | retries=0
- 14 search_corpus: {"query":"forecast"} | None | retries=0
- 15 llm_response: {"turn":4} | None | retries=0
- 16 get_clause: {"category":"Minimum Commitment","document_id":"cuad_871f14e107390dae4b35"} | None | retries=0
- 17 llm_response: {"turn":5} | None | retries=0
- 18 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Minimum Commitment","clause_quote":"[***] of each Forecast shall constitute a firm order and be a binding c | VALIDATION_ERROR | retries=0
- 19 llm_response: {"turn":6} | None | retries=0
- 20 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Minimum Commitment","clause_quote":"[***] of each Forecast shall constitute a firm order and be a binding c | VALIDATION_ERROR | retries=0
Terminal args: null

### dev-04 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 62547, "char_start": 60733}, "deadline": {"deadline_text": "during the term of this Agreement", "kind": "recurring", "period": "during_term"}, "owed_by": "customer", "type": "INS-COVERAGE"}, {"clause_category": "Minimum Commitment", "clause_ref": {"category": "Minimum Commitment", "char_end": 3102, "char_start": 2807}, "deadline": {"kind": "recurring", "period": "contract_year"}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}, {"clause_category": "Volume Restriction", "clause_ref": {"category": "Volume Restriction", "char_end": 16677, "char_start": 16466}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "PUR-VOLUME-RESTRICTION"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "Notwithstanding the foregoing, Schoolpop shall fund from AEIS a minimum of $52,000,000 of Cards (the \"Guaranteed Minimum\") in each Contract Year in order to maintain the exclusive right to sell Cards in the NPO Marketplace.", "deadline": {"kind": "recurring", "resolved_date": null}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"minimum"} | None | retries=0
- 4 search_corpus: {"query":"commitment"} | None | retries=0
- 5 search_corpus: {"query":"inventory"} | None | retries=0
- 6 llm_response: {"turn":2} | None | retries=0
- 7 get_clause: {"category":"Minimum Commitment","document_id":"cuad_b1fe09126a4d0b840349"} | None | retries=0
- 8 llm_response: {"turn":3} | None | retries=0
- 9 search_corpus: {"query":"Guaranteed Minimum"} | None | retries=0
- 10 search_corpus: {"query":"Card Inventory Penalty"} | None | retries=0
- 11 llm_response: {"turn":4} | None | retries=0
- 12 get_clause: {"category":"Competitive Restriction Exception","document_id":"cuad_b1fe09126a4d0b840349"} | None | retries=0
- 13 llm_response: {"turn":5} | None | retries=0
- 14 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Minimum Commitment","clause_quote":"Notwithstanding the foregoing, Schoolpop                   shall fund from | VALIDATION_ERROR | retries=0
- 15 llm_response: {"turn":6} | None | retries=0
- 16 search_corpus: {"query":"Notwithstanding the foregoing, Schoolpop"} | None | retries=0
- 17 llm_response: {"turn":7} | None | retries=0
- 18 get_clause: {"category":"Exclusivity","document_id":"cuad_b1fe09126a4d0b840349"} | None | retries=0
- 19 llm_response: {"turn":8} | None | retries=0
- 20 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Minimum Commitment","clause_quote":"Notwithstanding the foregoing, Schoolpop shall fund from AEIS a minimum of | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Minimum Commitment", "clause_quote": "Notwithstanding the foregoing, Schoolpop shall fund from AEIS a minimum of $52,000,000 of Cards (the \"Guaranteed Minimum\") in each Contract Year in order to maintain the exclusive right to sell Cards in the NPO Marketplace.", "confidence": 1, "consequence": "In any Contract Year in which Schoolpop fails to fund the Guaranteed Minimum, AEIS shall have the right, in its sole discretion, to (a) terminate the Agreement or (b) revoke the exclusivity.", "deadline": {"kind": "recurring", "raw_text": "in each Contract Year", "recurring_rule": "each Contract Year"}, "description": "Schoolpop (licensee) must fund from AEIS a minimum of $52,000,000 of Cards (the \"Guaranteed Minimum\") in each Contract Year in order to maintain the exclusive right to sell Cards in the NPO Marketplace.", "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}]}

### dev-05 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Minimum Commitment", "clause_ref": {"category": "Minimum Commitment", "char_end": 84468, "char_start": 84172}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}, {"clause_category": "Liquidated Damages", "clause_ref": {"category": "Liquidated Damages", "char_end": 25071, "char_start": 24803}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "LIA-LIQUIDATED-DAMAGES"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "The Sender shall notify the Transporter as soon as possible, if it is found that: (i) its deliveries during a month of Operation at a Point of  Entrance will be less than 95% of the Scheduled Capacity or (ii) its withdrawals at any Point of Exit shall be less than 95% of the Scheduled  Capacity.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"capacity shortfall"} | None | retries=0
- 4 search_corpus: {"query":"shipper"} | None | retries=0
- 5 search_corpus: {"query":"minimum commitment"} | None | retries=0
- 6 search_corpus: {"query":"volume restriction"} | None | retries=0
- 7 llm_response: {"turn":2} | None | retries=0
- 8 get_clause: {"category":"Minimum Commitment","document_id":"cuad_3c15a3be192ef6a9b14e"} | None | retries=0
- 9 get_clause: {"category":"Volume Restriction","document_id":"cuad_3c15a3be192ef6a9b14e"} | None | retries=0
- 10 llm_response: {"turn":3} | None | retries=0
- 11 search_corpus: {"query":"The Sender shall notify the Transporter as soon as possible"} | None | retries=0
- 12 search_corpus: {"query":"If by any reason the delivery is less than 95%"} | None | retries=0
- 13 llm_response: {"turn":4} | None | retries=0
- 14 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Minimum Commitment","clause_quote":"The Sender shall notify the Transporter as soon as possible, if it is f | VALIDATION_ERROR | retries=0
- 15 llm_response: {"turn":5} | None | retries=0
- 16 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Minimum Commitment","clause_quote":"The Sender shall notify the Transporter as soon as possible, if it is f | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Minimum Commitment", "clause_quote": "The Sender shall notify the Transporter as soon as possible, if it is found that: (i) its deliveries during a month of Operation at a Point of  Entrance will be less than 95% of the Scheduled Capacity or (ii) its withdrawals at any Point of Exit shall be less than 95% of the Scheduled  Capacity.", "confidence": 0.95, "consequence": null, "deadline": {"kind": "relative", "offset_days": null, "raw_text": "as soon as possible", "resolved_date": null}, "description": "The Sender must notify the Transporter as soon as possible if its deliveries during a month of operation at a point of entrance or withdrawals at a point of exit will be less than 95% of the scheduled capacity.", "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}]}

### dev-06 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Minimum Commitment", "clause_ref": {"category": "Minimum Commitment", "char_end": 38917, "char_start": 38632}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}, {"clause_category": "Notice Period To Terminate Renewal", "clause_ref": {"category": "Notice Period To Terminate Renewal", "char_end": 62892, "char_start": 62731}, "deadline": {"anchor_event": "expiration_date", "deadline_text": "at least six (6) months prior written notice of termination", "kind": "relative", "offset_days": -180}, "owed_by": "both", "type": "TRM-RENEWAL-NOTICE"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "Thereafter, this Agreement shall automatically continue in effect until either party gives the other at least six (6) months prior written notice of termination.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "customer", "type": "TRM-RENEWAL-NOTICE"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"renewal"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"Term and Renewal"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_clause: {"category":"Notice Period To Terminate Renewal","document_id":"cuad_c7256920fc58b74bbd37"} | None | retries=0
- 8 get_clause: {"category":"Renewal Term","document_id":"cuad_c7256920fc58b74bbd37"} | None | retries=0
- 9 get_clause: {"category":"Expiration Date","document_id":"cuad_c7256920fc58b74bbd37"} | None | retries=0
- 10 llm_response: {"turn":4} | None | retries=0
- 11 search_corpus: {"query":"10.2"} | None | retries=0
- 12 llm_response: {"turn":5} | None | retries=0
- 13 search_corpus: {"query":"Thereafter, this Agreement shall automatically continue"} | None | retries=0
- 14 llm_response: {"turn":6} | None | retries=0
- 15 get_clause: {"category":"Renewal Term","document_id":"cuad_c7256920fc58b74bbd37"} | None | retries=0
- 16 llm_response: {"turn":7} | None | retries=0
- 17 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Renewal Term","clause_quote":"Thereafter, this Agreement shall automatically continue in effect until either p | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Renewal Term", "clause_quote": "Thereafter, this Agreement shall automatically continue in effect until either party gives the other at least six (6) months prior written notice of termination.", "confidence": 1, "consequence": null, "deadline": {"kind": "relative", "offset_days": -180, "raw_text": "at least six (6) months prior written notice"}, "description": "Give at least six months prior written notice of termination to terminate the agreement upon expiration of the initial term or during the renewal term.", "owed_by": "customer", "type": "TRM-RENEWAL-NOTICE"}]}

### dev-07 — clear, constructed=False, difficulty 2
Failed: escalation_correct
Gold: {"obligations": [{"clause_category": "Audit Rights", "clause_ref": {"category": "Audit Rights", "char_end": 22018, "char_start": 21941}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}, {"clause_category": "Audit Rights", "clause_ref": {"category": "Audit Rights", "char_end": 64836, "char_start": 64464}, "deadline": {"anchor_event": "agreement_termination", "deadline_text": "During the Sale Term", "kind": "relative"}, "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "Merchant shall make its books and records available to Purchaser at all times", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}, {"clause_quote": "During the Sale Term, and thereafter until all of Merchant's and Purchaser's and Agent's obligations under this Agreement have been satisfied, Merchant and Purchaser shall have reasonable access to Merchant's and Purchaser's records with respect to the GOB Sale (including, but not limited to Merchandise, GOB Sale Proceeds, and Expenses) to review and audit such records.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"record"} | None | retries=0
- 4 search_corpus: {"query":"retention"} | None | retries=0
- 5 search_corpus: {"query":"going-out-of-business"} | None | retries=0
- 6 llm_response: {"turn":2} | None | retries=0
- 7 get_clause: {"category":"Audit Rights","document_id":"cuad_052975b81f9779a680c0"} | None | retries=0
- 8 llm_response: {"turn":3} | None | retries=0
- 9 get_document_dates: {"document_id":"cuad_052975b81f9779a680c0"} | None | retries=0
- 10 llm_response: {"turn":4} | None | retries=0
- 11 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Audit Rights","clause_quote":"Merchant shall make its books and records available to Purchaser at all times | VALIDATION_ERROR | retries=0
- 12 llm_response: {"turn":5} | None | retries=1
- 13 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Audit Rights","clause_quote":"Merchant shall make its books and records available to Purchaser at all times | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Audit Rights", "clause_quote": "Merchant shall make its books and records available to Purchaser at all times", "confidence": 0.95, "consequence": null, "deadline": {"kind": "none", "raw_text": "at all times"}, "description": "Merchant shall make its books and records available to Purchaser at all times.", "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}, {"clause_category": "Audit Rights", "clause_quote": "During the Sale Term, and thereafter until all of Merchant's and Purchaser's and Agent's obligations under this Agreement have been satisfied, Merchant and Purchaser shall have reasonable access to Merchant's and Purchaser's records with respect to the GOB Sale (including, but not limited to Merchandise, GOB Sale Proceeds, and Expenses) to review and audit such records.", "confidence": 0.95, "consequence": null, "deadline": {"anchor_event": "all of Merchant's and Purchaser's and Agent's obligations under this Agreement have been satisfied", "kind": "relative", "offset_days": null, "raw_text": "until all of Merchant's and Purchaser's and Agent's obligations under this Agreement have been satisfied", "resolved_date": null}, "description": "Merchant shall maintain access to records with respect to the GOB Sale until all obligations under the Agreement have been satisfied.", "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}]}

### dev-08 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 56941, "char_start": 56320}, "deadline": {"deadline_text": "during the Term and for a period of three (3) years thereafter (\"Insurance Period\")", "kind": "recurring", "period": "during_term"}, "owed_by": "customer", "type": "INS-COVERAGE"}, {"clause_category": "Covenant Not To Sue", "clause_ref": {"category": "Covenant Not To Sue", "char_end": 16680, "char_start": 15881}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "COV-NO-SUE"}, {"clause_category": "Non-Disparagement", "clause_ref": {"category": "Non-Disparagement", "char_end": 13670, "char_start": 13350}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "COV-NON-DISPARAGEMENT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"renewal"} | None | retries=0
- 4 search_corpus: {"query":"covenant"} | None | retries=0
- 5 llm_response: {"turn":2} | None | retries=0
- 6 search_corpus: {"query":"Term"} | None | retries=0
- 7 search_corpus: {"query":"Renewal Notice"} | None | retries=0
- 8 llm_response: {"turn":3} | None | retries=0
- 9 get_clause: {"category":"Insurance","document_id":"cuad_2a450f18c7649b3d7561"} | None | retries=0
- 10 get_clause: {"category":"Post-Termination Services","document_id":"cuad_2a450f18c7649b3d7561"} | None | retries=0
- 11 get_clause: {"category":"Competitive Restriction Exception","document_id":"cuad_2a450f18c7649b3d7561"} | None | retries=0
- 12 llm_response: {"turn":4} | None | retries=0
- 13 search_corpus: {"query":"procure and maintain"} | None | retries=0
- 14 search_corpus: {"query":"comprehensive general liability insurance"} | None | retries=0
- 15 llm_response: {"turn":5} | None | retries=0
- 16 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Insurance","clause_quote":"PAPA JOHN'S shall procure and maintain, at its sole cost and expense, and use comme | VALIDATION_ERROR | retries=0
- 17 llm_response: {"turn":6} | None | retries=0
- 18 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Insurance","clause_quote":"PAPA JOHN'S shall procure and maintain, at its sole cost and expense, and use comme | VALIDATION_ERROR | retries=0
Terminal args: null

### dev-09 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Irrevocable Or Perpetual License", "clause_ref": {"category": "Irrevocable Or Perpetual License", "char_end": 174659, "char_start": 174486}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}], "escalation": []}
Got: {"escalated": false, "escalation_codes": [], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"perpetual grant","top_k":5} | None | retries=0
- 4 search_corpus: {"query":"terminate","top_k":5} | None | retries=0
- 5 search_corpus: {"query":"survive","top_k":5} | None | retries=0
- 6 llm_response: {"turn":2} | None | retries=0
- 7 get_clause: {"category":"Irrevocable Or Perpetual License","document_id":"cuad_03a1e0f461f5359c5502"} | None | retries=0
- 8 llm_response: {"turn":3} | None | retries=0
- 9 search_corpus: {"query":"13.3 Effects Termination","top_k":5} | None | retries=0
- 10 llm_response: {"turn":4} | None | retries=0
- 11 search_corpus: {"query":"13.3.1 Effects of Termination","top_k":5} | None | retries=0
- 12 llm_response: {"turn":5} | None | retries=0
- 13 record_obligations: {"confidence":0,"escalate":false,"escalation_codes":[],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 0, "escalate": false, "escalation_codes": [], "obligations": []}

### dev-10 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Exclusivity", "clause_ref": {"category": "Exclusivity", "char_end": 8940, "char_start": 8636}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "COV-EXCLUSIVITY"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"renewal"} | None | retries=0
- 4 search_corpus: {"query":"self-publishing"} | None | retries=0
- 5 llm_response: {"turn":2} | None | retries=0
- 6 search_corpus: {"query":"self-publishing"} | None | retries=0
- 7 search_corpus: {"query":"self-published"} | None | retries=0
- 8 llm_response: {"turn":3} | None | retries=0
- 9 get_clause: {"category":"Renewal Term","document_id":"cuad_c72abcf3341f1ecf6365"} | None | retries=0
- 10 llm_response: {"turn":4} | None | retries=0
- 11 search_corpus: {"query":"30 September"} | None | retries=0
- 12 llm_response: {"turn":5} | None | retries=0
- 13 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Renewal Term","clause_quote":"If the Publishers exercise their right of renewal under Clause 17.1,             | VALIDATION_ERROR | retries=0
- 14 llm_response: {"turn":6} | None | retries=0
- 15 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Renewal Term","clause_quote":"If the Publishers exercise their right of renewal under Clause 17.1,             | VALIDATION_ERROR | retries=0
Terminal args: null

### dev-11 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Non-Compete", "clause_ref": {"category": "Non-Compete", "char_end": 110735, "char_start": 109480}, "deadline": {"anchor_event": "exclusive_period_end", "deadline_text": "During the applicable Exclusive Period", "kind": "relative"}, "owed_by": "customer", "type": "COV-NON-COMPETE"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"exclusive period field-team review licensee"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"field team review licensee OR SFJ OR PB"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"field-team OR field team OR review OR exclusive period"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"Competing Product OR exclusivity OR Exclusive Period"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 get_clause: {"category":"Non-Compete","document_id":"cuad_1bc91c6dfb434b456f99"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 get_document_dates: {"document_id":"cuad_1bc91c6dfb434b456f99"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 search_corpus: {"query":"\"Exclusive Period\" means"} | None | retries=0
- 16 llm_response: {"turn":8} | None | retries=0
- 17 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Non-Compete","clause_quote":"During the applicable Exclusive Period, SFJ shall not, and shall cause its Affili | VALIDATION_ERROR | retries=0
Terminal args: null

### dev-12 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Revenue/Profit Sharing", "clause_ref": {"category": "Revenue/Profit Sharing", "char_end": 88092, "char_start": 87456}, "deadline": {"anchor_event": "calendar_quarter_start", "deadline_text": "Commencing with the Calendar Quarter commencing on October 1, 2018", "kind": "recurring", "offset_days": null, "period": "quarterly", "resolved_date": null}, "owed_by": "customer", "type": "PAY-REVENUE-SHARE"}, {"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 137403, "char_start": 137034}, "deadline": {"anchor_event": "effective_date", "deadline_text": "during the Term, it shall maintain, through purchase or self- insurance, adequate insurance", "kind": "recurring", "offset_days": null, "period": "continuous", "resolved_date": null}, "owed_by": "both", "type": "INS-COVERAGE"}], "escalation": []}
Got: {"escalated": false, "escalation_codes": [], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"promotion fee"} | None | retries=0
- 4 search_corpus: {"query":"Dova"} | None | retries=0
- 5 search_corpus: {"query":"damages"} | None | retries=0
- 6 llm_response: {"turn":2} | None | retries=0
- 7 get_clause: {"category":"Cap On Liability","document_id":"cuad_93a7191ff01200e8fe44"} | None | retries=0
- 8 get_clause: {"category":"Uncapped Liability","document_id":"cuad_93a7191ff01200e8fe44"} | None | retries=0
- 9 llm_response: {"turn":3} | None | retries=0
- 10 search_corpus: {"query":"4.1.2"} | None | retries=0
- 11 llm_response: {"turn":4} | None | retries=0
- 12 search_corpus: {"query":"Section 4.1.2"} | None | retries=0
- 13 llm_response: {"turn":5} | None | retries=0
- 14 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": []}

### dev-13 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Source Code Escrow", "clause_ref": {"category": "Source Code Escrow", "char_end": 63335, "char_start": 63120}, "deadline": {"anchor_event": "effective_date", "deadline_text": "Within sixty (60) days of the Effective Date", "kind": "relative", "offset_days": 60}, "owed_by": "provider", "type": "LIC-SOURCE-ESCROW"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"governs"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_clause: {"category":"Governing Law","document_id":"cuad_5c2a9dcbe0cc7593bb1d"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"governed by the laws of the State of"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 record_obligations: {"confidence":0,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES"],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 0, "escalate": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": []}

### dev-14 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 48136, "char_start": 47917}, "deadline": {"anchor_event": "unresolved", "anchor_resolved": false, "deadline_text": "at all times during the Term and [*****]", "kind": "relative", "offset_days": null, "resolved_date": null}, "owed_by": "customer", "type": "INS-COVERAGE"}, {"clause_category": "Audit Rights", "clause_ref": {"category": "Audit Rights", "char_end": 36652, "char_start": 36541}, "deadline": {"anchor_event": "unresolved", "anchor_resolved": false, "deadline_text": "no later than [*****] prior to such audit", "kind": "relative", "offset_days": null, "resolved_date": null}, "owed_by": "provider", "type": "CTL-AUDIT-RIGHT"}, {"clause_category": "Warranty Duration", "clause_ref": {"category": "Warranty Duration", "char_end": 53701, "char_start": 53349}, "deadline": {"anchor_event": "delivery", "anchor_resolved": false, "deadline_text": "shall end [*****] thereafter", "kind": "relative", "offset_days": null, "resolved_date": null}, "owed_by": "provider", "type": "WAR-DURATION"}], "escalation": ["E3_CONDITIONAL_OR_AMBIGUOUS"]}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "Upon expiry of the Initial Term, this Agreement [*****] unless a Notice of non-renewal is given by either Party to the other Party [*****] prior to the expiry of the Initial Term or the end of a renewal period, if any.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "both", "type": "TRM-RENEWAL-NOTICE"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"term"} | None | retries=0
- 4 search_corpus: {"query":"notice"} | None | retries=0
- 5 search_corpus: {"query":"renewal"} | None | retries=0
- 6 search_corpus: {"query":"warranty"} | None | retries=0
- 7 llm_response: {"turn":2} | None | retries=0
- 8 get_clause: {"category":"Renewal Term","document_id":"cuad_08636f6df2840b29991a"} | None | retries=0
- 9 get_clause: {"category":"Notice Period To Terminate Renewal","document_id":"cuad_08636f6df2840b29991a"} | None | retries=0
- 10 get_clause: {"category":"Warranty Duration","document_id":"cuad_08636f6df2840b29991a"} | None | retries=0
- 11 get_clause: {"category":"Insurance","document_id":"cuad_08636f6df2840b29991a"} | None | retries=0
- 12 llm_response: {"turn":3} | None | retries=0
- 13 search_corpus: {"query":"duration and renewal"} | None | retries=0
- 14 llm_response: {"turn":4} | None | retries=0
- 15 get_clause: {"category":"Expiration Date","document_id":"cuad_08636f6df2840b29991a"} | None | retries=0
- 16 llm_response: {"turn":5} | None | retries=0
- 17 record_obligations: {"confidence":0.9,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Renewal Term","clause_quote":"Upon expiry of the Initial Term, this Agreement [*****] unless a Notice of non | None | retries=0
Terminal args: {"confidence": 0.9, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Renewal Term", "clause_quote": "Upon expiry of the Initial Term, this Agreement [*****] unless a Notice of non-renewal is given by either Party to the other Party [*****] prior to the expiry of the Initial Term or the end of a renewal period, if any.", "confidence": 0.9, "consequence": "The agreement expires or renews automatically depending on notice.", "deadline": {"kind": "relative", "offset_days": null, "raw_text": "[*****] prior to the expiry of the Initial Term or the end of a renewal period"}, "description": "Either Party may give a notice of non-renewal prior to the expiry of the Initial Term or the end of a renewal period to prevent renewal.", "owed_by": "both", "type": "TRM-RENEWAL-NOTICE"}]}

### dev-15 — clear, constructed=False, difficulty 1
Failed: escalation_correct
Gold: {"obligations": [], "escalation": ["E1_NO_OBLIGATION"]}
Got: {"escalated": false, "escalation_codes": [], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"joint filing agreement"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"agreement"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_clause: {"category":"Document Name","document_id":"cuad_cdbbcb9c511d8f86fe50"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": []}

### dev-16 — out_of_scope, constructed=False, difficulty 2
Failed: escalation_correct, schema_valid
Gold: {"obligations": [], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"renewal"} | None | retries=0
- 4 search_corpus: {"query":"schedule"} | None | retries=0
- 5 llm_response: {"turn":2} | None | retries=0
- 6 search_corpus: {"query":"Distributor"} | None | retries=0
- 7 search_corpus: {"query":"Term and Termination"} | None | retries=0
- 8 llm_response: {"turn":3} | None | retries=0
- 9 get_clause: {"category":"Expiration Date","document_id":"cuad_424083274037f63d7530"} | None | retries=0
- 10 llm_response: {"turn":4} | None | retries=0
- 11 search_corpus: {"query":"Strategic Alliance Agreement"} | None | retries=0
- 12 llm_response: {"turn":5} | None | retries=0
- 13 search_corpus: {"query":"renewal schedule"} | None | retries=0
- 14 search_corpus: {"query":"minimum purchase"} | None | retries=0
- 15 llm_response: {"turn":6} | None | retries=0
- 16 get_clause: {"category":"Cap On Liability","document_id":"cuad_424083274037f63d7530"} | None | retries=0
- 17 llm_response: {"turn":7} | None | retries=0
- 18 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Cap On Liability","clause_quote":"Without affecting Section 10 or the respective obligations of the parties | VALIDATION_ERROR | retries=0
- 19 llm_response: {"turn":8} | None | retries=0
- 20 search_corpus: {"query":"twelve calendar months preceding"} | None | retries=0
Terminal args: null

### dev-17 — out_of_scope, constructed=False, difficulty 2
Failed: escalation_correct
Gold: {"obligations": [], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "AEIS and/or their appointed representatives of AEIS or                   American Express Travel Related Services Inc. as solely                   determined by AEIS, shall be entitled to inspect and approve                   Seller's safekeeping facilities at any time during normal                   business hours.", "deadline": {"kind": "recurring", "resolved_date": null}, "owed_by": "provider", "type": "CTL-AUDIT-RIGHT"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"audit"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"reseller"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"Schoolpop"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"audit rights"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 get_clause: {"category":"Audit Rights","document_id":"cuad_b1fe09126a4d0b840349"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 search_corpus: {"query":"books and records"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 search_corpus: {"query":"audit or inspect or examination"} | None | retries=0
- 16 llm_response: {"turn":8} | None | retries=0
- 17 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Audit Rights","clause_quote":"AEIS and/or their appointed representatives of AEIS or                   America | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Audit Rights", "clause_quote": "AEIS and/or their appointed representatives of AEIS or                   American Express Travel Related Services Inc. as solely                   determined by AEIS, shall be entitled to inspect and approve                   Seller's safekeeping facilities at any time during normal                   business hours.", "confidence": 1, "consequence": null, "deadline": {"kind": "recurring", "raw_text": "at any time during normal business hours", "recurring_rule": "at any time during normal business hours"}, "description": "Licensor (AEIS) has the right to inspect and approve Seller's safekeeping facilities during normal business hours.", "owed_by": "provider", "type": "CTL-AUDIT-RIGHT"}]}

- dev-18 (out_of_scope, constructed=False): pass
- dev-19 (out_of_scope, constructed=False): pass
### dev-21 — adversarial, constructed=False, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 56941, "char_start": 56320}, "deadline": {"deadline_text": "during the Term and for a period of three (3) years thereafter (\"Insurance Period\")", "kind": "recurring", "period": "during_term"}, "owed_by": "customer", "type": "INS-COVERAGE"}, {"clause_category": "Covenant Not To Sue", "clause_ref": {"category": "Covenant Not To Sue", "char_end": 16680, "char_start": 15881}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "COV-NO-SUE"}, {"clause_category": "Non-Disparagement", "clause_ref": {"category": "Non-Disparagement", "char_end": 13670, "char_start": 13350}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "COV-NON-DISPARAGEMENT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "PAPA JOHN'S shall not, during the Term or at any time thereafter: (I) defame or disparage CELEBRITY or the Personality Rights (or any portion thereof), nor shall PAPA JOHN'S place the CELEBRITY or the Personality Rights (or any portion thereof) in a negative light, whether in connection with this Agreement or otherwise", "deadline": {"kind": "recurring", "resolved_date": null}, "owed_by": "customer", "type": "COV-NON-DISPARAGEMENT"}, {"clause_quote": "All Parties agree not to disparage or make derogatory comments, verbal or written, regarding the other Party during the Term of the Agreement, and for one year thereafter.", "deadline": {"kind": "recurring", "resolved_date": null}, "owed_by": "customer", "type": "COV-NON-DISPARAGEMENT"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"non-compete"} | None | retries=0
- 4 search_corpus: {"query":"solicit"} | None | retries=0
- 5 search_corpus: {"query":"confidential"} | None | retries=0
- 6 search_corpus: {"query":"exclusive"} | None | retries=0
- 7 llm_response: {"turn":2} | None | retries=0
- 8 get_clause: {"category":"Confidentiality","document_id":"adv_3e86dc8c4eb1f1086d9d"} | ClauseNotFound | retries=0
- 9 get_clause: {"category":"Non-Disparagement","document_id":"adv_3e86dc8c4eb1f1086d9d"} | None | retries=0
- 10 get_clause: {"category":"Non-Compete","document_id":"adv_3e86dc8c4eb1f1086d9d"} | ClauseNotFound | retries=0
- 11 get_clause: {"category":"Exclusivity","document_id":"adv_3e86dc8c4eb1f1086d9d"} | None | retries=0
- 12 llm_response: {"turn":3} | None | retries=0
- 13 search_corpus: {"query":"non-solicit"} | None | retries=0
- 14 search_corpus: {"query":"solicit"} | None | retries=0
- 15 search_corpus: {"query":"Confidential Information"} | None | retries=0
- 16 search_corpus: {"query":"10. Confidentiality"} | None | retries=0
- 17 llm_response: {"turn":4} | None | retries=0
- 18 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Non-Disparagement","clause_quote":"PAPA JOHN'S shall not, during the Term or at any time thereafter: (I) defam | VALIDATION_ERROR | retries=0
- 19 llm_response: {"turn":5} | None | retries=0
- 20 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Non-Disparagement","clause_quote":"PAPA JOHN'S shall not, during the Term or at any time thereafter: (I) defam | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Non-Disparagement", "clause_quote": "PAPA JOHN'S shall not, during the Term or at any time thereafter: (I) defame or disparage CELEBRITY or the Personality Rights (or any portion thereof), nor shall PAPA JOHN'S place the CELEBRITY or the Personality Rights (or any portion thereof) in a negative light, whether in connection with this Agreement or otherwise", "confidence": 1, "consequence": null, "deadline": {"kind": "recurring", "offset_days": null, "raw_text": "during the Term or at any time thereafter", "recurring_rule": "during the Term or at any time thereafter", "resolved_date": null}, "description": "Customer shall not defame or disparage Celebrity or Personality Rights or place them in a negative light during the Term or at any time thereafter.", "owed_by": "customer", "type": "COV-NON-DISPARAGEMENT"}, {"clause_category": "Non-Disparagement", "clause_quote": "All Parties agree not to disparage or make derogatory comments, verbal or written, regarding the other Party during the Term of the Agreement, and for one year thereafter.", "confidence": 1, "consequence": null, "deadline": {"kind": "recurring", "offset_days": null, "raw_text": "during the Term of the Agreement, and for one year thereafter", "recurring_rule": "during the Term of the Agreement, and for one year thereafter", "resolved_date": null}, "description": "Customer shall not disparage or make derogatory comments 

### dev-22 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Source Code Escrow", "clause_ref": {"category": "Source Code Escrow", "char_end": 63335, "char_start": 63120}, "deadline": {"anchor_event": "effective_date", "deadline_text": "Within sixty (60) days of the Effective Date", "kind": "relative", "offset_days": 60}, "owed_by": "provider", "type": "LIC-SOURCE-ESCROW"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"licence"} | None | retries=0
- 4 search_corpus: {"query":"governs"} | None | retries=0
- 5 llm_response: {"turn":2} | None | retries=0
- 6 get_clause: {"category":"Governing Law","document_id":"composite_d8416b5fddd1d8074804"} | None | retries=0
- 7 llm_response: {"turn":3} | None | retries=0
- 8 search_corpus: {"query":"Governing Law"} | None | retries=0
- 9 llm_response: {"turn":4} | None | retries=0
- 10 record_obligations: {"confidence":0.95,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES"],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": []}

### dev-23 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Irrevocable Or Perpetual License", "clause_ref": {"category": "Irrevocable Or Perpetual License", "char_end": 8913, "char_start": 7675}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "Either Party shall have the right to terminate this Agreement before the end of the Term for its convenience upon [***] written notice to the other Party (and any such termination shall become effective at the end of such [***]); [***].", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "both", "type": "TRM-CONVENIENCE"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"grant"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"irrevocable"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_clause: {"category":"License Grant","document_id":"composite_c5f9c6f4c2dbbf26ad52"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"irrevocable license"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 search_corpus: {"query":"termination"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 get_clause: {"category":"Termination For Convenience","document_id":"composite_c5f9c6f4c2dbbf26ad52"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Termination For Convenience","clause_quote":"Either Party shall have the right to terminate this Agreement  | VALIDATION_ERROR | retries=0
- 16 llm_response: {"turn":8} | None | retries=0
- 17 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Termination For Convenience","clause_quote":"Either Party shall have the right to terminate this Agreement  | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Termination For Convenience", "clause_quote": "Either Party shall have the right to terminate this Agreement before the end of the Term for its convenience upon [***] written notice to the other Party (and any such termination shall become effective at the end of such [***]); [***].", "confidence": 0.95, "consequence": "Termination of the agreement and cessation of agreement rights/obligations.", "deadline": {"anchor_event": "written notice", "kind": "relative", "offset_days": null, "raw_text": "[***] written notice", "resolved_date": null}, "description": "Right of either party to terminate the agreement for convenience upon written notice.", "owed_by": "both", "type": "TRM-CONVENIENCE"}]}

### dev-24 — conflicting, constructed=True, difficulty 3
Failed: execution error
Gold: {"obligations": [{"clause_category": "Post-Termination Services", "clause_ref": {"category": "Post-Termination Services", "char_end": 350136, "char_start": 349788}, "deadline": {"anchor_event": "termination", "deadline_text": "during the term of the Agreement and for three (3) years thereafter", "kind": "relative", "offset_days": 1095}, "owed_by": "provider", "type": "CTL-AUDIT-RIGHT"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "In the event of a Triggering Event, Manufacturer shall be liable for any actual amounts that Customer is contractually required to pay to any Third-Party customer of Customer that result from Customer's inability to supply the affected Product to such Third-Party customer as a direct result of such Triggering Event; provided that (1) Customer shall provide to Manufacturer appropriate evidence of such amounts (including invoices from the applicable customers) and the applicable contractual requirements (redacted, in each case, of information pertaining to pricing and other commercial terms that are not directly related to the claimed amounts), it being understood and agreed that, upon request, Manufacturer will enter into customary confidentiality arrangements prior to such information being shared and (2) Manufacturer shall not be liable for any such amounts in the aggregate in any Fiscal Year in excess of the aggregate Conversion Cost Markup during such Fiscal Year with respect to all Products manufactured at the Facility that is the subject of the applicable Triggering Event.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "provider", "type": "LIA-CAP"}, {"clause_quote": "Manufacturer will maintain complete and accurate Records. Any Records that are financial in nature such as, but not limited to, time sheets, billing Records, invoices, payment applications, payments of consultants and subcontractors and receipts relating to reimbursable expenses shall be maintained in accordance with applicable Law in the jurisdiction in which the applicable Facility is located. Manufacturer shall maintain such Records for a period equal to the later of (x) three (3) years after the expiration or termination of this Agreement or the applicable Facility Addendum, (y) the expiration of the statute of limitation for the Tax period applicable to such Records, or (z) for such per", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "provider", "type": "CTL-AUDIT-RIGHT"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"customer claims records"} | None | retries=0
- 4 search_corpus: {"query":"downstream customer claims"} | None | retries=0
- 5 llm_response: {"turn":2} | None | retries=0
- 6 search_corpus: {"query":"Triggering Event Manufacturer shall be liable"} | None | retries=0
- 7 search_corpus: {"query":"Triggering Event records customer claims"} | None | retries=0
- 8 llm_response: {"turn":3} | None | retries=0
- 9 get_clause: {"category":"Cap On Liability","document_id":"composite_1d5bf00304e51a76f89c"} | None | retries=0
- 10 get_clause: {"category":"Audit Rights","document_id":"composite_1d5bf00304e51a76f89c"} | None | retries=0
- 11 llm_response: {"turn":4} | None | retries=0
- 12 search_corpus: {"query":"Manufacturer will maintain complete and accurate Records"} | None | retries=0
- 13 llm_response: {"turn":5} | None | retries=0
- 14 search_corpus: {"query":"Manufacturer will maintain complete and accurate Records financial in nature"} | None | retries=0
- 15 llm_response: {"turn":6} | None | retries=0
- 16 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Cap On Liability","clause_quote":"In the event of a Triggering Event, Manufacturer shall be liable for any  | VALIDATION_ERROR | retries=0
- 17 llm_response: {"turn":7} | None | retries=0
- 18 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Cap On Liability","clause_quote":"In the event of a Triggering Event, Manufacturer shall be liable for any  | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Cap On Liability", "clause_quote": "In the event of a Triggering Event, Manufacturer shall be liable for any actual amounts that Customer is contractually required to pay to any Third-Party customer of Customer that result from Customer's inability to supply the affected Product to such Third-Party customer as a direct result of such Triggering Event; provided that (1) Customer shall provide to Manufacturer appropriate evidence of such amounts (including invoices from the applicable customers) and the applicable contractual requirements (redacted, in each case, of information pertaining to pricing and other commercial terms that are not directly related to the claimed amounts), it being understood and agreed that, upon request, Manufacturer will enter into customary confidentiality arrangements prior to such information being shared and (2) Manufacturer shall not be liable for any such amounts in the aggregate in any Fiscal Year in excess of the aggregate Conversion Cost Markup during such Fiscal Year with respect to all Products manufactured at the Facility that is the subject of the applicable Triggering Event.", "confidence": 0.95, "consequence": "Manufacturer is liable for actual amounts Customer is contractually required to pay third-party customers resulting from supply inability due to a Triggering Event, subject to annual aggregate Conversion Cost Markup cap", "deadlin

- dev-25 (conflicting, constructed=True): pass
### dev-26 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Cap On Liability", "clause_ref": {"category": "Cap On Liability", "char_end": 62596, "char_start": 61222}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIA-UNCAPPED"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"liability cap"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"10.4 Limitations on Liability"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_clause: {"category":"Cap On Liability","document_id":"composite_8fd5f85004f4197e9df5"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 get_clause: {"category":"Uncapped Liability","document_id":"composite_8fd5f85004f4197e9df5"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 record_obligations: {"confidence":0.9,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Cap On Liability","clause_quote":"Except in the event of (i) Third Party Claims subject to a Party's indemni | VALIDATION_ERROR | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 record_obligations: {"confidence":0.9,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Cap On Liability","clause_quote":"Except in the event of (i) Third Party Claims subject to a Party's indemni | VALIDATION_ERROR | retries=0
Terminal args: null

### dev-20 — adversarial, constructed=False, difficulty 1
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Warranty Duration", "clause_ref": {"category": "Warranty Duration", "char_end": 25665, "char_start": 25205}, "deadline": {"anchor_event": "installation", "deadline_text": "for a period of one (1) year following Installation of the Products at Customer's facility", "kind": "relative", "offset_days": 365}, "owed_by": "provider", "type": "WAR-DURATION"}, {"clause_category": "License Grant", "clause_ref": {"category": "License Grant", "char_end": 52836, "char_start": 52564}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}, {"clause_category": "Post-Termination Services", "clause_ref": {"category": "Post-Termination Services", "char_end": 38322, "char_start": 38022}, "deadline": {"anchor_event": "last_shipment", "deadline_text": "for a minimum period of 10 years after the last shipment of a System pursuant to this Agreement", "kind": "relative", "offset_days": 3650}, "owed_by": "provider", "type": "SVC-POST-TERMINATION"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"distributor agreement"} | None | retries=0
- 4 search_corpus: {"query":"installation"} | None | retries=0
- 5 search_corpus: {"query":"license"} | None | retries=0
- 6 search_corpus: {"query":"payment"} | None | retries=0
- 7 llm_response: {"turn":2} | None | retries=0
- 8 get_clause: {"category":"Warranty Duration","document_id":"cuad_424083274037f63d7530"} | None | retries=0
- 9 get_clause: {"category":"Cap On Liability","document_id":"cuad_424083274037f63d7530"} | None | retries=0
- 10 get_clause: {"category":"License Grant","document_id":"cuad_424083274037f63d7530"} | None | retries=0
- 11 get_clause: {"category":"Non-Transferable License","document_id":"cuad_424083274037f63d7530"} | None | retries=0
- 12 llm_response: {"turn":3} | None | retries=0
- 13 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Warranty Duration","clause_quote":"Accuray will provide a warranty to each Customer that the Products will be  | VALIDATION_ERROR | retries=0
- 14 llm_response: {"turn":4} | None | retries=0
- 15 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Warranty Duration","clause_quote":"Accuray will provide a warranty to each Customer that the Products will be  | VALIDATION_ERROR | retries=0
Terminal args: null

