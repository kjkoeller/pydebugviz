from pydebugviz.live import live_watch

def test_live_watch_smoke():
    def run(): x = 0; x += 1
    trace = live_watch(run, watch=["x"], interval=0.01, max_steps=10)
    assert isinstance(trace, list)

def test_live_watch_missing_vars():
    def test(): z = 123  # not 'x' or 'i'
    trace = live_watch(test, watch=["x", "i"], interval=0.01, max_steps=5)
    assert isinstance(trace, list)
