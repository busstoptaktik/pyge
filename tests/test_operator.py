from pyge.operator import Operator
from pytest import raises
from pyge.minimal import MinimalContext


def test_operation():
    ctx = MinimalContext()

    # Trying to access a non-existing OperationMethod raises NameError
    with raises(NameError):
        Operator("1234", "week_with_five_tuesdays", ctx)

    # Two proper steps and a lot of empty ones to be filtered out
    op = Operator("1234", " ||||inv addone a=1 b=2 | | | subone c=3 d=4|| ", ctx)

    # Outer level
    assert op.args["_name"] == "pipeline"
    assert op.id == "1234"
    # Empty steps are filtered out
    assert len(op.steps) == 2

    # First step
    assert op.steps[0].id == "step"
    assert op.steps[0].inverted
    assert op.steps[0].args["_name"] == "addone"
    assert op.steps[0].definition == "inv addone a=1 b=2"
    assert op.steps[0].args["a"] == "1"
    assert op.steps[0].args["b"] == "2"
    assert op.steps[0].args["inv"] == ""

    # Second step
    assert op.steps[1].id == "step"
    assert op.steps[1].inverted is False
    assert op.steps[1].args["_name"] == "subone"
    assert op.steps[1].definition == "subone c=3 d=4"
    assert op.steps[1].args["c"] == "3"
    assert op.steps[1].args["d"] == "4"
    assert "inv" not in op.steps[1].args
    assert "c" in op.steps[1].args
