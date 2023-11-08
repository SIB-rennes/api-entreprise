from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, auto


class StatusEnum(StrEnum):
    ok = auto()
    bad_gateway = auto()
    unknown = auto()
@dataclass
class HealthcheckStatus:
    """
    inspired from https://entreprise.api.gouv.fr/developpeurs#surveillance-etat-fournisseurs
    """
    status: StatusEnum
    last_update: datetime
    last_ok_status: datetime | None
