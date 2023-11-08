import time
import requests
import threading
from api_entreprise.models.certification_qualibat import CertificationQualibat
from api_entreprise.utils.url import join_fragments

from . import logger
from .models.config import Config
from .models.donnees_etablissement import DonneesEtablissement
from .models.healthcheck_status import HealthcheckStatus
from .models.numero_tva import NumeroTvaHolder
from .models.chiffre_daffaires import ChiffreDaffairesHolder
from .models.certification_rge import CertificationRgeHolder
from . import JSON_RESOURCE_IDENTIFIER
from . import API_ENTREPRISE_VERSION

from .handlers import raw_call_handler

from pyrate_limiter import BucketFullException

_ratelimiterlock = threading.Lock()


class ApiEntreprise:
    def __init__(self, conf: Config) -> None:
        self._config = conf
        self._ratelimiter = conf.rate_limiter
        self._timeout_s = conf.timeout_s

    def donnees_etablissement(self, siret: str) -> DonneesEtablissement | None:
        """Retourne les données établissement pour un siret donné

        Raises:
            Exception: LimitHitError si le ratelimiter de l'API est plein

        Returns:
            DonneesEtablissement | None: None si établissement non trouvé
        """
        json = self.raw_donnees_etablissement(siret)
        return self._json_to_dataclass(DonneesEtablissement, json)


    def donnees_etablissement_diffusibles(self, siret: str) -> DonneesEtablissement | None:
        """Retourne les données établissement diffusibles pour un siret donné

        Raises:
            Exception: LimitHitError si le ratelimiter de l'API est plein

        Returns:
            DonneesEtablissement | None: None si établissement non trouvé
        """
        json = self.raw_donnees_etablissement_diffusibles(siret)
        return self._json_to_dataclass(DonneesEtablissement, json)

    def healthcheck_fournisseur(self, suffix_url: str) -> HealthcheckStatus:
        """Retourne le statut d'un fournisseur
        En suivant la documentation suivante : https://entreprise.api.gouv.fr/developpeurs#surveillance-etat-fournisseurs \n
        Liste disponible : https://entreprise.api.gouv.fr/pings

        Parameters:
            suffix_url (str): url suffixe du fournisseur après "ping/" \n\t exemple : 'insee/sirene'

        Returns:
            HealthCheckSatus
        """
        json = self.raw_healthcheck_fournisseur(suffix_url)
        return self._json_to_dataclass_default(HealthcheckStatus, json)

    def numero_tva_intercommunautaire(self, siren: str) -> NumeroTvaHolder | None:
        """Retourne le numéro de TVA intercommunautaire pour un siren donné

        Args:
            siren (str): siren de l'établissement

        Returns:
            NumeroTvaReponse|None: None si ressource non trouvée
        """
        json = self.raw_numero_tva_intercommunautaire(siren)
        return self._json_to_dataclass(NumeroTvaHolder, json)

    def chiffre_d_affaires(self, siret: str | int) -> list[ChiffreDaffairesHolder]:
        """Retourne le chiffre d'affaires des trois derniers exercices
        faites auprès de la DGFIP

        Returns:
            ChiffreDaffairesResponse | None: None si ressource non trouvée
        """

        json = self.raw_chiffre_d_affaires(siret)
        return self._json_to_dataclass(ChiffreDaffairesHolder, json, many=True)

    def certifications_rge(self, siret: str | int) -> list[CertificationRgeHolder]:
        """Retourne les certifications RGE (Reconnu Garant de l'Environnement) d'un établissement

        Returns:
            list[CertificationRgeResponse]:
        """
        json = self.raw_certification_rge(siret)
        return self._json_to_dataclass(CertificationRgeHolder, json, many=True)

    def certification_qualibat(self, siret: str | int) -> CertificationQualibat | None:
        """Certification qualibat

        Returns:
            CertificationQualibat | None: None si pas de certification
        """
        json = self.raw_certification_qualibat(siret)
        return self._json_to_dataclass(CertificationQualibat, json)

    def raw_donnees_etablissement(self, siret: str) -> dict | None:
        f = lambda: self._donnees_etablissement(siret)
        return self._raw(f)

    def raw_donnees_etablissement_diffusibles(self, siret: str) -> dict | None:
        f = lambda: self._donnees_etablissement_diffusibles(siret)
        return self._raw(f)

    def raw_healthcheck_fournisseur(self, suffix_url) -> dict | None:
        f = lambda: self._healthcheck_fournisseur(suffix_url)
        return self._raw_health_response(f)

    def raw_numero_tva_intercommunautaire(self, siren: str | int) -> dict | None:
        f = lambda: self._numero_tva_intercommunautaire(siren)
        return self._raw(f)

    def raw_chiffre_d_affaires(self, siret: str | int) -> dict | None:
        f = lambda: self._chiffre_d_affaires(siret)
        return self._raw(f)

    def raw_certification_rge(self, siret: str | int) -> dict | None:
        f = lambda: self._certification_rge(siret)
        return self._raw(f)

    def raw_certification_qualibat(self, siret: str | int) -> dict | None:
        f = lambda: self._certification_qualibat(siret)
        return self._raw(f)

    @raw_call_handler
    def _raw(self, f) -> dict | None:
        response: requests.Response = f()
        response.raise_for_status()
        json = response.json()
        return json

    def _raw_health_response(self, f) -> dict | None:
        response: requests.Response = f()
        json = response.json()
        return json

    def _donnees_etablissement(self, siret) -> requests.Response:
        url = join_fragments(self._base_url, f"insee/sirene/etablissements/{siret}")
        return self._perform_get(url)

    def _donnees_etablissement_diffusibles(self, siret) -> requests.Response:
        url = join_fragments(self._base_url, f"insee/sirene/etablissements/diffusibles/{siret}")
        return self._perform_get(url)

    def _healthcheck_fournisseur(self, suffix_url: str) -> requests.Response:
        url = join_fragments(self._config.base_url, f"ping/{suffix_url}")
        return self._perform_default_get(url)

    def _numero_tva_intercommunautaire(self, siren: str | int) -> requests.Response:
        url = join_fragments(
            self._base_url,
            f"european_commission/unites_legales/{siren}/numero_tva",
        )
        return self._perform_get(url)

    def _chiffre_d_affaires(self, siret: str | int) -> requests.Response:
        url = join_fragments(
            self._base_url,
            f"dgfip/etablissements/{siret}/chiffres_affaires",
        )
        return self._perform_get(url)

    def _certification_rge(self, siret: str | int) -> requests.Response:
        url = join_fragments(
            self._base_url,
            f"ademe/etablissements/{siret}/certification_rge",
        )
        return self._perform_get(url)

    def _certification_qualibat(self, siret: str | int) -> requests.Response:
        url = join_fragments(
            self._base_url,
            f"qualibat/etablissements/{siret}/certification_batiment",
        )
        return self._perform_get(url)

    def _perform_get(self, url) -> requests.Response:
        # On utilise un lock avec le ratelimiter
        # car ce dernier se comporte mal en situation
        # d'un grand nombre de tâches en //
        with (
            _ratelimiterlock as _,
            self._ratelimiter.ratelimit(JSON_RESOURCE_IDENTIFIER) as _,
        ):
            response = requests.get(
                url,
                headers=self._auth_headers,
                params=self._query_params,
                timeout=self._timeout_s,  # pour les données structurées JSON, il est recommandé de mettre un timeout de 5 secondes par la doc API entreprise
            )
            self._empty_ratelimiter_if_429(response)

            return response

    def _perform_default_get(self, url) -> requests.Response:
            response = requests.get(
                url,
                timeout=self._timeout_s,  # pour les données structurées JSON, il est recommandé de mettre un timeout de 5 secondes par la doc API entreprise
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
        return join_fragments(self._config.base_url, API_ENTREPRISE_VERSION)

    def _json_to_dataclass(self, cls, json, many=False):
        if json is None:
            return None

        if many:
            schema = cls.ma_schema_many
        else:
            schema = cls.ma_schema

        dc = schema.load(json["data"])
        return dc

    def _json_to_dataclass_default(self, cls, json, many=False):
        if json is None:
            return None

        if many:
            schema = cls.ma_schema_many
        else:
            schema = cls.ma_schema

        dc = schema.load(json)
        return dc

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
