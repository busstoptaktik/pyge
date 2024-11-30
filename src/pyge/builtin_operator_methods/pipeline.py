from ..context import Context
from ..coordinateset import CoordinateSet
from ..operator_method import OperatorMethod
from ..operation import Operation


def pipeline_forward_function(
    op: Operation, ctx: Context, operands: CoordinateSet
) -> int:
    print(operands[0])
    print(operands[1])
    print(len(operands))
    n = len(operands)
    for step in op.steps:
        if step.omit_forward:
            continue
        m = step.fwd(ctx, operands)
        n = min(n, m)
    return n


def pipeline_inverse_function(
    op: Operation, ctx: Context, operands: CoordinateSet
) -> int:
    n = len(operands)
    for step in reversed(op.steps):
        if step.omit_inverse:
            continue
        m = step.inv(ctx, operands)
        n = min(n, m)
    return n


pipeline = OperatorMethod(
    id="pipeline",
    fwd=pipeline_forward_function,
    inv=pipeline_inverse_function,
    builtin=True,
)
