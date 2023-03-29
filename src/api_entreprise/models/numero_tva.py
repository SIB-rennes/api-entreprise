from dataclasses import dataclass
from ..utils.metaclasses import _AddMarshmallowSchema


@dataclass
class NumeroTvaReponse(metaclass=_AddMarshmallowSchema):
    tva_number: str
