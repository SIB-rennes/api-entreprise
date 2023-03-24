import logging

logger = logging.getLogger(__name__)

JSON_RESOURCE_IDENTIFIER = "api_entreprise"
"""Identifiant des ressources retournant du json pour l'utilisation avec le ratelimiter"""
API_ENTREPRISE_VERSION = "v3"

from .api import ApiEntreprise, Config
from .models import ContextInfo
from .exceptions import ApiError, Http429Error, LimitHitError
