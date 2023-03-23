import vcr
from .fixtures import *

from api_entreprise import ApiError, LimitHitError, Http429Error

vcr_folder = "tests/vcr/donnees_etablissement/"


@vcr.use_cassette(f"{vcr_folder}/megalis.yaml")
def test_make_api_entreprise(api: ApiEntreprise):
    etablissement = api.donnees_etablissement(25351449100047)
    assert etablissement is not None


@vcr.use_cassette(f"{vcr_folder}/same_recipient.error.yaml")
def test_siret_same_as_recipient(api: ApiEntreprise):
    """Lorsque le destinataire de l'appel est le même que le sujet, l'API renvoit un 422"""
    with pytest.raises(ApiError) as e:
        api.donnees_etablissement(26350579400028)

    assert e.value.errors[0].code is not None
    assert e.value.errors[0].detail is not None
    assert e.value.errors[0].title is not None


@vcr.use_cassette(f"{vcr_folder}/no-request.yaml")
def test_ratelimithit(api_with_emptyratelimiter: ApiEntreprise):
    with pytest.raises(LimitHitError) as e:
        api_with_emptyratelimiter.donnees_etablissement(25351449100047)


@vcr.use_cassette(f"{vcr_folder}/429-answer.yaml", record_mode="none")
def test_429_answer(api: ApiEntreprise):
    with pytest.raises(Http429Error) as e_1:
        api.donnees_etablissement(25351449100047)
