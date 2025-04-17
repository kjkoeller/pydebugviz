from typing import List, Dict, Optional
from .utils import validate_expressions, truncate_vars

def debug(func, *args,
          breakpoints: Optional[List[str]] = None,
          watch: Optional[List[str]] = None,
          validate: bool = True,
          max_steps: int = 10000,
          max_var_len: int = 100,
          **kwargs) -> List[Dict]:
    """
    Main debug function that supports:
    - breakpoints with syntax checking
    - truncation of large variable outputs
    - max step protection to prevent runaway traces
    """
    import sys

    trace = []
    step_count = 0

    if breakpoints:
        bad_exprs = validate_expressions(breakpoints)
        if bad_exprs:
            raise ValueError(f"Invalid breakpoint expressions: {bad_exprs}")

    def tracer(frame, event, arg):
        nonlocal step_count
        if event not in {"call", "line", "return", "exception"}:
            return tracer
        if step_count >= max_steps:
            print("[pydebugviz] Max step limit reached. Stopping trace.")
            return None
        step_count += 1

        frame_data = {
            "event": event,
            "function": frame.f_code.co_name,
            "line_no": frame.f_lineno,
            "locals": truncate_vars(frame.f_locals.copy(), max_len=max_var_len)
        }

        if event == "return":
            try:
                frame_data["return"] = str(arg)
            except Exception:
                frame_data["return"] = "<unrepr>"

        trace.append(frame_data)
        return tracer

    sys.settrace(tracer)
    try:
        func(*args, **kwargs)
    finally:
        sys.settrace(None)

    return trace
