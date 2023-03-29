import time
import requests
import threading
from api_entreprise.utils.url import join_fragments

from . import logger
from .models.config import Config
from .models.donnees_etablissement import DonneesEtablissement
from .models.numero_tva import NumeroTvaReponse
from .models.chiffre_daffaires import ChiffreDaffairesResponse
from .models.certification_rge import CertificationRgeResponse
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

    def chiffre_d_affaires(self, siret: str | int) -> list[ChiffreDaffairesResponse]:
        """Retourne le chiffre d'affaires des trois derniers exercices
        faites auprès de la DGFIP

        Returns:
            ChiffreDaffairesResponse | None: None si ressource non trouvée
        """

        json = self.raw_chiffre_d_affaires(siret)
        return self._json_to_chiffre_d_affaires(json)

    def certifications_rge(self, siret: str | int) -> list[CertificationRgeResponse]:
        """Retourne les certifications RGE (Reconnu Garant de l'Environnement) d'un établissement

        Returns:
            list[CertificationRgeResponse]:
        """
        json = self.raw_certification_rge(siret)
        return self._json_to_certification_rge(json)

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

    @_handle_response_in_error
    @_handle_httperr_404_returns_none
    @_handle_httperr_429_ex
    @_handle_bucketfull_ex
    def raw_chiffre_d_affaires(self, siret: str | int) -> dict | None:
        response = self._chiffre_d_affaires(siret)
        response.raise_for_status()
        json = response.json()
        return json

    @_handle_response_in_error
    @_handle_httperr_404_returns_none
    @_handle_httperr_429_ex
    @_handle_bucketfull_ex
    def raw_certification_rge(self, siret: str | int) -> dict | None:
        response = self._certification_rge(siret)
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
                join_fragments(self._base_url, f"insee/sirene/etablissements/{siret}"),
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
                join_fragments(
                    self._base_url,
                    f"european_commission/unites_legales/{siren}/numero_tva",
                ),
                headers=self._auth_headers,
                params=self._query_params,
            )
            self._empty_ratelimiter_if_429(response)

            return response

    def _chiffre_d_affaires(self, siret: str | int) -> requests.Response:
        with (
            _ratelimiterlock as _,
            self._ratelimiter.ratelimit(JSON_RESOURCE_IDENTIFIER) as _,
        ):
            # https://entreprise.api.gouv.fr/v3/dgfip/etablissements/{siret}/chiffres_affaires
            response = requests.get(
                join_fragments(
                    self._base_url, f"dgfip/etablissements/{siret}/chiffres_affaires"
                ),
                headers=self._auth_headers,
                params=self._query_params,
            )
            self._empty_ratelimiter_if_429(response)

            return response

    def _certification_rge(self, siret: str | int) -> requests.Response:
        with (
            _ratelimiterlock as _,
            self._ratelimiter.ratelimit(JSON_RESOURCE_IDENTIFIER) as _,
        ):
            # https://entreprise.api.gouv.fr/v3/ademe/etablissements/{siret}/certification_rge

            response = requests.get(
                join_fragments(
                    self._base_url, f"ademe/etablissements/{siret}/certification_rge"
                ),
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
        return join_fragments(self._config.base_url, API_ENTREPRISE_VERSION)

    def _json_to_donnees_etab(self, json):
        schema = DonneesEtablissement.ma_schema

        donnees = schema.load(json["data"])
        return donnees

    def _json_to_numero_tva_response(self, json):
        schema = NumeroTvaReponse.ma_schema

        tva = schema.load(json["data"])
        return tva

    def _json_to_chiffre_d_affaires(self, json):
        schema = ChiffreDaffairesResponse.ma_schema_many

        ca = schema.load(json["data"])
        return ca

    def _json_to_certification_rge(self, json):
        schema = CertificationRgeResponse.ma_schema_many

        certif = schema.load(json["data"])
        return certif

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
