from dataclasses import dataclass

from ..utils.metaclasses import _AddMarshmallowSchema


@dataclass
class CertificationQualibat(metaclass=_AddMarshmallowSchema):
    document_url: str
    expires_in: int
    """Nombre de secondes avant expiration"""
