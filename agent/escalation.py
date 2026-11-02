QUEUES = {'E1_NO_OBLIGATION':'legal-ops', 'E2_CONFLICTING_CLAUSES':'legal-ops', 'E3_CONDITIONAL_OR_AMBIGUOUS':'legal-ops', 'E4_SCHEMA_FAIL':'engineering', 'E5_LOW_CONFIDENCE':'legal-ops', 'E6_TOOL_FAILURE':'engineering'}
CONFLICT_PAIRS = (frozenset(('Cap On Liability','Uncapped Liability')),frozenset(('Irrevocable Or Perpetual License','Termination For Convenience')),frozenset(('Non-Compete','Exclusivity')))

def conflict_candidates(categories):
    cats=set(categories)
    return [sorted(pair) for pair in CONFLICT_PAIRS if pair <= cats]

def apply_floor(confidence, obligations, codes, floor):
    if floor is None: raise ValueError('E5 threshold is not calibrated')
    result = set(codes)
    if confidence < floor or any(o['confidence'] < floor for o in obligations): result.add('E5_LOW_CONFIDENCE')
    if result - QUEUES.keys(): raise ValueError('unknown escalation code')
    return sorted(result)
