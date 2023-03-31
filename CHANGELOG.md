# Changelog

Changelog basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Construction URL dans la cli
- Traitement lors des 404
- Cacher le header Authorization lors de la construction de cassettes

### Changed

- Les cassettes dont les réponses sont forgées à la main sont dans leur propre dossier.

## [3.1.0]

### Added

- Ajout certification RGE
- Ajout certification Qualibat

### Changed

- Renommage model
- handler qui groupe plusieurs autres handlers
- refactoring [api.py](./src/api_entreprise/api.py)

### Fixed

## [3.0.9]

### Added

- Ajout du endpoint pour récupérer la TVA intercommunautaire
- Ajout du endpoint pour récupérer le CA
- Ajout de `economie_sociale_et_solidaire` dans la réponse des données étabissement.

### Changed

### Fixed

- Bug dans la constitution d'URL pour l'API
