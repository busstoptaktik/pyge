"""The 3-parameter Helmert operator methods"""

from ..context import Context
from ..coordinateset import CoordinateSet
from ..operator_method import OperatorMethod
from ..operator import Operator


def helmert_forward(op: Operator, _ctx: Context, operands: CoordinateSet) -> int:
    xyz = op.parameter_as_floats("translation", (0, 0, 0))

    dimensions_affected = tuple(range(min(operands.dim(), len(xyz))))
    for i, operand in enumerate(operands):
        operands[i] = tuple(operand[j] + xyz[j] for j in dimensions_affected)
    return len(operands)


def helmert_inverse(op: Operator, _ctx: Context, operands: CoordinateSet) -> int:
    xyz = op.parameter_as_floats("translation", (0, 0, 0))

    dimensions_affected = tuple(range(min(operands.dim(), len(xyz))))
    for i, operand in enumerate(operands):
        operands[i] = tuple(operand[j] - xyz[j] for j in dimensions_affected)
    return len(operands)


helmert = OperatorMethod(
    id="helmert",
    fwd=helmert_forward,
    inv=helmert_inverse,
)
