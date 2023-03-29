from dataclasses import dataclass

from ..utils.metaclasses import _AddMarshmallowSchema


@dataclass
class ChiffreDaffaires:
    chiffre_affaires: float
    date_fin_exercice: str


@dataclass
class ChiffreDaffairesHolder(metaclass=_AddMarshmallowSchema):
    data: ChiffreDaffaires
