from pathlib import Path

from scripts import cache_artifact


def test_cache_artifact_pack_verify_unpack_is_deterministic(tmp_path):
    cache = tmp_path / "cache" / "llm"
    cache.mkdir(parents=True)
    (cache / "a.json").write_text('{"request":1}', encoding="utf-8")
    (cache / "b.json").write_text('{"request":2}', encoding="utf-8")

    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"
    cache_artifact.pack(cache, first)
    cache_artifact.pack(cache, second)
    assert cache_artifact.sha256(first) == cache_artifact.sha256(second)

    checksum = Path(str(first) + ".sha256")
    count, total, _ = cache_artifact.verify(first, checksum)
    assert count == 2
    assert total == len('{"request":1}') + len('{"request":2}')

    out = tmp_path / "out"
    cache_artifact.unpack(first, checksum, out)
    assert (out / "cache" / "llm" / "a.json").read_text(encoding="utf-8") == '{"request":1}'
    assert (out / "cache" / "llm" / "b.json").read_text(encoding="utf-8") == '{"request":2}'
