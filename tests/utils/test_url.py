from api_entreprise.utils.url import join_fragments


def test_join_fragments():
    assert (
        join_fragments("https://toto.tata/v3", "une/ressource")
        == "https://toto.tata/v3/une/ressource"
    )
    assert (
        join_fragments("https://toto.tata/v3", "/une/ressource")
        == "https://toto.tata/v3/une/ressource"
    )
    assert (
        join_fragments("https://toto.tata/v3/", "/une/ressource")
        == "https://toto.tata/v3/une/ressource"
    )
    assert (
        join_fragments("https://toto.tata/v3///", "une/ressource")
        == "https://toto.tata/v3/une/ressource"
    )
