#!/usr/bin/env python3
"""Portable venv helper for the shared make command on POSIX and Windows."""
import os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    if len(sys.argv)!=2 or sys.argv[1] not in ('setup','test'): raise ValueError('expected setup or test')
    if sys.argv[1]=='setup':
        if sys.version_info[:2]!=(3,11): raise ValueError('setup requires Python 3.11; set PYTHON to a 3.11 executable')
        subprocess.run([sys.executable,'-m','venv',str(ROOT/'.venv')],check=True)
    candidate=ROOT/('.venv/Scripts/python.exe' if os.name=='nt' else '.venv/bin/python')
    interpreter=str(candidate) if candidate.exists() else sys.executable
    if sys.argv[1]=='setup': subprocess.run([interpreter,'-m','pip','install','-r',str(ROOT/'requirements.txt')],cwd=ROOT,check=True)
    else:
        env={**os.environ,'B2_OFFLINE':'1'}
        subprocess.run([interpreter,'-m','pytest','-q'],cwd=ROOT,env=env,check=True)
        subprocess.run([interpreter,str(ROOT/'scripts/prompt_hygiene.py')],cwd=ROOT,env=env,check=True)
if __name__=='__main__':
    try: main()
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
