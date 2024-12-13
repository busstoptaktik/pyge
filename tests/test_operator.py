from pyge.context import OpDirection
from pyge.operator import Operator
from pyge.minimal import MinimalContext
from pyge.coordinateset import CoordinateSetRowWise

from pytest import raises
from math import nan, dist

# There are additional Operator-related tests in test_context.py


def test_operator_instantiation():
    ctx = MinimalContext()

    # Trying to access a non-existing OperationMethod raises NameError
    with raises(NameError):
        Operator("week_with_five_tuesdays", ctx)

    # The helmert operator method exists, but we provide some suspicious parameter values
    op = Operator("helmert xyz= 1, two, 3", ctx)

    with raises(ValueError):
        op.parameter_as_floats("xyz")
    # OK to access them as strings, though
    assert op.parameter_as_strs("xyz") == ("1", "two", "3")

    # The translation parameter is interpreted by the helmert preparation method
    op = Operator("helmert translation= 1, 2", ctx)
    assert op.prepared["translation"] == (1, 2, 0)
    # So it will fail at construction time if we provide non-numeric values
    with raises(ValueError):
        Operator("helmert translation= 1, two, 3", ctx)
    with raises(KeyError):
        op.prepared["cheese"] == (1, 2, 0)

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
    assert op.parameter_as_floats("a") == (1.0,)
    assert op.parameter_as_floats("a", (nan, 2, 3, nan)) == (1, 2, 3, nan)
    assert 3 == len(op.parameter_as_floats("b"))
    assert 0 == len(op.parameter_as_floats("no_such_param"))

    # Convert a parameter value to a list of strs

    assert op.parameter_as_strs("a") == ("1",)
    assert op.parameter_as_strs("a", ("", "33", "32", "")) == ("1", "33", "32", "")
    assert op.parameter_as_strs("c", ("", "", "")) == ("", "", "")
    assert op.parameter_as_strs("c", ("", "2", "3")) == ("", "2", "3")

    # The difference between a specified flag and a non-existing (which could be a un-specified flag)
    assert op.parameter_as_strs("d") == ("",)
    assert op.parameter_as_strs("no_such_param") == ()

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


def test_tmerc():
    ctx = MinimalContext()

    # tmerc ellipsoid handling
    with raises(NameError):
        Operator("tmerc ellps=a, f", ctx)
    with raises(NameError):
        Operator("tmerc ellps=1, 2, 3", ctx)
    with raises(NameError):
        ctx.op("tmerc ellps=1, 2, 3")

    op = Operator("tmerc ellps=1, 2", ctx)
    assert op.prepared["ellps"] == (1.0, 0.5)

    # Other tmerc parameters
    with raises(ValueError):
        Operator("tmerc x_0=cheese", ctx)
    op = Operator("tmerc x_0=1", ctx)
    assert op.prepared["offsets"] == (1, 0, 0, 0)

    geo = CoordinateSetRowWise(
        [[55.0, 12.0], [-55.0, 12.0], [55.0, -6.0], [-55.0, -6.0]]
    )

    projected = CoordinateSetRowWise(
        [
            [6_098_907.825_005_012, 691_875.632_139_661],
            [-6_098_907.825_005_012, 691_875.632_139_661],
            [6_198_246.671_090_279, -455_673.814_189_040],
            [-6_198_246.671_090_279, -455_673.814_189_040],
        ]
    )

    op = ctx.op("geo | tmerc x_0=500000 lon_0=9 k_0=0.9996 ellps=GRS80 | ne")
    ctx.apply(op, OpDirection.FWD, geo)
    for i in range(len(projected)):
        # Since we use the Bowring/Lee formulation, we do not exactly replicate the
        # PROJ results, using the Poder/Engsager/Krüger formulary: Out at 6W, i.e.
        # 15 degrees from the central meridian, we deviate by 4 mm from PROJ. Closer
        # to the central meridian, the difference is immaterial
        assert dist(geo[i], projected[i]) < 0.005

    # We hve overwritten geo, so we make a new copy
    geo = CoordinateSetRowWise(
        [[55.0, 12.0], [-55.0, 12.0], [55.0, -6.0], [-55.0, -6.0]]
    )

    ctx.apply(op, OpDirection.INV, projected)
    for i in range(len(projected)):
        # Since we use the Bowring/Lee formulation, we do not exactly replicate the
        # PROJ results, using the Poder/Engsager/Krüger formulary: Out at 6W, i.e.
        # 15 degrees from the central meridian, we deviate by a few decimeters from
        # PROJ. Closer to the central meridian, the difference is immaterial
        assert dist(geo[i], projected[i]) < 3e-6


def test_utm():
    ctx = MinimalContext()
    op = Operator("utm zone=32", ctx)
    assert op.prepared["x_0"] == 500_000.0
    assert op.prepared["k_0"] == 0.9996
    assert op.prepared["lat_0"] == 0
    assert op.prepared["lon_0"] == 9.0


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


def test_cart():
    ctx = MinimalContext()
    assert "cart" in ctx.builtins()
    cart = ctx.op("geo | cart ellps=GRS80 | cart inv ellps=GRS80 | geo inv")

    # Two dimensional case
    geo = CoordinateSetRowWise([[55.0, 12.0], [45.0, -6.0], [65.0, 6.0]])
    ego = CoordinateSetRowWise([[55.0, 12.0], [45.0, -6.0], [65.0, 6.0]])
    ctx.apply(cart, OpDirection.FWD, ego)
    for i in range(len(ego)):
        assert dist(ego[i], geo[i]) < 1e-12

    # Three dimensional case
    geo = CoordinateSetRowWise(
        [[55.0, 12.0, 10.0], [45.0, -6.0, 10.0], [65.0, 6.0, 10.0]]
    )
    ego = CoordinateSetRowWise(
        [[55.0, 12.0, 10.0], [45.0, -6.0, 10.0], [65.0, 6.0, 10.0]]
    )
    ctx.apply(cart, OpDirection.FWD, ego)
    for i in range(len(ego)):
        assert dist(ego[i][0:2], geo[i][0:2]) < 1e-12
        assert abs(ego[i][2] - geo[i][2]) < 1e-8

    # Two dimensional case, southern hemisphere
    cart = ctx.op("geo | cart ellps=GRS80 | cart inv south ellps=GRS80 | geo inv")
    geo = CoordinateSetRowWise([[-55.0, 12.0], [-45.0, -6.0], [-65.0, 6.0]])
    ego = CoordinateSetRowWise([[-55.0, 12.0], [-45.0, -6.0], [-65.0, 6.0]])
    ctx.apply(cart, OpDirection.FWD, ego)
    for i in range(len(ego)):
        assert dist(ego[i], geo[i]) < 1e-10
