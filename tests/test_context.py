from pyge.context import Context
from pyge.coordinateset import CoordinateSet
from pyge.operator_method import OperatorMethod
from pyge.minimal import MinimalContext
from pytest import raises


def test_minimal_context():
    ctx = MinimalContext()
    builtins = ctx.builtins()
    assert len(builtins) == 2
    assert set(builtins) == set(("addone", "subone"))
    assert ctx.op("addone") is not None


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
    ctx.register_method(subtwo)
    assert ctx.op("addtwo") is not None
    with raises(NameError):
        ctx.op("non_existing_method")
