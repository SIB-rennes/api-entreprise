from .fixtures import *

from api_entreprise import ApiEntreprise, CertificationQualibat

from .fixtures import vcr_folder


@vcr.use_cassette(f"{vcr_folder}/certif_qualibat.megalis.yml")
def test_raw_certification_qualibat(api: ApiEntreprise):
    certif = api.raw_certification_qualibat(25351449100047)
    assert certif is not None


@vcr.use_cassette(f"{vcr_folder}/certif_qualibat.megalis.yml")
def test_certification_qualibat(api: ApiEntreprise):
    certif = api.certification_qualibat(25351449100047)
    assert certif is not None
    assert isinstance(certif, CertificationQualibat)
