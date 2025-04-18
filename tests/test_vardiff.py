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

    # Collect all nested diff keys
    all_keys = []
    for frame in trace:
        var_diff = frame.get("var_diff", {})
        for var, change in var_diff.items():
            if isinstance(change, dict) and "nested" in change:
                all_keys.extend(change["nested"].keys())
            elif isinstance(change, dict):
                all_keys.append(var)

    found_flag = any("meta.flag" in key for key in all_keys)
    found_scores = any("scores[2]" in key for key in all_keys)

    assert found_flag, "Did not find nested diff for 'meta.flag'"
    assert found_scores, "Did not find nested diff for 'scores[2]'"
