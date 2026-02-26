from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from . import ContextInfo

if TYPE_CHECKING:
    from pyrate_limiter import Limiter


@dataclass
class Config:
    base_url: str
    token: str
    default_context_info: ContextInfo
    rate_limiter: Limiter | None = field(default=None)
    """Rate limiter optionnel. Installer le package avec l'extra 'ratelimit' et passer une instance de Limiter pour activer le rate limiting."""
    timeout_s: int = 5  # pour les données structurées JSON, il est recommandé de mettre un timeout de 5 secondes par la doc API entreprise
