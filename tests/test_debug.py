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