import csv, json
from pathlib import Path

def jsonwrite(path, data): Path(path).write_text(json.dumps(data,sort_keys=True,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def csvwrite(path, rows, columns):
    with Path(path).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def fmt(r):
    if not r or not r['denominator']: return 'not measurable (0 denominator)'
    a,b=r['wilson_95']; return f"{r['value']:.1%} ({r['numerator']}/{r['denominator']}; Wilson 95% {a:.1%}–{b:.1%})"

def summary(metrics, title):
    lines=['# '+title,'','Proportion intervals are Wilson 95%; intervals are not used for latency or cost.','','| Metric | Result |','|---|---|']
    for k in ('exception_rate','deadline_absolute','deadline_relative','obligation_recall','escalation_recall','false_escalation','grounded_rate','deadline_recurring','deadline_none'):
        lines.append('| '+k+' | '+fmt(metrics[k])+' |')
    lines += ['', 'Constructed E2 cases: '+str(metrics['constructed_e2_cases'])+'.', 'Constructed E2 exception rate: '+fmt(metrics['constructed_e2_exception_rate'])+'.', 'Constructed E2 code recall: '+fmt(metrics['constructed_e2_recall'])+'.']
    l=metrics['latency']; c=metrics['cost']
    lines+=['',f"Latency p50 / p95: {l['p50_ms']} / {l['p95_ms']} ms (n={l['n']}).",f"Mean cost: {c['mean_usd']} USD (n={c['n']}).",'', 'Small samples yield wide intervals; do not treat relative-deadline results as precise.','']
    return '\n'.join(lines)
