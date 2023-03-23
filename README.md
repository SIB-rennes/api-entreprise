# Projet de template pour une lib python

Template pour lib python simple. Basé sur `python 3.10`

- [./src/](./src/): les sources de la bibliothèque
- [./tests](./tests/): Les tests unitaires de la bibliothèque

Les données du projet sont décrites dans [./pyproject.toml](./pyproject.toml). 

Deux ensembles de dépendances `extras` existent pour le développement local:
- `dev` 
- `test`

Le versionning de la bibliothèque est dynamique et dépend du tag git. Plus d'informations avec [https://https://pypi.org/project/setuptools-scm/](https://https://pypi.org/project/setuptools-scm/).

## git hooks

La bibliothèque [https://pre-commit.com/index.html](https://pre-commit.com/index.html) est installée en dépendance de développement.

## Forge github

Le fichier [./.github/workflows/publish-test-pypi.yml](./.github/workflows/publish-test-pypi.yml) définit un *workflow github* pour la publication des tags sur la plateforme PyPI de test: [https://test.pypi.org/](https://https://test.pypi.org/)

Le script attend un secret contenant le token Test PyPI. Pour cela, renseignez un secret `TESTPYPI_TOKEN` avec le token correspondant, depuis la page de repo github, dans: `settings > secrets and variables > actions > New repository secret`

## Commandes

### Environement de dev

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pre-commit install
```

Le requirements.txt est un raccourci pour `pip install -e .`.
Une fois executé, les scripts définis dans [./pyproject.toml](./pyproject.toml) sont disponibles dans le shell local:

```bash
pip install -e .
python-library-template
```

**Vous pouvez utiliser pipx pour rendre le script disponible de manière globale**

```bash
pipx install .
```

### Construire le package

```bash
python -m build
```

### Tests

```bash
pytest
```