import requests

from api_entreprise.healthcheck.config import ConfigBase
from api_entreprise.healthcheck.healthcheck_status import HealthcheckStatus
from api_entreprise.utils.url import join_fragments


class HealthCheckApiEntreprise:
    def __init__(self, conf: ConfigBase) -> None:
        self._config = conf


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
    return self._json_to_dataclass(HealthcheckStatus, json)


def raw_healthcheck_fournisseur(self, suffix_url) -> dict | None:
        f = lambda: self._healthcheck_fournisseur(suffix_url)
        return self._raw_response(f)


def _healthcheck_fournisseur(self, suffix_url: str) -> requests.Response:
        url = join_fragments(self._base_url, f"ping/{suffix_url}")
        return self._perform_get(url)

