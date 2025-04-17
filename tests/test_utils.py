from pydebugviz.utils import validate_expressions, safe_eval, normalize_trace, check_trace_schema

def test_validation_tools():
    assert "x ==" in validate_expressions(["x > 1", "x =="])
    assert safe_eval("x > 2", {"x": 3}) is True

def test_trace_schema():
    raw = [{"event": "line", "function": "f", "line_no": 5, "locals": {"x": 1}}]
    norm = normalize_trace(raw)
    errors = check_trace_schema(norm)
    assert errors == []
