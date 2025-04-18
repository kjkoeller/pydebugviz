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