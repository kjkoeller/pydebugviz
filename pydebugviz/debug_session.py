from typing import List, Dict, Optional
from .utils import normalize_trace, check_trace_schema, safe_eval

class DebugSession:
    def __init__(self, trace: List[Dict]):
        self.trace = normalize_trace(trace)
        self.pointer = 0
        self.issues = check_trace_schema(self.trace)
        if self.issues:
            print("[pydebugviz] Trace schema issues detected:")
            for issue in self.issues:
                print("  -", issue)

    def jump_to(self, step: int):
        if 0 <= step < len(self.trace):
            self.pointer = step

    def current(self) -> Dict:
        return self.trace[self.pointer]

    def next(self):
        if self.pointer < len(self.trace) - 1:
            self.pointer += 1
        return self.current()

    def prev(self):
        if self.pointer > 0:
            self.pointer -= 1
        return self.current()

    def search(self, condition: str) -> List[int]:
        return [i for i, frame in enumerate(self.trace)
                if safe_eval(condition, frame.get("locals", {}))]

    def show_summary(self, fields: Optional[List[str]] = None):
        fields = fields or ["step", "event", "function", "line_no"]
        for frame in self.trace:
            row = {f: frame.get(f, "") for f in fields}
            print(" -", " | ".join(f"{k}: {v}" for k, v in row.items()))
