from pydebugviz import debug, normalize_trace
from pydebugviz.summary import show_summary

def test_summary_runs(capfd):
    def test(): a = 1; return a
    trace = debug(test)
    show_summary(trace)
    out, _ = capfd.readouterr()
    assert "Trace Summary" in out

def test_show_summary(capsys):
    def bar():
        a = 1
        a += 1

    trace = normalize_trace(debug(bar))
    show_summary(trace)
    out, _ = capsys.readouterr()
    assert "step" in out and "event" in out
