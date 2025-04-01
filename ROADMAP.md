# 📍 Roadmap - HexAPI Generator

Cette roadmap décrit les étapes de développement prévues pour le générateur d’API Hexagonale Java.

---

## ✅ Phase 1 : Setup initial (Terminé)
- [x] Structure de projet Python
- [x] Linter (`black`, `flake8`, `isort`)
- [x] GitHub Actions CI
- [x] Dockerfile
- [x] LICENSE (MIT) et badge CI

---

## 🚧 Phase 2 : Générateur d'entité (en cours)
- [X] Interface utilisateur (CLI/GUI) pour créer une classe Entity
- [ ] Choix des champs, types, annotations
- [ ] Génération du fichier `.java` avec :
  - Javadoc auto
  - Annotations JPA
  - `// testValues` pour les tests futurs

---

## 🔜 Phase 3 : Génération hexagonale
- [ ] Lecture d'une Entity `.java` validée
- [ ] Génération automatique de :
  - [ ] Mapper
  - [ ] Controller REST
  - [ ] ApplicationService / UseCase
  - [ ] DatasourcePort
  - [ ] Adapter Panache
  - [ ] DTO (optionnel)

---

## 🧪 Phase 4 : Ajout des tests automatiques
- [ ] Génération des tests JUnit
- [ ] Utilisation des `// testValues` pour peupler les mocks

---

## 🌐 Phase 5 : Améliorations
- [ ] Interface graphique (Tkinter, PyQt ou web)
- [ ] Mode SaaS (interface web + API)
- [ ] Export `.zip` complet de l’API
- [ ] Génération OpenAPI / Swagger

---

## 💡 Idées futures
- Génération Kotlin support
- Ajout d’autorisations / sécurité (JWT)
- Templates de style DDD / Clean Arch / CQRS

---

> ✨ Contributions bienvenues ! Voir `CONTRIBUTING.md`

# Idées d'ajouts :
💡 À prévoir pour enrichir le menu plus tard :
🔐 Fichier
Exporter la classe Java directement

Importer un JSON généré

Récent > liste des projets ouverts récemment

🧠 Aide
Tutoriel pas à pas

Lien vers les versions / changelog

Feedback utilisateur

⚙️ Outils
Générer une entité DTO, Mapper, ou Service

Personnaliser les noms de champs (suffixes, préfixes)
