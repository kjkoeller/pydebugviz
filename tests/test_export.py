import os
from pydebugviz import debug
from pydebugviz.export import export_html

def test_export_html(tmp_path):
    def test(): return 42
    trace = debug(test)
    path = tmp_path / "trace.html"
    export_html(trace, filepath=str(path))
    assert path.exists()
