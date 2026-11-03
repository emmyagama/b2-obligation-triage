#!/usr/bin/env python3
"""Compatibility entry point; defaults to offline like build_embeddings."""
import runpy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
runpy.run_module('scripts.build_embeddings',run_name='__main__')
