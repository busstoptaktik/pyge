"""The 3-parameter Helmert operator methods"""

from ..context import Context
from ..coordinateset import CoordinateSet
from ..operator_method import OperatorMethod
from ..operator import Operator


def helmert_forward(op: Operator, _ctx: Context, operands: CoordinateSet) -> int:
    xyz = op.param_as_floats("translation", (0, 0, 0))
    len_xyz = len(xyz)

    for i, operand in enumerate(operands):
        operands[i] = [operand[j] + xyz[j] for j in range(min(len(operand), len_xyz))]
    return len_xyz


def helmert_inverse(op: Operator, _ctx: Context, operands: CoordinateSet) -> int:
    xyz = op.param_as_floats("translation", (0, 0, 0))
    len_xyz = len(xyz)

    for i, operand in enumerate(operands):
        operands[i] = [operand[j] - xyz[j] for j in range(min(len(operand), len_xyz))]
    return len_xyz


helmert = OperatorMethod(
    id="helmert",
    fwd=helmert_forward,
    inv=helmert_inverse,
    builtin=True,
)
