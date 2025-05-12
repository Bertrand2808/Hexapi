"""Module contenant la barre de menu pour l'interface principale de HexAPI Generator."""

import os
import platform
import subprocess
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox

from generator.core.logger import LOG_DIR, logger

FONT_FAMILY = "Segoe UI"


def create_menu_bar(root):
    """Crée et attache la barre de menus à la fenêtre principale."""

    menu_bar = tk.Menu(
        root,
        bg="#2e2e3e",
        fg="#f0f0f0",
        activebackground="#3f3f5a",
        activeforeground="#ffffff",
        tearoff=0,
        bd=0,
        relief="flat",
        font=(FONT_FAMILY, 10),
    )
    root.config(menu=menu_bar)

    _add_file_menu(menu_bar)
    _add_help_menu(menu_bar)


def _add_file_menu(menu_bar):
    file_menu = tk.Menu(
        menu_bar,
        bg="#2e2e3e",
        fg="#f0f0f0",
        activebackground="#3f3f5a",
        activeforeground="#ffffff",
        tearoff=0,
        bd=0,
        relief="flat",
        font=(FONT_FAMILY, 10),
    )
    file_menu.add_command(label="Nouveau", command=_new_project)
    file_menu.add_command(label="Ouvrir un projet JSON...", command=_open_project)
    file_menu.add_command(label="Sauvegarder", command=_save_project)
    file_menu.add_separator()
    file_menu.add_command(label="Quitter", command=_quit_app)
    menu_bar.add_cascade(label="Fichier", menu=file_menu)


def _add_help_menu(menu_bar):
    help_menu = tk.Menu(
        menu_bar,
        bg="#2e2e3e",
        fg="#f0f0f0",
        activebackground="#3f3f5a",
        activeforeground="#ffffff",
        tearoff=0,
        bd=0,
        relief="flat",
        font=(FONT_FAMILY, 10),
    )
    help_menu.add_command(label="À propos", command=_show_about)
    help_menu.add_separator()
    help_menu.add_command(label="Ouvrir les logs", command=_open_logs)
    help_menu.add_command(label="Documentation", command=_open_docs)
    help_menu.add_command(label="GitHub", command=_open_github)
    menu_bar.add_cascade(label="Aide", menu=help_menu)


# === Callbacks ===


def _new_project():
    logger.info("Création d'un nouveau projet")
    print("[TODO] Nouveau projet vide")


def _open_project():
    logger.info("Ouverture d'un projet existant")
    path = filedialog.askopenfilename(filetypes=[("Fichiers JSON", "*.json")])
    if path:
        print(f"[TODO] Charger le projet depuis : {path}")


def _save_project():
    logger.info("Sauvegarde du projet actuel")
    print("[TODO] Sauvegarder le projet actuel")


def _quit_app():
    logger.info("Fermeture de l'application")
    exit(0)


def _show_about():
    logger.info("Affichage de l'information sur l'application")
    messagebox.showinfo(
        "À propos", "HexAPI Generator\nVersion 1.0\n© 2025 BertrandCorp"
    )


def _open_docs():
    logger.info("Ouverture de la documentation")
    webbrowser.open_new_tab("https://tonsite/docs")


def _open_github():
    logger.info("Ouverture du GitHub")
    webbrowser.open_new_tab("https://github.com/Bertrand2808/Hexapi")


def _open_logs():
    logger.info("Ouverture des logs")
    logger.info("Ouverture du dossier de logs: %s", LOG_DIR)

    if os.path.exists(LOG_DIR):
        if platform.system() == "Windows":
            subprocess.Popen(f'explorer "{LOG_DIR}"')
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", LOG_DIR])
        elif platform.system() == "Linux":
            subprocess.Popen(["xdg-open", LOG_DIR])
        else:
            logger.error(
                "Système d'exploitation non pris en charge: %s", platform.system()
            )
            messagebox.showerror(
                "Erreur",
                f"Impossible d'ouvrir le dossier des logs sur {platform.system()}",
            )
    else:
        logger.error("Le dossier de logs n'existe pas: %s", LOG_DIR)
        messagebox.showerror("Erreur", "Le dossier de logs n'existe pas")
