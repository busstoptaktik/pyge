from .context import Context, OpHandle, OpDirection
from .operation import Operation
from .operator_method import OperatorMethod
from .coordinateset import CoordinateSet
from .registeritem import RegisterItem
from .builtin_operator_methods import builtin_operator_methods


class MinimalContext(Context, RegisterItem):
    """Modes of communication between the *Rust Geodesy* internals and the external
    world (i.e. resources like grids, transformation definitions, or ellipsoid parameters)."""

    def __init__(self):
        self.ops: dict[OpHandle, Operation] = {}
        self.methods: dict[str, OperatorMethod] = dict(builtin_operator_methods)

    def method(self, id) -> OperatorMethod | None:
        if id in self.methods:
            return self.methods[id]
        return None

    def builtins(self) -> tuple[str]:
        print(self.methods)
        return tuple((val.id for val in self.methods.values() if val.builtin == True))

    def op(self, definition: str) -> OpHandle | None:
        """Instantiate the operation given by `definition`"""
        thehandle = OpHandle()
        theop = Operation(str(thehandle), definition, self)
        if theop is None:
            return None
        self.ops[thehandle] = theop
        return thehandle

    def apply(
        self, op: OpHandle, direction: OpDirection, operands: CoordinateSet
    ) -> int:
        """Apply operation `op` to `operands` in direction Fwd or Inv"""
        if op not in self.ops:
            return 0
        if direction == OpDirection.FWD:
            return self.ops[op].fwd(self, operands)
        return self.ops[op].inv(self, operands)
