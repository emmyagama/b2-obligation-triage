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
    "numerator": 3,
    "value": 0.6,
    "wilson_95": [
      0.2307242812760128,
      0.882379225767352
    ]
  },
  "cost": {
    "mean_usd": 0.007933336923076923,
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
    "numerator": 3,
    "value": 0.2,
    "wilson_95": [
      0.07047549346981563,
      0.45185448715169363
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
    "numerator": 22,
    "value": 0.8461538461538461,
    "wilson_95": [
      0.6646880067178652,
      0.9384996627642165
    ]
  },
  "false_escalation": {
    "denominator": 19,
    "numerator": 14,
    "value": 0.7368421052631579,
    "wilson_95": [
      0.5120844910218489,
      0.8819358765321748
    ]
  },
  "grounded_rate": {
    "denominator": 17,
    "numerator": 17,
    "value": 1.0,
    "wilson_95": [
      0.8156818649911483,
      1
    ]
  },
  "latency": {
    "n": 26,
    "p50_ms": 105640.5,
    "p95_ms": 126035.25
  },
  "mode": "live",
  "obligation_recall": {
    "denominator": 41,
    "numerator": 8,
    "value": 0.1951219512195122,
    "wilson_95": [
      0.10234437385158025,
      0.3401358518706343
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
    "mean_usd": 0.00770103,
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
    "p50_ms": 60937.5,
    "p95_ms": 115781.25
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
    "mean_usd": 0.008111494666666667,
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
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      0,
      0.22809537235419838
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
    "numerator": 12,
    "value": 0.9230769230769231,
    "wilson_95": [
      0.6668604907890041,
      0.9862895787574435
    ]
  },
  "grounded_rate": {
    "denominator": 10,
    "numerator": 10,
    "value": 1.0,
    "wilson_95": [
      0.7224672001371107,
      0.9999999999999999
    ]
  },
  "latency": {
    "n": 15,
    "p50_ms": 119171.0,
    "p95_ms": 131078.09999999998
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
    "numerator": 3,
    "value": 0.6,
    "wilson_95": [
      0.2307242812760128,
      0.882379225767352
    ]
  },
  "cost": {
    "mean_usd": 0.008578391999999999,
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
    "numerator": 2,
    "value": 0.6666666666666666,
    "wilson_95": [
      0.2076596008020477,
      0.9385080552796037
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
    "denominator": 5,
    "numerator": 5,
    "value": 1.0,
    "wilson_95": [
      0.5655175352168251,
      1
    ]
  },
  "latency": {
    "n": 5,
    "p50_ms": 105969.0,
    "p95_ms": 119912.2
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
    "mean_usd": 0.0065750800000000005,
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
    "p50_ms": 97195.5,
    "p95_ms": 105291.0
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
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Warranty Duration", "clause_ref": {"category": "Warranty Duration", "char_end": 25665, "char_start": 25205}, "deadline": {"anchor_event": "installation", "deadline_text": "for a period of one (1) year following Installation of the Products at Customer's facility", "kind": "relative", "offset_days": 365}, "owed_by": "provider", "type": "WAR-DURATION"}, {"clause_category": "License Grant", "clause_ref": {"category": "License Grant", "char_end": 52836, "char_start": 52564}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}, {"clause_category": "Post-Termination Services", "clause_ref": {"category": "Post-Termination Services", "char_end": 38322, "char_start": 38022}, "deadline": {"anchor_event": "last_shipment", "deadline_text": "for a minimum period of 10 years after the last shipment of a System pursuant to this Agreement", "kind": "relative", "offset_days": 3650}, "owed_by": "provider", "type": "SVC-POST-TERMINATION"}], "escalation": []}
Got: {"escalated": false, "escalation_codes": [], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"queries":"distributor"} | VALIDATION_ERROR | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"distributor"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"Accuray shall"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"indemnify"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 search_corpus: {"query":"confidential"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 search_corpus: {"query":"non-compete"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": []}

### dev-02 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Ip Ownership Assignment", "clause_ref": {"category": "Ip Ownership Assignment", "char_end": 14371, "char_start": 14068}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "IP-OWNERSHIP-ASSIGNMENT"}, {"clause_category": "No-Solicit Of Employees", "clause_ref": {"category": "No-Solicit Of Employees", "char_end": 13122, "char_start": 12301}, "deadline": {"anchor_event": "termination", "deadline_text": "during the Term and for a period of one year from the date of expiration or termination", "kind": "relative", "offset_days": 365}, "owed_by": "provider", "type": "COV-NO-SOLICIT-EMPLOYEE"}, {"clause_category": "Termination For Convenience", "clause_ref": {"category": "Termination For Convenience", "char_end": 4399, "char_start": 4039}, "deadline": {"anchor_event": "termination_date", "deadline_text": "prior to the expiry of the Term", "kind": "relative", "offset_days": -90}, "owed_by": "provider", "type": "TRM-CONVENIENCE"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "This Agreement can be terminated at any time prior to the expiry of the Term, as follows: (a) by the Consultant electing to give the Company not less than 3 months prior notice of such termination;", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "provider", "type": "TRM-CONVENIENCE"}, {"clause_quote": "The Consultant covenants, undertakes and agrees with the Company that during the Term and for a period of one year from the date of expiration or termination of this Agreement for any reason whatsoever, it shall not, on its own behalf or on behalf of any person, whether directly or indirectly, in any capacity whatsoever, offer employment to or solicit the employment of or otherwise entice away from the employment of the Company or any of the Affiliated Companies, any individual who is employed or engaged by the Company or any of the Affiliated Companies at the date of expiration or termination of this Agreement or who was employed or engaged by the Company or any of the Affiliated Companies, within the one year period immediately preceding the date of expiration or termination of this Agreement, as applicable.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "provider", "type": "COV-NO-SOLICIT-EMPLOYEE"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"resign"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"termination"} | None | retries=0
- 6 search_corpus: {"query":"Non-Compete"} | None | retries=0
- 7 llm_response: {"turn":3} | None | retries=0
- 8 search_corpus: {"query":"restrictive covenants non-competition"} | None | retries=0
- 9 llm_response: {"turn":4} | None | retries=0
- 10 search_corpus: {"query":"solicit customers"} | None | retries=0
- 11 llm_response: {"turn":5} | None | retries=0
- 12 search_corpus: {"query":"7.1"} | None | retries=0
- 13 llm_response: {"turn":6} | None | retries=0
- 14 search_corpus: {"query":"The Consultant covenants, undertakes and agrees with the Company that during the Term and for a period of one year"} | None | retries=0
- 15 llm_response: {"turn":7} | None | retries=0
- 16 get_clause: {"category":"Termination For Convenience","document_id":"cuad_7d139ce53ee5a9dbf8d5"} | None | retries=0
- 17 get_clause: {"category":"No-Solicit Of Employees","document_id":"cuad_7d139ce53ee5a9dbf8d5"} | None | retries=0
- 18 llm_response: {"turn":8} | None | retries=0
- 19 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Termination For Convenience","clause_quote":"This Agreement can be terminated at any time prior to the expi | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Termination For Convenience", "clause_quote": "This Agreement can be terminated at any time prior to the expiry of the Term, as follows: (a) by the Consultant electing to give the Company not less than 3 months prior notice of such termination;", "confidence": 0.95, "consequence": null, "deadline": {"kind": "relative", "offset_days": 90, "raw_text": "not less than 3 months prior notice"}, "description": "The consultant may terminate the agreement by giving the company not less than 3 months prior notice.", "owed_by": "provider", "type": "TRM-CONVENIENCE"}, {"clause_category": "No-Solicit Of Employees", "clause_quote": "The Consultant covenants, undertakes and agrees with the Company that during the Term and for a period of one year from the date of expiration or termination of this Agreement for any reason whatsoever, it shall not, on its own behalf or on behalf of any person, whether directly or indirectly, in any capacity whatsoever, offer employment to or solicit the employment of or otherwise entice away from the employment of the Company or any of the Affiliated Companies, any individual who is employed or engaged by the Company or any of the Affiliated Companies at the date of expiration or termination of this Agreement or who was employed or engaged by the Company or any of the Affiliated Companies, within the one year period immediately preceding the date of expiration

### dev-03 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Exclusivity", "clause_ref": {"category": "Exclusivity", "char_end": 22377, "char_start": 22066}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "COV-EXCLUSIVITY"}, {"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 90601, "char_start": 90052}, "deadline": {"deadline_text": "for a period of [***] thereafter", "kind": "recurring", "period": "during_term"}, "owed_by": "both", "type": "INS-COVERAGE"}, {"clause_category": "Anti-Assignment", "clause_ref": {"category": "Anti-Assignment", "char_end": 93421, "char_start": 92958}, "deadline": {"kind": "none"}, "owed_by": "both", "type": "CTL-NO-ASSIGNMENT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"licensor"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"manufactur"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"ARTICLE 2 MANUFACTURING AND SUPPLY OBLIGATIONS"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"AMAG, or a Third Person manufacturing"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 search_corpus: {"query":"Quality Agreement"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 search_corpus: {"query":"audit"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 get_clause: {"category":"Audit Rights","document_id":"cuad_871f14e107390dae4b35"} | None | retries=0
- 16 llm_response: {"turn":8} | None | retries=0
- 17 get_document_dates: {"document_id":"cuad_871f14e107390dae4b35"} | None | retries=0
Terminal args: null

### dev-04 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 62547, "char_start": 60733}, "deadline": {"deadline_text": "during the term of this Agreement", "kind": "recurring", "period": "during_term"}, "owed_by": "customer", "type": "INS-COVERAGE"}, {"clause_category": "Minimum Commitment", "clause_ref": {"category": "Minimum Commitment", "char_end": 3102, "char_start": 2807}, "deadline": {"kind": "recurring", "period": "contract_year"}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}, {"clause_category": "Volume Restriction", "clause_ref": {"category": "Volume Restriction", "char_end": 16677, "char_start": 16466}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "PUR-VOLUME-RESTRICTION"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "Notwithstanding the foregoing, Schoolpop shall fund from AEIS a minimum of $52,000,000 of Cards (the \"Guaranteed Minimum\") in each Contract Year in order to maintain the exclusive right to sell Cards in the NPO Marketplace.", "deadline": {"kind": "recurring", "resolved_date": null}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}, {"clause_quote": "At any given time during this Agreement, Schoolpop's inactive Card inventory shall be limited to $3,000,000 in Card value as determined by the Point denomination on each Card.", "deadline": {"kind": "recurring", "resolved_date": null}, "owed_by": "customer", "type": "PUR-VOLUME-RESTRICTION"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"minimum commitment volume restriction inventory cap purchase reseller"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_clause: {"category":"Minimum Commitment","document_id":"cuad_b1fe09126a4d0b840349"} | None | retries=0
- 6 get_clause: {"category":"Volume Restriction","document_id":"cuad_b1fe09126a4d0b840349"} | None | retries=0
- 7 search_corpus: {"query":"Schoolpop shall discontinue reselling Encompass"} | None | retries=0
- 8 llm_response: {"turn":3} | None | retries=0
- 9 search_corpus: {"query":"Schoolpop shall provide to AEIS, no later than January 5"} | None | retries=0
- 10 llm_response: {"turn":4} | None | retries=0
- 11 get_document_dates: {"document_id":"cuad_b1fe09126a4d0b840349"} | None | retries=0
- 12 llm_response: {"turn":5} | None | retries=0
- 13 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Minimum Commitment","clause_quote":"Notwithstanding the foregoing, Schoolpop                   shall fund f | VALIDATION_ERROR | retries=0
- 14 llm_response: {"turn":6} | None | retries=0
- 15 search_corpus: {"query":"inactive Card inventory shall be limited to $3,000,000"} | None | retries=0
- 16 llm_response: {"turn":7} | None | retries=0
- 17 get_clause: {"category":"Minimum Commitment","document_id":"cuad_b1fe09126a4d0b840349"} | None | retries=0
- 18 llm_response: {"turn":8} | None | retries=0
- 19 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Minimum Commitment","clause_quote":"Notwithstanding the foregoing, Schoolpop shall fund from AEIS a minimum | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Minimum Commitment", "clause_quote": "Notwithstanding the foregoing, Schoolpop shall fund from AEIS a minimum of $52,000,000 of Cards (the \"Guaranteed Minimum\") in each Contract Year in order to maintain the exclusive right to sell Cards in the NPO Marketplace.", "confidence": 0.95, "consequence": "AEIS shall have the right, in its sole discretion, to (a) terminate the Agreement or (b) revoke the exclusivity.", "deadline": {"kind": "recurring", "raw_text": "in each Contract Year", "recurring_rule": "in each Contract Year"}, "description": "Licensee (Schoolpop) must fund a minimum of $52,000,000 of Cards in each Contract Year to maintain exclusive resale rights in the NPO Marketplace.", "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}, {"clause_category": "Volume Restriction", "clause_quote": "At any given time during this Agreement, Schoolpop's inactive Card inventory shall be limited to $3,000,000 in Card value as determined by the Point denomination on each Card.", "confidence": 0.95, "consequence": "AEIS shall cease fulfilling Orders from Schoolpop until such time that Schoolpop's inventory returns to an acceptable level based on the established maximums.", "deadline": {"kind": "recurring", "raw_text": "At any given time during this Agreement", "recurring_rule": "At any given time during this Agreement"}, "description": "Licensee (Schoolpop) must maintain inactive

### dev-05 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Minimum Commitment", "clause_ref": {"category": "Minimum Commitment", "char_end": 84468, "char_start": 84172}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}, {"clause_category": "Liquidated Damages", "clause_ref": {"category": "Liquidated Damages", "char_end": 25071, "char_start": 24803}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "LIA-LIQUIDATED-DAMAGES"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "The Sender shall notify the Transporter as soon as possible, if it is found that: (i) its deliveries during a month of Operation at a Point of  Entrance will be less than 95% of the Scheduled Capacity or (ii) its withdrawals at any Point of Exit shall be less than 95% of the Scheduled Capacity.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"capacity shortfall"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"The Sender shall notify the Transporter as soon as possible"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_clause: {"category":"Minimum Commitment","document_id":"cuad_3c15a3be192ef6a9b14e"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"If by any reason the delivery is less than 95%"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 get_document_dates: {"document_id":"cuad_3c15a3be192ef6a9b14e"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 record_obligations: {"confidence":0.9,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Minimum Commitment","clause_quote":"The Sender shall notify the Transporter as soon as possible, if it is fo | None | retries=0
Terminal args: {"confidence": 0.9, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Minimum Commitment", "clause_quote": "The Sender shall notify the Transporter as soon as possible, if it is found that: (i) its deliveries during a month of Operation at a Point of  Entrance will be less than 95% of the Scheduled Capacity or (ii) its withdrawals at any Point of Exit shall be less than 95% of the Scheduled Capacity.", "confidence": 0.9, "consequence": null, "deadline": {"anchor_event": "discovery that deliveries or withdrawals will be less than 95% of Scheduled Capacity", "kind": "relative", "offset_days": null, "raw_text": "as soon as possible", "recurring_rule": null, "resolved_date": null}, "description": "Customer (Sender) must notify Provider (Transporter) as soon as possible upon finding that deliveries during an operation month at a Point of Entrance or withdrawals at any Point of Exit will be less than 95% of the Scheduled Capacity.", "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}]}

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
- 7 search_corpus: {"query":"Initial Term"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"Renewal"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 get_clause: {"category":"Renewal Term","document_id":"cuad_c7256920fc58b74bbd37"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 get_clause: {"category":"Renewal Notice Date","document_id":"cuad_c7256920fc58b74bbd37"} | ClauseNotFound | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 get_clause: {"category":"Renewal Term Notice Requirement","document_id":"cuad_c7256920fc58b74bbd37"} | ClauseNotFound | retries=0
- 16 llm_response: {"turn":8} | None | retries=0
- 17 get_document_dates: {"document_id":"cuad_c7256920fc58b74bbd37"} | None | retries=0
Terminal args: null

### dev-07 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Audit Rights", "clause_ref": {"category": "Audit Rights", "char_end": 22018, "char_start": 21941}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}, {"clause_category": "Audit Rights", "clause_ref": {"category": "Audit Rights", "char_end": 64836, "char_start": 64464}, "deadline": {"anchor_event": "agreement_termination", "deadline_text": "During the Sale Term", "kind": "relative"}, "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "During the Sale Term, and thereafter until all of Merchant's and Purchaser's and Agent's obligations under this Agreement have been satisfied, Merchant and Purchaser shall have reasonable access to Merchant's and Purchaser's records with respect to the GOB Sale (including, but not limited to Merchandise, GOB Sale Proceeds, and Expenses) to review and audit such records.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"record retention going out of business sale"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"records retention merchant"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_clause: {"category":"Audit Rights","document_id":"cuad_052975b81f9779a680c0"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"books and records available to Purchaser at all times"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 get_document_dates: {"document_id":"cuad_052975b81f9779a680c0"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Audit Rights","clause_quote":"During the Sale Term, and thereafter until all of Merchant's and Purchaser's  | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Audit Rights", "clause_quote": "During the Sale Term, and thereafter until all of Merchant's and Purchaser's and Agent's obligations under this Agreement have been satisfied, Merchant and Purchaser shall have reasonable access to Merchant's and Purchaser's records with respect to the GOB Sale (including, but not limited to Merchandise, GOB Sale Proceeds, and Expenses) to review and audit such records.", "confidence": 0.95, "consequence": null, "deadline": {"kind": "relative", "offset_days": null, "raw_text": "thereafter until all of Merchant's and Purchaser's and Agent's obligations under this Agreement have been satisfied", "resolved_date": null}, "description": "Merchant shall provide reasonable access to its records with respect to the GOB Sale during the Sale Term and thereafter until all obligations under the agreement have been satisfied.", "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}]}

### dev-08 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 56941, "char_start": 56320}, "deadline": {"deadline_text": "during the Term and for a period of three (3) years thereafter (\"Insurance Period\")", "kind": "recurring", "period": "during_term"}, "owed_by": "customer", "type": "INS-COVERAGE"}, {"clause_category": "Covenant Not To Sue", "clause_ref": {"category": "Covenant Not To Sue", "char_end": 16680, "char_start": 15881}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "COV-NO-SUE"}, {"clause_category": "Non-Disparagement", "clause_ref": {"category": "Non-Disparagement", "char_end": 13670, "char_start": 13350}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "COV-NON-DISPARAGEMENT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"renewal"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"covenant"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"Renewal Notice"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"Term"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 search_corpus: {"query":"Section 2"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 search_corpus: {"query":"Term of Agreement"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 get_clause: {"category":"Non-Disparagement","document_id":"cuad_2a450f18c7649b3d7561"} | None | retries=0
- 16 llm_response: {"turn":8} | None | retries=0
- 17 get_clause: {"category":"Exclusivity","document_id":"cuad_2a450f18c7649b3d7561"} | None | retries=0
Terminal args: null

### dev-09 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Irrevocable Or Perpetual License", "clause_ref": {"category": "Irrevocable Or Perpetual License", "char_end": 174659, "char_start": 174486}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"perpetual grant"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_clause: {"category":"Irrevocable Or Perpetual License","document_id":"cuad_03a1e0f461f5359c5502"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"termination by customer convenience or walk-out or breach"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"termination by Ginkgo for convenience or breach"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 search_corpus: {"query":"termination for convenience"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 search_corpus: {"query":"13.2 Termination With Cause"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 search_corpus: {"query":"13.2.1 Material Breach"} | None | retries=0
- 16 llm_response: {"turn":8} | None | retries=0
- 17 get_clause: {"category":"Post-Termination Services","document_id":"cuad_03a1e0f461f5359c5502"} | None | retries=0
Terminal args: null

### dev-10 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Exclusivity", "clause_ref": {"category": "Exclusivity", "char_end": 8940, "char_start": 8636}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "COV-EXCLUSIVITY"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "If the Publishers exercise their right of renewal under Clause 17.1,             then the Publishers shall have a further right of renewal for each             of the subsequent three years, provided that the right to renew             shall be conditional upon the Publishers having exercised their             right in the previous year, and giving notice on or before the 30             September before the renewal is to take effect.", "deadline": {"kind": "recurring", "resolved_date": null}, "owed_by": "customer", "type": "TRM-RENEWAL-NOTICE"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"renewal"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_clause: {"category":"Renewal Term","document_id":"cuad_c72abcf3341f1ecf6365"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_document_dates: {"document_id":"cuad_c72abcf3341f1ecf6365"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"notice"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Renewal Term","clause_quote":"If the Publishers exercise their right of renewal under Clause 17.1,             | VALIDATION_ERROR | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Renewal Term","clause_quote":"If the Publishers exercise their right of renewal under Clause 17.1,             | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Renewal Term", "clause_quote": "If the Publishers exercise their right of renewal under Clause 17.1,             then the Publishers shall have a further right of renewal for each             of the subsequent three years, provided that the right to renew             shall be conditional upon the Publishers having exercised their             right in the previous year, and giving notice on or before the 30             September before the renewal is to take effect.", "confidence": 1, "consequence": "Renewal does not take effect for the subsequent year", "deadline": {"kind": "recurring", "offset_days": null, "raw_text": "on or before the 30 September before the renewal is to take effect", "recurring_rule": "on or before the 30 September before the renewal is to take effect", "resolved_date": null}, "description": "Publisher must give notice of renewal on or before 30 September before the renewal is to take effect.", "owed_by": "customer", "type": "TRM-RENEWAL-NOTICE"}]}

### dev-11 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Non-Compete", "clause_ref": {"category": "Non-Compete", "char_end": 110735, "char_start": 109480}, "deadline": {"anchor_event": "exclusive_period_end", "deadline_text": "During the applicable Exclusive Period", "kind": "relative"}, "owed_by": "customer", "type": "COV-NON-COMPETE"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"exclusive period licensee"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"field-team"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"review exclusive period"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"field team review"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 search_corpus: {"query":"review exclusive period licensee field"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 search_corpus: {"query":"Non-Compete"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 get_clause: {"category":"Non-Compete","document_id":"cuad_1bc91c6dfb434b456f99"} | None | retries=0
- 16 llm_response: {"turn":8} | None | retries=0
- 17 get_clause: {"category":"Competitive Restriction Exception","document_id":"cuad_1bc91c6dfb434b456f99"} | None | retries=0
Terminal args: null

### dev-12 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Revenue/Profit Sharing", "clause_ref": {"category": "Revenue/Profit Sharing", "char_end": 88092, "char_start": 87456}, "deadline": {"anchor_event": "calendar_quarter_start", "deadline_text": "Commencing with the Calendar Quarter commencing on October 1, 2018", "kind": "recurring", "offset_days": null, "period": "quarterly", "resolved_date": null}, "owed_by": "customer", "type": "PAY-REVENUE-SHARE"}, {"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 137403, "char_start": 137034}, "deadline": {"anchor_event": "effective_date", "deadline_text": "during the Term, it shall maintain, through purchase or self- insurance, adequate insurance", "kind": "recurring", "offset_days": null, "period": "continuous", "resolved_date": null}, "owed_by": "both", "type": "INS-COVERAGE"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": [{"clause_quote": "Notwithstanding the above, the sole remedy of Dova for breach of this Section 4.1.2 shall be (i) the adjustment to the promotion fee as set forth in Section 6.1.2 and (ii) the termination right set out in Section 12.2.2.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "customer", "type": "LIA-CAP"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"promotion fee"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"Dova"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"sole remedy of Dova"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 get_clause: {"category":"Cap On Liability","document_id":"cuad_93a7191ff01200e8fe44"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 search_corpus: {"query":"11.4"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 search_corpus: {"query":"11.4 Limitation of Liability"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 search_corpus: {"query":"4.1.2"} | None | retries=0
- 16 llm_response: {"turn":8} | None | retries=0
- 17 record_obligations: {"confidence":0.9,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES"],"obligations":[{"clause_category":"Cap On Liability","clause_quote":"Notwithstanding the above, the sole remedy of Dova  | None | retries=0
Terminal args: {"confidence": 0.9, "escalate": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": [{"clause_category": "Cap On Liability", "clause_quote": "Notwithstanding the above, the sole remedy of Dova for breach of this Section 4.1.2 shall be (i) the adjustment to the promotion fee as set forth in Section 6.1.2 and (ii) the termination right set out in Section 12.2.2.", "confidence": 0.9, "consequence": "Dova's remedies for breach of Section 4.1.2 are limited to promotion fee adjustment and termination right.", "deadline": {"kind": "none", "raw_text": null}, "description": "Limits Dova's remedies for breach of Section 4.1.2 exclusively to promotion fee adjustment and termination.", "owed_by": "customer", "type": "LIA-CAP"}]}

### dev-13 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Source Code Escrow", "clause_ref": {"category": "Source Code Escrow", "char_end": 63335, "char_start": 63120}, "deadline": {"anchor_event": "effective_date", "deadline_text": "Within sixty (60) days of the Effective Date", "kind": "relative", "offset_days": 60}, "owed_by": "provider", "type": "LIC-SOURCE-ESCROW"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES", "E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "This Agreement shall be governed by the laws of the State of California, USA, excluding conflict of laws provisions and excluding the 1980 United Nations Convention on Contracts for the International Sale of Goods.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "unclear", "type": "COV-NO-SUE"}, {"clause_quote": "This Agreement shall be governed by and construed in accordance with the laws of the State of New York without reference to its conflict or choice of law rules or principles.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "unclear", "type": "COV-NO-SUE"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"governing law jurisdiction dispute sue"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"Governing Law State of New York this Agreement shall be governed"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_clause: {"category":"Governing Law","document_id":"cuad_5c2a9dcbe0cc7593bb1d"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 record_obligations: {"confidence":1,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES"],"obligations":[{"clause_category":"Governing Law","clause_quote":"This Agreement shall be governed by the laws of the Stat | None | retries=0
Terminal args: {"confidence": 1, "escalate": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": [{"clause_category": "Governing Law", "clause_quote": "This Agreement shall be governed by the laws of the State of California, USA, excluding conflict of laws provisions and excluding the 1980 United Nations Convention on Contracts for the International Sale of Goods.", "confidence": 1, "consequence": null, "deadline": {"kind": "none", "raw_text": null}, "description": "Governing law specifies the laws of the State of California.", "owed_by": "unclear", "type": "COV-NO-SUE"}, {"clause_category": "Governing Law", "clause_quote": "This Agreement shall be governed by and construed in accordance with the laws of the State of New York without reference to its conflict or choice of law rules or principles.", "confidence": 1, "consequence": null, "deadline": {"kind": "none", "raw_text": null}, "description": "Governing law specifies the laws of the State of New York.", "owed_by": "unclear", "type": "COV-NO-SUE"}]}

### dev-14 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 48136, "char_start": 47917}, "deadline": {"anchor_event": "unresolved", "anchor_resolved": false, "deadline_text": "at all times during the Term and [*****]", "kind": "relative", "offset_days": null, "resolved_date": null}, "owed_by": "customer", "type": "INS-COVERAGE"}, {"clause_category": "Audit Rights", "clause_ref": {"category": "Audit Rights", "char_end": 36652, "char_start": 36541}, "deadline": {"anchor_event": "unresolved", "anchor_resolved": false, "deadline_text": "no later than [*****] prior to such audit", "kind": "relative", "offset_days": null, "resolved_date": null}, "owed_by": "provider", "type": "CTL-AUDIT-RIGHT"}, {"clause_category": "Warranty Duration", "clause_ref": {"category": "Warranty Duration", "char_end": 53701, "char_start": 53349}, "deadline": {"anchor_event": "delivery", "anchor_resolved": false, "deadline_text": "shall end [*****] thereafter", "kind": "relative", "offset_days": null, "resolved_date": null}, "owed_by": "provider", "type": "WAR-DURATION"}], "escalation": ["E3_CONDITIONAL_OR_AMBIGUOUS"]}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"warranty"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_clause: {"category":"Warranty Duration","document_id":"cuad_08636f6df2840b29991a"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"insurance"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 get_clause: {"category":"Insurance","document_id":"cuad_08636f6df2840b29991a"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Insurance","clause_quote":"Without prejudice to any term and condition under this Agreement, the Company sh | VALIDATION_ERROR | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Insurance","clause_quote":"Without prejudice to any term and condition under this Agreement, the Company sh | VALIDATION_ERROR | retries=0
Terminal args: null

### dev-15 — clear, constructed=False, difficulty 1
Failed: escalation_correct
Gold: {"obligations": [], "escalation": ["E1_NO_OBLIGATION"]}
Got: {"escalated": false, "escalation_codes": [], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"agreement"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"agreement by and among them"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_document_dates: {"document_id":"cuad_cdbbcb9c511d8f86fe50"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": []}

- dev-16 (out_of_scope, constructed=False): pass
### dev-17 — out_of_scope, constructed=False, difficulty 2
Failed: escalation_correct
Gold: {"obligations": [], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "AEIS and/or their appointed representatives of AEIS or                   American Express Travel Related Services Inc. as solely                   determined by AEIS, shall be entitled to inspect and approve                   Seller's safekeeping facilities at any time during normal                   business hours.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "provider", "type": "CTL-AUDIT-RIGHT"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"audit"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"Audit Rights"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_clause: {"category":"Audit Rights","document_id":"cuad_b1fe09126a4d0b840349"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"books and records"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 get_document_dates: {"document_id":"cuad_b1fe09126a4d0b840349"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Audit Rights","clause_quote":"AEIS and/or their appointed representatives of AEIS or                   America | VALIDATION_ERROR | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Audit Rights","clause_quote":"AEIS and/or their appointed representatives of AEIS or                   America | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Audit Rights", "clause_quote": "AEIS and/or their appointed representatives of AEIS or                   American Express Travel Related Services Inc. as solely                   determined by AEIS, shall be entitled to inspect and approve                   Seller's safekeeping facilities at any time during normal                   business hours.", "confidence": 1, "consequence": null, "deadline": {"kind": "none", "raw_text": null}, "description": "Licensor (AEIS) has the right to inspect and approve Seller's safekeeping facilities at any time during normal business hours.", "owed_by": "provider", "type": "CTL-AUDIT-RIGHT"}]}

- dev-18 (out_of_scope, constructed=False): pass
- dev-19 (out_of_scope, constructed=False): pass
### dev-21 — adversarial, constructed=False, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 56941, "char_start": 56320}, "deadline": {"deadline_text": "during the Term and for a period of three (3) years thereafter (\"Insurance Period\")", "kind": "recurring", "period": "during_term"}, "owed_by": "customer", "type": "INS-COVERAGE"}, {"clause_category": "Covenant Not To Sue", "clause_ref": {"category": "Covenant Not To Sue", "char_end": 16680, "char_start": 15881}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "COV-NO-SUE"}, {"clause_category": "Non-Disparagement", "clause_ref": {"category": "Non-Disparagement", "char_end": 13670, "char_start": 13350}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "COV-NON-DISPARAGEMENT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"covenant"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"solicit"} | None | retries=0
- 6 search_corpus: {"query":"compete"} | None | retries=0
- 7 search_corpus: {"query":"disparagement"} | None | retries=0
- 8 search_corpus: {"query":"exclusive"} | None | retries=0
- 9 llm_response: {"turn":3} | None | retries=0
- 10 get_clause: {"category":"Non-Disparagement","document_id":"adv_3e86dc8c4eb1f1086d9d"} | None | retries=0
- 11 get_clause: {"category":"Covenant Not To Sue","document_id":"adv_3e86dc8c4eb1f1086d9d"} | None | retries=0
- 12 llm_response: {"turn":4} | None | retries=0
- 13 search_corpus: {"query":"insurance"} | None | retries=0
- 14 search_corpus: {"query":"indemnification"} | None | retries=0
- 15 llm_response: {"turn":5} | None | retries=0
- 16 get_document_dates: {"document_id":"adv_3e86dc8c4eb1f1086d9d"} | None | retries=0
- 17 llm_response: {"turn":6} | None | retries=0
- 18 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Non-Disparagement","clause_quote":"PAPA JOHN'S shall not, during the Term or at any time thereafter: (I) de | VALIDATION_ERROR | retries=0
- 19 llm_response: {"turn":7} | None | retries=0
- 20 search_corpus: {"query":"PAPA JOHN'S shall not, during the Term or at any time thereafter: (I) defame or disparage"} | None | retries=0
- 21 llm_response: {"turn":8} | None | retries=0
- 22 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Non-Disparagement","clause_quote":"PAPA JOHN'S shall not, during the Term or at any time thereafter: (i) de | VALIDATION_ERROR | retries=0
Terminal args: null

### dev-22 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Source Code Escrow", "clause_ref": {"category": "Source Code Escrow", "char_end": 63335, "char_start": 63120}, "deadline": {"anchor_event": "effective_date", "deadline_text": "Within sixty (60) days of the Effective Date", "kind": "relative", "offset_days": 60}, "owed_by": "provider", "type": "LIC-SOURCE-ESCROW"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"law governs dispute dispute resolution jurisdiction governing law"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_clause: {"category":"Governing Law","document_id":"composite_d8416b5fddd1d8074804"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"governing law California New York conflicting governing law"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 record_obligations: {"confidence":0.85,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES"],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 0.85, "escalate": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": []}

### dev-23 — conflicting, constructed=True, difficulty 3
Failed: execution error
Gold: {"obligations": [{"clause_category": "Irrevocable Or Perpetual License", "clause_ref": {"category": "Irrevocable Or Perpetual License", "char_end": 8913, "char_start": 7675}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES", "E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "Subject to the terms and conditions of this          Agreement, Changepoint hereby grants to Corio a fee-bearing,          irrevocable, nonexclusive, nontransferable (except in accordance with          Section 14.1 of this Agreement) license in the Territory to (i)          reproduce the Software in machine executable object code format only          for installation on the Corio Servers; (ii) install multiple copies of          the Software on Corio's Servers which will be made remotely accessible          to Corio's Customers for their internal business purposes, (iii) permit          limited access to and use of the Software by Customers through Corio          Servers solely for such Customer's internal business purposes; (iv)          sublicense an unlimited number of Customers to access and use the          Software only through the installation on Corio Servers solely for such          Customer's internal business purposes; and (v) use Changepoint's tools          and utilities, if any, subject to any restrictions placed on the          Changepoint by third party software providers and payment of any          applicable fees required by such third parties, to configure, integrate          and manage the Software. Corio shall not authorize Customers to          download or reproduce the Software for use except as necessary in          connection with the Corio Services.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "provider", "type": "LIC-GRANT"}, {"clause_quote": "Either Party shall have the right to terminate this Agreement before the end of the Term for its convenience upon [***] written notice to the other Party (and any such termination shall become effective at the end of such [***]); [***].", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "both", "type": "TRM-CONVENIENCE"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"grant irrevocable"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"irrevocable license"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"termination convenience"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 get_clause: {"category":"Termination For Convenience","document_id":"composite_c5f9c6f4c2dbbf26ad52"} | None | retries=0
- 10 get_clause: {"category":"License Grant","document_id":"composite_c5f9c6f4c2dbbf26ad52"} | None | retries=0
- 11 llm_response: {"turn":5} | None | retries=0
- 12 search_corpus: {"query":"irrevocable license terminate convenience"} | None | retries=0
- 13 llm_response: {"turn":6} | None | retries=0
- 14 record_obligations: {"confidence":0.95,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES"],"obligations":[{"clause_category":"License Grant","clause_quote":"Subject to the terms and conditions of this           | VALIDATION_ERROR | retries=0
- 15 llm_response: {"turn":7} | None | retries=0
- 16 record_obligations: {"confidence":0.95,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES"],"obligations":[{"clause_category":"License Grant","clause_quote":"Subject to the terms and conditions of this           | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": [{"clause_category": "License Grant", "clause_quote": "Subject to the terms and conditions of this          Agreement, Changepoint hereby grants to Corio a fee-bearing,          irrevocable, nonexclusive, nontransferable (except in accordance with          Section 14.1 of this Agreement) license in the Territory to (i)          reproduce the Software in machine executable object code format only          for installation on the Corio Servers; (ii) install multiple copies of          the Software on Corio's Servers which will be made remotely accessible          to Corio's Customers for their internal business purposes, (iii) permit          limited access to and use of the Software by Customers through Corio          Servers solely for such Customer's internal business purposes; (iv)          sublicense an unlimited number of Customers to access and use the          Software only through the installation on Corio Servers solely for such          Customer's internal business purposes; and (v) use Changepoint's tools          and utilities, if any, subject to any restrictions placed on the          Changepoint by third party software providers and payment of any          applicable fees required by such third parties, to configure, integrate          and manage the Software. Corio shall not authorize Customers to          download or reproduce the Software for use except as nec

### dev-24 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Post-Termination Services", "clause_ref": {"category": "Post-Termination Services", "char_end": 350136, "char_start": 349788}, "deadline": {"anchor_event": "termination", "deadline_text": "during the term of the Agreement and for three (3) years thereafter", "kind": "relative", "offset_days": 1095}, "owed_by": "provider", "type": "CTL-AUDIT-RIGHT"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "Manufacturer will maintain complete and accurate Records. Any Records that are financial in nature such as, but not limited to, time sheets, billing Records, invoices, payment applications, payments of consultants and subcontractors and receipts relating to reimbursable expenses shall be maintained in accordance with applicable Law in the jurisdiction in which the applicable Facility is located. Manufacturer shall maintain such Records for a period equal to the later of (x) three (3) years after the expiration or termination of this Agreement or the applicable Facility Addendum, (y) the expiration of the statute of limitation for the Tax period applicable to such Records, or (z) for such period as otherwise may be required by applicable Law (the \"Record Retention Period\").", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "provider", "type": "SVC-POST-TERMINATION"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"customer claims records audit retention downstream"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"customer claims warranty downstream complaints product quality records manufacturer"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"Manufacturer will maintain complete and accurate Records"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 get_clause: {"category":"Audit Rights","document_id":"composite_1d5bf00304e51a76f89c"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 search_corpus: {"query":"Record Retention Period three years expiration termination statute of limitation Tax"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 get_document_dates: {"document_id":"composite_1d5bf00304e51a76f89c"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Audit Rights","clause_quote":"Manufacturer will maintain complete and accurate Records. Any Records that ar | VALIDATION_ERROR | retries=0
- 16 llm_response: {"turn":8} | None | retries=0
- 17 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Audit Rights","clause_quote":"Manufacturer will maintain complete and accurate Records. Any Records that ar | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Audit Rights", "clause_quote": "Manufacturer will maintain complete and accurate Records. Any Records that are financial in nature such as, but not limited to, time sheets, billing Records, invoices, payment applications, payments of consultants and subcontractors and receipts relating to reimbursable expenses shall be maintained in accordance with applicable Law in the jurisdiction in which the applicable Facility is located. Manufacturer shall maintain such Records for a period equal to the later of (x) three (3) years after the expiration or termination of this Agreement or the applicable Facility Addendum, (y) the expiration of the statute of limitation for the Tax period applicable to such Records, or (z) for such period as otherwise may be required by applicable Law (the \"Record Retention Period\").", "confidence": 0.95, "consequence": null, "deadline": {"anchor_event": "expiration or termination of this Agreement or the applicable Facility Addendum", "kind": "relative", "offset_days": 1095, "raw_text": "three (3) years after the expiration or termination of this Agreement or the applicable Facility Addendum", "resolved_date": null}, "description": "Manufacturer must maintain complete and accurate records (including financial records, timesheets, billing records, invoices, payment applications, payments to consultants/subcontractors, and reimbursable expense receipts) f

- dev-25 (conflicting, constructed=True): pass
### dev-26 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Cap On Liability", "clause_ref": {"category": "Cap On Liability", "char_end": 62596, "char_start": 61222}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIA-UNCAPPED"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": false, "escalation_codes": [], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"liability cap cash exposure survive"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"Limitation of Liability"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_clause: {"category":"Cap On Liability","document_id":"composite_8fd5f85004f4197e9df5"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"Section 2.5(e)"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 search_corpus: {"query":"Section 2.5(e) Triggering Event"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 get_document_dates: {"document_id":"composite_8fd5f85004f4197e9df5"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 record_obligations: {"confidence":0.9,"escalate":false,"escalation_codes":[],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 0.9, "escalate": false, "escalation_codes": [], "obligations": []}

### dev-20 — adversarial, constructed=False, difficulty 1
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Warranty Duration", "clause_ref": {"category": "Warranty Duration", "char_end": 25665, "char_start": 25205}, "deadline": {"anchor_event": "installation", "deadline_text": "for a period of one (1) year following Installation of the Products at Customer's facility", "kind": "relative", "offset_days": 365}, "owed_by": "provider", "type": "WAR-DURATION"}, {"clause_category": "License Grant", "clause_ref": {"category": "License Grant", "char_end": 52836, "char_start": 52564}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}, {"clause_category": "Post-Termination Services", "clause_ref": {"category": "Post-Termination Services", "char_end": 38322, "char_start": 38022}, "deadline": {"anchor_event": "last_shipment", "deadline_text": "for a minimum period of 10 years after the last shipment of a System pursuant to this Agreement", "kind": "relative", "offset_days": 3650}, "owed_by": "provider", "type": "SVC-POST-TERMINATION"}], "escalation": []}
Got: {"escalated": false, "escalation_codes": [], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"queries":"distributor"} | VALIDATION_ERROR | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"distributor"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"Accuray shall"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"indemnify"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 search_corpus: {"query":"confidential"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 search_corpus: {"query":"non-compete"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": []}

