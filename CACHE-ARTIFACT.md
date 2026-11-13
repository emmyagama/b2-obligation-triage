# LLM cache artifact

The checkout currently tracks 10,479 provider-response files under `cache/llm/` (about 90.8 MB). That keeps offline replay simple, but it is most of the tracked file count and a large part of the clone. The proposed replacement is one versioned, compressed artifact with a published SHA-256 checksum.

## Status

The artifact is not published and the tracked files have not been migrated. The current `cache/llm/*.json` files remain the replay source. Migration should happen only after a clean-clone replay from the artifact passes and the privacy review below is complete.

The cache stores request payloads as well as responses. Those payloads can contain contract text. Treat the artifact as sensitive; do not publish it publicly without a licensing and privacy review, and do not attach it to a public release if the source contracts are restricted.

## Artifact contract

- Asset name: `b2-llm-cache-v1.zip`
- Checksum asset: `b2-llm-cache-v1.zip.sha256`
- Contents: only `cache/llm/<key>.json`
- Deterministic entry order and timestamps; no absolute paths, `..` entries or non-JSON files
- The checksum covers the complete ZIP byte stream

`scripts/cache_artifact.py` creates and verifies this format.

## Build locally

From a checkout that already has the released cache:

```sh
python scripts/cache_artifact.py pack --out dist/b2-llm-cache-v1.zip
```

This writes `dist/b2-llm-cache-v1.zip` and `dist/b2-llm-cache-v1.zip.sha256`. `dist/` is ignored by Git.

Verify before publishing:

```sh
python scripts/cache_artifact.py verify \
  --archive dist/b2-llm-cache-v1.zip \
  --checksum dist/b2-llm-cache-v1.zip.sha256
```

## Publish

Attach both files to the release or tag that contains the matching evaluation code. The exact asset names above are part of the contract. Do not rename them per release; use a new versioned filename if the cache changes.

## Download

With GitHub CLI, download the exact assets from the release tag:

```sh
gh release download <tag> --pattern 'b2-llm-cache-v1.zip*'
```

The tag is the release carrying the artifact. The download must produce exactly `b2-llm-cache-v1.zip` and `b2-llm-cache-v1.zip.sha256`.

## Verify and replay from a clean clone

POSIX:

```sh
git clone <repo-url> b2-clean
cd b2-clean
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
gh release download <tag> --pattern 'b2-llm-cache-v1.zip*'
sha256sum -c b2-llm-cache-v1.zip.sha256
.venv/bin/python scripts/cache_artifact.py unpack \
  --archive b2-llm-cache-v1.zip \
  --checksum b2-llm-cache-v1.zip.sha256 \
  --dest .
B2_OFFLINE=1 .venv/bin/python run_eval.py --split test
.venv/bin/python check_readme.py
```

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
gh release download <tag> --pattern "b2-llm-cache-v1.zip*"
$expected = (Get-Content .\b2-llm-cache-v1.zip.sha256).Split()[0]
$actual = (Get-FileHash .\b2-llm-cache-v1.zip -Algorithm SHA256).Hash.ToLower()
if ($actual -ne $expected) { throw "SHA-256 mismatch" }
.\.venv\Scripts\python.exe scripts\cache_artifact.py unpack --archive .\b2-llm-cache-v1.zip --checksum .\b2-llm-cache-v1.zip.sha256 --dest .
$env:B2_OFFLINE = '1'
.\.venv\Scripts\python.exe run_eval.py --split test
.\.venv\Scripts\python.exe check_readme.py
```

Success means `check_readme.py` prints `README matches evaluation results`. Replay is offline; no API key or network call is required after the artifact is present.

## Migration follow-up

After the clean-clone replay passes:

1. Remove the individual `cache/llm/*.json` files from Git tracking.
2. Add `cache/llm/` to `.gitignore`.
3. Update CI to download the release asset, verify the checksum, and unpack it before the replay leg.
4. Keep `cache/llm/` blocked by the pre-push guard so response payloads are not accidentally committed.
5. Re-run `python run_eval.py --split test`, `python check_readme.py`, `make test`, and the clean-clone replay.

Do not delete the tracked cache until the artifact is published and the clean-clone replay has passed.
