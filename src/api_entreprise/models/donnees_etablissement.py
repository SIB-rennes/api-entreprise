from dataclasses import dataclass, field

from ..utils.metaclasses import _AddMarshmallowSchema


## Tranche effectif salarié
@dataclass
class TrancheEffectifSalarie:
    code: str | None
    intitule: str | None
    date_reference: str | None
    de: int | None
    a: int | None


## Activite Principale
@dataclass
class ActivitePrincipale:
    code: str
    libelle: str | None
    nomenclature: str


## Unité légale
@dataclass
class PersonneMoraleAttributs:
    raison_sociale: str | None
    sigle: str | None


@dataclass
class FormeJuridique:
    code: str
    libelle: str


@dataclass
class UniteLegale:
    personne_morale_attributs: PersonneMoraleAttributs
    forme_juridique: FormeJuridique
    activite_principale: ActivitePrincipale
    tranche_effectif_salarie: TrancheEffectifSalarie


## Adresse
@dataclass
class AcheminementPostal:
    l1: str
    l2: str
    l3: str
    l4: str
    l5: str
    l6: str
    l7: str


@dataclass
class Adresse:
    code_commune: str | None
    acheminement_postal: AcheminementPostal


##
@dataclass
class DonneesEtablissement(metaclass=_AddMarshmallowSchema):
    siret: str

    activite_principale: ActivitePrincipale

    tranche_effectif_salarie: TrancheEffectifSalarie

    unite_legale: UniteLegale

    date_creation: int
    """Date de création sous format de timestamp"""

    adresse: Adresse

    adresse_postale_legere: str = field(init=False)
    """A partir des données API entreprise. Génère une adresse postale "light"
    Concaténation des lignes 4 à 7 du champ acheminement postal.
    voir: https://entreprise.api.gouv.fr/developpeurs/openapi#tag/Informations-generales/paths/~1v3~1insee~1sirene~1etablissements~1%7Bsiret%7D~1adresse/get
    """

    def __post_init__(self):
        acheminement_postal = self.adresse.acheminement_postal
        components = (
            acheminement_postal.l4,
            acheminement_postal.l5,
            acheminement_postal.l6,
            acheminement_postal.l7,
        )
        self.adresse_postale_legere = " ".join(components)
