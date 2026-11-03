# B2 contract-obligation triage — evaluation pending

CUAD comprises US commercial contracts, not evidence about Nigerian or Gulf law; this is not legal advice. CUAD clause-category labels are agent inputs, so clause location is not evaluated. The 25 title-derived buckets are project-defined, not an official CUAD taxonomy. Emmanuel alone authors the obligation/deadline gold under the human guide.

**No evaluation results are available.** The human sweep found no genuine E2 conflict among the 40 selected contracts. All 14 planned E2 examples are constructed composites of real clauses, with human-selected pairs and human-authored gold; they are not natural conflicts in source contracts. Their E2 results will be shown separately.

The planned split is dev 26 (14 clear / 5 constructed conflicting / 5 out-of-scope / 2 adversarial) and test 30 (12 / 9 / 5 / 4), total 56. The existing dev work contains 21 cases; five composite cases remain human work. No held-out cases or generated test-synthetic materials are released here. Metrics, calibration, live runs and human review are pending.

## Lean retrieval and local synthesis

Runtime uses text-free NumPy indexes and brute-force cosine; float16 vectors are converted to float32 for comparison, scores rounded to four decimals, ties by chunk ID. Text is recovered from exact character slices of source documents. The legacy Chroma store is needed only for one-time export; it is not a runtime or CI dependency. See `BUNDLE-NOTES.md` for local export and verification, base index completion, test-shard commands, freeze gates, case schema and unresolved guide implications. No synthetic script chooses conflict pairs or writes gold.

Run `make setup` with Python 3.11 and `make test` for offline fixtures. Replay is the default and a cache miss exits 3; `B2_OFFLINE=1` prohibits HTTP. A completed frozen test run and released cache are prerequisites for the held-out replay CI leg. Neither these fixtures nor eventual constructed E2 results establish natural-conflict performance.
