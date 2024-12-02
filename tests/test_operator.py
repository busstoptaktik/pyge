from pyge.context import OpDirection
from pyge.operator import Operator
from pytest import raises
from pyge.minimal import MinimalContext
from pyge.coordinateset import CoordinateSetRowWise
from math import nan

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
    op = Operator("inv helmert a=1 b=2,3,4", ctx)
    assert op.inverted
    assert op.args["_name"] == "helmert"
    assert op.definition == "inv helmert a=1 b=2,3,4"
    assert op.args["a"] == "1"
    assert op.args["b"] == "2,3,4"
    assert op.args["inv"] == ""

    # Convert a parameter to a list of floats
    assert op.param_as_floats("a") == [1.0]
    assert op.param_as_floats("a", (nan, 2, 3, nan)) == [1, 2, 3, nan]
    assert 3 == len(op.param_as_floats("b"))
    assert 0 == len(op.param_as_floats("no_such_param"))

    # Two proper steps and a lot of empty ones to be filtered out
    op = Operator(" ||||inv helmert a=1 b=2 | | | subone c=3 d=4|| ", ctx)

    # Outer level
    assert op.args["_name"] == "pipeline"
    # Empty steps are filtered out
    assert len(op.steps) == 2

    # First step
    assert op.steps[0].inverted
    assert op.steps[0].args["_name"] == "helmert"
    assert op.steps[0].definition == "inv helmert a=1 b=2"
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


def test_helmert():
    ctx = MinimalContext()

    # `helmert` is registered as a builtin?
    assert "helmert" in ctx.builtins()

    # `helmert` can be instantiated?
    helmert = ctx.op("helmert  translation=1,2,3")
    assert helmert is not None

    # `helmert` behaves as expected, forward and inverse?
    coord = CoordinateSetRowWise([[1, 2, 3, 4], [5, 6, 7, 8]])
    ctx.apply(helmert, OpDirection.FWD, coord)
    assert [coord[0], coord[1]] == [[2, 4, 6, 4], [6, 8, 10, 8]]
    ctx.apply(helmert, OpDirection.INV, coord)
    assert [coord[0], coord[1]] == [[1, 2, 3, 4], [5, 6, 7, 8]]

    # `helmert` can be instantiated in inverse mode?
    helmert = ctx.op("inv helmert  translation=1,2,3")
    assert helmert is not None

    # The inverted `helmert` behaves as expected, forward and inverse?
    coord = CoordinateSetRowWise([[1, 2, 3, 4], [5, 6, 7, 8]])
    ctx.apply(helmert, OpDirection.INV, coord)
    assert [coord[0], coord[1]] == [[2, 4, 6, 4], [6, 8, 10, 8]]
    ctx.apply(helmert, OpDirection.FWD, coord)
    assert [coord[0], coord[1]] == [[1, 2, 3, 4], [5, 6, 7, 8]]
