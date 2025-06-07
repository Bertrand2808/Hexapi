📦 HexAPI Generator
=====================

Bienvenue dans HexAPI Generator !
Ce logiciel vous permet de générer automatiquement des fichiers Java pour structurer une API hexagonale à partir d’une interface graphique intuitive.

---

🚀 LANCEMENT DE L'APPLICATION
-----------------------------

1. ❗ Aucune installation n'est nécessaire.
2. ✅ Double-cliquez simplement sur le fichier :

       HexAPI Generator.exe

   Il se trouve à la racine du dossier que vous venez de dézipper.

---

📂 STRUCTURE DU LOGICIEL
-------------------------

Voici les dossiers importants une fois l'application lancée :

- `output/`
  → Contient tous les fichiers Java générés (Entity, Mapper, Controller, etc.)
  → Arborescence organisée par entreprise / projet / package.

- `temp/`
  → Contient les fichiers temporaires JSON créés à partir de vos entités.
  → Sert d'entrée pour la génération de code.

- `logs/`
  → Contient les journaux de l'application.
  → En cas d'erreur, consultez `app.log` pour comprendre ce qu’il s’est passé.

---

🧰 CONSEILS D’UTILISATION
--------------------------

1. Renseignez les informations de projet (nom de l’entreprise, projet, package Java…).
2. Ajoutez vos entités en cliquant sur **“Add Entity”**.
3. Pour chaque entité, précisez ses champs (nom, type, description, valeur de test, si c'est un id, non nullable, etc.).
4. Cliquez sur **“Generate”** pour générer les classes automatiquement.

---

❗ EN CAS DE PROBLÈME
----------------------

- Vérifiez que vous avez bien dézippé tous les fichiers.
- Consultez le fichier `logs/hexapi.log` pour les messages d’erreur détaillés.
- Assurez-vous que vous avez les droits pour écrire dans le dossier `output/`.

N'hésitez pas à me contacter si vous avez des questions ou des suggestions.

---

🧡 Merci d’utiliser HexAPI Generator !
