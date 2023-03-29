import vcr
from .fixtures import *

from .fixtures import vcr_folder

from api_entreprise import ApiEntreprise, NumeroTvaHolder


@vcr.use_cassette(f"{vcr_folder}/tva.megalis.yml")
def test_raw_tva(api: ApiEntreprise):
    tva = api.raw_numero_tva_intercommunautaire(821936291)
    assert tva is not None


@vcr.use_cassette(f"{vcr_folder}/tva.megalis.yml")
def test_tva(api: ApiEntreprise):
    tva = api.numero_tva_intercommunautaire(821936291)
    assert tva is not None
    assert isinstance(tva, NumeroTvaHolder)
