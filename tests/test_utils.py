from pydebugviz.utils import validate_expressions, safe_eval, normalize_trace, check_trace_schema, compute_var_diff

def test_validation_tools():
    assert "x ==" in validate_expressions(["x > 1", "x =="])
    assert safe_eval("x > 2", {"x": 3}) is True

def test_trace_schema():
    raw = [{"event": "line", "function": "f", "line_no": 5, "locals": {"x": 1}}]
    norm = normalize_trace(raw)
    errors = check_trace_schema(norm)
    assert errors == []

def test_invalid_expressions():
    bad = ["x === 5", "def x", "for i in 3"]
    result = validate_expressions(bad)
    assert set(result) == set(bad)

def test_safe_eval_failures():
    context = {"x": 5}
    assert safe_eval("x / 0", context) is None
    assert safe_eval("y + 2", context) is None
    assert safe_eval("x > 3", context) is True

def test_normalize_missing_keys():
    raw = [{"function": "f", "line_no": 10, "locals": {"a": 1}}]
    norm = normalize_trace(raw)
    assert isinstance(norm, list)
    assert "event" in norm[0]
    assert "annotation" in norm[0]

def test_validate_expressions():
    result = validate_expressions(["x == 1", "bad =="])
    assert "bad ==" in result

def test_safe_eval():
    assert safe_eval("x > 5", {"x": 10}) is True

def test_compute_var_diff():
    prev = {"x": 1}
    curr = {"x": 2, "y": 5}
    diff = compute_var_diff(prev, curr)
    assert "x" in diff and diff["x"]["to"] == 2
