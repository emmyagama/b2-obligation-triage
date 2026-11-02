#!/usr/bin/env python3
import sys,zipfile
from pathlib import PurePosixPath
try:
    with zipfile.ZipFile(sys.argv[1]) as z:
        for n in z.namelist():
            p=PurePosixPath(n)
            if p.is_absolute() or '..' in p.parts or not (n.startswith('prompts/') or n=='config/tool_descriptions.yaml' or n.startswith('ROUND_') and n.endswith('_NOTES.md')):
                raise ValueError('disallowed patch path: '+n)
    print('patch surface passed')
except Exception as e:
    print(str(e),file=sys.stderr); sys.exit(1)
