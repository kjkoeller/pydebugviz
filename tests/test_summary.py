from pydebugviz import debug
from pydebugviz.summary import show_summary

def test_summary_runs(capfd):
    def test(): a = 1; return a
    trace = debug(test)
    show_summary(trace)
    out, _ = capfd.readouterr()
    assert "Trace Summary" in out
