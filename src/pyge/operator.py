from math import isnan

from .registeritem import RegisterItem
from .coordinateset import CoordinateSet
from .context import Context


class Operator(RegisterItem):
    """Attempt at a potentially simplified operator/operation class

    The term *operation* in the *Coordinate Operations* package of the current
    ISO-19111 and OGC Topic 2 standards, entangles two related concepts:

    - **Operator**, i.e. an entity able to operate on an operand
    - **Operation**, i.e. the act of applying an operator to an operand

    Here, we attempt to untangle the two, by explicitly introducing the
    class `Operator` for objects able to *operate* on an *operand*.
    The actual operation is carried out using the `Context`-method `apply()`,
    which applies the operator to an operand (of base class CoordinateSet).

    Hence, we have this collection of disentangled concepts:

    - **OperatorMethod**: The mathematical functionality of an operator
    - **Operator**: An instantiation of an **OperatorMethod** and its associated
      defining constants
    - Operator definition: A textual representation of an Operator
      (e.g. `utm zone=32 ellps=GRS80`), which can be used to instantiate
      the corresponding Operator
    - Operand: The **CoordinateSet** operated on by an **Operator**
    - Operation: The act of applying the **Operator** to the operand

    Note that the term 'operator' is heavily overloaded in computer science,
    so in some programming languages 'operator' may be a reserved word. Hence,
    it may not be possible to define an element with that name.

    In Python, however, this is not the case, so for conceptual clarity, we
    represent operators as instantiations of the class **Operator**.
    """

    def __init__(self, definition: str, ctx: Context):
        self.definition = definition
        self.steps: tuple[Operator] = ()
        self.args: dict[str, str] = {}
        self.forward_function = None
        self.inverse_function = None
        self.ctx = ctx

        # We use the Rust Geodesy syntax, where steps are separated by the
        # vertical bar ("pipe") character, and we strip out empty steps.
        # This may lead to empty definitions, which is OK: An operator consists
        # of zero or more steps. An empty definition is represented as a pipeline
        # with zero steps. Hence the `len(definitions != 1)`, rather than
        # `len(definitions > 1)` in the condition for detecting pipelines below
        definitions = [
            stripped for d in definition.split("|") if len(stripped := d.strip()) > 0
        ]

        # For a pipeline of operators, recursively call the constructor for each step
        if len(definitions) != 1:
            method = ctx.operator_method("pipeline")
            if method is None:
                raise NameError(f"Unknown OperatorMethod 'pipeline' in '{definition}'")
            self.args["_name"] = "pipeline"
            self.forward_function = method.fwd
            self.inverse_function = method.inv
            self.steps = tuple(Operator(d, ctx) for d in definitions)
            return

        # Not a pipeline, so parse the definition into arguments and build the object
        theargs = definitions[0].split()

        # The potentially-prefix modifiers, and the operator method name,
        # need special treatment: All modifiers are moved to the back, to
        # ensure that the operator name is at the front. Once that is done,
        # the operator name foo is handled as if given as "_name=foo", in
        # alignment with the general style of the argument list
        modifiers = ["inv", "omit_fwd", "omit_inv"]
        for modifier in modifiers:
            if modifier in theargs:
                del theargs[theargs.index(modifier)]
                self.args[modifier] = ""

        id = theargs[0]
        self.args["_name"] = id
        del theargs[0]

        # Build the rest of the argument list
        for arg in theargs:
            argval = arg.split("=")
            # Flags get an empty value
            if len(argval) == 1:
                argval.append("")
            self.args[argval[0]] = argval[1]

        method = ctx.operator_method(id)
        if method is None:
            raise NameError(f"Unknown OperatorMethod '{id}'  in '{definition}'")
        self.forward_function = method.fwd
        self.inverse_function = method.inv

        return

    @property
    def is_noop(self) -> bool:
        return self.args["_name"] == "pipeline" and len(self.steps) == 0

    @property
    def inverted(self) -> bool:
        return "inv" in self.args

    @property
    def omit_forward(self) -> bool:
        return "omit_fwd" in self.args

    @property
    def omit_inverse(self) -> bool:
        return "omit_inv" in self.args

    def param_as_floats(
        self, param: str, mask: list[float] | tuple[float] = ()
    ) -> list[float]:
        """Convert the value of parameter `param` to a list of floats

        The mask provides defaults and extension values to pad the value to the expected dimension.
        """

        if param in self.args:
            values = [float(v) for v in self.args[param].split(",")]
        else:
            values = []

        # If too short, extend the values using the tail of the mask
        n = len(values)
        if n < len(mask):
            values.extend(mask[n:])

        # Then update NaNs in the original coordinate tuple, with mask content
        for index, mask_value in enumerate(mask):
            if isnan(values[index]):
                values[index] = float(mask_value)

        return values

    def fwd(self, ctx: Context, operands: CoordinateSet) -> int:
        if self.omit_forward:
            return len(operands)
        if self.inverted:
            return self.inverse_function(self, ctx, operands)
        return self.forward_function(self, ctx, operands)

    def inv(self, ctx: Context, operands: CoordinateSet) -> int:
        if self.omit_inverse:
            return len(operands)
        if self.inverted:
            return self.forward_function(self, ctx, operands)
        return self.inverse_function(self, ctx, operands)
