from dataclasses import dataclass
from ..utils.metaclasses import _AddMarshmallowSchema


@dataclass
class Qualification:
    code: str
    nom: str


@dataclass
class CertificationRge:
    url: str
    nom_certificat: str
    domaine: str
    meta_domaine: str
    qualification: Qualification
    organisme: str
    date_attribution: str
    date_expiration: str
    # meta


@dataclass
class CertificationRgeHolder(metaclass=_AddMarshmallowSchema):
    data: CertificationRge
