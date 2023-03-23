from dataclasses import dataclass

from . import ContextInfo
from pyrate_limiter import Limiter


@dataclass
class Config:
    base_url: str
    token: str
    default_context_info: ContextInfo
    rate_limiter: Limiter
