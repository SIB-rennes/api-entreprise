import os
import logging
import argparse
import json

from pyrate_limiter import Limiter, Rate

from api_entreprise.models.config import Config
from api_entreprise.models.context_info import ContextInfo

TOKEN = os.environ.get("API_ENTREPRISE_TOKEN", "")
CONTEXT = os.environ.get("API_ENTREPRISE_CONTEXT", "Client API Entreprise")
RECIPIENT = os.environ.get("API_ENTREPRISE_RECIPIENT", "26350579400028")
OBJECT = os.environ.get("API_ENTREPRISE_OBJECT", "Client API Entreprise")
TIMEOUT = os.environ.get("API_ENTREPRISE_TIMEOUT", 5)

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("CLI API Entreprise")

from api_entreprise import ApiEntreprise

available_resources = ["donnees_etablissement"]


def donnees_etablissement(api: ApiEntreprise, *args):
    siret = args[0]

    logger.info(f"Données établissement: {args}")
    logger.debug(f"Siret: {siret}")

    response = api.raw_donnees_etablissement(siret)
    print(json.dumps(response))


def main():
    parser = argparse.ArgumentParser(description="CLI API Entreprise")
    parser.add_argument(
        "ressource", help="Ressource à requêter", choices=available_resources
    )
    parser.add_argument("rest", help="Arguments pour la ressource", nargs="*")

    parser.add_argument(
        "--base-url",
        dest="base_url",
        help="URL de base à utiliser",
        default="https://entreprise.api.gouv.fr",
    )
    parser.add_argument(
        "--context",
        dest="context",
        help="Contexte",
        default=CONTEXT,
    )
    parser.add_argument(
        "--object",
        dest="object",
        help="Object",
        default=OBJECT,
    )
    parser.add_argument(
        "--recipient",
        dest="recipient",
        help="Recipient",
        default=RECIPIENT,
    )

    parser.add_argument(
        "--token",
        dest="token",
        help="Token d'authentification à utiliser",
        default=TOKEN,
    )

    parser.add_argument(
        "--timeout",
        dest="timeout",
        help="Timeout pour la requête",
        default=TIMEOUT,
    )
    args = parser.parse_args()

    ctx = ContextInfo(args.context, args.recipient, args.object)

    conf = Config(
        base_url=args.base_url,
        token=args.token,
        default_context_info=ctx,
        rate_limiter=Limiter(Rate(250, 60)),
        timeout_s=args.timeout,
    )
    api_entreprise = ApiEntreprise(conf)

    match args.ressource:
        case "donnees_etablissement":
            return donnees_etablissement(api_entreprise, *args.rest)
        case _:
            raise Exception("Ressource inconnue")


if "__main__" == __name__:
    main()
