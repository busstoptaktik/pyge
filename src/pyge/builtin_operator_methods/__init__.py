from .addone import addone, subone
from .helmert import helmert
from .tmerc import tmerc, utm
from .conventions import geo, gis, ne
from .pipeline import pipeline
from ..operator_method import OperatorMethod

builtin_operator_methods: dict[str, OperatorMethod] = {
    "addone": addone,
    "subone": subone,
    "helmert": helmert,
    "pipeline": pipeline,
    "tmerc": tmerc,
    "utm": utm,
    "geo": geo,
    "gis": gis,
    "ne": ne,
}
