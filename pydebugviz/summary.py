from typing import List, Dict, Optional

def show_summary(trace: List[Dict], fields: Optional[List[str]] = None):
    """
    Prints a concise summary of a trace using selected fields.

    Args:
        trace (List[Dict]): The trace to summarize.
        fields (List[str], optional): Which fields to show per frame. Defaults to common fields.
    """
    if not trace:
        print("[pydebugviz] Empty trace.")
        return

    print(f"[pydebugviz] Trace Summary: {len(trace)} steps")
    fields = fields or ["step", "event", "function", "line_no"]

    for frame in trace:
        row = {f: frame.get(f, "") for f in fields}
        print(" -", " | ".join(f"{k}: {v}" for k, v in row.items()))
