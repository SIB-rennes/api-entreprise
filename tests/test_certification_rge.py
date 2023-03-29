import vcr

from .fixtures import *

from api_entreprise import ApiEntreprise

from .fixtures import vcr_folder


@vcr.use_cassette(f"{vcr_folder}/certif_rge.megalis.yml")
def test_raw_ca(api: ApiEntreprise):
    certif = api.raw_certification_rge(25351449100047)
    assert certif is not None


@vcr.use_cassette(f"{vcr_folder}/certif_rge.megalis.yml")
def test_ca(api: ApiEntreprise):
    certif = api.certifications_rge(25351449100047)
    assert certif is not None
    assert isinstance(certif, list)
