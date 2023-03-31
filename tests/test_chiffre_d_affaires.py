from .fixtures import *

from api_entreprise import ApiEntreprise, ChiffreDaffairesHolder

from .fixtures import vcr_folder


@vcr.use_cassette(f"{vcr_folder}/ca.megalis.yml")
def test_raw_ca(api: ApiEntreprise):
    ca = api.raw_chiffre_d_affaires(25351449100047)
    assert ca is not None


@vcr.use_cassette(f"{vcr_folder}/ca.megalis.yml")
def test_ca(api: ApiEntreprise):
    ca = api.chiffre_d_affaires(25351449100047)
    assert ca is not None
    assert len(ca) > 0
    assert isinstance(ca[0], ChiffreDaffairesHolder)
