from .fixtures import *

from unittest.mock import patch

from api_entreprise import ApiEntreprise, ApiEntrepriseClientError

from requests import ReadTimeout


def test_readtimeout(api: ApiEntreprise):
    with patch.object(api, "_perform_get", side_effect=ReadTimeout("Un timeout mocké")):
        with pytest.raises(ApiEntrepriseClientError) as excinfo:
            api.donnees_etablissement("12345")

        assert isinstance(excinfo.value.__cause__, ReadTimeout)
