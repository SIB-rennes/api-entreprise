from dataclasses import dataclass

from ..utils.metaclasses import _AddMarshmallowSchema


@dataclass
class ApiError:
    code: str
    detail: str
    title: str


@dataclass
class ApiErrorResponse(metaclass=_AddMarshmallowSchema):
    errors: list[ApiError]
