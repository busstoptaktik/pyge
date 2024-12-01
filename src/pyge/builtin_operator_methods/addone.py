"""The addone and subone operator methods"""

from ..context import Context
from ..coordinateset import CoordinateSet
from ..operator_method import OperatorMethod
from ..operator import Operator


def addone_forward_function(
    _op: Operator, _ctx: Context, operands: CoordinateSet
) -> int:
    n = len(operands)
    for i in range(n):
        operand = operands[i]
        operand[0] += 1
        operands[i] = operand
    return n


def addone_inverse_function(
    _op: Operator, _ctx: Context, operands: CoordinateSet
) -> int:
    n = len(operands)
    for i in range(n):
        operand = operands[i]
        operand[0] -= 1
        operands[i] = operand
    return n


addone = OperatorMethod(
    id="addone", fwd=addone_forward_function, inv=addone_inverse_function, builtin=True
)

subone = OperatorMethod(
    id="subone", inv=addone_forward_function, fwd=addone_inverse_function, builtin=True
)
