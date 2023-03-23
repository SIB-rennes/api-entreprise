from .fixtures import *

from api_entreprise import ApiError, LimitHitError


def test_make_api_entreprise(api):
    etablissement = api.donnees_etablissement(25351449100047)
    assert etablissement is not None


def test_siret_same_as_recipient(api):
    """Lorsque le destinataire de l'appel est le même que le sujet, l'API renvoit un 422"""
    with pytest.raises(ApiError) as e:
        api.donnees_etablissement(26350579400028)

    assert e.value.errors[0].code is not None
    assert e.value.errors[0].detail is not None
    assert e.value.errors[0].title is not None


def test_ratelimithit(api_with_emptyratelimiter):
    """"""
    with pytest.raises(LimitHitError) as e:
        api_with_emptyratelimiter.donnees_etablissement(25351449100047)
