# v1.1 freeze protocol

The v1.0 freeze remains immutable: `scripts/freeze_check.py`, `code-frozen`,
`guide-v1.0`, `test-frozen` and `targets-v1` are unchanged. An old-baseline
checkout still validates with the v1.0 guard.

## Selection

`scripts/freeze_select.py` selects the guard:

- `code-frozen-v1.1` tag present: use `scripts/freeze_check_v11.py`.
- tag absent: use the preserved v1.0 `scripts/freeze_check.py`.

If a v1.1 tree contains protected changes but no v1.1 tag, the v1.0 guard
fails closed. The selector is used by `run_eval.py`, the pre-push guard and the
failure digest, so replay and release checks do not bypass the old guard.

## v1.1 guard

`scripts/freeze_check_v11.py` verifies:

- the old held-out and synthetic commitments are still intact;
- test/dev counts match `config/splits.yaml`;
- `guide-v1.0` still matches `guide/`;
- protected paths match `code-frozen-v1.1`;
- no untracked protected files are present;
- the threshold calibration report hash matches, and thresholds are not
  provisional.

Protected v1.1 paths are the same code, prompt, taxonomy, config, scoring,
guide, corpus, database and dev/test commitment paths as v1.0, plus the v1.1
guard/selector under `scripts/`.

## Tagging rule

Create `code-frozen-v1.1` only on the reviewed v1.1 release commit, after the
offline replay and README checks pass. Never move the v1.0 tags. Any later
change to a protected path requires a new reviewed freeze point; do not update
the tag in place.

This protocol does not yet define a new v1.1 held-out test population or
commitment. The guard continues to validate the existing commitments. A new
test protocol, tags and logs must be added before any new held-out evaluation.
