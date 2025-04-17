import sys
import time
from typing import List, Dict, Optional

def live_watch(func, watch: Optional[List[str]] = None, interval: float = 0.2, max_steps: int = 10000):
    """
    Live variable capture while a function runs. Works in CLI and Jupyter.

    Args:
        func (callable): The function to trace.
        watch (List[str], optional): List of variable names to watch.
        interval (float): Time between updates in seconds (used for pacing display).
        max_steps (int): Safety limit on max trace steps.
    """
    trace = []
    step_count = 0
    watch = watch or []

    def tracer(frame, event, arg):
        nonlocal step_count
        if event not in {"call", "line", "return"}:
            return tracer
        if step_count >= max_steps:
            print("[live_watch] Max step limit reached.")
            return None
        step_count += 1

        locals_snapshot = frame.f_locals.copy()
        watched_vars = {k: str(locals_snapshot.get(k, "<not defined>")) for k in watch}
        step_info = f"[Step {step_count}] {frame.f_code.co_name}:{frame.f_lineno} | " + ", ".join(f"{k}={v}" for k, v in watched_vars.items())

        print(step_info)
        trace.append({
            "step": step_count,
            "function": frame.f_code.co_name,
            "line_no": frame.f_lineno,
            "event": event,
            "locals": locals_snapshot
        })
        time.sleep(interval)
        return tracer

    sys.settrace(tracer)
    try:
        func()
    finally:
        sys.settrace(None)

    return trace
