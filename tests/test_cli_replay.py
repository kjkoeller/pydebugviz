import subprocess
import sys
import tempfile
import os
from pydebugviz import debug, normalize_trace
from pydebugviz.replay import replay_trace_cli

def write_script():
    code = """
def main():
    x = 0
    for i in range(3):
        x += i
    return x
"""
    path = os.path.join(tempfile.gettempdir(), "cli_script.py")
    with open(path, "w") as f:
        f.write(code.strip())
    return path

def test_cli_summary():
    script = write_script()
    result = subprocess.run(
        [sys.executable, "-m", "pydebugviz", script, "--summary"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    assert "[pydebugviz] Trace Summary:" in result.stdout

def test_cli_auto_play():
    script = write_script()
    result = subprocess.run(
        [sys.executable, "-m", "pydebugviz", script, "--auto-play", "--delay", "0.1"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    assert "Step" in result.stdout

def test_cli_headless():
    script = write_script()
    result = subprocess.run(
        [sys.executable, "-m", "pydebugviz", script, "--headless"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    assert "Step" in result.stdout

def test_replay_trace_cli_headless(capsys):
    def sample():
        a = 1
        a += 2

    trace = normalize_trace(debug(sample))
    replay_trace_cli(trace, headless=True)
    out, _ = capsys.readouterr()
    assert "[Step" in out

def test_replay_trace_cli_auto_play(capsys):
    def sample():
        x = 0
        x += 1

    trace = normalize_trace(debug(sample))
    replay_trace_cli(trace, auto_play=True, delay=0.01)
    out, _ = capsys.readouterr()
    assert "Step" in out or "Δ Changes:" in out
