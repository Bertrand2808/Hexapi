---
# 📘 Mise en place de SonarQube en local (avec Docker)
---

## ✅ Objectif

- Déployer **SonarQube Community** en local via Docker
- Lancer des analyses de code depuis un conteneur `scanner`
- Utiliser un fichier `.env` pour stocker ton token Sonar
- Visualiser les résultats sur une interface web locale (`http://localhost:9000`)

---

## 1. 🐳 Pré-requis

- Docker installé et fonctionnel
- Projet local avec un minimum de code (ex : `.py`)
- Fichier `docker-compose.yml`

---

## 2. ⚙️ `docker-compose.yml`

Crée un fichier `docker-compose.yml` à la racine de ton projet :

```yaml
version: "3"

services:
  sonarqube:
    image: sonarqube:community
    ports:
      - "9000:9000"
    environment:
      - SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true
    volumes:
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_logs:/opt/sonarqube/logs
      - sonarqube_extensions:/opt/sonarqube/extensions

  scanner:
    image: sonarsource/sonar-scanner-cli
    depends_on:
      - sonarqube
    volumes:
      - .:/usr/src
    working_dir: /usr/src
    environment:
      - SONAR_HOST_URL=http://sonarqube:9000
      - SONAR_TOKEN=${SONAR_TOKEN}
    entrypoint: ["sonar-scanner"]

volumes:
  sonarqube_data:
  sonarqube_logs:
  sonarqube_extensions:
```

---

## 3. 🔐 `.env` (à ne **jamais** versionner)

Crée un fichier `.env` à la racine :

```env
SONAR_TOKEN=ton_token_sonar_ici
```

> Tu généreras ce token plus tard via l'interface web.

Ajoute `.env` à ton `.gitignore` :

```gitignore
.env
```

---

## 4. 📄 `sonar-project.properties`

Crée ce fichier à la racine du projet :

```properties
sonar.projectKey=hexapi-generator
sonar.projectName=HexAPI Generator
sonar.sources=.
sonar.sourceEncoding=UTF-8
sonar.python.version=3.11
sonar.exclusions=tests/**
```

---

## 5. ▶️ Lancement

### 1. Démarre SonarQube :

```bash
docker compose up -d sonarqube
```

### 2. 🕓 Attends que Sonar soit prêt (30-60 sec)

Vérifie :

```bash
docker compose logs -f sonarqube
```

Et attends de voir : `SonarQube is up`

### 3. Crée ton **Project Analysis Token** :

- Va sur [http://localhost:9000](http://localhost:9000)
- Login : `admin` / `admin`
- En haut à droite > **My Account** > **Security**
- Génère un **Project Analysis Token** lié à `hexapi-generator`
- Copie-le dans `.env`

---

## 6. 🔍 Lancer l’analyse

Une fois le serveur prêt :

```bash
docker compose run --rm scanner
```

Tu verras un message du type :

```
ANALYSIS SUCCESSFUL, view it at http://localhost:9000/dashboard?id=hexapi-generator
```

---

## 7. (Optionnel) `Makefile` pour simplifier

```makefile
up:
	docker compose up -d sonarqube

logs:
	docker compose logs -f sonarqube

scan:
	docker compose run --rm scanner

down:
	docker compose down
```

---

## ✅ Résultat attendu

- Interface dispo sur : [http://localhost:9000](http://localhost:9000)
- Résultats visibles projet par projet
- Qualité de code analysée en local avant push/merge

---
