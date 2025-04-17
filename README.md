# pydebugviz v1.5

**Visual Time Travel Debugger for Python**  
Enhanced with trace validation, better error handling, and structured APIs.

---

## Key Features

- Time-travel debugging
- Step-by-step trace with locals
- Visual summary (Jupyter or CLI)
- Live variable capture
- Function call graphs
- Smart breakpoints and variable watch
- 🔒 **NEW**: Trace structure validation (auto-enabled)
- 🧠 Built-in `debug()` function with safer evaluation

---

## Installation

```bash
pip install pydebugviz
```

---

## What's New in v1.5

- ✅ Built-in trace validation via `validate_trace()`
- ✅ Updated `debug(..., validate=True)` for safety checks
- ✅ Improved trace schema consistency
- ✅ Future-ready for file export and metadata

---

## Sample Usage

```python
from pydebugviz import debug

def test_func():
    x = 0
    for i in range(5):
        x += i
    return x

trace = debug(test_func, breakpoints=["x > 5"], validate=True)
```

---

## Trace Validation

All trace frames must include:
- `"event"`: `"line"`, `"call"`, `"return"`, `"exception"`
- `"function"`: function name
- `"line_no"`: int
- `"locals"`: dict

Automatically checked in `debug()` with `validate=True`.

---

## Environment Support

| Feature                | CLI | Jupyter | IDE |
|------------------------|-----|---------|-----|
| `debug()`              | ✅  | ✅      | ✅  |
| `validate_trace()`     | ✅  | ✅      | ✅  |
| `show_summary()`       | ✅  | ✅      | ⚠️  |
| `export_html()`        | ✅  | ✅      | ✅  |
| `live_watch()`         | ✅  | ✅      | ✅  |
| `DebugSession` object  | ✅  | ✅      | ✅  |

---

## License

MIT License © 2025  
Built for developers who debug with style.
