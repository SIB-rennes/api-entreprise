import requests
import threading
from urllib.parse import urljoin

from . import logger
from .models.config import Config
from .models.donnees_etablissement import DonneesEtablissement
from . import API_ENTREPRISE_RATELIMITER_ID
from . import API_ENTREPRISE_VERSION

from .handlers import (
    _handle_httperr_429_ex,
    _handle_bucketfull_ex,
    _handle_httperr_404_returns_none,
    _handle_response_in_error,
)

from pyrate_limiter import BucketFullException

_ratelimiterlock = threading.Lock()


class ApiEntreprise:
    def __init__(self, conf: Config) -> None:
        self._config = conf
        self._ratelimiter = conf.rate_limiter

    @_handle_response_in_error
    @_handle_httperr_404_returns_none
    @_handle_httperr_429_ex
    @_handle_bucketfull_ex
    def donnees_etablissement(self, siret: str) -> DonneesEtablissement | None:
        """Retourne les données établissement pour un siret donné

        Raises:
            Exception: LimitHitError si le ratelimiter de l'API est plein

        Returns:
            DonneesEtablissement | None: None si établissement non trouvé
        """

        response = self._donnees_etablissement(siret)
        response.raise_for_status()
        json = response.json()
        return self._json_to_donnees_etab(json)

    def _donnees_etablissement(self, siret) -> requests.Response:
        # On utilise un lock avec le ratelimiter
        # car ce dernier se comporte mal en situation
        # d'un grand nombre de tâches en //
        with (
            _ratelimiterlock as _,
            self._ratelimiter.ratelimit(API_ENTREPRISE_RATELIMITER_ID) as _,
        ):
            response = requests.get(
                f"{self._base_url}/insee/sirene/etablissements/{siret}",
                headers=self._auth_headers,
                params=self._query_params,
            )
            return response

    @property
    def _auth_headers(self):
        return {"Authorization": f"Bearer {self._config.token}"}

    @property
    def _query_params(self):
        return {
            "context": self._config.default_context_info.context,
            "object": self._config.default_context_info.object,
            "recipient": self._config.default_context_info.recipient,
        }

    @property
    def _base_url(self):
        return urljoin(self._config.base_url, API_ENTREPRISE_VERSION)

    def _json_to_donnees_etab(self, json):
        schema = DonneesEtablissement.ma_schema

        donnees = schema.load(json["data"])
        return donnees

    def empty_ratelimiter(self):
        logger.info("On vide le ratelimiter")
        while True:
            try:
                with self._ratelimiter.ratelimit(
                    API_ENTREPRISE_RATELIMITER_ID, delay=False
                ):
                    pass
            except BucketFullException as e:
                break
        logger.info("ratelimiter vide")
