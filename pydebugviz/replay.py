import time

def replay_trace_cli(trace, auto_play=False, delay=0.5, headless=False):
    if not trace:
        print("No trace available.")
        return

    step = 0
    max_step = len(trace) - 1

    def print_frame(idx):
        frame = trace[idx]
        print(f"\\n[Step {idx}/{max_step}] {frame.get('event', '')} | {frame.get('function', '')} line {frame.get('line_no', '')}")
        for k, v in frame.get("locals", {}).items():
            print(f"{k} = {v}")
        if "var_diff" in frame and frame["var_diff"]:
            print("Δ Changes:")
            for var, change in frame["var_diff"].items():
                print(f"  {var}: {change['from']} → {change['to']}")

    if headless or auto_play:
        while step <= max_step:
            print_frame(step)
            step += 1
            time.sleep(delay if auto_play else 0)
        return

    print("Interactive Replay Mode (type '→' to step, '←' back, 'j N' to jump, 'q' to quit)")

    while True:
        print_frame(step)
        cmd = input("Command [→, ←, j N, q]: ").strip()

        if cmd in ["q", "quit", "exit"]:
            break
        elif cmd in ["→", "n", "next", ""]:
            step = min(step + 1, max_step)
        elif cmd in ["←", "p", "prev", "back"]:
            step = max(step - 1, 0)
        elif cmd.startswith("j "):
            try:
                jump_to = int(cmd.split()[1])
                if 0 <= jump_to <= max_step:
                    step = jump_to
                else:
                    print("Step out of range.")
            except ValueError:
                print("Invalid jump target.")
        else:
            print("Unrecognized command.")
