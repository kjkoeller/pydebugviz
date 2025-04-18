from ipywidgets import IntSlider, Play, HBox, VBox, Output, jslink
from IPython.display import display, clear_output

def timeline_slider(trace):
    if not trace:
        print("No trace available.")
        return

    out = Output()
    slider = IntSlider(
        min=0, max=len(trace) - 1, step=1, description="Step"
    )
    play = Play(
        value=0, min=0, max=len(trace) - 1, step=1,
        interval=500, description="Play"
    )
    jslink((play, 'value'), (slider, 'value'))

    def show_frame(change):
        with out:
            clear_output(wait=True)
            frame = trace[slider.value]
            print(f"[Step {slider.value}] {frame.get('event', '')} | {frame.get('function', '')} line {frame.get('line_no', '')}")
            for k, v in frame.get("locals", {}).items():
                print(f"{k} = {v}")
            if "var_diff" in frame and frame["var_diff"]:
                print("\nΔ Changes:")
                for var, change in frame["var_diff"].items():
                    print(f"{var}: {change['from']} → {change['to']}")

    slider.observe(show_frame, names='value')
    show_frame({'new': 0})  # initial render

    display(VBox([HBox([play, slider]), out]))