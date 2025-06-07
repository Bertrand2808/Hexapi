[![CI](https://github.com/Bertrand2808/Hexapi/actions/workflows/python.yml/badge.svg)](https://github.com/Bertrand2808/Hexapi/actions/workflows/python.yml)
[![Version](https://img.shields.io/badge/version-0.0.1-blue.svg)](https://github.com/Bertrand2808/Hexapi)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

# HexAPI Generator

Un générateur d'API Java hexagonale basé sur des entités définies par l'utilisateur. Cet outil permet de générer automatiquement une architecture hexagonale complète à partir d'une interface graphique intuitive.

## ✨ Fonctionnalités

- 🎯 Interface graphique intuitive pour la définition des entités
- 📦 Génération automatique de l'architecture hexagonale complète :
  - Entities avec Javadoc et annotations
  - Mappers
  - Controllers
  - Adapters
  - Datasource ports


## 🚀 Installation

1. Clonez le repository :

```bash
git clone https://github.com/Bertrand2808/Hexapi.git
cd Hexapi
```

2. Créez et activez l'environnement virtuel :

```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate # Linux/Mac
```

3. Installez les dépendances :

```bash
pip install -r requirements.txt
```

4. Lancez l'application :

```bash
python main.py
```

5. Générer un exécutable :

```bash
python setup.py build
```

## 📸 Captures d'écran

![Interface principale](doc/img/img1.png)
![Éditeur d'entité](doc/img/img2.png)

## 🛠️ Développement

### Prérequis

- Python 3.8+
- Java 11+ (pour la génération du code)
- Docker (pour l'analyse SonarQube)

### Structure du projet

```
hexapi/
├── generator/          # Code source du générateur
│   ├── gui/           # Interface graphique
│   ├── templates/     # Templates de génération
│   └── scripts/       # Scripts utilitaires
├── output/            # Code généré
└── temp/             # Fichiers temporaires
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez notre [guide de contribution](CONTRIBUTING.md) pour plus de détails.

## 👥 Auteurs

- Bertrand2808 - [GitHub](https://github.com/Bertrand2808)

---

⭐ N'hésitez pas à donner une étoile au projet si vous l'appréciez !
