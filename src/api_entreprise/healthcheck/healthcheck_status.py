from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, auto

from api_entreprise.utils.metaclasses import _AddMarshmallowSchema


class StatusEnum(StrEnum):
    ok = auto()
    bad_gateway = auto()
    unknown = auto()


@dataclass
class HealthcheckStatus(metaclass=_AddMarshmallowSchema):
    """
    inspired from https://entreprise.api.gouv.fr/developpeurs#surveillance-etat-fournisseurs
    """
    status: StatusEnum
    last_update: datetime
    last_ok_status: datetime | None
