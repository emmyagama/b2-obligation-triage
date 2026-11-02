# INTEGRATION-LOG.md

Environment fixes and small code fixes made by the execution agent (rule 1 of the handoff brief). Each entry: file, reason, diff.

## 2026-11-02 — Environment: GitHub CLI (`gh`) missing

- **File / component:** host environment (no project file touched).
- **Reason:** the brief requires `gh auth status` in Phase A4 and `gh run watch` in Phase G; `gh` was not installed (`Get-Command gh` → CommandNotFound).
- **Action:** `winget install --id GitHub.cli -e --accept-source-agreements --accept-package-agreements --disable-interactivity` → installed GitHub CLI 2.103.3 to `C:\Program Files\GitHub CLI\gh.exe`.
- **Diff:** none in the repository.
- **Follow-up:** `gh auth status` reports *not logged in* — the credential stored by Git Credential Manager is rejected by `gh auth login --with-token` with `error validating token: missing required scope 'read:org'`. Worked around by using the GitHub REST API with the same stored credential for repository creation (token never printed). See `reports/phase-A.md` open issue OI-1.

## 2026-11-02 — Environment: CUAD download URL invalid as written in the brief

- **File / component:** `data/cuad/data.zip` (gitignored data).
- **Reason:** `github.com/TheAtticusProject/cuad/raw/master/data.zip` returns HTTP 404 (repository renamed to `The-Atticus-Project`, default branch `main`); the first download attempt received a 231,223-byte GitHub HTML page instead of a ZIP.
- **Action:** re-downloaded from `https://raw.githubusercontent.com/The-Atticus-Project/cuad/main/data.zip` (18,309,308 bytes, sha256 `F8161D18BEA4E9C05E78FA6DDA61C19C846FB8087EA969C172753BC2F45B999A`), verified ZIP magic `50 4B 03 04`, extracted to `data/cuad/`.
- **Diff:** none in the repository (data is gitignored).
