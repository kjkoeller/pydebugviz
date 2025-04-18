from pydebugviz import debug, show_summary, normalize_trace

def test_variable_diff_capture(capfd):
    def demo():
        x = 1
        x += 2
        x += 3

    trace = debug(demo)
    trace = normalize_trace(trace)
    show_summary(trace, include_diff=True)

    # Capture output and check for diff indicators
    out, _ = capfd.readouterr()
    assert "→" in out
    
def test_nested_diff_tracking():
    def example():
        data = {"scores": [1, 2], "meta": {"flag": True}}
        data["scores"].append(3)
        data["meta"]["flag"] = False
        return data

    trace = normalize_trace(debug(example, deep_copy=True))
    nested_diffs = [frame.get("var_diff", {}) for frame in trace if "var_diff" in frame]

    # Confirm that nested keys are diffed
    found_flag_change = any(
        "data.meta.flag" in diff.get("data", {}).get("nested", {}) for diff in nested_diffs if isinstance(diff.get("data"), dict)
    )
    found_list_append = any(
        "data.scores[2]" in diff.get("data", {}).get("nested", {}) for diff in nested_diffs if isinstance(diff.get("data"), dict)
    )

    assert found_flag_change, "Did not find nested diff for 'meta.flag'"
    assert found_list_append, "Did not find nested diff for 'scores[2]'"
