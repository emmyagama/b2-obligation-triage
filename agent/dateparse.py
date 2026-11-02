"""Conservative parsing of explicit unambiguous dates; never infer missing parts."""
import re
from datetime import datetime
MONTH=r'(?:January|February|March|April|May|June|July|August|September|October|November|December)'
PATTERN=rf'\b(?:\d{{4}}-\d{{2}}-\d{{2}}|{MONTH}\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+\d{{4}}|\d{{1,2}}(?:st|nd|rd|th)?\s+{MONTH}\s+\d{{4}})\b'
def explicit_dates(text):
    values=set()
    for text in re.findall(PATTERN,text or '',re.I):
        text=re.sub(r'(?<=\d)(st|nd|rd|th)\b','',text,flags=re.I).replace(',','')
        for fmt in ('%Y-%m-%d','%B %d %Y','%d %B %Y'):
            try: values.add(datetime.strptime(text,fmt).date().isoformat());break
            except ValueError: pass
    return values
