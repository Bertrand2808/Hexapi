[![CI](https://github.com/Bertrand2808/Hexapi/actions/workflows/python.yml/badge.svg)](https://github.com/Bertrand2808/Hexapi/actions/workflows/python.yml)

# HexAPI Generator

Un générateur d'API Java hexagonale basé sur des entités définies par l'utilisateur.

## Fonctionnalités

- Génération de classes Entity (avec Javadoc, annotations, commentaires test)
- Génération automatique de mapper, controller, adapter, datasource port

## Utilisation

```bash
.\.venv\Scripts\activate
python generator.py
```

## 🔍 Analyse SonarQube

Ce projet utilise **SonarQube** pour analyser la qualité du code (duplications, bugs potentiels, conventions, etc.).

### ▶️ Analyse locale

L’analyse est actuellement réalisée **en local via Docker**.

#### Pré-requis

- Docker installé
- Token généré sur votre instance SonarQube locale (par défaut sur [http://localhost:9000](http://localhost:9000))

#### Commandes utiles

Lancer le serveur SonarQube local :
```bash
make up
```

Attendre qu’il soit prêt (via `make logs`), puis lancer l’analyse :
```bash
make scan
```

Arrêter le serveur :
```bash
make down
```

> Le token Sonar doit être défini dans un fichier `.env` à la racine :
> ```env
> SONAR_TOKEN=votre_token_sonar
> ```

---

### 🌍 Intégration GitHub Actions (à venir)

Une configuration est prête dans `.github/workflows/python.yml` pour permettre une analyse automatique via GitHub Actions.

#### Étapes pour l’activer :

1. Déployer une instance **publique** de SonarQube (Render, Railway, VPS…)
2. Ajouter les secrets suivants dans GitHub :
   - `SONAR_TOKEN` → token lié au projet
   - `SONAR_HOST_URL` → URL publique de l’instance
3. Décommenter le bloc `sonar:` dans `python.yml`

---

📘 Une documentation complète est disponible dans [`docs/sonar.md`](docs/sonar.md)

---
