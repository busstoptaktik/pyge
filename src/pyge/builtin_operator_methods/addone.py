from ..context import Context
from ..coordinateset import CoordinateSet
from ..operator_method import OperatorMethod


def addone_forward_function(
    _args: dict[str, str], _ctx: Context, operands: CoordinateSet
) -> int:
    for i in range(len(operands)):
        operand = operands[i]
        operand[0] += 1
        operands[i] = operand


def addone_inverse_function(
    _args: dict[str, str], _ctx: Context, operands: CoordinateSet
) -> int:
    for i in range(len(operands)):
        operand = operands[i]
        operand[0] -= 1
        operands[i] = operand


addone = OperatorMethod(
    id="addone", builtin=True, fwd=addone_forward_function, inv=addone_inverse_function
)

subone = OperatorMethod(
    id="subone", builtin=True, inv=addone_forward_function, fwd=addone_inverse_function
)
