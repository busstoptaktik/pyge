from pyge.operation import Operation
from pyge.context import Context


def test_operation():
    ctx = Context()

    # Two proper steps and a lot of empty ones to be filtered out
    op = Operation("1234", " ||||inv first a=1 b=2 | | | second c=3 d=4|| ", ctx)

    # Outer level
    assert op.args["_name"] == "pipeline"
    assert op.id == "1234"
    # Empty steps are filtered out
    assert len(op.steps) == 2

    # First step
    assert op.steps[0].id == "step"
    assert op.steps[0].inverted() is True
    assert op.steps[0].args["_name"] == "first"
    assert op.steps[0].definition == "inv first a=1 b=2"
    assert op.steps[0].args["a"] == "1"
    assert op.steps[0].args["b"] == "2"
    assert op.steps[0].args["inv"] == ""

    # Second step
    assert op.steps[1].id == "step"
    assert op.steps[1].inverted() is False
    assert op.steps[1].args["_name"] == "second"
    assert op.steps[1].definition == "second c=3 d=4"
    assert op.steps[1].args["c"] == "3"
    assert op.steps[1].args["d"] == "4"
    assert "inv" not in op.steps[1].args
    assert "c" in op.steps[1].args
