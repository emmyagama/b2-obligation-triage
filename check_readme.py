#!/usr/bin/env python3
import sys
from pathlib import Path
from scripts.render_readme import render
try:
    if Path(__file__).with_name('README.md').read_text()!=render(): raise ValueError('README drift: regenerate from evaluation results')
    print('README matches evaluation results')
except Exception as e:
    print(str(e),file=sys.stderr);sys.exit(1)
