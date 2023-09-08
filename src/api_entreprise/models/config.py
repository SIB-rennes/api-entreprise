from dataclasses import dataclass

from . import ContextInfo
from pyrate_limiter import Limiter


@dataclass
class Config:
    base_url: str
    token: str
    default_context_info: ContextInfo
    rate_limiter: Limiter
    timeout_s = 5 # pour les données structurées JSON, il est recommandé de mettre un timeout de 5 secondes par la doc API entreprise
