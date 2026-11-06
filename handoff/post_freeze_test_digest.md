# Failure digest

Split: test; mode: live; cases: 30

## Aggregate metrics

```json
{
  "constructed_e2_cases": 9,
  "constructed_e2_exception_rate": {
    "denominator": 9,
    "numerator": 9,
    "value": 1.0,
    "wilson_95": [
      0.7008549515804559,
      1
    ]
  },
  "constructed_e2_recall": {
    "denominator": 9,
    "numerator": 3,
    "value": 0.3333333333333333,
    "wilson_95": [
      0.1205838183869109,
      0.6457978644196036
    ]
  },
  "cost": {
    "mean_usd": 0.007870434333333332,
    "n": 30
  },
  "deadline_absolute": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_none": {
    "denominator": 18,
    "numerator": 1,
    "value": 0.05555555555555555,
    "wilson_95": [
      0.009875190978303097,
      0.25757300781872594
    ]
  },
  "deadline_recurring": {
    "denominator": 18,
    "numerator": 3,
    "value": 0.16666666666666666,
    "wilson_95": [
      0.05836576805861446,
      0.39222038103915724
    ]
  },
  "deadline_relative": {
    "denominator": 5,
    "numerator": 1,
    "value": 0.2,
    "wilson_95": [
      0.03622410863243014,
      0.6244653702374747
    ]
  },
  "escalation_recall": {
    "denominator": 9,
    "numerator": 7,
    "value": 0.7777777777777778,
    "wilson_95": [
      0.45258896910698887,
      0.9367748928821533
    ]
  },
  "exception_rate": {
    "denominator": 30,
    "numerator": 29,
    "value": 0.9666666666666667,
    "wilson_95": [
      0.8332960900859082,
      0.9940914096183874
    ]
  },
  "false_escalation": {
    "denominator": 21,
    "numerator": 17,
    "value": 0.8095238095238095,
    "wilson_95": [
      0.5999943530979508,
      0.9233243494723822
    ]
  },
  "grounded_rate": {
    "denominator": 38,
    "numerator": 38,
    "value": 1.0,
    "wilson_95": [
      0.908190131774416,
      0.9999999999999999
    ]
  },
  "latency": {
    "n": 30,
    "p50_ms": 74656.0,
    "p95_ms": 120603.0
  },
  "mode": "live",
  "obligation_recall": {
    "denominator": 41,
    "numerator": 11,
    "value": 0.2682926829268293,
    "wilson_95": [
      0.1569496404781167,
      0.41933533107076637
    ]
  },
  "split": "test"
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
    "mean_usd": 0.006568615,
    "n": 4
  },
  "deadline_absolute": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_none": {
    "denominator": 2,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      0,
      0.6576197724933469
    ]
  },
  "deadline_recurring": {
    "denominator": 5,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      0,
      0.43448246478317476
    ]
  },
  "deadline_relative": {
    "denominator": 1,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      0,
      0.7934506856227626
    ]
  },
  "escalation_recall": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "exception_rate": {
    "denominator": 4,
    "numerator": 4,
    "value": 1.0,
    "wilson_95": [
      0.5101091635454027,
      1
    ]
  },
  "false_escalation": {
    "denominator": 4,
    "numerator": 3,
    "value": 0.75,
    "wilson_95": [
      0.30064184258240184,
      0.9544127391902995
    ]
  },
  "grounded_rate": {
    "denominator": 9,
    "numerator": 9,
    "value": 1.0,
    "wilson_95": [
      0.7008549515804559,
      1
    ]
  },
  "latency": {
    "n": 4,
    "p50_ms": 45461.0,
    "p95_ms": 103180.7
  },
  "obligation_recall": {
    "denominator": 8,
    "numerator": 1,
    "value": 0.125,
    "wilson_95": [
      0.02241749145005667,
      0.4708881822128535
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
    "mean_usd": 0.008553511666666666,
    "n": 12
  },
  "deadline_absolute": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_none": {
    "denominator": 10,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      0,
      0.2775327998628892
    ]
  },
  "deadline_recurring": {
    "denominator": 11,
    "numerator": 3,
    "value": 0.2727272727272727,
    "wilson_95": [
      0.09746059290024889,
      0.5656453011761291
    ]
  },
  "deadline_relative": {
    "denominator": 3,
    "numerator": 1,
    "value": 0.3333333333333333,
    "wilson_95": [
      0.06149194472039621,
      0.7923403991979522
    ]
  },
  "escalation_recall": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "exception_rate": {
    "denominator": 12,
    "numerator": 12,
    "value": 1.0,
    "wilson_95": [
      0.7575059933447592,
      1
    ]
  },
  "false_escalation": {
    "denominator": 12,
    "numerator": 11,
    "value": 0.9166666666666666,
    "wilson_95": [
      0.646120088858883,
      0.9851349055950829
    ]
  },
  "grounded_rate": {
    "denominator": 21,
    "numerator": 21,
    "value": 1.0,
    "wilson_95": [
      0.8453609810751531,
      1
    ]
  },
  "latency": {
    "n": 12,
    "p50_ms": 76640.5,
    "p95_ms": 128349.9
  },
  "obligation_recall": {
    "denominator": 24,
    "numerator": 9,
    "value": 0.375,
    "wilson_95": [
      0.21159367559548778,
      0.5729003755732572
    ]
  }
}
```
### conflicting
```json
{
  "constructed_e2_cases": 9,
  "constructed_e2_exception_rate": {
    "denominator": 9,
    "numerator": 9,
    "value": 1.0,
    "wilson_95": [
      0.7008549515804559,
      1
    ]
  },
  "constructed_e2_recall": {
    "denominator": 9,
    "numerator": 3,
    "value": 0.3333333333333333,
    "wilson_95": [
      0.1205838183869109,
      0.6457978644196036
    ]
  },
  "cost": {
    "mean_usd": 0.006883714444444442,
    "n": 9
  },
  "deadline_absolute": {
    "denominator": 0,
    "numerator": 0,
    "value": null,
    "wilson_95": null
  },
  "deadline_none": {
    "denominator": 6,
    "numerator": 1,
    "value": 0.16666666666666666,
    "wilson_95": [
      0.030053369748306635,
      0.5635028221864702
    ]
  },
  "deadline_recurring": {
    "denominator": 2,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      0,
      0.6576197724933469
    ]
  },
  "deadline_relative": {
    "denominator": 1,
    "numerator": 0,
    "value": 0.0,
    "wilson_95": [
      0,
      0.7934506856227626
    ]
  },
  "escalation_recall": {
    "denominator": 9,
    "numerator": 7,
    "value": 0.7777777777777778,
    "wilson_95": [
      0.45258896910698887,
      0.9367748928821533
    ]
  },
  "exception_rate": {
    "denominator": 9,
    "numerator": 9,
    "value": 1.0,
    "wilson_95": [
      0.7008549515804559,
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
    "denominator": 4,
    "numerator": 4,
    "value": 1.0,
    "wilson_95": [
      0.5101091635454027,
      1
    ]
  },
  "latency": {
    "n": 9,
    "p50_ms": 73547.0,
    "p95_ms": 120121.6
  },
  "obligation_recall": {
    "denominator": 9,
    "numerator": 1,
    "value": 0.1111111111111111,
    "wilson_95": [
      0.019890887638544907,
      0.434999705576656
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
    "mean_usd": 0.0090486,
    "n": 5
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
    "denominator": 5,
    "numerator": 4,
    "value": 0.8,
    "wilson_95": [
      0.37553462976252533,
      0.9637758913675698
    ]
  },
  "false_escalation": {
    "denominator": 5,
    "numerator": 3,
    "value": 0.6,
    "wilson_95": [
      0.2307242812760128,
      0.882379225767352
    ]
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
    "p50_ms": 74828.0,
    "p95_ms": 117684.2
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

### test-01 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 123159, "char_start": 120940}, "deadline": {"anchor_event": "effective_date", "deadline_text": "during the term of this Agreement", "kind": "recurring", "period": "term"}, "owed_by": "customer", "type": "INS-COVERAGE"}, {"clause_category": "Minimum Commitment", "clause_ref": {"category": "Minimum Commitment", "char_end": 22887, "char_start": 22534}, "deadline": {"anchor_event": "commencement_date", "deadline_text": "beginning six (6) months after the Commencement Date", "kind": "recurring", "offset_days": 180, "period": "monthly"}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "19.3.3 Own, maintain, develop, operate, engage in, franchise or license, make loans to, lease real or personal property to, be associated with, accept any compensation or remuneration from, and/or have any whatsoever interest in, or render services or give advice to, any Competitive Business.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "customer", "type": "COV-NON-COMPETE"}, {"clause_quote": "19.3.1 Divert or attempt to divert any actual or potential business or customer of any Goosehead Business to any competitor or otherwise take any action injurious or prejudicial to the goodwill associated with the Marks and the System.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "customer", "type": "COV-NO-SOLICIT-CUSTOMER"}, {"clause_quote": "19.3.2 Employ or seek to employ any person who is then employed by us or any other Goosehead Business franchisee or developer, or otherwise directly or indirectly induce such person to leave his or her employment.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "customer", "type": "COV-NO-SOLICIT-EMPLOYEE"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"covenant"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_clause: {"category":"Non-Compete","document_id":"cuad_c92227514f576d98317e"} | None | retries=0
- 6 get_clause: {"category":"No-Solicit Of Customers","document_id":"cuad_c92227514f576d98317e"} | None | retries=0
- 7 get_clause: {"category":"No-Solicit Of Employees","document_id":"cuad_c92227514f576d98317e"} | None | retries=0
- 8 llm_response: {"turn":3} | None | retries=0
- 9 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Non-Compete","clause_quote":"19.3.3 Own, maintain, develop, operate, engage in, franchise or license, make  | VALIDATION_ERROR | retries=0
- 10 llm_response: {"turn":4} | None | retries=0
- 11 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Non-Compete","clause_quote":"19.3.3 Own, maintain, develop, operate, engage in, franchise or license, make  | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Non-Compete", "clause_quote": "19.3.3 Own, maintain, develop, operate, engage in, franchise or license, make loans to, lease real or personal property to, be associated with, accept any compensation or remuneration from, and/or have any whatsoever interest in, or render services or give advice to, any Competitive Business.", "confidence": 0.95, "consequence": null, "deadline": {"anchor_event": "expiration or termination of this Agreement, and/or a transfer as contemplated in Section 16 above", "kind": "relative", "offset_days": null, "raw_text": "during the term of this Agreement and for a continuous period of two (2) years after the expiration or termination of this Agreement, and/or a transfer as contemplated in Section 16 above", "resolved_date": null}, "description": "Do not own, maintain, develop, operate, engage in, franchise or license, make loans to, lease real or personal property to, be associated with, accept any compensation or remuneration from, and/or have any whatsoever interest in, or render services or give advice to, any Competitive Business during the term and for two years post-term/transfer.", "owed_by": "customer", "type": "COV-NON-COMPETE"}, {"clause_category": "No-Solicit Of Customers", "clause_quote": "19.3.1 Divert or attempt to divert any actual or potential business or customer of any Goosehead Business to any competitor or otherwise take any action

### test-02 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct
Gold: {"obligations": [{"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 139324, "char_start": 138971}, "deadline": {"anchor_event": "effective_date", "kind": "recurring", "period": "term"}, "owed_by": "customer", "type": "INS-COVERAGE"}, {"clause_category": "Revenue/Profit Sharing", "clause_ref": {"category": "Revenue/Profit Sharing", "char_end": 44082, "char_start": 43715}, "deadline": {"anchor_event": "effective_date", "deadline_text": "a  continuing  Royalty of seven  percent  (7%)", "kind": "recurring", "period": "weekly"}, "owed_by": "customer", "type": "PAY-REVENUE-SHARE"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "Franchisee,  in  partial  consideration  of the  grant of a  franchise, agrees to pay to Pretzel  Time a  continuing  Royalty of seven  percent  (7%) of Franchisee's  net  revenues  (as  defined  in  Section  1) on a weekly  basis as specified in this  Section;  provided  only 4% Royalty  shall be payable on TCBY frozen yogurt and other TCBY frozen yogurt products.", "deadline": {"kind": "recurring", "resolved_date": null}, "owed_by": "customer", "type": "PAY-REVENUE-SHARE"}, {"clause_quote": "Franchisee shall maintain at Franchisee's expense, in form, amounts and with insurers  satisfactory  to Pretzel Time,  which  insurers must have an A.M. Best  Company  rating of \"A-\" or better and naming  Pretzel  Time an  additional insured,  insurance  against all types of public  liability with personal injury coverage and property damage coverage.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "customer", "type": "INS-COVERAGE"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"renewal"} | None | retries=0
- 4 search_corpus: {"query":"royalty"} | None | retries=0
- 5 search_corpus: {"query":"insurance"} | None | retries=0
- 6 llm_response: {"turn":2} | None | retries=0
- 7 get_clause: {"category":"Insurance","document_id":"cuad_7714bf6314a468cda863"} | None | retries=0
- 8 get_clause: {"category":"Revenue/Profit Sharing","document_id":"cuad_7714bf6314a468cda863"} | None | retries=0
- 9 llm_response: {"turn":3} | None | retries=0
- 10 search_corpus: {"query":"Franchisee shall maintain at Franchisee's expense"} | None | retries=0
- 11 search_corpus: {"query":"Franchisee shall pay weekly by electronic funds transfer"} | None | retries=0
- 12 search_corpus: {"query":"renewal fee is due and payable thirty days prior"} | None | retries=0
- 13 llm_response: {"turn":4} | None | retries=0
- 14 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Revenue/Profit Sharing","clause_quote":"Franchisee,  in  partial  consideration  of the  grant of a  franch | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Revenue/Profit Sharing", "clause_quote": "Franchisee,  in  partial  consideration  of the  grant of a  franchise, agrees to pay to Pretzel  Time a  continuing  Royalty of seven  percent  (7%) of Franchisee's  net  revenues  (as  defined  in  Section  1) on a weekly  basis as specified in this  Section;  provided  only 4% Royalty  shall be payable on TCBY frozen yogurt and other TCBY frozen yogurt products.", "confidence": 0.95, "consequence": null, "deadline": {"kind": "recurring", "raw_text": "on a weekly basis as specified in this Section", "recurring_rule": "weekly"}, "description": "Franchisee agrees to pay to Pretzel Time a continuing Royalty of seven percent (7%) of Franchisee's net revenues (or 4% on TCBY frozen yogurt products) on a weekly basis.", "owed_by": "customer", "type": "PAY-REVENUE-SHARE"}, {"clause_category": "Insurance", "clause_quote": "Franchisee shall maintain at Franchisee's expense, in form, amounts and with insurers  satisfactory  to Pretzel Time,  which  insurers must have an A.M. Best  Company  rating of \"A-\" or better and naming  Pretzel  Time an  additional insured,  insurance  against all types of public  liability with personal injury coverage and property damage coverage.", "confidence": 0.95, "consequence": null, "deadline": {"kind": "none", "raw_text": "at all times during the term (implied by maintenance)"}, "description": "Franchisee shal

### test-03 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 49821, "char_start": 48360}, "deadline": {"anchor_event": "effective_date", "deadline_text": "during the Term", "kind": "recurring", "period": "term"}, "owed_by": "provider", "type": "INS-COVERAGE"}, {"clause_category": "Post-Termination Services", "clause_ref": {"category": "Post-Termination Services", "char_end": 7514, "char_start": 7007}, "deadline": {"anchor_event": "termination", "anchor_resolved": false, "deadline_text": "all necessary assistance to facilitate the orderly transition of Services", "kind": "relative"}, "owed_by": "provider", "type": "SVC-POST-TERMINATION"}], "escalation": []}
Got: {"escalated": false, "escalation_codes": [], "obligations": [{"clause_quote": "In addition, Metavante agrees to provide to Customer, at Customer's expense, all necessary assistance to facilitate the orderly transition of Services to Customer or its designee (\"Termination Assistance\"). As part of the Termination Assistance, Metavante shall assist Customer to develop a plan for the transition of all Services then being performed by Metavante under this Agreement, from Metavante to Customer or Customer's designee, on a reasonable schedule developed jointly by Metavante and Customer.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "provider", "type": "SVC-POST-TERMINATION"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"conversion"} | None | retries=0
- 4 search_corpus: {"query":"continuing duties"} | None | retries=0
- 5 llm_response: {"turn":2} | None | retries=0
- 6 search_corpus: {"query":"Metavante shall continue to provide"} | None | retries=0
- 7 search_corpus: {"query":"after Conversion"} | None | retries=0
- 8 llm_response: {"turn":3} | None | retries=0
- 9 get_clause: {"category":"Post-Termination Services","document_id":"cuad_3d9c71ed150a6a3c3f1f"} | None | retries=0
- 10 llm_response: {"turn":4} | None | retries=0
- 11 search_corpus: {"query":"Services specified"} | None | retries=0
- 12 llm_response: {"turn":5} | None | retries=0
- 13 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Post-Termination Services","clause_quote":"In addition, Metavante agrees to provide to Customer, at Custome | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Post-Termination Services", "clause_quote": "In addition, Metavante agrees to provide to Customer, at Customer's expense, all necessary assistance to facilitate the orderly transition of Services to Customer or its designee (\"Termination Assistance\"). As part of the Termination Assistance, Metavante shall assist Customer to develop a plan for the transition of all Services then being performed by Metavante under this Agreement, from Metavante to Customer or Customer's designee, on a reasonable schedule developed jointly by Metavante and Customer.", "confidence": 0.95, "consequence": null, "deadline": {"kind": "none", "raw_text": "none"}, "description": "Provide necessary assistance and assist in developing a plan for the orderly transition of Services to Customer or its designee upon termination (Termination Assistance).", "owed_by": "provider", "type": "SVC-POST-TERMINATION"}]}

### test-04 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "License Grant", "clause_ref": {"category": "License Grant", "char_end": 26760, "char_start": 26271}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}, {"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 134646, "char_start": 134467}, "deadline": {"anchor_event": "effective_date", "deadline_text": "shall maintain product liability and other appropriate insurance", "kind": "recurring", "period": "term"}, "owed_by": "both", "type": "INS-COVERAGE"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"supplier"} | None | retries=0
- 4 search_corpus: {"query":"distributor"} | None | retries=0
- 5 search_corpus: {"query":"shall"} | None | retries=0
- 6 llm_response: {"turn":2} | None | retries=0
- 7 search_corpus: {"query":"Zogenix shall"} | None | retries=0
- 8 search_corpus: {"query":"Supplier shall"} | None | retries=0
- 9 search_corpus: {"query":"supply agreement terms"} | None | retries=0
- 10 llm_response: {"turn":3} | None | retries=0
- 11 search_corpus: {"query":"Promptly after the Effective Date, the Parties shall commence negotiating a supply agreement"} | None | retries=0
- 12 llm_response: {"turn":4} | None | retries=0
- 13 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"License Grant","clause_quote":"Zogenix shall supply, or cause to be supplied, Product to Distributor in accord | VALIDATION_ERROR | retries=0
- 14 llm_response: {"turn":5} | None | retries=0
- 15 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"License Grant","clause_quote":"Zogenix shall supply, or cause to be supplied, Product to Distributor in accord | VALIDATION_ERROR | retries=0
Terminal args: null

### test-05 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "License Grant", "clause_ref": {"category": "License Grant", "char_end": 73394, "char_start": 72888}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}, {"clause_category": "Ip Ownership Assignment", "clause_ref": {"category": "Ip Ownership Assignment", "char_end": 118642, "char_start": 118335}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "IP-OWNERSHIP-ASSIGNMENT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "Sanofi shall, at RevMed's request, for a period not to exceed [***] following the effective date of termination, provide reasonable technical assistance up to a total of [***] and, to the extent not already provided to RevMed, transfer copies of (including when available, in electronic format) all Sanofi Sole Program Know-How to RevMed or its designee, including without limitation: [***], in each case to the extent such materials are exclusively related to the Termination Product.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "provider", "type": "SVC-POST-TERMINATION"}, {"clause_quote": "Furthermore, Sanofi shall within [***] after the effective date of such termination, transfer to RevMed all files and documents relating to the prosecution, defense or enforcement of the RevMed Licensed Patents or Joint Program Patents and provide reasonable assistance for a period not to exceed [***] following the effective date of termination, up to a total of [***], in the transfer of the prosecution, defense and enforcement responsibilities to RevMed, including by executing any documents reasonable necessary therefor.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "provider", "type": "SVC-POST-TERMINATION"}, {"clause_quote": "At the end of the sell-off period set forth in Section 12.3(c)(iii), Sanofi shall transfer to RevMed any and all inventory of SHP2 Inhibitors and Termination Products (including all research materials, final product, bulk drug substance, intermediates, work-in-process, formulation materials, reference standards, drug product clinical reserve samples, packaged retention samples, and the like) then in the possession of Sanofi, its Affiliates or Sublicensees, and continue or have continued any ongoing stability studies pertaining to any materials so transferred to RevMed for a reasonable period of time until RevMed can assume responsibility for such activities", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "provider", "type": "SVC-POST-TERMINATION"}, {"clause_quote": "In addition to the foregoing, Sanofi shall use reasonable efforts with respect to those activities for which it is responsible hereunder to cooperate with RevMed to achieve an orderly transition of the Development, Manufacturing and Commercialization of Termination Products from Sanofi or its applicable Affiliate to RevMed.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "provider", "type": "SVC-POST-TERMINATION"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"exit hand-over termination transition"} | None | retries=0
- 4 search_corpus: {"query":"post-termination transition hand-over"} | None | retries=0
- 5 search_corpus: {"query":"post-termination services"} | None | retries=0
- 6 llm_response: {"turn":2} | None | retries=1
- 7 get_clause: {"category":"Post-Termination Services","document_id":"cuad_8535780896bd997df598"} | None | retries=0
- 8 llm_response: {"turn":3} | None | retries=0
- 9 get_document_dates: {"document_id":"cuad_8535780896bd997df598"} | None | retries=0
- 10 llm_response: {"turn":4} | None | retries=0
- 11 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Post-Termination Services","clause_quote":"Sanofi shall, at RevMed's request, for a period not to exceed [* | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Post-Termination Services", "clause_quote": "Sanofi shall, at RevMed's request, for a period not to exceed [***] following the effective date of termination, provide reasonable technical assistance up to a total of [***] and, to the extent not already provided to RevMed, transfer copies of (including when available, in electronic format) all Sanofi Sole Program Know-How to RevMed or its designee, including without limitation: [***], in each case to the extent such materials are exclusively related to the Termination Product.", "confidence": 0.95, "consequence": null, "deadline": {"kind": "relative", "offset_days": null, "raw_text": "for a period not to exceed [***] following the effective date of termination", "resolved_date": null}, "description": "Provide reasonable technical assistance up to a total of [***] and transfer copies of all Sanofi Sole Program Know-How exclusively related to the Termination Product upon RevMed's request following termination.", "owed_by": "provider", "type": "SVC-POST-TERMINATION"}, {"clause_category": "Post-Termination Services", "clause_quote": "Furthermore, Sanofi shall within [***] after the effective date of such termination, transfer to RevMed all files and documents relating to the prosecution, defense or enforcement of the RevMed Licensed Patents or Joint Program Patents and provide reasonable assistance for a period not to exceed [***] f

### test-06 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Ip Ownership Assignment", "clause_ref": {"category": "Ip Ownership Assignment", "char_end": 39043, "char_start": 38489}, "deadline": {"anchor_event": "closing_date", "anchor_resolved": false, "deadline_text": "Effective as of the applicable Closing Date", "kind": "relative"}, "owed_by": "provider", "type": "IP-OWNERSHIP-ASSIGNMENT"}, {"clause_category": "Anti-Assignment", "clause_ref": {"category": "Anti-Assignment", "char_end": 112724, "char_start": 111761}, "deadline": {"kind": "none"}, "owed_by": "both", "type": "CTL-NO-ASSIGNMENT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"survives"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"Intellectual Property"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"assignment"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 get_clause: {"category":"Ip Ownership Assignment","document_id":"cuad_944e0822aba9ea79bbd5"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 search_corpus: {"query":"survive"} | None | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 search_corpus: {"query":"remain in force and survive"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 record_obligations: {"confidence":0.9,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Ip Ownership Assignment","clause_quote":"Effective as of the applicable Closing Date, the Seller hereby sell | VALIDATION_ERROR | retries=0
- 16 llm_response: {"turn":8} | None | retries=0
- 17 record_obligations: {"confidence":0.9,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Ip Ownership Assignment","clause_quote":"Effective as of the applicable Closing Date, the Seller hereby sell | VALIDATION_ERROR | retries=0
Terminal args: null

### test-07 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Minimum Commitment", "clause_ref": {"category": "Minimum Commitment", "char_end": 81189, "char_start": 80594}, "deadline": {"anchor_event": "month", "deadline_text": "forecasted for each Calendar Month of the Firm Zone", "kind": "recurring", "period": "monthly"}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}, {"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 152543, "char_start": 151954}, "deadline": {"anchor_event": "effective_date", "deadline_text": "Each Party will maintain at its sole cost and expense", "kind": "recurring", "period": "term"}, "owed_by": "both", "type": "INS-COVERAGE"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "Unless otherwise set forth in a relevant Module, the quantity of Miltenyi Product(s) forecasted for each Calendar Month of the Firm Zone of the most recent rolling Monthly Forecast submitted pursuant to Section 5.1(a) of this Agreement shall be binding on both Parties, commencing on the Effecctive Date of the Agreement (but not for the first three months thereto), and in each Calendar Month during the Term, Bellicum shall have the firm obligation to order at a minimum the amount of Miltenyi Product(s) specified for the first (1st) Calendar Month of the most recent rolling Monthly Forecast", "deadline": {"kind": "recurring", "resolved_date": null}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}, {"clause_quote": "Each Party will maintain at its sole cost and expense, an adequate amount of commercial general liability and product liability insurance throughout the Term and for a period of five (5) years thereafter, to protect against potential liabilities and risk arising out of products supplied or activities to be performed under this Agreement and any Quality Agreement related hereto upon such terms (including coverages, deductible limits and self-insured retentions) as are customary in the industry for the products supplied or activities to be conducted by such Party under this Agreement.", "deadline": {"kind": "recurring", "resolved_date": null}, "owed_by": "customer", "type": "INS-COVERAGE"}, {"clause_quote": "Each Party shall provide the other Party with written proof of the existence of such insurance upon reasonable written request.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "customer", "type": "INS-COVERAGE"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"forecast commitment"} | None | retries=0
- 4 search_corpus: {"query":"insurance"} | None | retries=0
- 5 llm_response: {"turn":2} | None | retries=0
- 6 get_clause: {"category":"Minimum Commitment","document_id":"cuad_ac330c6c3a9cc0496f44"} | None | retries=0
- 7 get_clause: {"category":"Insurance","document_id":"cuad_ac330c6c3a9cc0496f44"} | None | retries=0
- 8 llm_response: {"turn":3} | None | retries=0
- 9 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Minimum Commitment","clause_quote":"Unless otherwise set forth in a relevant Module, the quantity of Miltenyi  | VALIDATION_ERROR | retries=0
- 10 llm_response: {"turn":4} | None | retries=0
- 11 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Minimum Commitment","clause_quote":"Unless otherwise set forth in a relevant Module, the quantity of Miltenyi  | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Minimum Commitment", "clause_quote": "Unless otherwise set forth in a relevant Module, the quantity of Miltenyi Product(s) forecasted for each Calendar Month of the Firm Zone of the most recent rolling Monthly Forecast submitted pursuant to Section 5.1(a) of this Agreement shall be binding on both Parties, commencing on the Effecctive Date of the Agreement (but not for the first three months thereto), and in each Calendar Month during the Term, Bellicum shall have the firm obligation to order at a minimum the amount of Miltenyi Product(s) specified for the first (1st) Calendar Month of the most recent rolling Monthly Forecast", "confidence": 1, "consequence": null, "deadline": {"kind": "recurring", "raw_text": "each Calendar Month during the Term", "recurring_rule": "each Calendar Month during the Term"}, "description": "Customer (Bellicum) must order at a minimum the amount of product specified for the first Calendar Month of the most recent rolling Monthly Forecast (Firm Zone requirements).", "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}, {"clause_category": "Insurance", "clause_quote": "Each Party will maintain at its sole cost and expense, an adequate amount of commercial general liability and product liability insurance throughout the Term and for a period of five (5) years thereafter, to protect against potential liabilities and risk arising out of products suppl

### test-08 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Revenue/Profit Sharing", "clause_ref": {"category": "Revenue/Profit Sharing", "char_end": 127575, "char_start": 127416}, "deadline": {"anchor_event": "calendar_quarter", "kind": "recurring", "period": "quarterly"}, "owed_by": "customer", "type": "PAY-REVENUE-SHARE"}, {"clause_category": "Audit Rights", "clause_ref": {"category": "Audit Rights", "char_end": 115059, "char_start": 114380}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "Such records will be open for inspection during such three (3) year period by an independent certified public accounting firm of nationally (the US or Japan) recognized standing (the \"Auditor\"), chosen by Array and reasonably acceptable to Ono for the purpose of verifying the amounts payable by Ono hereunder. Such inspections may be made no more than once each Calendar Year, at reasonable times and on reasonable prior written notice. Such records for any particular calendar quarter shall be subject to no more than one inspection.", "deadline": {"kind": "recurring", "resolved_date": null}, "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"audit"} | None | retries=0
- 4 search_corpus: {"query":"royalty"} | None | retries=0
- 5 search_corpus: {"query":"payment"} | None | retries=0
- 6 llm_response: {"turn":2} | None | retries=0
- 7 get_clause: {"category":"Audit Rights","document_id":"cuad_a0e14c30056968d88209"} | None | retries=0
- 8 get_clause: {"category":"Revenue/Profit Sharing","document_id":"cuad_a0e14c30056968d88209"} | None | retries=0
- 9 get_clause: {"category":"Minimum Commitment","document_id":"cuad_a0e14c30056968d88209"} | None | retries=0
- 10 llm_response: {"turn":3} | None | retries=0
- 11 search_corpus: {"query":"Ono shall keep, and require its Affiliates and Sublicensees to keep"} | None | retries=0
- 12 search_corpus: {"query":"books of accounts and records for the purpose of determining the amounts payable"} | None | retries=0
- 13 llm_response: {"turn":4} | None | retries=0
- 14 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Audit Rights","clause_quote":"Such records will be open for inspection during such three (3) year period by an | VALIDATION_ERROR | retries=0
- 15 llm_response: {"turn":5} | None | retries=0
- 16 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Audit Rights","clause_quote":"Such records will be open for inspection during such three (3) year period by an | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Audit Rights", "clause_quote": "Such records will be open for inspection during such three (3) year period by an independent certified public accounting firm of nationally (the US or Japan) recognized standing (the \"Auditor\"), chosen by Array and reasonably acceptable to Ono for the purpose of verifying the amounts payable by Ono hereunder. Such inspections may be made no more than once each Calendar Year, at reasonable times and on reasonable prior written notice. Such records for any particular calendar quarter shall be subject to no more than one inspection.", "confidence": 1, "consequence": "If an underpayment exceeding [*] of the amount paid for the inspected period is established, Ono must pay all reasonable costs relating to the inspection and any unpaid amounts together with interest.", "deadline": {"kind": "recurring", "raw_text": "no more than once each Calendar Year", "recurring_rule": "once each Calendar Year"}, "description": "Customer (Ono) must permit records to be open for inspection by an independent certified public accounting firm chosen by Provider (Array) no more than once each Calendar Year upon reasonable prior written notice.", "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}]}

### test-09 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "License Grant", "clause_ref": {"category": "License Grant", "char_end": 37500, "char_start": 37117}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}, {"clause_category": "Exclusivity", "clause_ref": {"category": "Exclusivity", "char_end": 17225, "char_start": 16776}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "COV-EXCLUSIVITY"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"exclusivity"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"3. EXCLUSIVITY"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"CERES-IGER Collaboration Agreement Page 8"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"EXCLUSIVITY"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 get_clause: {"category":"COV-EXCLUSIVITY","document_id":"cuad_7c7b9fab0f2daf6004b0"} | ClauseNotFound | retries=0
- 12 llm_response: {"turn":6} | None | retries=0
- 13 search_corpus: {"query":"Page 8 of 75"} | None | retries=0
- 14 llm_response: {"turn":7} | None | retries=0
- 15 search_corpus: {"query":"CERES-IGER Collaboration Agreement"} | None | retries=0
- 16 llm_response: {"turn":8} | None | retries=0
- 17 search_corpus: {"query":"EXCLUSIVITY"} | None | retries=0
Terminal args: null

### test-10 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "Non-Compete", "clause_ref": {"category": "Non-Compete", "char_end": 18428, "char_start": 18226}, "deadline": {"anchor_event": "effective_date", "deadline_text": "during the Term of this Agreement", "kind": "recurring", "period": "term"}, "owed_by": "customer", "type": "COV-NON-COMPETE"}, {"clause_category": "Minimum Commitment", "clause_ref": {"category": "Minimum Commitment", "char_end": 30099, "char_start": 29544}, "deadline": {"anchor_event": "month", "kind": "recurring", "period": "monthly"}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "Excite@Home shall not offer any Excite-branded or Excite-co-branded         service during the Term of this Agreement that is substantially similar         in functionally to the Co-Branded Application.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "customer", "type": "COV-NON-COMPETE"}, {"clause_quote": "Excite@Home will not serve advertising on the Co-Branded Application for      any \"Application Provider Named Competitor,\" as specified in EXHIBIT E.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "customer", "type": "COV-NON-COMPETE"}, {"clause_quote": "In no event may either party sell, disclose, transfer, rent, or             license Payment-Eligible User Data to the other party's Named             Competitors as listed in EXHIBIT E.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "both", "type": "COV-NON-COMPETE"}, {"clause_quote": "Excite@Home will supply to Application Provider a minimum of                ***** Payment-Eligible User Data records for General Program                Members containing all available information set forth in Section                1(h)  [DEFINITIONS] in each quarter during the Term of this Agreement, beginning                with the quarter in which the Launch Date (as hereinafter                defined) falls, for a minimum of ***** of these General                Program Member User Data records during the Term of this                Agreement.", "deadline": {"kind": "recurring", "resolved_date": null}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}, {"clause_quote": "Excite@Home will supply to e-centives a minimum of *****           Payment-Eligible User Data records for Qualified Program Members           containing all available information set forth in Section 1(h)  [DEFINITIONS] in each           quarter during the Term of this Agreement, beginning with the quarter           in which the Launch Date (as hereinafter defined) falls, for a minimum           of ***** of these Qualified Program Member User Data records           during the Term of this Agreement.", "deadline": {"kind": "recurring", "resolved_date": null}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"non-compete"} | None | retries=0
- 4 search_corpus: {"query":"compete"} | None | retries=0
- 5 search_corpus: {"query":"solicit"} | None | retries=0
- 6 search_corpus: {"query":"supply"} | None | retries=0
- 7 llm_response: {"turn":2} | None | retries=0
- 8 get_clause: {"category":"Non-Compete","document_id":"cuad_a08094c0e438a7a9c7e5"} | None | retries=0
- 9 get_clause: {"category":"No-Solicit Of Customers","document_id":"cuad_a08094c0e438a7a9c7e5"} | None | retries=0
- 10 llm_response: {"turn":3} | None | retries=0
- 11 search_corpus: {"query":"data supply"} | None | retries=0
- 12 search_corpus: {"query":"floor"} | None | retries=0
- 13 search_corpus: {"query":"supply e-centives"} | None | retries=0
- 14 search_corpus: {"query":"Qualified Program Member User Data"} | None | retries=0
- 15 llm_response: {"turn":4} | None | retries=0
- 16 search_corpus: {"query":"floor data supply"} | None | retries=0
- 17 search_corpus: {"query":"minimum data supply"} | None | retries=0
- 18 search_corpus: {"query":"General Program Member User Data records shall provide"} | None | retries=0
- 19 search_corpus: {"query":"shall provide in excess of"} | None | retries=0
- 20 llm_response: {"turn":5} | None | retries=0
- 21 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Non-Compete","clause_quote":"Excite@Home shall not offer any Excite-branded or Excite-co-branded         se | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Non-Compete", "clause_quote": "Excite@Home shall not offer any Excite-branded or Excite-co-branded         service during the Term of this Agreement that is substantially similar         in functionally to the Co-Branded Application.", "confidence": 0.95, "consequence": null, "deadline": {"kind": "relative", "offset_days": null, "raw_text": "during the Term of this Agreement"}, "description": "Excite@Home (customer) shall not offer any Excite-branded or Excite-co-branded service during the Term of this Agreement that is substantially similar in functionally to the Co-Branded Application.", "owed_by": "customer", "type": "COV-NON-COMPETE"}, {"clause_category": "Non-Compete", "clause_quote": "Excite@Home will not serve advertising on the Co-Branded Application for      any \"Application Provider Named Competitor,\" as specified in EXHIBIT E.", "confidence": 0.95, "consequence": null, "deadline": {"kind": "none", "raw_text": "none"}, "description": "Excite@Home (customer) will not serve advertising on the Co-Branded Application for any Application Provider Named Competitor.", "owed_by": "customer", "type": "COV-NON-COMPETE"}, {"clause_category": "Non-Compete", "clause_quote": "In no event may either party sell, disclose, transfer, rent, or             license Payment-Eligible User Data to the other party's Named             Competitors as listed in EXHIBIT E.", "confidence": 0.95

### test-11 — clear, constructed=False, difficulty 3
Failed: deadlines_captured, escalation_correct
Gold: {"obligations": [{"clause_category": "Rofr/Rofo/Rofn", "clause_ref": {"category": "Rofr/Rofo/Rofn", "char_end": 94293, "char_start": 93627}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "TRM-ROFR-ROFO-ROFN"}, {"clause_category": "No-Solicit Of Employees", "clause_ref": {"category": "No-Solicit Of Employees", "char_end": 120714, "char_start": 120471}, "deadline": {"anchor_event": "termination", "deadline_text": "for the duration of the Noncompetition Period and for the two years thereafter", "kind": "relative", "offset_days": 730}, "owed_by": "customer", "type": "COV-NO-SOLICIT-EMPLOYEE"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "The Agent agrees that for the duration of the Noncompetition Period, without the prior written consent of Monsanto, it will not, nor will it permit any of its Affiliates to (i) solicit for employment any person then employed who works primarily with Roundup Products or with other products with Lawn & Garden Uses (\"Lawn & Garden Employee\") by Monsanto or any of its Affiliates or (ii) knowingly employ any Lawn & Garden Employee of Monsanto or any of its Affiliates who voluntarily terminates such employment with Monsanto (or such Affiliate) after the Effective Date, until three months have passed following termination of such employment.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "customer", "type": "COV-NO-SOLICIT-EMPLOYEE"}, {"clause_quote": "In the event that the Agent develops, or obtains access to, any new natural nonselective weedkiller products (including, without limitation, any herbicidally active substances which are plant extracts, including those derived from oleic acid or which are derived from plant extracts by processing including active substances) in Canada during the respective term of this Agreement, the Agent will grant Monsanto a right of first refusal to include such new products in the Roundup P&L on the same terms as agreed for the current Natural Products, and if accepted, such new products will become Natural Products.", "deadline": {"kind": "recurring", "resolved_date": null}, "owed_by": "customer", "type": "TRM-ROFR-ROFO-ROFN"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"no-poach"} | None | retries=0
- 4 search_corpus: {"query":"first-offer"} | None | retries=0
- 5 search_corpus: {"query":"solicit"} | None | retries=0
- 6 search_corpus: {"query":"non-compete"} | None | retries=0
- 7 llm_response: {"turn":2} | None | retries=0
- 8 get_clause: {"category":"Non-Solicitation by Monsanto","document_id":"cuad_412f6a035ef9763e47c2"} | ClauseNotFound | retries=0
- 9 get_clause: {"category":"Non-Solicitation by the Agent","document_id":"cuad_412f6a035ef9763e47c2"} | ClauseNotFound | retries=0
- 10 get_clause: {"category":"Rofr/Rofo/Rofn","document_id":"cuad_412f6a035ef9763e47c2"} | None | retries=0
- 11 search_corpus: {"query":"first offer"} | None | retries=0
- 12 llm_response: {"turn":3} | None | retries=0
- 13 get_clause: {"category":"Non-Solicitation by the Agent","document_id":"cuad_412f6a035ef9763e47c2"} | ClauseNotFound | retries=0
- 14 search_corpus: {"query":"Non-Solicitation by the Agent"} | None | retries=0
- 15 llm_response: {"turn":4} | None | retries=0
- 16 search_corpus: {"query":"(e) Non-Solicitation by the Agent"} | None | retries=0
- 17 search_corpus: {"query":"(d) Non-Solicitation by Monsanto"} | None | retries=0
- 18 llm_response: {"turn":5} | None | retries=0
- 19 get_clause: {"category":"No-Solicit Of Employees","document_id":"cuad_412f6a035ef9763e47c2"} | None | retries=0
- 20 search_corpus: {"query":"(e) Non-Solicitation by the Agent."} | None | retries=0
- 21 llm_response: {"turn":6} | None | retries=0
- 22 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"No-Solicit Of Employees","clause_quote":"The Agent agrees that for the duration of the Noncompetition Period,  | VALIDATION_ERROR | retries=0
- 23 llm_response: {"turn":7} | None | retries=0
- 24 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"No-Solicit Of Employees","clause_quote":"The Agent agrees that for the duration of the Noncompetition Period,  | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "No-Solicit Of Employees", "clause_quote": "The Agent agrees that for the duration of the Noncompetition Period, without the prior written consent of Monsanto, it will not, nor will it permit any of its Affiliates to (i) solicit for employment any person then employed who works primarily with Roundup Products or with other products with Lawn & Garden Uses (\"Lawn & Garden Employee\") by Monsanto or any of its Affiliates or (ii) knowingly employ any Lawn & Garden Employee of Monsanto or any of its Affiliates who voluntarily terminates such employment with Monsanto (or such Affiliate) after the Effective Date, until three months have passed following termination of such employment.", "confidence": 1, "consequence": null, "deadline": {"kind": "relative", "offset_days": null, "raw_text": "for the duration of the Noncompetition Period"}, "description": "Customer (Agent) agrees not to solicit for employment or knowingly employ (until three months have passed) certain Monsanto employees for the duration of the Noncompetition Period without prior written consent.", "owed_by": "customer", "type": "COV-NO-SOLICIT-EMPLOYEE"}, {"clause_category": "Rofr/Rofo/Rofn", "clause_quote": "In the event that the Agent develops, or obtains access to, any new natural nonselective weedkiller products (including, without limitation, any herbicidally active substances which are plant extracts, including tho

### test-12 — clear, constructed=False, difficulty 2
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Audit Rights", "clause_ref": {"category": "Audit Rights", "char_end": 28542, "char_start": 28197}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "CTL-AUDIT-RIGHT"}, {"clause_category": "Ip Ownership Assignment", "clause_ref": {"category": "Ip Ownership Assignment", "char_end": 10306, "char_start": 10002}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "IP-OWNERSHIP-ASSIGNMENT"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"audit"} | None | retries=0
- 4 search_corpus: {"query":"intellectual property"} | None | retries=0
- 5 search_corpus: {"query":"assign"} | None | retries=0
- 6 llm_response: {"turn":2} | None | retries=0
- 7 get_clause: {"category":"Audit Rights","document_id":"cuad_96943dfc7ec66b62e263"} | None | retries=0
- 8 get_clause: {"category":"Ip Ownership Assignment","document_id":"cuad_96943dfc7ec66b62e263"} | None | retries=0
- 9 llm_response: {"turn":3} | None | retries=0
- 10 search_corpus: {"query":"cooperate fully"} | None | retries=0
- 11 llm_response: {"turn":4} | None | retries=0
- 12 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Audit Rights","clause_quote":"If such an inspection is requested, IAC will reasonably furnish all relevant sup | VALIDATION_ERROR | retries=0
- 13 llm_response: {"turn":5} | None | retries=0
- 14 get_clause: {"category":"Ip Ownership Assignment","document_id":"cuad_96943dfc7ec66b62e263"} | None | retries=0
- 15 llm_response: {"turn":6} | None | retries=0
- 16 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Audit Rights","clause_quote":"If such an inspection is requested, IAC will reasonably furnish all relevant sup | VALIDATION_ERROR | retries=0
Terminal args: null

### test-13 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "License Grant", "clause_ref": {"category": "License Grant", "char_end": 40911, "char_start": 39823}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"law"} | None | retries=0
- 4 search_corpus: {"query":"governs"} | None | retries=0
- 5 search_corpus: {"query":"dispute"} | None | retries=0
- 6 search_corpus: {"query":"franchise"} | None | retries=0
- 7 llm_response: {"turn":2} | None | retries=0
- 8 get_clause: {"category":"Governing Law","document_id":"composite_61c626a3b683b3ef71c2"} | None | retries=0
- 9 llm_response: {"turn":3} | None | retries=0
- 10 search_corpus: {"query":"governed by, and construed in accordance with"} | None | retries=0
- 11 llm_response: {"turn":4} | None | retries=0
- 12 record_obligations: {"confidence":1,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES"],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 1, "escalate": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": []}

### test-14 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Ip Ownership Assignment", "clause_ref": {"category": "Ip Ownership Assignment", "char_end": 39043, "char_start": 38489}, "deadline": {"anchor_event": "closing_date", "anchor_resolved": false, "deadline_text": "Effective as of the applicable Closing Date", "kind": "relative"}, "owed_by": "provider", "type": "IP-OWNERSHIP-ASSIGNMENT"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"governing law"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_clause: {"category":"Governing Law","document_id":"composite_3ff5786d0f09b2611a63"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"IP Agreement"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 record_obligations: {"confidence":0.8,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES"],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 0.8, "escalate": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": []}

### test-15 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Minimum Commitment", "clause_ref": {"category": "Minimum Commitment", "char_end": 22887, "char_start": 22534}, "deadline": {"anchor_event": "commencement_date", "deadline_text": "beginning six (6) months after the Commencement Date", "kind": "recurring", "offset_days": 180, "period": "monthly"}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"royalty"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"Royalty Fee payment"} | None | retries=0
- 6 search_corpus: {"query":"Gross Revenues Royalty Fee"} | None | retries=0
- 7 llm_response: {"turn":3} | None | retries=0
- 8 search_corpus: {"query":"governing law applicable law jurisdiction franchise agreement"} | None | retries=0
- 9 llm_response: {"turn":4} | None | retries=0
- 10 get_clause: {"category":"Governing Law","document_id":"composite_4bf3f94d05591e5d2eb6"} | None | retries=0
- 11 llm_response: {"turn":5} | None | retries=0
- 12 search_corpus: {"query":"This Agreement shall be governed by, and construed in accordance with, the laws of the State of New York"} | None | retries=0
- 13 llm_response: {"turn":6} | None | retries=0
- 14 search_corpus: {"query":"This Agreement shall be governed by, and construed in accordance with, the laws of the State of"} | None | retries=0
- 15 llm_response: {"turn":7} | None | retries=0
- 16 record_obligations: {"confidence":0.85,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES"],"obligations":[{"clause_category":"Governing Law","clause_quote":"This Agreement will be interpreted and construed excl | VALIDATION_ERROR | retries=0
- 17 llm_response: {"turn":8} | None | retries=0
- 18 record_obligations: {"confidence":0.85,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES"],"obligations":[{"clause_category":"Governing Law","clause_quote":"This Agreement will be interpreted and construed excl | VALIDATION_ERROR | retries=0
Terminal args: null

### test-16 — conflicting, constructed=True, difficulty 3
Failed: escalation_correct
Gold: {"obligations": [{"clause_category": "License Grant", "clause_ref": {"category": "License Grant", "char_end": 66646, "char_start": 66065}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "LIC-GRANT"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": false, "escalation_codes": [], "obligations": [{"clause_quote": "You hereby grant to us (and agree to obtain from your affiliates, owners, employees, and/or contractors), a perpetual, non-exclusive, and worldwide right to use any such ideas, concepts, methods, techniques and products in any businesses that we and/or our affiliates, franchisees and designees operate.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "customer", "type": "LIC-GRANT"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"grant-back"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_clause: {"category":"Affiliate License-Licensor","document_id":"composite_75c622f527ea034356a9"} | None | retries=0
- 6 get_clause: {"category":"Irrevocable Or Perpetual License","document_id":"composite_75c622f527ea034356a9"} | None | retries=0
- 7 llm_response: {"turn":3} | None | retries=0
- 8 search_corpus: {"query":"concept, method, technique or product"} | None | retries=0
- 9 llm_response: {"turn":4} | None | retries=0
- 10 get_clause: {"category":"Ip Ownership Assignment","document_id":"composite_75c622f527ea034356a9"} | None | retries=0
- 11 llm_response: {"turn":5} | None | retries=0
- 12 search_corpus: {"query":"All such products, services, concepts, methods, techniques, and new information will be deemed to be our sole and exclusive property"} | None | retries=0
- 13 llm_response: {"turn":6} | None | retries=0
- 14 search_corpus: {"query":"All such products, services, concepts, methods, techniques, and new information will be deemed to be our sole and exclusive property and works made-for-hire"} | None | retries=0
- 15 llm_response: {"turn":7} | None | retries=0
- 16 search_corpus: {"query":"works made-for-hire"} | None | retries=0
- 17 llm_response: {"turn":8} | None | retries=0
- 18 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Irrevocable Or Perpetual License","clause_quote":"You hereby grant to us (and agree to obtain from your aff | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Irrevocable Or Perpetual License", "clause_quote": "You hereby grant to us (and agree to obtain from your affiliates, owners, employees, and/or contractors), a perpetual, non-exclusive, and worldwide right to use any such ideas, concepts, methods, techniques and products in any businesses that we and/or our affiliates, franchisees and designees operate.", "confidence": 0.95, "consequence": null, "deadline": {"kind": "none", "raw_text": null}, "description": "Grant-back of a perpetual, non-exclusive, and worldwide right to use ideas, concepts, methods, techniques, and products created or developed by the franchisee.", "owed_by": "customer", "type": "LIC-GRANT"}]}

### test-17 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found
Gold: {"obligations": [{"clause_category": "License Grant", "clause_ref": {"category": "License Grant", "char_end": 53863, "char_start": 51797}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "LIC-GRANT"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": false, "escalation_codes": [], "obligations": [], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"license"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 get_clause: {"category":"Irrevocable Or Perpetual License","document_id":"composite_12f8dcd43b68eb16d09d"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 search_corpus: {"query":"terminate license"} | None | retries=0
- 8 llm_response: {"turn":4} | None | retries=0
- 9 search_corpus: {"query":"perpetual license terminate"} | None | retries=0
- 10 llm_response: {"turn":5} | None | retries=0
- 11 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[]} | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": []}

### test-18 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Liquidated Damages", "clause_ref": {"category": "Liquidated Damages", "char_end": 39066, "char_start": 38832}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "LIA-LIQUIDATED-DAMAGES"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "Customer may elect to terminate this Agreement for any reason upon six months written notice to Metavante, provided Customer shall pay Metavante the \"Termination Fee\" defined and computed in accordance with the table below.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "customer", "type": "TRM-CONVENIENCE"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"remedy waiver"} | None | retries=0
- 4 search_corpus: {"query":"exit costing"} | None | retries=0
- 5 search_corpus: {"query":"waiver"} | None | retries=0
- 6 llm_response: {"turn":2} | None | retries=0
- 7 get_clause: {"category":"Cap On Liability","document_id":"composite_134e5c3bea32a9a6632a"} | None | retries=0
- 8 get_clause: {"category":"Liquidated Damages","document_id":"composite_134e5c3bea32a9a6632a"} | None | retries=0
- 9 llm_response: {"turn":3} | None | retries=0
- 10 search_corpus: {"query":"Customer acknowledges that the Termination Fee is a reasonable approximation"} | None | retries=0
- 11 llm_response: {"turn":4} | None | retries=0
- 12 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Liquidated Damages","clause_quote":"Customer may elect to terminate this Agreement for any reason upon six  | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Liquidated Damages", "clause_quote": "Customer may elect to terminate this Agreement for any reason upon six months written notice to Metavante, provided Customer shall pay Metavante the \"Termination Fee\" defined and computed in accordance with the table below.", "confidence": 0.95, "consequence": "Customer must pay the Termination Fee defined and computed in accordance with the agreement.", "deadline": {"kind": "relative", "offset_days": 180, "raw_text": "six months written notice"}, "description": "Customer must provide six months written notice and pay the Termination Fee upon electing to terminate the agreement for convenience.", "owed_by": "customer", "type": "TRM-CONVENIENCE"}]}

### test-19 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Liquidated Damages", "clause_ref": {"category": "Liquidated Damages", "char_end": 142875, "char_start": 142328}, "deadline": {"kind": "none"}, "owed_by": "customer", "type": "LIA-LIQUIDATED-DAMAGES"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": [{"clause_quote": "IN NO EVENT SHALL ANY PARTY BE LIABLE TO THE OTHER PARTY FOR ANY INDIRECT, SPECIAL, EXEMPLARY, PUNITIVE OR CONSEQUENTIAL DAMAGES, OR LOST PROFITS OR LOST REVENUES THAT THE OTHER PARTY MAY INCUR BY REASON OF ITS HAVING ENTERED INTO OR RELIED UPON THIS AGREEMENT, OR IN CONNECTION WITH ANY OF THE SERVICES PROVIDED HEREUNDER OR THE FAILURE THEREOF, REGARDLESS OF THE FORM OF ACTION IN WHICH SUCH DAMAGES ARE ASSERTED, WHETHER IN CONTRACT OR TORT (INCLUDING NEGLIGENCE) OR OTHERWISE, EVEN IF ADVISED OF THE POSSIBILITY OF THE SAME OTHER THAN TO THE EXTENT AWARDED IN A THIRD PARTY CLAIM.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "both", "type": "LIA-CAP"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"termination"} | None | retries=0
- 4 search_corpus: {"query":"damages"} | None | retries=0
- 5 search_corpus: {"query":"fee"} | None | retries=0
- 6 search_corpus: {"query":"exclusion"} | None | retries=0
- 7 llm_response: {"turn":2} | None | retries=0
- 8 get_clause: {"category":"Cap On Liability","document_id":"composite_4e4b51c5cd3f6a4c7ea9"} | None | retries=0
- 9 llm_response: {"turn":3} | None | retries=0
- 10 record_obligations: {"confidence":0.9,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES"],"obligations":[{"clause_category":"Cap On Liability","clause_quote":"IN NO EVENT SHALL ANY PARTY BE LIABLE TO THE OTHER  | VALIDATION_ERROR | retries=0
- 11 llm_response: {"turn":4} | None | retries=0
- 12 record_obligations: {"confidence":0.9,"escalate":true,"escalation_codes":["E2_CONFLICTING_CLAUSES"],"obligations":[{"clause_category":"Cap On Liability","clause_quote":"IN NO EVENT SHALL ANY PARTY BE LIABLE TO THE OTHER  | None | retries=0
Terminal args: {"confidence": 0.9, "escalate": true, "escalation_codes": ["E2_CONFLICTING_CLAUSES"], "obligations": [{"clause_category": "Cap On Liability", "clause_quote": "IN NO EVENT SHALL ANY PARTY BE LIABLE TO THE OTHER PARTY FOR ANY INDIRECT, SPECIAL, EXEMPLARY, PUNITIVE OR CONSEQUENTIAL DAMAGES, OR LOST PROFITS OR LOST REVENUES THAT THE OTHER PARTY MAY INCUR BY REASON OF ITS HAVING ENTERED INTO OR RELIED UPON THIS AGREEMENT, OR IN CONNECTION WITH ANY OF THE SERVICES PROVIDED HEREUNDER OR THE FAILURE THEREOF, REGARDLESS OF THE FORM OF ACTION IN WHICH SUCH DAMAGES ARE ASSERTED, WHETHER IN CONTRACT OR TORT (INCLUDING NEGLIGENCE) OR OTHERWISE, EVEN IF ADVISED OF THE POSSIBILITY OF THE SAME OTHER THAN TO THE EXTENT AWARDED IN A THIRD PARTY CLAIM.", "confidence": 0.9, "consequence": "Loss of right to recover indirect, special, exemplary, punitive, or consequential damages, or lost profits or lost revenues.", "deadline": {"kind": "none", "raw_text": "none"}, "description": "Neither party shall be liable to the other party for any indirect, special, exemplary, punitive, or consequential damages, or lost profits or lost revenues incurred in connection with the agreement or services.", "owed_by": "both", "type": "LIA-CAP"}]}

### test-20 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, obligations_found
Gold: {"obligations": [{"clause_category": "Minimum Commitment", "clause_ref": {"category": "Minimum Commitment", "char_end": 81189, "char_start": 80594}, "deadline": {"anchor_event": "month", "deadline_text": "forecasted for each Calendar Month of the Firm Zone", "kind": "recurring", "period": "monthly"}, "owed_by": "customer", "type": "PUR-MINIMUM-COMMITMENT"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "EACH PARTY'S MAXIMUM LIABILITY FOR ANY DAMAGES FOR BREACH OF THIS AGREEMENT SHALL BE LIMITED TO DIRECT AND ACTUAL DAMAGES. IN NO ONE EVENT SHALL EITHER PARTY'S AGGREGATE LIABILITY FOR DAMAGES OR LOSSES UNDER THIS AGREEMENT EXCEED THE AGGREGATE AMOUNT OF THE PRODUCT PRICES PAID BY BELLICUM FOR THE MILTENYI PRODUCT(S) DURING THE TWELVE (12) MONTH PERIOD IMMEDIATELY PRECEDING THE EVENT GIVING RISE TO SUCH LIABILITY; AND FURTHER PROVIDED THAT SUCH AGGREGATE LIABILITY DURING SUCH PERIOD ALSO SHALL NOT EXCEED THE AMOUNT OF SUCH PARTY'S INSURANCE COVERAGE FOR SUCH AGGREGATE LIABILITY.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "both", "type": "LIA-CAP"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"liability cap"} | None | retries=0
- 4 search_corpus: {"query":"aggregate liability"} | None | retries=0
- 5 llm_response: {"turn":2} | None | retries=0
- 6 get_clause: {"category":"Cap On Liability","document_id":"composite_496a5d6b32df2bf1e091"} | None | retries=0
- 7 get_clause: {"category":"Uncapped Liability","document_id":"composite_496a5d6b32df2bf1e091"} | None | retries=0
- 8 llm_response: {"turn":3} | None | retries=0
- 9 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Cap On Liability","clause_quote":"EACH PARTY'S MAXIMUM LIABILITY FOR ANY DAMAGES FOR BREACH OF THIS AGREEMENT  | VALIDATION_ERROR | retries=0
- 10 llm_response: {"turn":4} | None | retries=0
- 11 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Cap On Liability","clause_quote":"EACH PARTY'S MAXIMUM LIABILITY FOR ANY DAMAGES FOR BREACH OF THIS AGREEMENT  | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Cap On Liability", "clause_quote": "EACH PARTY'S MAXIMUM LIABILITY FOR ANY DAMAGES FOR BREACH OF THIS AGREEMENT SHALL BE LIMITED TO DIRECT AND ACTUAL DAMAGES. IN NO ONE EVENT SHALL EITHER PARTY'S AGGREGATE LIABILITY FOR DAMAGES OR LOSSES UNDER THIS AGREEMENT EXCEED THE AGGREGATE AMOUNT OF THE PRODUCT PRICES PAID BY BELLICUM FOR THE MILTENYI PRODUCT(S) DURING THE TWELVE (12) MONTH PERIOD IMMEDIATELY PRECEDING THE EVENT GIVING RISE TO SUCH LIABILITY; AND FURTHER PROVIDED THAT SUCH AGGREGATE LIABILITY DURING SUCH PERIOD ALSO SHALL NOT EXCEED THE AMOUNT OF SUCH PARTY'S INSURANCE COVERAGE FOR SUCH AGGREGATE LIABILITY.", "confidence": 1, "consequence": null, "deadline": {"kind": "none", "raw_text": "none"}, "description": "Each party's aggregate liability for damages or losses under this agreement shall not exceed the aggregate amount of product prices paid by Bellicum for the Miltenyi product(s) during the twelve month period immediately preceding the event giving rise to such liability, and shall not exceed the amount of such party's insurance coverage for such aggregate liability.", "owed_by": "both", "type": "LIA-CAP"}]}

### test-21 — conflicting, constructed=True, difficulty 3
Failed: deadlines_captured, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Audit Rights", "clause_ref": {"category": "Audit Rights", "char_end": 14487, "char_start": 13918}, "deadline": {"kind": "none"}, "owed_by": "provider", "type": "CTL-AUDIT-RIGHT"}], "escalation": ["E2_CONFLICTING_CLAUSES"]}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"transition services"} | None | retries=0
- 4 search_corpus: {"query":"service credits"} | None | retries=0
- 5 search_corpus: {"query":"fees cap"} | None | retries=0
- 6 llm_response: {"turn":2} | None | retries=0
- 7 get_clause: {"category":"Document Name","document_id":"composite_975deac30eb0cdb76eed"} | None | retries=0
- 8 llm_response: {"turn":3} | None | retries=0
- 9 search_corpus: {"query":"cap against per-day service credits"} | None | retries=0
- 10 search_corpus: {"query":"per-day service credits"} | None | retries=0
- 11 search_corpus: {"query":"Service Level Monthly Cap"} | None | retries=0
- 12 llm_response: {"turn":4} | None | retries=0
- 13 record_obligations: {"confidence":0.8,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":null,"clause_quote":"Service Level Credits applied during any month shall not exceed twenty percent (20%) of  | VALIDATION_ERROR | retries=0
- 14 llm_response: {"turn":5} | None | retries=0
- 15 record_obligations: {"confidence":0.8,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"unlabelled paragraph","clause_quote":"Service Level Credits applied during any month shall not exceed twenty | VALIDATION_ERROR | retries=0
Terminal args: null

### test-22 — out_of_scope, constructed=False, difficulty 2
Failed: escalation_correct
Gold: {"obligations": [], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "SMBC shall have ten (10) days from the date of delivery of any such notice to agree to purchase all, but not less than all, of such Additional Units, for the price and upon the terms specified in the notice, by delivering written notice to Moelis Holdings.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "customer", "type": "TRM-ROFR-ROFO-ROFN"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"limited partner"} | None | retries=0
- 4 search_corpus: {"query":"investor"} | None | retries=0
- 5 search_corpus: {"query":"capital contribution"} | None | retries=0
- 6 search_corpus: {"query":"confidentiality"} | None | retries=0
- 7 llm_response: {"turn":2} | None | retries=0
- 8 get_clause: {"category":"Confidentiality","document_id":"cuad_1f9cab5d8d6e18e6f1a8"} | ClauseNotFound | retries=0
- 9 get_clause: {"category":"Rofr/Rofo/Rofn","document_id":"cuad_1f9cab5d8d6e18e6f1a8"} | None | retries=0
- 10 get_clause: {"category":"Cap On Liability","document_id":"cuad_1f9cab5d8d6e18e6f1a8"} | None | retries=0
- 11 get_clause: {"category":"Parties","document_id":"cuad_1f9cab5d8d6e18e6f1a8"} | None | retries=0
- 12 llm_response: {"turn":3} | None | retries=0
- 13 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Rofr/Rofo/Rofn","clause_quote":"SMBC shall have ten (10) days from the date of delivery of any such notice  | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Rofr/Rofo/Rofn", "clause_quote": "SMBC shall have ten (10) days from the date of delivery of any such notice to agree to purchase all, but not less than all, of such Additional Units, for the price and upon the terms specified in the notice, by delivering written notice to Moelis Holdings.", "confidence": 0.95, "consequence": null, "deadline": {"anchor_event": "delivery of notice", "kind": "relative", "offset_days": 10, "raw_text": "ten (10) days from the date of delivery of any such notice", "resolved_date": null}, "description": "SMBC must exercise its right of first refusal to purchase Additional Units within ten days of notice delivery.", "owed_by": "customer", "type": "TRM-ROFR-ROFO-ROFN"}]}

### test-23 — out_of_scope, constructed=False, difficulty 2
Failed: escalation_correct
Gold: {"obligations": [], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E3_CONDITIONAL_OR_AMBIGUOUS"], "obligations": [{"clause_quote": "The Company hereby agrees that, until the earlier of (i) the expiration of the Standstill Period or (ii) any material breach of this Agreement by an Investor (provided that such Investor shall have three (3) business days following written notice from the Company of any material breach to remedy such material breach if capable of remedy), neither it nor any of its Affiliates will, and it will cause each of its Affiliates not to, directly or indirectly, publicly make, express, transmit, speak, write, verbalize or otherwise publicly communicate in any way (or cause, further, assist, solicit, encourage, support or participate in any of the foregoing), any remark, comment, message, information, declaration, communication or other statement of any kind, whether verbal or in writing, that might reasonably be construed to be derogatory or critical of, or negative toward, the Investors or their Affiliates or Associates or any of their agents or representatives (collectively, the \"Investor Agents\"), or that reveals, discloses, incorporates, is based upon, discusses, includes or otherwise involves any confidential or proprietary information of any Investor or its Affiliates or Associates, or to malign, harm, disparage, defame or damage the reputation or good name of any Investor, its business or any of the Investor Agents.", "deadline": {"kind": "relative", "resolved_date": null}, "owed_by": "provider", "type": "COV-NON-DISPARAGEMENT"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"solicit"} | None | retries=0
- 4 search_corpus: {"query":"compete"} | None | retries=0
- 5 search_corpus: {"query":"confidential"} | None | retries=0
- 6 search_corpus: {"query":"termination"} | None | retries=0
- 7 llm_response: {"turn":2} | None | retries=0
- 8 get_clause: {"category":"Non-Disparagement","document_id":"cuad_2ef7ad1e760173ae3b0f"} | None | retries=0
- 9 get_clause: {"category":"Change Of Control","document_id":"cuad_2ef7ad1e760173ae3b0f"} | None | retries=0
- 10 search_corpus: {"query":"Standstill Period"} | None | retries=0
- 11 search_corpus: {"query":"7. Non-Disparagement"} | None | retries=0
- 12 llm_response: {"turn":3} | None | retries=0
- 13 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Non-Disparagement","clause_quote":"The Company hereby agrees that, until the earlier of (i) the expiration of  | VALIDATION_ERROR | retries=0
- 14 llm_response: {"turn":4} | None | retries=0
- 15 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Non-Disparagement","clause_quote":"The Company hereby agrees that, until the earlier of (i) the expiration of  | None | retries=0
Terminal args: {"confidence": 1, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Non-Disparagement", "clause_quote": "The Company hereby agrees that, until the earlier of (i) the expiration of the Standstill Period or (ii) any material breach of this Agreement by an Investor (provided that such Investor shall have three (3) business days following written notice from the Company of any material breach to remedy such material breach if capable of remedy), neither it nor any of its Affiliates will, and it will cause each of its Affiliates not to, directly or indirectly, publicly make, express, transmit, speak, write, verbalize or otherwise publicly communicate in any way (or cause, further, assist, solicit, encourage, support or participate in any of the foregoing), any remark, comment, message, information, declaration, communication or other statement of any kind, whether verbal or in writing, that might reasonably be construed to be derogatory or critical of, or negative toward, the Investors or their Affiliates or Associates or any of their agents or representatives (collectively, the \"Investor Agents\"), or that reveals, discloses, incorporates, is based upon, discusses, includes or otherwise involves any confidential or proprietary information of any Investor or its Affiliates or Associates, or to malign, harm, disparage, defame or damage the reputation or good name of any Investor, its business or any of the Investor Agents.", "confidence": 1, "conseque

- test-24 (out_of_scope, constructed=False): pass
### test-25 — out_of_scope, constructed=False, difficulty 2
Failed: execution error
Gold: {"obligations": [], "escalation": []}
Got: {"escalated": false, "escalation_codes": [], "obligations": [{"clause_quote": "Party B shall not advertise, or make any statement favorable for, any competitor having the same or similar business scope as Party A in the services it provides.", "deadline": {"kind": "none", "resolved_date": null}, "owed_by": "customer", "type": "COV-NON-COMPETE"}], "schema_valid": true}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"agreement"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"Party A Party B"} | None | retries=0
- 6 llm_response: {"turn":3} | None | retries=0
- 7 get_clause: {"category":"Non-Compete","document_id":"cuad_aa43b2240f866f2fc18d"} | None | retries=0
- 8 get_clause: {"category":"Anti-Assignment","document_id":"cuad_aa43b2240f866f2fc18d"} | None | retries=0
- 9 get_clause: {"category":"Effective Date","document_id":"cuad_aa43b2240f866f2fc18d"} | None | retries=0
- 10 get_clause: {"category":"Expiration Date","document_id":"cuad_aa43b2240f866f2fc18d"} | None | retries=0
- 11 llm_response: {"turn":4} | None | retries=0
- 12 search_corpus: {"query":"Party A shall"} | None | retries=0
- 13 llm_response: {"turn":5} | None | retries=0
- 14 get_document_dates: {"document_id":"cuad_aa43b2240f866f2fc18d"} | None | retries=0
- 15 llm_response: {"turn":6} | None | retries=0
- 16 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Non-Compete","clause_quote":"Party B shall not advertise, or make any statement favorable for, any competit | VALIDATION_ERROR | retries=0
- 17 llm_response: {"turn":7} | None | retries=0
- 18 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Non-Compete","clause_quote":"Party B shall not advertise, or make any statement favorable for, any competit | None | retries=0
Terminal args: {"confidence": 0.95, "escalate": false, "escalation_codes": [], "obligations": [{"clause_category": "Non-Compete", "clause_quote": "Party B shall not advertise, or make any statement favorable for, any competitor having the same or similar business scope as Party A in the services it provides.", "confidence": 0.95, "consequence": null, "deadline": {"kind": "none", "raw_text": "during the term hereof"}, "description": "Party B (customer/licensee) shall not advertise, or make any statement favorable for, any competitor having the same or similar business scope as Party A (provider/licensor) in the services it provides.", "owed_by": "customer", "type": "COV-NON-COMPETE"}]}

### test-26 — out_of_scope, constructed=False, difficulty 2
Failed: escalation_correct, schema_valid
Gold: {"obligations": [], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"supply agreement"} | None | retries=0
- 4 llm_response: {"turn":2} | None | retries=0
- 5 search_corpus: {"query":"obligation"} | None | retries=0
- 6 search_corpus: {"query":"non-compete"} | None | retries=0
- 7 search_corpus: {"query":"exclusivity"} | None | retries=0
- 8 search_corpus: {"query":"solicit"} | None | retries=0
- 9 llm_response: {"turn":3} | None | retries=0
- 10 get_clause: {"category":"Non-Compete","document_id":"cuad_412f6a035ef9763e47c2"} | None | retries=0
- 11 get_clause: {"category":"Competitive Restriction Exception","document_id":"cuad_412f6a035ef9763e47c2"} | None | retries=0
- 12 get_clause: {"category":"Anti-Assignment","document_id":"cuad_412f6a035ef9763e47c2"} | None | retries=0
- 13 llm_response: {"turn":4} | None | retries=0
- 14 search_corpus: {"query":"Non-Solicitation by Monsanto"} | None | retries=0
- 15 search_corpus: {"query":"Non-Solicitation by the Agent"} | None | retries=0
- 16 llm_response: {"turn":5} | None | retries=0
- 17 get_clause: {"category":"Non-Disparagement","document_id":"cuad_412f6a035ef9763e47c2"} | None | retries=0
- 18 llm_response: {"turn":6} | None | retries=0
- 19 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Non-Compete","clause_quote":"Monsanto covenants and agrees that for the Noncompetition Period, Monsanto wil | VALIDATION_ERROR | retries=0
- 20 llm_response: {"turn":7} | None | retries=0
- 21 get_clause: {"category":"No-Solicit Of Employees","document_id":"cuad_412f6a035ef9763e47c2"} | None | retries=0
- 22 llm_response: {"turn":8} | None | retries=0
- 23 record_obligations: {"confidence":0.95,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"Non-Compete","clause_quote":"Monsanto covenants and agrees that for the Noncompetition Period, Monsanto wil | VALIDATION_ERROR | retries=0
Terminal args: null

### test-29 — adversarial, constructed=False, difficulty 3
Failed: deadlines_captured, escalation_correct, obligations_found, schema_valid
Gold: {"obligations": [{"clause_category": "Insurance", "clause_ref": {"category": "Insurance", "char_end": 139324, "char_start": 138971}, "deadline": {"anchor_event": "effective_date", "kind": "recurring", "period": "term"}, "owed_by": "customer", "type": "INS-COVERAGE"}, {"clause_category": "Revenue/Profit Sharing", "clause_ref": {"category": "Revenue/Profit Sharing", "char_end": 44082, "char_start": 43715}, "deadline": {"anchor_event": "effective_date", "deadline_text": "a  continuing  Royalty of seven  percent  (7%)", "kind": "recurring", "period": "weekly"}, "owed_by": "customer", "type": "PAY-REVENUE-SHARE"}], "escalation": []}
Got: {"escalated": true, "escalation_codes": ["E4_SCHEMA_FAIL"], "obligations": [], "schema_valid": false}
Ungrounded quotes: []
Trace:
- 1 retrieval_precheck: {"categories":["Affiliate License-Licensee","Affiliate License-Licensor","Anti-Assignment","Audit Rights","Cap On Liability","Change Of Control","Covenant Not To Sue","Exclusivity","Insurance","Ip Own | None | retries=0
- 2 llm_response: {"turn":1} | None | retries=0
- 3 search_corpus: {"query":"renewal"} | None | retries=0
- 4 search_corpus: {"query":"insurance"} | None | retries=0
- 5 search_corpus: {"query":"royalty"} | None | retries=0
- 6 llm_response: {"turn":2} | None | retries=0
- 7 get_clause: {"category":"Revenue/Profit Sharing","document_id":"adv_27af83733ab09ead99b0"} | None | retries=0
- 8 get_clause: {"category":"Insurance","document_id":"adv_27af83733ab09ead99b0"} | None | retries=0
- 9 llm_response: {"turn":3} | None | retries=0
- 10 search_corpus: {"query":"renewal fee is due and payable thirty (30) days prior"} | None | retries=0
- 11 llm_response: {"turn":4} | None | retries=0
- 12 record_obligations: {"confidence":1,"escalate":false,"escalation_codes":[],"obligations":[{"clause_category":"unlabelled paragraph","clause_quote":"Franchisee  agrees that in consideration of the grant of the \"Successor | VALIDATION_ERROR | retries=0
- 13 llm_response: {"turn":5} | None | retries=0
- 14 get_clause: {"category":"unlabelled paragraph","document_id":"adv_27af83733ab09ead99b0"} | ClauseNotFound | retries=0
- 15 llm_response: {"turn":6} | None | retries=0
- 16 search_corpus: {"query":"Franchisee agrees that in consideration of the grant of the Successor Franchise"} | None | retries=0
- 17 llm_response: {"turn":7} | None | retries=

[Truncated at 100,000 characters.]

