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
    op = Operator(" | inv helmert a  =  1 b=2,3, 4 d c=,, | ", ctx)
    assert op.inverted
    assert op.definition == " | inv helmert a  =  1 b=2,3, 4 d c=,, | "
    assert op.normalized_definition == "inv helmert a=1 b=2,3,4 d c=,,"
    assert op.parameters["_name"] == "helmert"
    assert op.parameters["a"] == "1"
    assert op.parameters["b"] == "2,3,4"
    assert op.parameters["inv"] == ""

    # Convert a parameter value to a list of floats
    assert op.parameter_as_floats("a") == [1.0]
    assert op.parameter_as_floats("a", (nan, 2, 3, nan)) == [1, 2, 3, nan]
    assert 3 == len(op.parameter_as_floats("b"))
    assert 0 == len(op.parameter_as_floats("no_such_param"))

    # Convert a parameter value to a list of strs

    assert op.parameter_as_strs("a") == ["1"]
    assert op.parameter_as_strs("a", ("", "33", "32", "")) == ["1", "33", "32", ""]
    assert op.parameter_as_strs("c", ("", "", "")) == ["", "", ""]
    assert op.parameter_as_strs("c", ("", "2", "3")) == ["", "2", "3"]

    # The difference between a specified flag and a non-existing (which could be a un-specified flag)
    assert op.parameter_as_strs("d") == [""]
    assert op.parameter_as_strs("no_such_param") == []

    assert 3 == len(op.parameter_as_strs("b"))
    assert 4 == len(op.parameter_as_strs("no_such_param", ("", "33", "32", "")))
    assert 3 == len(op.parameter_as_strs("c"))
    assert 1 == len(op.parameter_as_strs("d"))

    # Two proper steps and a lot of empty ones to be filtered out
    op = Operator(" #\n||||inv\n# foo\n helmert a=1 b=2 | | | subone c=3 d=4|| ", ctx)

    # Outer level
    assert op.parameters["_name"] == "pipeline"
    # Empty steps are filtered out
    assert len(op.steps) == 2

    # First step
    assert op.steps[0].inverted
    assert op.steps[0].parameters["_name"] == "helmert"
    assert op.steps[0].definition == "inv helmert a=1 b=2"
    assert op.steps[0].parameters["a"] == "1"
    assert op.steps[0].parameters["b"] == "2"
    assert op.steps[0].parameters["inv"] == ""

    # Second step
    assert op.steps[1].inverted is False
    assert op.steps[1].parameters["_name"] == "subone"
    assert op.steps[1].definition == "subone c=3 d=4"
    assert op.steps[1].parameters["c"] == "3"
    assert op.steps[1].parameters["d"] == "4"
    assert "inv" not in op.steps[1].parameters
    assert "c" in op.steps[1].parameters


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
