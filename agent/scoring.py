from datetime import date
import re

def normal_ws(s): return re.sub(r'\s+', ' ', s).strip()

def deadline_match(g, p):
    if g.get('kind') != p.get('kind'): return False
    if g['kind'] == 'none': return True
    gd = g.get('resolved_date'); pd = p.get('resolved_date')
    if gd is None: return pd is None  # absent anchor must not be fabricated
    if pd is None: return False
    try: return abs((date.fromisoformat(gd)-date.fromisoformat(pd)).days) <= 1
    except (ValueError, TypeError): return False

def score(case, output, document, error=None):
    gold=case['gold_obligations']; got=output.get('obligations',[]); used=set(); matches=[]
    # Maximum deadline-compatible matching first; then match remaining identity-only pairs.
    edges={gi:[pi for pi,p in enumerate(got) if (p['type'],p['owed_by'])==(g['type'],g['owed_by']) and deadline_match(g['deadline'],p['deadline'])] for gi,g in enumerate(gold)}
    owner={}; gold_used=set()
    def augment(gi,seen):
        for pi in edges[gi]:
            if pi in seen: continue
            seen.add(pi)
            if pi not in owner or augment(owner[pi],seen): owner[pi]=gi; return True
        return False
    for gi in range(len(gold)): augment(gi,set())
    for pi,gi in sorted(owner.items()): gold_used.add(gi); used.add(pi); matches.append((gold[gi],got[pi]))
    for gi,g in enumerate(gold):
        if gi in gold_used: continue
        for pi,p in enumerate(got):
            if pi not in used and (p['type'],p['owed_by'])==(g['type'],g['owed_by']):
                gold_used.add(gi); used.add(pi); matches.append((g,p)); break
    grounded=all(normal_ws(o['clause_quote']) in normal_ws(document) and bool(normal_ws(o['clause_quote'])) for o in got)
    fields={'schema_valid':bool(output.get('schema_valid',False)), 'obligations_found':len(matches)==len(gold) and len(got)-len(used)<=1,
       'deadlines_captured':len(matches)==len(gold) and all(deadline_match(g['deadline'],p['deadline']) for g,p in matches),
       'escalation_correct':output.get('escalated')==case['gold_should_escalate'], 'grounded':grounded}
    fields['exception']=not all(fields.values()) or bool(error)
    return fields, matches
