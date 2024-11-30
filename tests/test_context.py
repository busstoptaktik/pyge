from pyge.context import Context, OpHandle, OpDirection
from pyge.coordinateset import CoordinateSet, CoordinateSetRowWise
from pyge.operator_method import OperatorMethod
from pyge.minimal import MinimalContext
from pytest import raises


def test_minimal_context():
    ctx = MinimalContext()

    # `OpHandle` initializes an instance variable, not a class variable?
    assert OpHandle() != OpHandle()

    # `addone` is registered as a builtin?
    assert "addone" in ctx.builtins()

    # `addone` can be instantiated
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


# A user defined OperationMethod, for testing the register_method functionality


def addtwo_forward_function(
    _args: dict[str, str], _ctx: Context, operands: CoordinateSet
) -> int:
    for i in range(len(operands)):
        operand = operands[i]
        operand[0] += 2
        operands[i] = operand


def addtwo_inverse_function(
    _args: dict[str, str], _ctx: Context, operands: CoordinateSet
) -> int:
    for i in range(len(operands)):
        operand = operands[i]
        operand[0] -= 2
        operands[i] = operand


addtwo = OperatorMethod(
    id="addtwo", fwd=addtwo_forward_function, inv=addtwo_inverse_function
)

subtwo = OperatorMethod(
    id="subtwo", inv=addtwo_forward_function, fwd=addtwo_inverse_function
)


def test_register_method():
    ctx = MinimalContext()

    ctx.register_method(addtwo)
    assert ctx.op("addtwo") is not None

    ctx.register_method(subtwo)
    assert ctx.op("subtwo") is not None

    with raises(NameError):
        ctx.op("non_existing_method")
