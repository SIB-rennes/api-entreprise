from ..fixtures import *

from api_entreprise import ApiError, LimitHitError, Http429Error, DonneesEtablissement

from ..fixtures import vcr_folder


@vcr.use_cassette(f"{vcr_folder}/forges/megalis-no-naf.yaml")
def test_donnees_etablissement_no_activite_principale(api: ApiEntreprise):
    etablissement = api.donnees_etablissement(25351449100047)
    assert etablissement is not None
    assert isinstance(etablissement, DonneesEtablissement)

@vcr.use_cassette(f"{vcr_folder}/forges/megalis-no-naf-no-l6-on-acheminementpostal.yaml")
def test_donnees_etablissement_no_l6(api: ApiEntreprise):
    etablissement = api.donnees_etablissement(25351449100047)
    assert etablissement is not None
    assert isinstance(etablissement, DonneesEtablissement)


@vcr.use_cassette(f"{vcr_folder}/megalis.yaml")
def test_raw_donnees_etablissement(api: ApiEntreprise):
    etablissement = api.raw_donnees_etablissement(25351449100047)
    assert etablissement is not None


@vcr.use_cassette(f"{vcr_folder}/megalis.yaml")
def test_donnees_etablissement(api: ApiEntreprise):
    etablissement = api.donnees_etablissement(25351449100047)
    assert etablissement is not None
    assert isinstance(etablissement, DonneesEtablissement)
