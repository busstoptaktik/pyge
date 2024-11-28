from .registeritem import RegisterItem
import pyge.context as context
from .coordinateset import CoordinateSet
from typing import Callable

class Operation(RegisterItem):
    """Attempt at a potentially simplified operation class"""

    # Still demo time. Not ready for the units etc.
    #
    # left_units: tuple[str] = ()
    # left_norvis: tuple[int] = (1, 2, 3, 4)
    # left_id: str = None
    #
    # right_units: tuple[str] = ()
    # right_norvis: tuple[int] = (1, 2, 3, 4)
    # right_id: str = None

    def __init__(
        self,
        id: str,
        definition: str,
        ctx: context.Context
    ):
        self.id = id
        self.definition = definition
        self.steps: tuple[Operation] = ()
        self.args: dict[str, str] = {}
        self.forward_function = None
        self.inverse_function = None
        self.ctx = ctx

        # We use the Rust Geodesy syntax, where steps are separated by the
        # vertical bar ("pipe") character
        definitions = definition.split("|")

        # For a pipeline of operations, fill the steps-list and be done with it
        if len(definitions) > 1:
            self.args["_name"] = "pipeline"
            self.steps = tuple(
                Operation("step", definition.strip(), ctx)
                for definition in definitions
                if len(definition.strip()) > 0
            )
            return

        # Otherwise parse the definition into arguments and build the object
        theargs = definitions[0].split()

        # The potentially-prefix modifiers, and the operator method name,
        # need special treatment: Modifiers are moved to the back, to
        # ensure that the operator name is at the front

        modifiers = ["inv", "omit_fwd", "omit_inv"]
        for modifier in modifiers:
            if modifier in theargs:
                del theargs[theargs.index(modifier)]
                self.args[modifier] = ""
        self.args["_name"] = theargs[0]
        del theargs[0]

        # Build the rest of the argument list
        for arg in theargs:
            argval = arg.split("=")
            # Flags get an empty value
            if len(argval) == 1:
                argval.append("")
            self.args[argval[0]] = argval[1]

        # TODO: Look up operator method fwd and inv by a call to ctx
        # self.forward_function = fwd
        # self.inverse_function = inv

        return

    def inverted(self):
        return "inv" in self.args

    def omit_forward(self):
        return "omit_fwd" in self.args

    def omit_inverse(self):
        return "omit_inv" in self.args

    def fwd(self, operands: CoordinateSet) -> int | None:
        if self.omit_forward():
            return None
        if self.inverted:
            return self.inverse_function(self.args, operands)
        self.forward_function(self.args, operands)

    def inv(self, operands: CoordinateSet):
        if self.omit_inverse():
            return None
        if self.inverted:
            return self.forward_function(self.args, operands)
        self.inverse_function(self.args, operands)



def addone_forward_function(args: dict[str, str], ctx: context.Context, operands: CoordinateSet) -> int:
    for i in range(len(operands)):
        operand = operands[i]
        operand[0] += 1
        operands[i] = operand

def addone_inverse_function(args: dict[str, str], ctx: context.Context, operands: CoordinateSet) -> int:
    for i in range(len(operands)):
        operand = operands[i]
        operand[0] += 1
        operands[i] = operand
