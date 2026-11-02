from datetime import date, timedelta
import calendar,re

def add_months(d, months):
    total=d.year*12+d.month-1+months; year,month=divmod(total,12); month+=1
    return date(year,month,min(d.day,calendar.monthrange(year,month)[1]))

def anniversary(d, year):
    try: return d.replace(year=year)
    except ValueError: return d.replace(year=year, day=28)

def resolve(deadline, anchors):
    """Resolve unambiguous structured dates, preserving raw text and escalating uncertainty."""
    out=dict(deadline); kind=out['kind']; unresolved=False
    if kind=='absolute':
        if not out.get('resolved_date'): raise ValueError('absolute deadline requires resolved_date')
        date.fromisoformat(out['resolved_date'])
    elif kind=='relative':
        anchor=anchors.get(out.get('anchor_event'));offset=out.get('offset_days')
        if anchor is None or offset is None: out['resolved_date']=None;unresolved=True
        else: out['resolved_date']=(date.fromisoformat(anchor)+timedelta(days=offset)).isoformat()
    elif kind=='recurring':
        anchor=anchors.get('effective_date'); rule=(out.get('recurring_rule') or '').lower().strip(); first=None
        if anchor:
            d=date.fromisoformat(anchor)
            # Only explicit anniversary-based or anchor-relative cycles are safe to compute.
            if 'anniversary' in rule and not re.search(r'\b(?:termination|expiration|expiry|execution|closing)\b',rule): first=anniversary(d,d.year+1)
            elif re.search(r'\b(?:monthly|each month|every month)\b',rule) and re.search(r'\b(?:after|following)\s+(?:the\s+)?effective date\b',rule): first=add_months(d,1)
            elif re.search(r'\b(?:quarterly|each quarter|every quarter)\b',rule) and re.search(r'\b(?:after|following)\s+(?:the\s+)?effective date\b',rule): first=add_months(d,3)
            elif re.search(r'\b(?:weekly|each week|every week)\b',rule) and re.search(r'\b(?:after|following)\s+(?:the\s+)?effective date\b',rule): first=d+timedelta(days=7)
        out['resolved_date']=first.isoformat() if first else None
        unresolved=first is None
    elif kind=='none': out['resolved_date']=None
    else: raise ValueError('unknown deadline kind')
    return out,unresolved
