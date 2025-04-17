import os, tempfile
from pydebugviz import debug
from pydebugviz.export import export_html

def test_export_html(tmp_path):
    def test(): return 42
    trace = debug(test)
    path = tmp_path / "trace.html"
    export_html(trace, filepath=str(path))
    assert path.exists()

def test_html_export_with_sparse_trace():
    trace = [{"step": 0, "event": "call", "function": "demo", "line_no": 1, "locals": {}, "annotation": ""}]
    path = os.path.join(tempfile.gettempdir(), "test_export.html")
    export_html(trace, path)
    assert os.path.exists(path)

