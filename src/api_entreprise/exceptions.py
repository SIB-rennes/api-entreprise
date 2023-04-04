from . import logger

from .models.errors import ApiErrorResponse


class ApiEntrepriseClientError(Exception):
    """Exception de base pour le client API entreprise"""

    pass


class ApiError(ApiEntrepriseClientError):
    """Erreur renvoyée par l'API entreprise.
    Elle porte la structure ApiErrorResponse
    """

    def __init__(self, api_error_response: ApiErrorResponse) -> None:
        self.errors = api_error_response.errors


class LimitHitError(ApiEntrepriseClientError):
    """Exception qui se produit lorsque la limite d'appel de l'api entreprise est atteinte."""

    def __init__(self, delay: float, default_remaining=60) -> None:
        actual = delay
        if actual is None:
            actual = default_remaining

        self.delay = actual
        """Temps restant jusqu'à ce que la limite se réinitialise"""


class Http429Error(LimitHitError):
    """Exception qui se produit lorsque la limite d'appel de l'api entreprise est atteinte
    avec le code retour HTTP 429
    """

    def __init__(self, retry_after: str | None, default_delay=60) -> None:
        retry_after = retry_after if retry_after is not None else default_delay
        delay = int(retry_after)
        if delay < 1:
            delay = default_delay
            logger.warning(
                "[API ENTREPRISE]"
                f"Retry-after: {retry_after} incohérent. On attendra {default_delay}"
            )

        super().__init__(delay)
