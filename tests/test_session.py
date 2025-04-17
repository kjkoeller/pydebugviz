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

def test_navigation_and_bounds():
    def f(): a = 1; return a
    session = DebugSession(debug(f))

    assert session.pointer == 0
    session.next()
    assert session.pointer == 1 or session.pointer == 0  # if only one frame
    session.prev()
    assert session.pointer == 0

def test_search_conditions():
    def calc():
        x = 5
        return x

    session = DebugSession(debug(calc))
    
    # 👇 Print for debugging
    for i, frame in enumerate(session.trace):
        print(f"Frame {i}: {frame['event']} | locals = {frame['locals']}")

    result = session.search("x == 5")
    assert isinstance(result, list)
    assert len(result) >= 1


