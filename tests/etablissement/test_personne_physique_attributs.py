from api_entreprise.models.donnees_etablissement import PersonnePhysiqueAttributs


def test_personne_physique_default():
    attrs = PersonnePhysiqueAttributs()

    assert (
        attrs.sexe is None
    ), "Une personne physique par défaut doit avoir tous ses attributs à None"
    assert (
        attrs._denomination() is None
    ), "Une personne physique par défaut doit avoir tous ses attributs à None"


def test_personne_physique_denomination_nom_prenom():
    attrs = PersonnePhysiqueAttributs(nom_usage="Dupont", prenom_usuel="Jean")

    denomination = attrs.denomination
    assert denomination == "entrepreneur individuel DUPONT Jean", (
        "[...] 'Pour les personnes physiques, la raison sociale / dénomination / nom de l'entreprise correspond"
        " toujours au nom de famille et au prénom, précédés ou suivis de la mention"
        ' "entrepreneur individuel" ou "EI".\' [...]'
    )


def test_personne_physique_denomination_nom_prenom_nonreg1():
    attrs = PersonnePhysiqueAttributs(nom_naissance="Duchesse", prenom_usuel="Anne")

    denomination = attrs.denomination
    assert (
        denomination == "entrepreneur individuel DUCHESSE Anne"
    ), "Pour le siret 53766664600022"
