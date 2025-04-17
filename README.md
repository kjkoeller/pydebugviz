[![Python OS 3.8, 3.9, 3.10](https://github.com/kjkoeller/pydebugviz/actions/workflows/ci_tests.yml/badge.svg)](https://github.com/kjkoeller/pydebugviz/actions/workflows/ci_tests.yml)
[![PyPI version](https://badge.fury.io/py/pydebugviz.svg)](https://badge.fury.io/py/pydebugviz)
[![GitHub release](https://img.shields.io/github/v/release/kjkoeller/pydebugviz)](https://github.com/kjkoeller/pydebugviz/releases/)

# pydebugviz

**Visual Time-Travel Debugging for Python**  
Trace everything. Watch everything. Export everything.

---

## Overview

`pydebugviz` captures your Python function’s execution step-by-step and lets you explore it in:
- **Jupyter**
- **Terminal (CLI)**
- **IDEs**

Now in v1.0.0:
- ✅ `DebugSession` interactive navigator
- ✅ `live_watch()` for real-time variable display
- ✅ `show_summary()` for CLI/Jupyter-friendly overview
- ✅ `export_html()` for trace visualization
- ✅ Validation tools, safe evaluation, and large var protection

---

## Installation

```bash
pip install pydebugviz
```

---

## Feature Matrix

| Feature             | Jupyter | CLI | IDE |
|---------------------|---------|-----|-----|
| `debug()`           | ✅      | ✅  | ✅  |
| `DebugSession`      | ✅      | ✅  | ✅  |
| `show_summary()`    | ✅      | ✅  | ✅  |
| `export_html()`     | ✅      | ✅  | ✅  |
| `live_watch()`      | ✅      | ✅  | ✅  |
| `validate_trace()`  | ✅      | ✅  | ✅  |

---

## Quick Start

```python
from pydebugviz import debug, show_summary

def test():
    x = 0
    for i in range(4):
        x += i
    return x

trace = debug(test, breakpoints=["x > 3"], max_steps=100)
show_summary(trace)
```

---

## Interactive DebugSession

```python
from pydebugviz import DebugSession

session = DebugSession(trace)
session.jump_to(3)
print(session.current())
session.show_summary()
```

---

## Live Watch Mode

```python
from pydebugviz import live_watch

def my_function():
    x = 1
    for i in range(3): x += i

live_watch(my_function, watch=["x", "i"], interval=0.1)
```

---

## Export HTML

```python
from pydebugviz import export_html

export_html(trace, filepath="trace_output.html")
```

---

## Validation + Safe Eval

```python
from pydebugviz import validate_expressions, safe_eval

print(validate_expressions(["x > 3", "bad =="]))   # syntax check
print(safe_eval("x > 5", {"x": 7}))                # safely evaluate
```

---

## Trace Schema Enforcement

```python
from pydebugviz import normalize_trace, check_trace_schema

normalized = normalize_trace(trace)
issues = check_trace_schema(normalized)
print("Schema issues:", issues)
```

---

## License

MIT License  
(c) 2025 pydebugviz contributors
