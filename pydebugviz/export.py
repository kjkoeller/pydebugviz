from typing import List, Dict
import html

def export_html(trace: List[Dict], filepath: str = "trace.html") -> None:
    """
    Exports the trace to a simple standalone HTML table for inspection.

    Args:
        trace (List[Dict]): Normalized trace to export.
        filepath (str): Output HTML file path.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("<html><head><title>Trace Export</title>")
        f.write("<style>body { font-family: sans-serif; } table { border-collapse: collapse; } td, th { padding: 6px; border: 1px solid #ccc; }</style>")
        f.write("</head><body><h2>pydebugviz Trace Export</h2>")
        f.write(f"<p>{len(trace)} steps</p><table><tr>")

        headers = ["step", "event", "function", "line_no", "locals", "annotation", "var_diff"]
        for header in headers:
            f.write(f"<th>{header}</th>")
        f.write("</tr>")

        for frame in trace:
            f.write("<tr>")
            for key in headers:
                if key == "var_diff":
                    diff = frame.get("var_diff", {})
                    if diff:
                        value = "<br>".join(
                            f"{html.escape(k)}: {html.escape(str(v['from']))} → {html.escape(str(v['to']))}"
                            for k, v in diff.items()
                        )
                    else:
                        value = ""
                elif key == "locals":
                    value = "<br>".join(
                        f"{html.escape(k)} = {html.escape(str(v))}"
                        for k, v in frame.get("locals", {}).items()
                    )
                else:
                    value = html.escape(str(frame.get(key, "")))
                f.write(f"<td>{value}</td>")
            f.write("</tr>")

        f.write("</table></body></html>")