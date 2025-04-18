from pydebugviz import debug

def test_basic_trace():
    def sample():
        x = 1
        for i in range(3):
            x += i
        return x

    trace = debug(sample)
    assert isinstance(trace, list)
    assert any("line_no" in f for f in trace)
    
def test_debug_trace_collection():
    def sample():
        x = 1
        x += 1
        return x

    trace = debug(sample)
    assert isinstance(trace, list)
    assert any("event" in frame for frame in trace)
