import argparse
import sys
from pydebugviz import debug, normalize_trace, show_summary, export_html
from pydebugviz.replay import replay_trace_cli

def load_script_function(script_path):
    import runpy
    return runpy.run_path(script_path).get('main')

def main():
    parser = argparse.ArgumentParser(description="pydebugviz - Visual Debugging Tool")
    parser.add_argument("script", help="Python script to trace (must contain a 'main()' function)")
    parser.add_argument("--html", action="store_true", help="Export HTML after trace")
    parser.add_argument("--summary", action="store_true", help="Show summary in terminal")
    parser.add_argument("--play", action="store_true", help="Enter interactive replay mode")
    parser.add_argument("--auto-play", action="store_true", help="Auto-play through trace steps")
    parser.add_argument("--headless", action="store_true", help="Dump all steps non-interactively")
    parser.add_argument("--delay", type=float, default=0.5, help="Step delay (for auto-play)")

    args = parser.parse_args()

    try:
        func = load_script_function(args.script)
        trace = debug(func)
        trace = normalize_trace(trace)

        if args.summary:
            show_summary(trace)

        if args.html:
            export_html(trace)

        if args.play or args.auto_play or args.headless:
            replay_trace_cli(
                trace,
                auto_play=args.auto_play,
                delay=args.delay,
                headless=args.headless
            )

    except Exception as e:
        print(f"[pydebugviz] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()