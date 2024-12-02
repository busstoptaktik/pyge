from .addone import addone, subone
from .helmert import helmert
from .pipeline import pipeline
from ..operator_method import OperatorMethod

builtin_operator_methods: dict[str, OperatorMethod] = {
    "addone": addone,
    "subone": subone,
    "helmert": helmert,
    "pipeline": pipeline,
}
