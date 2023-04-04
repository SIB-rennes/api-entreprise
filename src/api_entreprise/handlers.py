import functools

from requests import RequestException, HTTPError, Response
from pyrate_limiter import BucketFullException, Limiter

from . import logger
from . import JSON_RESOURCE_IDENTIFIER

from .exceptions import Http429Error, LimitHitError, ApiError, ApiEntrepriseClientError
from .models.errors import ApiErrorResponse


def _self(*args):
    return args[0]


def _transform_to_api_error_or_none(e: HTTPError) -> ApiError | None:
    try:
        response: Response = e.response
        schema = ApiErrorResponse.ma_schema
        api_error_response = schema.load(response.json())
        return ApiError(api_error_response)
    except Exception as e:
        logger.debug(f"L'API n'a pas renvoyé un message d'erreur au bon format")
    return None


def _handle_request_error(f):
    """Décorateur qui gère une exception lors de la requête"""

    @functools.wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except RequestException as e:
            raise ApiEntrepriseClientError(
                "Une erreur non standard s'est passée lors de la requête vers l'API entreprise."
            ) from e

    return inner


def _handle_response_in_httperror(f):
    """Décorateur qui gère une erreur de l'API entreprise générique"""

    @functools.wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except HTTPError as e:
            api_error = _transform_to_api_error_or_none(e)
            if api_error is not None:
                raise api_error from e
            else:
                raise

    return inner


def _handle_response_429(response: Response, api_entreprise):
    ratelimiter: Limiter = api_entreprise._ratelimiter
    volume = ratelimiter.get_current_volume(JSON_RESOURCE_IDENTIFIER)

    headers = response.headers
    limit = headers.get("RateLimit-Limit")
    remaining = headers.get("RateLimit-Remaining")
    reset = headers.get("RateLimit-Reset")
    retry_after = headers.get("Retry-After")

    logger.warning(
        "[API ENTREPRISE]"
        f"Ratelimiter de l'API entreprise déclenché. "
        "Cela ne devrait pas se produire (ou peu)! "
        f"{remaining}/{limit} - reset: {reset}. retry after: {retry_after}. "
        f"Quant à lui, notre ratelimiter a un volume de {volume}"
    )

    raise Http429Error(retry_after)


def _handle_httperr_429_ex(f):
    """Décorateur qui gère l'erreur transforme l'erreur HTTPError 429 en Http429Error"""

    @functools.wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except HTTPError as e:
            response: Response = e.response
            if response.status_code != 429:
                raise

            _handle_response_429(response, _self(*args))

    return inner


def _handle_bucketfull_ex(f):
    """Décorateur qui gère l'erreur BucketFullException renvoyé par le ratelimite de pyratelimiter"""

    @functools.wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except BucketFullException as e:
            logger.debug(f"Ratelimiter plein.")
            remaining = max(e.meta_info["remaining_time"], 1)
            raise LimitHitError(remaining) from e

    return inner


def _handle_httperr_404_returns_none(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except HTTPError as e:
            response: Response = e.response

            if response.status_code == 404:
                return None
            else:
                raise

    return inner


def raw_call_handler(f):
    """handler qui combine la gestion d'erreur pour un appel API entreprise"""

    @functools.wraps(f)
    @_handle_request_error
    @_handle_response_in_httperror
    @_handle_httperr_404_returns_none
    @_handle_httperr_429_ex
    @_handle_bucketfull_ex
    def inner(*args, **kwargs):
        return f(*args, **kwargs)

    return inner
