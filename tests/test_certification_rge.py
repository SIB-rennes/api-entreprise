from .fixtures import *

from api_entreprise import ApiEntreprise, CertificationRgeHolder

from .fixtures import vcr_folder


@vcr.use_cassette(f"{vcr_folder}/certif_rge.megalis.yml")
def test_raw_certif_rge(api: ApiEntreprise):
    certif = api.raw_certification_rge(25351449100047)
    assert certif is not None


@vcr.use_cassette(f"{vcr_folder}/certif_rge.megalis.yml")
def test_certif_rge(api: ApiEntreprise):
    certif = api.certifications_rge(25351449100047)
    assert certif is not None
    assert isinstance(certif, list)
    assert len(certif) > 0
    assert isinstance(certif[0], CertificationRgeHolder)
