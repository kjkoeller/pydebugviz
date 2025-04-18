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

def compute_var_diff(prev, curr):
    def is_primitive(x):
        return isinstance(x, (int, float, str, bool, type(None)))

    def shallow_diff(a, b):
        return {"from": a, "to": b}

    def recursive_diff(a, b, prefix=""):
        diffs = {}
        if type(a) != type(b):
            diffs[prefix] = shallow_diff(a, b)
        elif isinstance(a, dict):
            keys = set(a) | set(b)
            for key in keys:
                subkey = f"{prefix}.{key}" if prefix else str(key)
                if key in a and key in b:
                    subdiffs = recursive_diff(a[key], b[key], prefix=subkey)
                    diffs.update(subdiffs)
                elif key in a:
                    diffs[subkey] = {"from": a[key], "to": "<deleted>"}
                else:
                    diffs[subkey] = {"from": "<missing>", "to": b[key]}
        elif isinstance(a, list):
            for i, (ai, bi) in enumerate(zip(a, b)):
                subkey = f"{prefix}[{i}]"
                subdiffs = recursive_diff(ai, bi, subkey)
                diffs.update(subdiffs)
            if len(a) < len(b):
                for i in range(len(a), len(b)):
                    subkey = f"{prefix}[{i}]"
                    diffs[subkey] = {"from": "<missing>", "to": b[i]}
            elif len(a) > len(b):
                for i in range(len(b), len(a)):
                    subkey = f"{prefix}[{i}]"
                    diffs[subkey] = {"from": a[i], "to": "<deleted>"}
        elif is_primitive(a) and a != b:
            diffs[prefix] = shallow_diff(a, b)
        elif not is_primitive(a) and str(a) != str(b):
            diffs[prefix] = shallow_diff(str(a), str(b))
        return diffs

    diff = {}
    for key in set(prev) | set(curr):
        val_a = prev.get(key, "<missing>")
        val_b = curr.get(key, "<missing>")

        # ✅ Always call recursive_diff, even if a == b
        nested = recursive_diff(val_a, val_b, key)
        if nested:
            diff[key] = {"nested": nested} if len(nested) > 1 else list(nested.values())[0]

    return diff

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

        # Compute variable diffs using raw_locals if available
        if i > 0:
            prev_raw = trace[i - 1].get("raw_locals", {})
            curr_raw = frame.get("raw_locals", {})
            norm["var_diff"] = compute_var_diff(prev_raw, curr_raw)
        else:
            norm["var_diff"] = {}

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


def safe_deepcopy(obj):
    try:
        return copy.deepcopy(obj)
    except Exception:
        return obj

def deepcopy_locals(locals_dict):
    copied = {}
    for key, val in locals_dict.items():
        copied[key] = safe_deepcopy(val)
    return copied
