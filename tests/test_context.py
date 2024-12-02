from pyge.context import Context, OpHandle, OpDirection
from pyge.coordinateset import CoordinateSet, CoordinateSetRowWise
from pyge.operator_method import OperatorMethod
from pyge.operator import Operator
from pyge.minimal import MinimalContext
from pytest import raises


def test_op_handle():
    # `OpHandle` initializes an instance variable, not a class variable?
    assert OpHandle() != OpHandle()


def test_minimal_context():
    ctx = MinimalContext()

    # `addone` is registered as a builtin?
    assert "addone" in ctx.builtins()

    # `addone` can be instantiated?
    addone = ctx.op("addone")
    assert addone is not None

    # `addone` behaves as expected, forward and inverse?
    coord = CoordinateSetRowWise([[1, 2, 3, 4], [5, 6, 7, 8]])
    ctx.apply(addone, OpDirection.FWD, coord)
    assert coord[0][0] == 2
    assert coord[1][0] == 6
    ctx.apply(addone, OpDirection.INV, coord)
    assert coord[0][0] == 1
    assert coord[1][0] == 5

    # `addone` can be instantiated in inverse mode?
    addone = ctx.op("inv addone")
    assert addone is not None

    # The inverted `addone` behaves as expected, forward and inverse?
    coord = CoordinateSetRowWise([[1, 2, 3, 4], [5, 6, 7, 8]])
    ctx.apply(addone, OpDirection.FWD, coord)
    assert coord[0][0] == 0
    assert coord[1][0] == 4
    ctx.apply(addone, OpDirection.INV, coord)
    assert coord[0][0] == 1
    assert coord[1][0] == 5

    # A no-operator can be instantiated?
    no_op = ctx.op("")
    assert no_op is not None
    # The no-operator behaves as expected, forward and inverse?
    coord = CoordinateSetRowWise([[1, 2, 3, 4], [5, 6, 7, 8]])
    assert 2 == ctx.apply(no_op, OpDirection.FWD, coord)
    assert coord[0][0] == 1
    assert coord[1][0] == 5
    assert 2 == ctx.apply(no_op, OpDirection.INV, coord)
    assert coord[0][0] == 1
    assert coord[1][0] == 5


def test_register_method():
    global addtwo
    ctx = MinimalContext()

    ctx.register_operator_method(addtwo)
    assert ctx.op("addtwo") is not None

    ctx.register_operator_method(subtwo)
    assert ctx.op("subtwo") is not None

    # `addtwo` can be instantiated?
    addtwo = ctx.op("addtwo")
    assert addtwo is not None

    # `addtwo` behaves as expected, forward and inverse?
    coord = CoordinateSetRowWise([[1, 2, 3, 4], [5, 6, 7, 8]])
    ctx.apply(addtwo, OpDirection.FWD, coord)
    assert coord[0][0] == 3
    assert coord[1][0] == 7
    ctx.apply(addtwo, OpDirection.INV, coord)
    assert coord[0][0] == 1
    assert coord[1][0] == 5

    # Pipelines can be instantiated?
    # A convoluted way of adding one...
    addone_c = ctx.op("addtwo | subone")
    assert addone_c is not None

    print(f"{ctx.ops[addone_c].forward_function}")

    # The pipeline behaves as expected, forward and inverse?
    coord = CoordinateSetRowWise([[1, 2, 3, 4], [5, 6, 7, 8]])
    ctx.apply(addone_c, OpDirection.FWD, coord)
    assert coord[0][0] == 2
    assert coord[1][0] == 6
    ctx.apply(addone_c, OpDirection.INV, coord)
    assert coord[0][0] == 1
    assert coord[1][0] == 5

    with raises(NameError):
        ctx.op("non_existing_method")


# A user defined OperationMethod, for testing the register_method functionality


def addtwo_forward_function(
    _op: Operator, _ctx: Context, operands: CoordinateSet
) -> int:
    n = len(operands)
    for i in range(n):
        operand = operands[i]
        operand[0] += 2
        operands[i] = operand
    return n


def addtwo_inverse_function(
    _op: Operator, _ctx: Context, operands: CoordinateSet
) -> int:
    n = len(operands)
    for i in range(n):
        operand = operands[i]
        operand[0] -= 2
        operands[i] = operand
    return n


addtwo = OperatorMethod(
    id="addtwo", fwd=addtwo_forward_function, inv=addtwo_inverse_function
)

subtwo = OperatorMethod(
    id="subtwo", inv=addtwo_forward_function, fwd=addtwo_inverse_function
)
