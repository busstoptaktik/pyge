from pyge.operator import Operator
from pytest import raises
from pyge.minimal import MinimalContext

# There are additional Operator-related tests in test_context.py


def test_operator_instantiation():
    ctx = MinimalContext()

    # Trying to access a non-existing OperationMethod raises NameError
    with raises(NameError):
        Operator("week_with_five_tuesdays", ctx)

    # Effectively empty pipelines
    op = Operator("", ctx)
    assert op.is_noop
    op = Operator(" |||| | | | || ", ctx)
    assert op.is_noop

    # A plain non-pipeline operator
    op = Operator("inv addone a=1 b=2", ctx)
    assert op.inverted
    assert op.args["_name"] == "addone"
    assert op.definition == "inv addone a=1 b=2"
    assert op.args["a"] == "1"
    assert op.args["b"] == "2"
    assert op.args["inv"] == ""

    # Two proper steps and a lot of empty ones to be filtered out
    op = Operator(" ||||inv addone a=1 b=2 | | | subone c=3 d=4|| ", ctx)

    # Outer level
    assert op.args["_name"] == "pipeline"
    # Empty steps are filtered out
    assert len(op.steps) == 2

    # First step
    assert op.steps[0].inverted
    assert op.steps[0].args["_name"] == "addone"
    assert op.steps[0].definition == "inv addone a=1 b=2"
    assert op.steps[0].args["a"] == "1"
    assert op.steps[0].args["b"] == "2"
    assert op.steps[0].args["inv"] == ""

    # Second step
    assert op.steps[1].inverted is False
    assert op.steps[1].args["_name"] == "subone"
    assert op.steps[1].definition == "subone c=3 d=4"
    assert op.steps[1].args["c"] == "3"
    assert op.steps[1].args["d"] == "4"
    assert "inv" not in op.steps[1].args
    assert "c" in op.steps[1].args
