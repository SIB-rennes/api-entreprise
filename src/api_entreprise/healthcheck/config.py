from dataclasses import dataclass


@dataclass
class ConfigBase:
    base_url: str
    token: str
    timeout_s = 5 # pour les données structurées JSON, il est recommandé de mettre un timeout de 5 secondes par la doc API entreprise