from typing import List, Dict, Optional

def show_summary(trace: List[Dict], fields: Optional[List[str]] = None, include_diff: bool = True):
    """
    Prints a concise summary of a trace using selected fields.

    Args:
        trace (List[Dict]): The trace to summarize.
        fields (List[str], optional): Which fields to show per frame. Defaults to common fields.
        include_diff (bool): If True, display variable diffs between steps.
    """
    if not trace:
        print("[pydebugviz] Empty trace.")
        return

    print(f"[pydebugviz] Trace Summary: {len(trace)} steps")
    fields = fields or ["step", "event", "function", "line_no"]

    for i, frame in enumerate(trace):
        row = {f: frame.get(f, "") for f in fields}
        base = " - " + " | ".join(f"{k}: {v}" for k, v in row.items())
        
        if include_diff and "var_diff" in frame and frame["var_diff"]:
            changes = ", ".join(f"{k}: {v['from']} → {v['to']}" for k, v in frame["var_diff"].items())
            print(f"{base} | Δ {changes}")
        else:
            print(base)