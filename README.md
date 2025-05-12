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
- 🧪 Tests unitaires générés automatiquement
- 🎨 Interface moderne et responsive
- 🔄 Gestion des dépendances entre entités

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

## 🔍 Analyse SonarQube

Ce projet utilise **SonarQube** pour analyser la qualité du code.

### Analyse locale

#### Prérequis

- Docker installé
- Token SonarQube (généré sur [http://localhost:9000](http://localhost:9000))

#### Commandes

```bash
make up    # Démarre SonarQube
make scan  # Lance l'analyse
make down  # Arrête SonarQube
```

> ⚠️ Configurez votre token dans `.env` :
>
> ```env
> SONAR_TOKEN=votre_token_sonar
> ```

### Intégration GitHub Actions (à venir)

1. Déployez une instance SonarQube publique
2. Configurez les secrets GitHub :
   - `SONAR_TOKEN`
   - `SONAR_HOST_URL`
3. Activez l'analyse dans `.github/workflows/python.yml`

## 📚 Documentation

- [Guide d'utilisation](docs/usage.md)
- [Architecture](docs/architecture.md)
- [Configuration SonarQube](docs/sonar.md)

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez notre [guide de contribution](CONTRIBUTING.md) pour plus de détails.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👥 Auteurs

- Bertrand2808 - [GitHub](https://github.com/Bertrand2808)

---

⭐ N'hésitez pas à donner une étoile au projet si vous l'appréciez !
