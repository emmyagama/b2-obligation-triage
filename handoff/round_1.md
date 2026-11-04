# Failure digest

Split: dev; mode: replay; cases: 26

## Aggregate metrics

```json
{
  "constructed_e2_cases": 5,
  "constructed_e2_exception_rate": {
    "denominator": 5,
    "numerator": 5,
    "value": 1.0,
    "wilson_95": [
      0.5655175352168251,
      1
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
    "mean_usd": 0.005383806923076922,
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
    "numerator": 1,
    "value": 0.05263157894736842,
    "wilson_95": [
      0.009351994062300362,
      0.24638731166898786
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
    "numerator": 5,
    "value": 0.7142857142857143,
    "wilson_95": [
      0.35893445183261935,
      0.9177810759959433
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
    "numerator": 12,
    "value": 0.631578947368421,
    "wilson_95": [
      0.41039533164803066,
      0.8085048725486492
    ]
  },
  "grounded_rate": {
    "denominator": 7,
    "numerator": 7,
    "value": 1.0,
    "wilson_95": [
      0.6456695649333126,
      1
    ]
  },
  "latency": {
    "n": 26,
    "p50_ms": 82828.0,
    "p95_ms": 121492.0
  },
  "mode": "replay",
  "obligation_recall": {
    "denominator": 41,
    "numerator": 6,
    "value": 0.14634146341463414,
    "wilson_95": [
      0.0688424814129593,
      0.28443458042480957
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
    "mean_usd": 0.0021343,
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
    "numerator": 1,
    "value": 0.5,
    "wilson_95": [
      0.09453120573423074,
      0.9054687942657693
    ]
  },
  "grounded_rate": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "latency": {
    "n": 2,
    "p50_ms": 37461.0,
    "p95_ms": 71175.9
  },
  "obligation_recall": {
    "denominator": 6,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      2.7755575615628914e-17,
      0.3903342879021653
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
    "mean_usd": 0.006236238666666666,
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
    "numerator": 4,
    "value": 0.36363636363636365,
    "wilson_95": [
      0.15166471095367573,
      0.6461988254921511
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
    "numerator": 10,
    "value": 0.7692307692307693,
    "wilson_95": [
      0.49743624053272495,
      0.9182047128150143
    ]
  },
  "grounded_rate": {
    "denominator": 7,
    "numerator": 7,
    "value": 1.0,
    "wilson_95": [
      0.6456695649333126,
      1
    ]
  },
  "latency": {
    "n": 15,
    "p50_ms": 90579.0,
    "p95_ms": 137805.99999999994
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
    "numerator": 5,
    "value": 1.0,
    "wilson_95": [
      0.5655175352168251,
      1
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
    "mean_usd": 0.005187056,
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
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      5.551115123125783e-17,
      0.5614970317550454
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
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      0,
      0.6576197724933469
    ]
  },
  "escalation_recall": {
    "denominator": 5,
    "numerator": 4,
    "value": 0.8,
    "wilson_95": [
      0.37553462976252533,
      0.9637758913675698
    ]
  },
  "exception_rate": {
    "denominator": 5,
    "numerator": 5,
    "value": 1.0,
    "wilson_95": [
      0.5655175352168251,
      1
    ]
  },
  "false_escalation": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "grounded_rate": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "latency": {
    "n": 5,
    "p50_ms": 89735.0,
    "p95_ms": 113443.4
  },
  "obligation_recall": {
    "denominator": 5,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      0,
      0.43448246478317476
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
    "mean_usd": 0.00405788,
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
    "numerator": 1,
    "value": 0.25,
    "wilson_95": [
      0.04558726080970055,
      0.6993581574175981
    ]
  },
  "false_escalation": {
    "denominator": 4,
    "numerator": 1,
    "value": 0.25,
    "wilson_95": [
      0.04558726080970055,
      0.6993581574175981
    ]
  },
  "grounded_rate": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "latency": {
    "n": 4,
    "p50_ms": 67156.5,
    "p95_ms": 87852.7
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
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Warranty Duration", "clause_ref": {"category": "Warranty Duration", "char_end": 25665, "char_start": 25205}, "deadline": {"anchor_event": "installation", "deadline_text": "for a period of one (1) year following Installation of the Products at Customer's facility", "kind": "relative", "offset_days": 365}, "owed_by": "provider", "type": "WAR-DURATION"}, {"clause_category": "License Grant", "clause_ref": {"category": "License Grant", "char_end": 52836, "char_start": 52564}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}, {"clause_category": "Post-Termination Services", "clause_ref": {"category": "Post-Termination Services", "char_end": 38322, "char_start": 38022}, "deadline": {"anchor_event": "last_shipment", "deadline_text": "for a minimum period of 10 years after the last shipment of a System pursuant to this Agreement", "kind": "relative", "offset_days": 3650}, "owed_by": "provider", "type": "SVC-POST-TERMINATION"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"queries":["*"]} | VALIDATION_ERROR | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"agreement"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_document_dates: {"document_id":"cuad_424083274037f63d7530"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"audit"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 search_corpus: {"query":"obligation"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 record_obligations: {"confidence":0,"escalate":true,"escalation_codes":["E3_CONDITIONAL_OR_AMBIGUOUS"],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 0, "escalate": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": []}

### dev-02 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Ip Ownership Assignment", "clause_ref": {"category": "Ip Ownership Assignment", "char_end": 14371, "char_start": 14068}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "IP-OWNERSHIP-ASSIGNMENT"}, {"clause_category": "No-Solicit Of Employees", "clause_ref": {"category": "No-Solicit Of Employees", "char_end": 13122, "char_start": 12301}, "deadline": {"anchor_event": "termination", "deadline_text": "during the Term and for a period of one year from the date of expiration or termination", "kind": "relative", "offset_days": 365}, "owed_by": "provider", "type": "COV-NO-SOLICIT-EMPLOYEE"}, {"clause_category": "Termination For Convenience", "clause_ref": {"category": "Termination For Convenience", "char_end": 4399, "char_start": 4039}, "deadline": {"anchor_event": "termination_date", "deadline_text": "prior to the expiry of the Term", "kind": "relative", "offset_days": -90}, "owed_by": "provider", "type": "TRM-CONVENIENCE"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "This Agreement can be terminated at any time prior to the expiry of the Term, as follows: (a) by the Consultant electing to give the Company not less than 3 months prior notice of such termination", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "provider", "type": "TRM-CONVENIENCE"}, {"clause_quote": "The Consultant covenants, undertakes and agrees with the Company that during the Term and for a period of one year from the date of expiration or termination of this Agreement for any reason whatsoever, it shall not, on its own behalf or on behalf of any person, whether directly or indirectly, in any capacity whatsoever, offer employment to or solicit the employment of or otherwise entice away from the employment of the Company or any of the Affiliated Companies, any individual who is employed or engaged by the Company or any of the Affiliated Companies at the date of expiration or termination of this Agreement or who was employed or engaged by the Company or any of the Affiliated Companies, within the one year period immediately preceding the date of expiration or termination of this Agreement, as applicable.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "provider", "type": "COV-NO-SOLICIT-EMPLOYEE"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"resign"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"Termination"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_document_dates: {"document_id":"cuad_7d139ce53ee5a9dbf8d5"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 get_clause: {"category":"Termination For Convenience","document_id":"cuad_7d139ce53ee5a9dbf8d5"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 get_clause: {"category":"No-Solicit Of Employees","document_id":"cuad_7d139ce53ee5a9dbf8d5"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Termination For Convenience","clause_quote":"This Agreement can be terminated at any time prior to the expi | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Termination For Convenience", "clause_quote": "This Agreement can be terminated at any time prior to the expiry of the Term, as follows: (a) by the Consultant electing to give the Company not less than 3 months prior notice of such termination", "confidence": 1, "consequence": "Termination of the agreement following the required notice period.", "deadline": {"kind": "relative", "offset_days": 90, "raw_text": "not less than 3 months prior notice"}, "description": "The Consultant (Licensor) must give the Company not less than 3 months prior notice of termination if electing to terminate.", "owed_by": "provider", "type": "TRM-CONVENIENCE"}, {"clause_category": "No-Solicit Of Employees", "clause_quote": "The Consultant covenants, undertakes and agrees with the Company that during the Term and for a period of one year from the date of expiration or termination of this Agreement for any reason whatsoever, it shall not, on its own behalf or on behalf of any person, whether directly or indirectly, in any capacity whatsoever, offer employment to or solicit the employment of or otherwise entice away from the employment of the Company or any of the Affiliated Companies, any individual who is employed or engaged by the Company or any of the Affiliated Companies at the date of expiration or termination of this Agreement or who was employed or engaged by the Company or any of the Affiliated

### dev-03 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Exclusivity", "clause_ref": {"category": "Exclusivity", "char_end": 22377, "char_start": 22066}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "COV-EXCLUSIVITY"}, {"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 90601, "char_start": 90052}, "deadline": {"deadline_text": "for a period of [***] thereafter", "kind": "recurring", "period": "during_term"}, "owed_by": "both", "type": "INS-COVERAGE"}, {"clause_category": "Anti-Assignment", "clause_ref": {"category": "Anti-Assignment", "char_end": 93421, "char_start": 92958}, "deadline": {"kind": "none"}, "owed_by": "both", "type": "CTL-NO-ASSIGNMENT"}], "escalation": []}
Got: {"escalated": false, "escalation_codes": [], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"*"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_document_dates: {"document_id":"cuad_871f14e107390dae4b35"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"licensor"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"audit"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 get_clause: {"category":"Audit Rights","document_id":"cuad_871f14e107390dae4b35"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 search_corpus: {"query":"batch"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": []}

### dev-04 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 62547, "char_start": 60733}, "deadline": {"deadline_text": "during the term of this Agreement", "kind": "recurring", "period": "during_term"}, "owed_by": "customer", "type": "INS-COVERAGE"}, {"clause_category": "Minimum Commitment", "clause_ref": {"category": "Minimum Commitment", "char_end": 3102, "char_start": 2807}, "deadline": {"kind": "recurring", "period": "contract_year"}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}, {"clause_category": "Volume Restriction", "clause_ref": {"category": "Volume Restriction", "char_end": 16677, "char_start": 16466}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "PUR-VOLUME-RESTRICTION"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "Notwithstanding the foregoing, Schoolpop shall fund from AEIS a minimum of $52,000,000 of Cards (the \"Guaranteed Minimum\") in each Contract Year in order to maintain the exclusive right to sell Cards in the NPO Marketplace.", "deadline": {"kind": "recurring", "resolved_date": null}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"minimum commitment volume restriction purchase order"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_clause: {"category":"Minimum Commitment","document_id":"cuad_b1fe09126a4d0b840349"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_clause: {"category":"Volume Restriction","document_id":"cuad_b1fe09126a4d0b840349"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 get_document_dates: {"document_id":"cuad_b1fe09126a4d0b840349"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Minimum Commitment","clause_quote":"Notwithstanding the foregoing, Schoolpop                   shall fund from | VALIDATION_ERROR | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 search_corpus: {"query":"Notwithstanding the foregoing, Schoolpop shall fund from AEIS"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Minimum Commitment","clause_quote":"Notwithstanding the foregoing, Schoolpop shall fund from AEIS a minimum of | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Minimum Commitment", "clause_quote": "Notwithstanding the foregoing, Schoolpop shall fund from AEIS a minimum of $52,000,000 of Cards (the \"Guaranteed Minimum\") in each Contract Year in order to maintain the exclusive right to sell Cards in the NPO Marketplace.", "confidence": 1, "consequence": "AEIS shall have the right, in its sole discretion, to (a) terminate the Agreement or (b) revoke the exclusivity.", "deadline": {"kind": "recurring", "raw_text": "each Contract Year", "recurring_rule": "each Contract Year"}, "description": "Schoolpop (licensee) must fund from AEIS a minimum of $52,000,000 of Cards (the Guaranteed Minimum) in each Contract Year in order to maintain the exclusive right to sell Cards in the NPO Marketplace.", "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}]}

### dev-05 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Minimum Commitment", "clause_ref": {"category": "Minimum Commitment", "char_end": 84468, "char_start": 84172}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}, {"clause_category": "Liquidated Damages", "clause_ref": {"category": "Liquidated Damages", "char_end": 25071, "char_start": 24803}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "LIA-LIQUIDATED-DAMAGES"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "The Sender shall notify the Transporter as soon as possible, if it is found that: (i) its deliveries during a month of Operation at a Point of  Entrance will be less than 95% of the Scheduled Capacity or (ii) its withdrawals at any Point of Exit shall be less than 95% of the Scheduled  Capacity.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"shipper capacity shortfall"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_document_dates: {"document_id":"cuad_3c15a3be192ef6a9b14e"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_clause: {"category":"Minimum Commitment","document_id":"cuad_3c15a3be192ef6a9b14e"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Minimum Commitment","clause_quote":"The Sender shall notify the Transporter as soon as possible, if it is foun | VALIDATION_ERROR | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Minimum Commitment","clause_quote":"The Sender shall notify the Transporter as soon as possible, if it is foun | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Minimum Commitment", "clause_quote": "The Sender shall notify the Transporter as soon as possible, if it is found that: (i) its deliveries during a month of Operation at a Point of  Entrance will be less than 95% of the Scheduled Capacity or (ii) its withdrawals at any Point of Exit shall be less than 95% of the Scheduled  Capacity.", "confidence": 1, "consequence": "Contractual breach / potential sanctions or charges related to delivery shortfalls.", "deadline": {"anchor_event": null, "kind": "none", "offset_days": null, "raw_text": "as soon as possible", "recurring_rule": null, "resolved_date": null}, "description": "The Sender (Customer) must notify the Transporter as soon as possible if it is found that its deliveries during a month of operation at a point of entrance or withdrawals at any point of exit will be less than 95% of the scheduled capacity.", "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}]}

### dev-06 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Minimum Commitment", "clause_ref": {"category": "Minimum Commitment", "char_end": 38917, "char_start": 38632}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}, {"clause_category": "Notice Period To Terminate Renewal", "clause_ref": {"category": "Notice Period To Terminate Renewal", "char_end": 62892, "char_start": 62731}, "deadline": {"anchor_event": "expiration_date", "deadline_text": "at least six (6) months prior written notice of termination", "kind": "relative", "offset_days": -180}, "owed_by": "both", "type": "TRM-RENEWAL-NOTICE"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"renewal"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"term"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"10.1"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"Initial Term"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 get_document_dates: {"document_id":"cuad_c7256920fc58b74bbd37"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 search_corpus: {"query":"renewal extension automatic term"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 get_clause: {"category":"Renewal Term","document_id":"cuad_c7256920fc58b74bbd37"} | None | retries=0
- 16 llm_response: {"turn":8} | None | retries=0
- 17 get_clause: {"category":"Notice Period To Terminate Renewal","document_id":"cuad_c7256920fc58b74bbd37"} | None | retries=0
Terminal args: null

### dev-07 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Audit Rights", "clause_ref": {"category": "Audit Rights", "char_end": 22018, "char_start": 21941}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}, {"clause_category": "Audit Rights", "clause_ref": {"category": "Audit Rights", "char_end": 64836, "char_start": 64464}, "deadline": {"anchor_event": "agreement_termination", "deadline_text": "During the Sale Term", "kind": "relative"}, "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "During the Sale Term, and thereafter until all of Merchant's and Purchaser's and Agent's obligations under this Agreement have been satisfied, Merchant and Purchaser shall have reasonable access to Merchant's and Purchaser's records with respect to the GOB Sale (including, but not limited to Merchandise, GOB Sale Proceeds, and Expenses) to review and audit such records.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"merchant record-retention duties after the going-out-of-business sale"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"records retention"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_clause: {"category":"Audit Rights","document_id":"cuad_052975b81f9779a680c0"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 get_document_dates: {"document_id":"cuad_052975b81f9779a680c0"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Audit Rights","clause_quote":"During the Sale Term, and thereafter until all of Merchant's and Purchaser's and | VALIDATION_ERROR | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Audit Rights","clause_quote":"During the Sale Term, and thereafter until all of Merchant's and Purchaser's and | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Audit Rights", "clause_quote": "During the Sale Term, and thereafter until all of Merchant's and Purchaser's and Agent's obligations under this Agreement have been satisfied, Merchant and Purchaser shall have reasonable access to Merchant's and Purchaser's records with respect to the GOB Sale (including, but not limited to Merchandise, GOB Sale Proceeds, and Expenses) to review and audit such records.", "confidence": 1, "consequence": null, "deadline": {"anchor_event": "satisfaction of all obligations under the agreement", "kind": "relative", "offset_days": null, "raw_text": "thereafter until all of Merchant's and Purchaser's and Agent's obligations under this Agreement have been satisfied", "resolved_date": null}, "description": "Merchant shall maintain and provide reasonable access to records with respect to the GOB Sale (including Merchandise, GOB Sale Proceeds, and Expenses) during the Sale Term and thereafter until all obligations under the agreement have been satisfied.", "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}]}

### dev-08 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 56941, "char_start": 56320}, "deadline": {"deadline_text": "during the Term and for a period of three (3) years thereafter (\"Insurance Period\")", "kind": "recurring", "period": "during_term"}, "owed_by": "customer", "type": "INS-COVERAGE"}, {"clause_category": "Covenant Not To Sue", "clause_ref": {"category": "Covenant Not To Sue", "char_end": 16680, "char_start": 15881}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "COV-NO-SUE"}, {"clause_category": "Non-Disparagement", "clause_ref": {"category": "Non-Disparagement", "char_end": 13670, "char_start": 13350}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "COV-NON-DISPARAGEMENT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"*"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_document_dates: {"document_id":"cuad_2a450f18c7649b3d7561"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"non-compete exclusivity non-disparagement solicit"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"exclusive exclusivity restrict compete solicit disparag"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 search_corpus: {"query":"PAPA JOHN'S covenants agree shall will"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 search_corpus: {"query":"\"PAPA JOHN'S shall\""} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 search_corpus: {"query":"\"PAPA JOHN'S shall not\""} | None | retries=0
- 16 llm_response: {"turn":8} | None | retries=0
- 17 get_clause: {"category":"Non-Disparagement","document_id":"cuad_2a450f18c7649b3d7561"} | None | retries=0
Terminal args: null

### dev-09 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Irrevocable Or Perpetual License", "clause_ref": {"category": "Irrevocable Or Perpetual License", "char_end": 174659, "char_start": 174486}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}], "escalation": []}
Got: {"escalated": false, "escalation_codes": [], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"perpetual"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_clause: {"category":"Irrevocable Or Perpetual License","document_id":"cuad_03a1e0f461f5359c5502"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_document_dates: {"document_id":"cuad_03a1e0f461f5359c5502"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": []}

### dev-10 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Exclusivity", "clause_ref": {"category": "Exclusivity", "char_end": 8940, "char_start": 8636}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "COV-EXCLUSIVITY"}], "escalation": []}
Got: {"escalated": false, "escalation_codes": [], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=1
- 3 search_corpus: {"queries":["renewal","notice","term","termination"]} | VALIDATION_ERROR | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"renewal"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_document_dates: {"document_id":"cuad_c72abcf3341f1ecf6365"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 get_clause: {"category":"Renewal Term","document_id":"cuad_c72abcf3341f1ecf6365"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": []}

### dev-11 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Non-Compete", "clause_ref": {"category": "Non-Compete", "char_end": 110735, "char_start": 109480}, "deadline": {"anchor_event": "exclusive_period_end", "deadline_text": "During the applicable Exclusive Period", "kind": "relative"}, "owed_by": "customer", "type": "COV-NON-COMPETE"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"*","top_k":10} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_document_dates: {"document_id":"cuad_1bc91c6dfb434b456f99"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"exclusive","top_k":10} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"field-team","top_k":10} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 record_obligations: {"confidence":0,"escalate":true,"escalation_codes":["E3_CONDITIONAL_OR_AMBIGUOUS"],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 0, "escalate": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": []}

### dev-12 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Revenue/Profit Sharing", "clause_ref": {"category": "Revenue/Profit Sharing", "char_end": 88092, "char_start": 87456}, "deadline": {"anchor_event": "calendar_quarter_start", "deadline_text": "Commencing with the Calendar Quarter commencing on October 1, 2018", "kind": "recurring", "offset_days": null, "period": "quarterly", "resolved_date": null}, "owed_by": "customer", "type": "PAY-REVENUE-SHARE"}, {"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 137403, "char_start": 137034}, "deadline": {"anchor_event": "effective_date", "deadline_text": "during the Term, it shall maintain, through purchase or self- insurance, adequate insurance", "kind": "recurring", "offset_days": null, "period": "continuous", "resolved_date": null}, "owed_by": "both", "type": "INS-COVERAGE"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"Dova"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"limitation of liability cap limitation on damages"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_clause: {"category":"Cap On Liability","document_id":"cuad_93a7191ff01200e8fe44"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 get_clause: {"category":"Uncapped Liability","document_id":"cuad_93a7191ff01200e8fe44"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 search_corpus: {"query":"Section 4.1.2 promotion fee"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 search_corpus: {"query":"Section 4.1.2"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 get_document_dates: {"document_id":"cuad_93a7191ff01200e8fe44"} | None | retries=0
- 16 llm_response: {"turn":8} | None | retries=0
- 17 record_obligations: {"confidence":0.85,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES","E3_CONDITIONAL_OR_AMBIGUOUS"],"obligations":[{"clause_category":"Cap On Liability","clause_quote":"Notwithstanding the  | VALIDATION_ERROR | retries=0
Terminal args: null

### dev-13 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Source Code Escrow", "clause_ref": {"category": "Source Code Escrow", "char_end": 63335, "char_start": 63120}, "deadline": {"anchor_event": "effective_date", "deadline_text": "Within sixty (60) days of the Effective Date", "kind": "relative", "offset_days": 60}, "owed_by": "provider", "type": "LIC-SOURCE-ESCROW"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": [{"clause_quote": "This Agreement shall be governed by          the laws of the State of California, USA, excluding conflict of laws          provisions and excluding the 1980 United Nations Convention on          Contracts for the International Sale of Goods.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "both", "type": "COV-NO-SUE"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"governing law"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_clause: {"category":"Governing Law","document_id":"cuad_5c2a9dcbe0cc7593bb1d"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_document_dates: {"document_id":"cuad_5c2a9dcbe0cc7593bb1d"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 record_obligations: {"confidence":0.8,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES"],"obligations":[{"clause_category":"Governing Law","clause_quote":"This Agreement shall be governed by          the laws  | VALIDATION_ERROR | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 record_obligations: {"confidence":0.8,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES"],"obligations":[{"clause_category":"Governing Law","clause_quote":"This Agreement shall be governed by          the laws  | None | retries=0
Terminal args: {"confidence": 0.8, "escalate": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": [{"clause_category": "Governing Law", "clause_quote": "This Agreement shall be governed by          the laws of the State of California, USA, excluding conflict of laws          provisions and excluding the 1980 United Nations Convention on          Contracts for the International Sale of Goods.", "confidence": 0.8, "consequence": "Governing law is conflicting due to multiple governing law clauses specifying different jurisdictions.", "deadline": {"kind": "none", "raw_text": null}, "description": "The agreement specifies California law in one section and New York law in another section.", "owed_by": "both", "type": "COV-NO-SUE"}]}

### dev-14 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 48136, "char_start": 47917}, "deadline": {"anchor_event": "unresolved", "anchor_resolved": false, "deadline_text": "at all times during the Term and [*****]", "kind": "relative", "offset_days": null, "resolved_date": null}, "owed_by": "customer", "type": "INS-COVERAGE"}, {"clause_category": "Audit Rights", "clause_ref": {"category": "Audit Rights", "char_end": 36652, "char_start": 36541}, "deadline": {"anchor_event": "unresolved", "anchor_resolved": false, "deadline_text": "no later than [*****] prior to such audit", "kind": "relative", "offset_days": null, "resolved_date": null}, "owed_by": "provider", "type": "CTL-AUDIT-RIGHT"}, {"clause_category": "Warranty Duration", "clause_ref": {"category": "Warranty Duration", "char_end": 53701, "char_start": 53349}, "deadline": {"anchor_event": "delivery", "anchor_resolved": false, "deadline_text": "shall end [*****] thereafter", "kind": "relative", "offset_days": null, "resolved_date": null}, "owed_by": "provider", "type": "WAR-DURATION"}], "escalation": ["E3_CONDITIONAL_OR_AMBIGUOUS"]}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "Upon each renewal of the relevant insurance policies, the Company shall on reasonable request provide the Repairer with relevant insurance certificates in order to evidence insurance is maintained in accordance with this Clause 8.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "customer", "type": "INS-COVERAGE"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"maintenance agreement term renewal notice non-compete exclusivity IP confidentiality warranty limit of liability insurance","top_k":10} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_document_dates: {"document_id":"cuad_08636f6df2840b29991a"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_clause: {"category":"Insurance","document_id":"cuad_08636f6df2840b29991a"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Insurance","clause_quote":"Upon each renewal of the relevant insurance policies, the Company shall on reasonab | VALIDATION_ERROR | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Insurance","clause_quote":"Upon each renewal of the relevant insurance policies, the Company shall on reasonab | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Insurance", "clause_quote": "Upon each renewal of the relevant insurance policies, the Company shall on reasonable request provide the Repairer with relevant insurance certificates in order to evidence insurance is maintained in accordance with this Clause 8.", "confidence": 1, "consequence": null, "deadline": {"anchor_event": "renewal of the relevant insurance policies", "kind": "relative", "offset_days": null, "raw_text": "Upon each renewal of the relevant insurance policies", "recurring_rule": null, "resolved_date": null}, "description": "Provide the Repairer with relevant insurance certificates upon each renewal of the relevant insurance policies on reasonable request to evidence insurance maintained under Clause 8.", "owed_by": "customer", "type": "INS-COVERAGE"}]}

### dev-15 — clear, constructed=False, difficulty 1
Failed: escalation_correct
Gold: {"obligations": [], "escalation": ["E1_NO_OBLIGATION"]}
Got: {"escalated": false, "escalation_codes": [], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"queries":["agreement","obligation","terminate","confidential","notice","party"]} | VALIDATION_ERROR | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"agreement"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_document_dates: {"document_id":"cuad_cdbbcb9c511d8f86fe50"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"joint filing"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": []}

### dev-16 — out_of_scope, constructed=False, difficulty 2
Failed: escalation_correct
Gold: {"obligations": [], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"renewal"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"renewal notice term"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"Term Extension Renewal Schedule"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 get_document_dates: {"document_id":"cuad_424083274037f63d7530"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 record_obligations: {"confidence":0,"escalate":true,"escalation_codes":["E3_CONDITIONAL_OR_AMBIGUOUS"],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 0, "escalate": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": []}

- dev-17 (out_of_scope, constructed=False): pass
- dev-18 (out_of_scope, constructed=False): pass
- dev-19 (out_of_scope, constructed=False): pass
### dev-21 — adversarial, constructed=False, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 56941, "char_start": 56320}, "deadline": {"deadline_text": "during the Term and for a period of three (3) years thereafter (\"Insurance Period\")", "kind": "recurring", "period": "during_term"}, "owed_by": "customer", "type": "INS-COVERAGE"}, {"clause_category": "Covenant Not To Sue", "clause_ref": {"category": "Covenant Not To Sue", "char_end": 16680, "char_start": 15881}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "COV-NO-SUE"}, {"clause_category": "Non-Disparagement", "clause_ref": {"category": "Non-Disparagement", "char_end": 13670, "char_start": 13350}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "COV-NON-DISPARAGEMENT"}], "escalation": []}
Got: {"escalated": false, "escalation_codes": [], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"*"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_document_dates: {"document_id":"adv_3e86dc8c4eb1f1086d9d"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"non-compete"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"exclusivity"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": []}

### dev-22 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Source Code Escrow", "clause_ref": {"category": "Source Code Escrow", "char_end": 63335, "char_start": 63120}, "deadline": {"anchor_event": "effective_date", "deadline_text": "Within sixty (60) days of the Effective Date", "kind": "relative", "offset_days": 60}, "owed_by": "provider", "type": "LIC-SOURCE-ESCROW"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"governs dispute law jurisdiction"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_clause: {"category":"Governing Law","document_id":"composite_d8416b5fddd1d8074804"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"governed by the laws of the State of California"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 record_obligations: {"confidence":0,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES"],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 0, "escalate": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": []}

### dev-23 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Irrevocable Or Perpetual License", "clause_ref": {"category": "Irrevocable Or Perpetual License", "char_end": 8913, "char_start": 7675}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"grant"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"irrevocable"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_document_dates: {"document_id":"composite_c5f9c6f4c2dbbf26ad52"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 record_obligations: {"confidence":0,"escalate":true,"escalation_codes":["E3_CONDITIONAL_OR_AMBIGUOUS"],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 0, "escalate": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": []}

### dev-24 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Post-Termination Services", "clause_ref": {"category": "Post-Termination Services", "char_end": 350136, "char_start": 349788}, "deadline": {"anchor_event": "termination", "deadline_text": "during the term of the Agreement and for three (3) years thereafter", "kind": "relative", "offset_days": 1095}, "owed_by": "provider", "type": "CTL-AUDIT-RIGHT"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"customer claims records"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"Records Retention Period manufacturer claims"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"Recall customer claims indemnification manufacturer"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 get_document_dates: {"document_id":"composite_1d5bf00304e51a76f89c"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Audit Rights","clause_quote":"Manufacturer will maintain complete and accurate Records. Any Records that are f | VALIDATION_ERROR | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Audit Rights","clause_quote":"Manufacturer will maintain complete and accurate Records. Any Records that are f | VALIDATION_ERROR | retries=0
Terminal args: null

### dev-25 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Liquidated Damages", "clause_ref": {"category": "Liquidated Damages", "char_end": 25071, "char_start": 24803}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "LIA-LIQUIDATED-DAMAGES"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"penalty"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_document_dates: {"document_id":"composite_bc622aa361019f6836c9"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_clause: {"category":"Liquidated Damages","document_id":"composite_bc622aa361019f6836c9"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"limitation of liability damages exclude"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 search_corpus: {"query":"LIMITATION OF LIABILITY"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 search_corpus: {"query":"consequential damages indirect damages limitation liability"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 search_corpus: {"query":"indirect consequential damages limitation liability loss of profit"} | None | retries=0
- 16 llm_response: {"turn":8} | None | retries=0
- 17 record_obligations: {"confidence":0,"escalate":true,"escalation_codes":["E3_CONDITIONAL_OR_AMBIGUOUS"],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 0, "escalate": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": []}

### dev-26 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Cap On Liability", "clause_ref": {"category": "Cap On Liability", "char_end": 62596, "char_start": 61222}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIA-UNCAPPED"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": false, "escalation_codes": [], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"liability cap"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"10.4 Limitations on Liability"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"aggregate liability for the initial twelve"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 get_clause: {"category":"Cap On Liability","document_id":"composite_8fd5f85004f4197e9df5"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 get_document_dates: {"document_id":"composite_8fd5f85004f4197e9df5"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": []}

### dev-20 — adversarial, constructed=False, difficulty 1
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Warranty Duration", "clause_ref": {"category": "Warranty Duration", "char_end": 25665, "char_start": 25205}, "deadline": {"anchor_event": "installation", "deadline_text": "for a period of one (1) year following Installation of the Products at Customer's facility", "kind": "relative", "offset_days": 365}, "owed_by": "provider", "type": "WAR-DURATION"}, {"clause_category": "License Grant", "clause_ref": {"category": "License Grant", "char_end": 52836, "char_start": 52564}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}, {"clause_category": "Post-Termination Services", "clause_ref": {"category": "Post-Termination Services", "char_end": 38322, "char_start": 38022}, "deadline": {"anchor_event": "last_shipment", "deadline_text": "for a minimum period of 10 years after the last shipment of a System pursuant to this Agreement", "kind": "relative", "offset_days": 3650}, "owed_by": "provider", "type": "SVC-POST-TERMINATION"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"queries":["*"]} | VALIDATION_ERROR | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"agreement"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_document_dates: {"document_id":"cuad_424083274037f63d7530"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"audit"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 search_corpus: {"query":"obligation"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 record_obligations: {"confidence":0,"escalate":true,"escalation_codes":["E3_CONDITIONAL_OR_AMBIGUOUS"],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 0, "escalate": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": []}

