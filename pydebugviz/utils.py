from typing import List, Dict, Any, Optional
import ast

def safe_eval(expr: str, context: dict) -> Optional[bool]:
    try:
        return eval(expr, {}, context)
    except Exception:
        return None

def validate_expressions(expressions: List[str]) -> List[str]:
    invalid = []
    for expr in expressions:
        try:
            ast.parse(expr, mode="eval")
        except SyntaxError:
            invalid.append(expr)
    return invalid

def truncate_vars(locals_dict: Dict[str, Any], max_len: int = 100) -> Dict[str, str]:
    truncated = {}
    for k, v in locals_dict.items():
        try:
            s = str(v)
            if len(s) > max_len:
                s = s[:max_len] + "..."
            truncated[k] = s
        except Exception:
            truncated[k] = "<unrepr>"
    return truncated

def normalize_trace(trace: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for i, frame in enumerate(trace):
        norm = {
            "step": i,
            "event": str(frame.get("event", "line")),
            "function": str(frame.get("function", "unknown")),
            "line_no": int(frame.get("line_no", -1)),
            "locals": frame.get("locals", {}) or {},
            "annotation": frame.get("annotation", "")
        }
        if "return" in frame:
            norm["return"] = frame["return"]
        if "exception" in frame:
            norm["exception"] = frame["exception"]
        normalized.append(norm)
    return normalized

def check_trace_schema(trace: List[Dict[str, Any]]) -> List[str]:
    errors = []
    for i, frame in enumerate(trace):
        if not isinstance(frame, dict):
            errors.append(f"Step {i}: Frame is not a dict.")
            continue
        required_keys = ["step", "event", "function", "line_no", "locals", "annotation"]
        for key in required_keys:
            if key not in frame:
                errors.append(f"Step {i}: Missing key '{key}'.")

        if frame["event"] not in {"call", "line", "return", "exception"}:
            errors.append(f"Step {i}: Invalid event '{frame['event']}'.")

        if not isinstance(frame["step"], int):
            errors.append(f"Step {i}: 'step' must be an int.")
        if not isinstance(frame["function"], str):
            errors.append(f"Step {i}: 'function' must be a string.")
        if not isinstance(frame["line_no"], int):
            errors.append(f"Step {i}: 'line_no' must be an int.")
        if not isinstance(frame["locals"], dict):
            errors.append(f"Step {i}: 'locals' must be a dict.")
        if not isinstance(frame["annotation"], str):
            errors.append(f"Step {i}: 'annotation' must be a string.")

    return errors

# Alias for legacy support
validate_trace = check_trace_schema
