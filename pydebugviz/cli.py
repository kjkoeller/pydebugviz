import argparse
import sys
from pydebugviz import debug, normalize_trace, show_summary, export_html
from pydebugviz.replay import replay_trace_cli

def load_script_function(script_path):
    # Dynamically load a function from a Python script
    import runpy
    return runpy.run_path(script_path).get('main')

def main():
    parser = argparse.ArgumentParser(description="pydebugviz - Visual Debugging Tool")
    parser.add_argument("script", help="Python script to trace (must contain a 'main()' function)")
    parser.add_argument("--html", action="store_true", help="Export HTML after trace")
    parser.add_argument("--play", action="store_true", help="Replay trace in CLI")
    parser.add_argument("--summary", action="store_true", help="Show CLI summary after trace")

    args = parser.parse_args()

    try:
        func = load_script_function(args.script)
        trace = debug(func)
        trace = normalize_trace(trace)

        if args.summary:
            show_summary(trace)

        if args.html:
            export_html(trace)

        if args.play:
            replay_trace_cli(trace)

    except Exception as e:
        print(f"[pydebugviz] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()