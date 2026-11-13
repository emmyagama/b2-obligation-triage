from scripts.render_readme import fmt_cost


def test_fmt_cost_rounds_both_float_representations_to_same_text():
    expected = "$0.0079 per transaction, n=30"
    assert fmt_cost({"n": 30, "mean_usd": 0.007870434333333332}) == expected
    assert fmt_cost({"n": 30, "mean_usd": 0.007870434333333334}) == expected


def test_fmt_cost_handles_empty_denominator():
    assert fmt_cost({"n": 0, "mean_usd": None}) == "not measurable (0 denominator)"
