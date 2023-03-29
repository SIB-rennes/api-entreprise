from dataclasses import dataclass
from ..utils.metaclasses import _AddMarshmallowSchema


@dataclass
class NumeroTvaHolder(metaclass=_AddMarshmallowSchema):
    tva_number: str
