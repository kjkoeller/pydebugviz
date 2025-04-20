from typing import List, Dict, Optional, Any
from .utils import validate_expressions, truncate_vars, deepcopy_locals
import sys

def debug(func, *args,
          breakpoints: Optional[List[str]] = None,
          watch: Optional[List[str]] = None,
          validate: bool = True,
          max_steps: int = 10000,
          max_var_len: int = 100,
          deep_copy: bool = False,
          **kwargs) -> List[Dict]:

    trace = []
    step_count = 0
    prev_raw_locals = None

    if breakpoints and validate:
        bad_exprs = validate_expressions(breakpoints)
        if bad_exprs:
            raise ValueError(f"Invalid breakpoint expressions: {bad_exprs}")

    def tracer(frame, event, arg):
        nonlocal step_count, prev_raw_locals
        if event not in {"call", "line", "return", "exception"}:
            return tracer
        if step_count >= max_steps:
            print("[pydebugviz] Max step limit reached. Stopping trace.")
            return None

        raw_locals = frame.f_locals.copy()
        copied_raw_locals = deepcopy_locals(raw_locals) if deep_copy else raw_locals.copy()

        # Detect change from previous snapshot
        changed = prev_raw_locals != copied_raw_locals
        is_new_event = event in {"call", "return", "exception"}

        if changed or is_new_event:
            frame_data = {
                "event": event,
                "function": frame.f_code.co_name,
                "line_no": frame.f_lineno,
                "locals": truncate_vars(raw_locals, max_len=max_var_len),
                "raw_locals": copied_raw_locals
            }

            if event == "return":
                try:
                    frame_data["return"] = str(arg)
                except Exception:
                    frame_data["return"] = "<unrepr>"

            trace.append(frame_data)
            step_count += 1
            prev_raw_locals = copied_raw_locals

        return tracer

    sys.settrace(tracer)
    try:
        func(*args, **kwargs)
    finally:
        sys.settrace(None)

    return trace
