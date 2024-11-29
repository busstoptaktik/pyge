from pyge.minimal import MinimalContext


def test_minimal_context():
    ctx = MinimalContext()
    builtins = ctx.builtins()
    assert len(builtins) == 2
    assert "addone" in builtins
    assert "subone" in builtins
