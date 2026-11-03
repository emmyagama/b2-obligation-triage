from math import sqrt, floor, ceil

def wilson(k,n,z=1.959963984540054):
    if n == 0: return None
    p=k/n; den=1+z*z/n; mid=(p+z*z/(2*n))/den; half=z*sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return (max(0,mid-half),min(1,mid+half))

def rate(k,n): return {'numerator':k,'denominator':n,'value':k/n if n else None,'wilson_95':wilson(k,n)}

def percentile(xs, q):
    if not xs: return None
    xs=sorted(xs); pos=(len(xs)-1)*q; lo=floor(pos); hi=ceil(pos)
    return xs[lo] + (xs[hi]-xs[lo])*(pos-lo)

def aggregate(records):
    from .scoring import deadline_match,normal_ws
    n=len(records)
    gold=sum(len(r['case']['gold_obligations']) for r in records)
    found=sum(len(r['matches']) for r in records)
    positives=sum(bool(r['case']['gold_should_escalate']) for r in records)
    negatives=n-positives
    escalated_true=sum(bool(r['case']['gold_should_escalate']) and bool(r['output'].get('escalated')) for r in records)
    escalated_false=sum(not r['case']['gold_should_escalate'] and bool(r['output'].get('escalated')) for r in records)
    quoted=[(o,r['document']) for r in records for o in r['output'].get('obligations',[])]
    m={'exception_rate':rate(sum(r['checks']['exception'] for r in records),n), 'obligation_recall':rate(found,gold),
       'escalation_recall':rate(escalated_true,positives),'false_escalation':rate(escalated_false,negatives),
       'grounded_rate':rate(sum(bool(normal_ws(o['clause_quote'])) and normal_ws(o['clause_quote']) in normal_ws(doc) for o,doc in quoted),len(quoted))}
    for kind in ('absolute','relative','recurring','none'):
        denom=sum(g['deadline']['kind']==kind for r in records for g in r['case']['gold_obligations'])
        num=sum(g['deadline']['kind']==kind and deadline_match(g['deadline'],p['deadline']) for r in records for g,p in r['matches'])
        m['deadline_'+kind]=rate(num,denom)
    lat=[r['latency_ms'] for r in records if r.get('latency_ms') is not None]
    costs=[r['cost_usd'] for r in records if r.get('cost_usd') is not None]
    constructed=[r for r in records if r['case'].get('constructed') is True and r['case']['class']=='conflicting']
    m['constructed_e2_cases']=len(constructed)
    m['constructed_e2_exception_rate']=rate(sum(r['checks']['exception'] for r in constructed),len(constructed))
    positives=[r for r in constructed if 'E2_CONFLICTING_CLAUSES' in r['case'].get('gold_escalation_codes',[])]
    m['constructed_e2_recall']=rate(sum('E2_CONFLICTING_CLAUSES' in r['output'].get('escalation_codes',[]) for r in positives),len(positives))
    m['latency']={'n':len(lat),'p50_ms':percentile(lat,.5),'p95_ms':percentile(lat,.95)}
    m['cost']={'n':len(costs),'mean_usd':sum(costs)/len(costs) if costs else None}
    return m

def aggregate_csv(rows):
    """Independently reconstruct published aggregates from per-case CSV."""
    def number(v): return int(v)
    def boolean(v):
        if v not in ('True','False'): raise ValueError('invalid boolean in results CSV')
        return v=='True'
    n=len(rows); pos=sum(boolean(r['gold_escalate']) for r in rows); neg=n-pos
    m={'exception_rate':rate(sum(boolean(r['exception']) for r in rows),n),
       'obligation_recall':rate(sum(number(r['matched_count']) for r in rows),sum(number(r['gold_count']) for r in rows)),
       'escalation_recall':rate(sum(boolean(r['gold_escalate']) and boolean(r['escalated']) for r in rows),pos),
       'false_escalation':rate(sum(not boolean(r['gold_escalate']) and boolean(r['escalated']) for r in rows),neg),
       'grounded_rate':rate(sum(number(r['grounded_quote_count']) for r in rows),sum(number(r['quote_count']) for r in rows))}
    for k in ('absolute','relative','recurring','none'):
        m['deadline_'+k]=rate(sum(number(r['deadline_'+k+'_correct']) for r in rows),sum(number(r['deadline_'+k+'_total']) for r in rows))
    lat=[float(r['latency_ms']) for r in rows if r['latency_ms'] not in ('','None')]; costs=[float(r['cost_usd']) for r in rows if r['cost_usd'] not in ('','None')]
    constructed=[r for r in rows if boolean(r['constructed']) and r['class']=='conflicting']
    positives=[r for r in constructed if boolean(r['gold_e2'])]
    m['constructed_e2_cases']=len(constructed)
    m['constructed_e2_exception_rate']=rate(sum(boolean(r['exception']) for r in constructed),len(constructed))
    m['constructed_e2_recall']=rate(sum(boolean(r['predicted_e2']) for r in positives),len(positives))
    m['latency']={'n':len(lat),'p50_ms':percentile(lat,.5),'p95_ms':percentile(lat,.95)}
    m['cost']={'n':len(costs),'mean_usd':sum(costs)/len(costs) if costs else None}
    return m
