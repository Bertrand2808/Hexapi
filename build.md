# Guide de build - HexAPI Generator

Ce guide explique comment générer l'exécutable Windows (.exe) de HexAPI Generator.

## Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)
- Git (pour cloner le repository)

## Installation des dépendances de build

1. Clonez le repository si ce n'est pas déjà fait :

```bash
git clone https://github.com/Bertrand2808/Hexapi.git
cd Hexapi
```

2. Créez et activez l'environnement virtuel :

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. Installez les dépendances de build :

```bash
pip install -r requirements.txt
pip install pyinstaller
```

## Génération de l'exécutable

1. Assurez-vous d'être dans le répertoire racine du projet :

```bash
cd hexapi
```

2. Exécutez PyInstaller avec les options suivantes :

```bash
pyinstaller --name="HexAPI Generator" ^
            --windowed ^
            --icon=assets/icon.ico ^
            --add-data="generator/templates;generator/templates" ^
            --add-data="generator/gui/style.py;generator/gui" ^
            --hidden-import=jinja2 ^
            --hidden-import=tkinter ^
            --hidden-import=ttkthemes ^
            --clean ^
            main.py
```

### Options expliquées

- `--name` : Nom de l'exécutable
- `--windowed` : Mode sans console
- `--icon` : Icône de l'application
- `--add-data` : Fichiers additionnels à inclure
- `--hidden-import` : Modules Python à inclure
- `--clean` : Nettoyage avant build

## Structure des fichiers générés

Après la génération, vous trouverez :

```
dist/
└── HexAPI Generator/
    ├── HexAPI Generator.exe
    ├── generator/
    │   ├── templates/
    │   └── gui/
    └── [autres fichiers]
```

## Distribution

1. Compressez le dossier `dist/HexAPI Generator` en ZIP
2. Renommez le fichier ZIP avec la version : `HexAPI-Generator-v0.0.1.zip`

## Notes importantes

- L'exécutable inclut toutes les dépendances Python nécessaires
- Les templates sont inclus dans l'exécutable
- La taille finale est d'environ 50-100 MB
- L'application nécessite Windows 10 ou supérieur

## Dépannage

### Problèmes courants

1. **Erreur "Missing module"**

   - Vérifiez que tous les `--hidden-import` sont présents
   - Ajoutez les modules manquants avec `--hidden-import`

2. **Fichiers manquants**

   - Vérifiez les chemins dans `--add-data`
   - Assurez-vous que les fichiers existent

3. **Erreur d'icône**
   - Vérifiez que le fichier .ico existe
   - Utilisez un chemin relatif correct

### Logs de build

Les logs de build sont disponibles dans :

- `build/HexAPI Generator/warn-HexAPI Generator.txt`
- `build/HexAPI Generator/debug-HexAPI Generator.txt`

## Mise à jour de la version

Pour mettre à jour la version :

1. Modifiez la constante `VERSION` dans `generator/gui/main.py`
2. Régénérez l'exécutable
3. Mettez à jour le nom du fichier ZIP

## Support

Pour toute question concernant le build, ouvrez une issue sur GitHub.
