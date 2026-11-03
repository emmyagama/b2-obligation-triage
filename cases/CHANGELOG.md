# Cases changelog

Case-level changes to `cases/src`, newest first. Guide text changes live in `guide/annotation-guide.md` §13; decisions of record in `DECISIONS.md`; both splits are described in `DEV-NOTES.md` and `TEST-NOTES.md`.

## 2026-11-04

- **dev-15** moved from `out_of_scope` to `clear`; `gold_should_escalate` false→true, `gold_escalation_codes` `[]`→`[E1_NO_OBLIGATION]`. Reason: the document carries only trivial labels, and guide §8 places E1 inside `clear` cases. Found while calibrating, not from reading model output. Guide unchanged.
- `config/splits.yaml` dev line → `{clear: 15, conflicting: 5, out_of_scope: 4, adversarial: 2}` = 26. Test line unchanged at 12 / 9 / 5 / 4 = 30; the held-out set was not touched, so `cases/FROZEN.sha256` was **not** re-signed for this change.
- `config/thresholds.yaml`: `e1` provenance `provisional-dev-only` → `uncalibrated`; value left at `-1.0`, which disables the floor. One dev E1 positive is not enough to calibrate a retrieval threshold, and E1 is a role-mapping answer a floor cannot detect. Held-out runs refuse an `uncalibrated` E1 floor. E1 coverage for the sweep must come from the pilot's double annotation (guide §11.3 rule 5 requires E1 at least twice).
- No obligation records changed. `dev-15` has no gold obligations before or after.
