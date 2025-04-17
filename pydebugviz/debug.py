from typing import List, Dict, Optional

def validate_trace(trace: List[Dict]) -> List[str]:
    required_keys = {"event", "function", "line_no", "locals"}
    problems = []
    for i, frame in enumerate(trace):
        if not isinstance(frame, dict):
            problems.append(f"Step {i}: Frame is not a dict.")
            continue
        missing = required_keys - frame.keys()
        if missing:
            problems.append(f"Step {i}: Missing keys: {missing}")
        if "line_no" in frame and not isinstance(frame["line_no"], int):
            problems.append(f"Step {i}: 'line_no' must be an int.")
        if "locals" in frame and not isinstance(frame["locals"], dict):
            problems.append(f"Step {i}: 'locals' must be a dict.")
        if "event" in frame and frame["event"] not in {"call", "line", "return", "exception"}:
            problems.append(f"Step {i}: Unknown event type '{frame['event']}'.")
    return problems

def debug(func, *args,
          breakpoints: Optional[List[str]] = None,
          watch: Optional[List[str]] = None,
          validate: bool = True,
          **kwargs) -> List[Dict]:
    import sys
    trace = []
    def tracer(frame, event, arg):
        if event not in {"call", "line", "return", "exception"}:
            return tracer
        frame_data = {
            "event": event,
            "function": frame.f_code.co_name,
            "line_no": frame.f_lineno,
            "locals": frame.f_locals.copy()
        }
        if event == "return":
            frame_data["return"] = arg
        trace.append(frame_data)
        return tracer
    sys.settrace(tracer)
    try:
        func(*args, **kwargs)
    finally:
        sys.settrace(None)
    if validate:
        issues = validate_trace(trace)
        if issues:
            print("[pydebugviz] Trace validation found issues:")
            for issue in issues:
                print("  -", issue)
        else:
            print("[pydebugviz] Trace passed validation.")
    return trace
