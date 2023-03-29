import time
import requests
import threading
from urllib.parse import urljoin

from . import logger
from .models.config import Config
from .models.donnees_etablissement import DonneesEtablissement
from .models.numero_tva import NumeroTvaReponse
from . import JSON_RESOURCE_IDENTIFIER
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

    def donnees_etablissement(self, siret: str) -> DonneesEtablissement | None:
        """Retourne les données établissement pour un siret donné

        Raises:
            Exception: LimitHitError si le ratelimiter de l'API est plein

        Returns:
            DonneesEtablissement | None: None si établissement non trouvé
        """
        json = self.raw_donnees_etablissement(siret)
        return self._json_to_donnees_etab(json)

    def numero_tva_intercommunautaire(self, siren: str) -> NumeroTvaReponse | None:
        """Retourne le numéro de TVA intercommunautaire pour un siren donné

        Args:
            siren (str): siren de l'établissement

        Returns:
            NumeroTvaReponse|None: None si ressource non trouvée
        """
        json = self.raw_numero_tva_intercommunautaire(siren)
        return self._json_to_numero_tva_response(json)

    @_handle_response_in_error
    @_handle_httperr_404_returns_none
    @_handle_httperr_429_ex
    @_handle_bucketfull_ex
    def raw_donnees_etablissement(self, siret: str) -> dict | None:
        response = self._donnees_etablissement(siret)
        response.raise_for_status()
        json = response.json()
        return json

    @_handle_response_in_error
    @_handle_httperr_404_returns_none
    @_handle_httperr_429_ex
    @_handle_bucketfull_ex
    def raw_numero_tva_intercommunautaire(self, siren: str | int) -> dict | None:
        response = self._numero_tva_intercommunautaire(siren)
        response.raise_for_status()
        json = response.json()
        return json

    def _donnees_etablissement(self, siret) -> requests.Response:
        # On utilise un lock avec le ratelimiter
        # car ce dernier se comporte mal en situation
        # d'un grand nombre de tâches en //
        with (
            _ratelimiterlock as _,
            self._ratelimiter.ratelimit(JSON_RESOURCE_IDENTIFIER) as _,
        ):
            response = requests.get(
                f"{self._base_url}/insee/sirene/etablissements/{siret}",
                headers=self._auth_headers,
                params=self._query_params,
            )
            self._empty_ratelimiter_if_429(response)

            return response

    def _numero_tva_intercommunautaire(self, siren: str | int) -> requests.Response:
        with (
            _ratelimiterlock as _,
            self._ratelimiter.ratelimit(JSON_RESOURCE_IDENTIFIER) as _,
        ):
            # https://entreprise.api.gouv.fr/v3/european_commission/unites_legales/{siren}/numero_tva
            response = requests.get(
                f"{self._base_url}/european_commission/unites_legales/{siren}/numero_tva",
                headers=self._auth_headers,
                params=self._query_params,
            )
            self._empty_ratelimiter_if_429(response)

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

    def _json_to_numero_tva_response(self, json):
        schema = NumeroTvaReponse.ma_schema

        tva = schema.load(json["data"])
        return tva

    def _empty_ratelimiter_if_429(self, response: requests.Response):
        if response.status_code == 429:
            self._empty_ratelimiter()

    def _empty_ratelimiter(self):
        start = time.perf_counter()

        logger.debug(
            "[API ENTREPRISE] On a reçu une réponse 429 (too many requests). "
            "Par précaution, on consomme toutes les utilisation de la ressource "
            f"{JSON_RESOURCE_IDENTIFIER} de notre ratelimiter..."
        )
        while True:
            try:
                with self._ratelimiter.ratelimit(JSON_RESOURCE_IDENTIFIER, delay=False):
                    pass
            except BucketFullException as e:
                break

        elapsed = time.perf_counter() - start
        if elapsed > 1:
            logger.warning(
                f"[API ENTREPRISE] ratelimiter vidé en {elapsed:.03f} secondes"
            )
