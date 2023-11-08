from api_entreprise.models.healthcheck_status import HealthcheckStatus
from ..fixtures import *

from ..fixtures import vcr_folder


@vcr.use_cassette(f"{vcr_folder}/healthcheck/healthcheck_insee_sirene_ok.yml")
def test_healthcheck_ok(api: ApiEntreprise):
    healthcheck = api.healthcheck_fournisseur("insee/sirene")
    assert healthcheck is not None
    assert isinstance(healthcheck, HealthcheckStatus)
    assert healthcheck.status == "ok"

@vcr.use_cassette(f"{vcr_folder}/healthcheck/healthcheck_insee_sirene_unknown.yml")
def test_healthcheck_unknown(api: ApiEntreprise):
    healthcheck = api.healthcheck_fournisseur("insee/sirene")
    assert healthcheck is not None
    assert isinstance(healthcheck, HealthcheckStatus)
    assert healthcheck.status == "unknown"

@vcr.use_cassette(f"{vcr_folder}/healthcheck/healthcheck_insee_sirene_bad_gateway.yml")
def test_healthcheck_bad_gateway(api: ApiEntreprise):
    healthcheck = api.healthcheck_fournisseur("insee/sirene")
    assert healthcheck is not None
    assert isinstance(healthcheck, HealthcheckStatus)
    assert healthcheck.status == "bad_gateway"
