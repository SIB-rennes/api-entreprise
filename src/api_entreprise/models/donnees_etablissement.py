from dataclasses import dataclass, field
from enum import Enum

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
    code: str | None
    libelle: str | None
    nomenclature: str | None


## Unité légale
@dataclass
class PersonneMoraleAttributs:
    raison_sociale: str | None
    sigle: str | None


class Sexe(str, Enum):
    M = "M"
    F = "F"


@dataclass
class PersonnePhysiqueAttributs:
    pseudonyme: str | None = None
    prenom_usuel: str | None = None
    prenom_1: str | None = None
    prenom_2: str | None = None
    prenom_3: str | None = None
    prenom_4: str | None = None
    nom_usage: str | None = None
    nom_naissance: str | None = None
    _sexe: str | None = None

    sexe: Sexe | None = field(init=False)
    denomination: str | None = field(init=False)

    def __post_init__(self):
        self.denomination = self._denomination()
        self.sexe = self._sexe if self._sexe else None

    def _denomination(self, prefix="entrepreneur individuel", suffix=None):
        """Dénomination de l'entreprise dans le cas d'un entrepreneur individuel"""
        nom = self.nom_usage.upper() if self.nom_usage is not None else None
        if nom is None:
            nom = self.nom_naissance.upper() if self.nom_naissance is not None else None

        # fmt:off
        to_join = [ x for x in ( nom, self.prenom_usuel,) if x is not None ]
        # fmt:on
        if len(to_join) == 0:
            return None

        # fmt:off
        to_join = [ x for x in ( prefix, *to_join, suffix,) if x is not None ]
        # fmt:on

        return " ".join(to_join)


@dataclass
class FormeJuridique:
    code: str
    libelle: str


@dataclass
class UniteLegale:
    personne_morale_attributs: PersonneMoraleAttributs
    personne_physique_attributs: PersonnePhysiqueAttributs
    forme_juridique: FormeJuridique
    activite_principale: ActivitePrincipale
    tranche_effectif_salarie: TrancheEffectifSalarie
    economie_sociale_et_solidaire: bool | None


## Adresse
@dataclass
class AcheminementPostal:
    """- l1 : Si l'établissement correspond à une personne morale : la dénomination sociale de la personne morale. Le cas contraire: cette variable est vide.
    - l2 : Si l'établissement correspond à une personne physique : concaténation du nom et prénom
    - l3 : Complément d'adresse comme décrit dans la clé complement_adresse
    - l4 : Concaténation du numéro de voie, d'indice de répétition, du type de voie et du libellé de la voie
    - l5 :  Distribution spéciale comme décrit dans la clé distribution_speciale
    - l6 : Si le code cedex est existant : code cedex accompagné de son libellé ; sinon, si le pays est en France : code postal accompagné de son libellé, sinon : libellé de la commune de l'établissement situé à l'étranger. XXX: vu dans une réponse d'API, l6 peut être null
    - l7 : Pays de l'établissement
    """
    l1: str
    l2: str
    l3: str
    l4: str
    l5: str
    l6: str | None
    l7: str


@dataclass
class Adresse:
    code_commune: str | None
    code_postal: str | None
    code_cedex: str | None
    libelle_commune: str | None
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
            acheminement_postal.l6 if acheminement_postal.l6 is not None else "#",
            acheminement_postal.l7,
        )
        self.adresse_postale_legere = " ".join(components)
