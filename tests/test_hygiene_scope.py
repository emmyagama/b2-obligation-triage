import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import prompt_hygiene as ph


def _root(tmp_path, rel, text):
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return tmp_path


def test_cuad_id_in_prompt_and_tool_description_fail(tmp_path):
    prompt = _root(tmp_path / "a", "prompts/system.md", "Use CUAD_%d as an identifier." % 12)
    with pytest.raises(ValueError, match="identifier pattern"):
        ph.check(prompt)

    tool = _root(tmp_path / "b", "config/tool_descriptions.yaml", "search_corpus: see CUAD_%d" % 34)
    with pytest.raises(ValueError, match="identifier pattern"):
        ph.check(tool)


def test_record_paths_contains_only_agreed_entries():
    assert ph.RECORD_PATHS == ("handoff/", "DECISIONS.md", "reports/", "INTEGRATION-LOG.md")


def test_records_are_skipped_but_model_facing_files_still_scanned(tmp_path):
    _root(tmp_path, "handoff/round_9.md", "trailing CUAD_%d" % 56)
    _root(tmp_path, "DECISIONS.md", "see CUAD_%d" % 78)
    _root(tmp_path, "reports/phase-E.md", "notes CUAD_%d" % 90)
    _root(tmp_path, "prompts/system.md", "clean prompt text")
    ph.check(tmp_path)

    with pytest.raises(ValueError, match="identifier pattern"):
        ph.check(_root(tmp_path / "c", "prompts/system.md", "planted CUAD_%d" % 123))
