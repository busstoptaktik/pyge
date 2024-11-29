from .addone import addone, subone
from ..operator_method import OperatorMethod

builtin_operator_methods: dict[str, OperatorMethod] = {
    "addone": addone,
    "subone": subone,
}
