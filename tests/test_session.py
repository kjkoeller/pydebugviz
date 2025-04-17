from pydebugviz import debug, DebugSession

def test_jump_and_search():
    def calc():
        x = 0
        for i in range(5): x += i
        return x

    session = DebugSession(debug(calc))
    session.jump_to(3)
    assert session.pointer == 3
    results = session.search("x > 3")
    assert isinstance(results, list)
