from .addone import addone, subone
from .cart import cart
from .helmert import helmert
from .tmerc import tmerc, utm
from .conventions import geo, gis, ne
from .pipeline import pipeline
from ..operator_method import OperatorMethod

builtin_operator_methods: dict[str, OperatorMethod] = {
    "addone": addone,
    "cart": cart,
    "geo": geo,
    "gis": gis,
    "helmert": helmert,
    "ne": ne,
    "pipeline": pipeline,
    "subone": subone,
    "tmerc": tmerc,
    "utm": utm,
}
