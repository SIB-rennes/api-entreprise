# Client API entreprise

Client pour [https://api.gouv.fr/les-api/api-entreprise](https://api.gouv.fr/les-api/api-entreprise).


## Ajout de la dépendance dans un requirements.txt

Par exemple:

```
api-entreprise>=31,<32
```

## Uilisation de la cli

Une CLI est fournie avec la bibliothèque

### Installation

```bash
python -m pipx install api-entreprise
```

### Utilisation

```bash
api-entreprise --help
```

## Utilisation d'un ratelimiter client

Il est possible d'utiliser un ratelimiter client basé sur https://pypi.org/project/pyrate-limiter/ en version 2.10+ pour éviter de faire des appels à l'API entreprise trop rapidement et de se faire bloquer. Notez tout de même que ce client reste compatible avec les headers de ratelimit (429).

Depuis la version 31, le ratelimiter client est optionnel. Il est possible de l'installer avec l'extras `api-entreprise[ratelimiter]`.
