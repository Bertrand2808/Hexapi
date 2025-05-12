"""Module principal de l'interface graphique HexAPI Generator."""

# === Imports ===
import json
import os
import shutil
import tkinter as tk
from tkinter import messagebox, ttk

from generator.core.logger import logger
from generator.gui.layout.entity_board import EntityBoard
from generator.gui.layout.entity_editor import EntityEditorWindow
from generator.gui.layout.project_header import ProjectHeader
from generator.gui.menubar import create_menu_bar
from generator.gui.style import (
    ACCENT_COLOR,
    ACCENT_HOVER,
    BG_DARK,
    BG_LIGHT,
    BG_LIGHTER,
    BORDER_COLOR,
    ERROR_COLOR,
    FONT_FAMILY,
    FONT_SIZE_LABEL,
    LABELFRAME_BG,
    PADDING,
    SUCCESS_COLOR,
    TEXT_COLOR,
)
from generator.gui.widgets import load_icons
from generator.scripts.generate_entity import generate_all_templates

# === Constants ===
VERSION = "0.0.1"


def clean_folders():
    """Nettoie le dossier temp au lancement de l'application."""
    temp_dir = "temp"
    output_dir = "output"
    if os.path.exists(temp_dir):
        logger.info("Cleaning temp folder: %s", temp_dir)
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    logger.info("Temp folder created: %s", temp_dir)

    if os.path.exists(output_dir):
        logger.info("Cleaning output folder: %s", output_dir)
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    logger.info("Output folder created: %s", output_dir)


def create_main_window():
    """Crée et configure la fenêtre principale de l'application."""
    root = tk.Tk()
    root.title("HexAPI Generator")
    root.geometry("1200x900")
    root.configure(bg=BG_DARK)
    root.minsize(1000, 700)  # Taille minimale de la fenêtre
    return root


def apply_style(root):
    """Applique le thème clair et les styles personnalisés aux composants Tkinter."""
    style = ttk.Style(root)
    style.theme_use("clam")

    # Style général
    style.configure(
        ".",
        background=BG_DARK,
        foreground=TEXT_COLOR,
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
    )

    # Labels
    style.configure(
        "TLabel",
        background=BG_DARK,
        foreground=TEXT_COLOR,
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
    )

    # Entrées
    style.configure(
        "TEntry",
        fieldbackground=BG_LIGHTER,
        foreground=TEXT_COLOR,
        borderwidth=1,
        relief="solid",
        padding=12,
        bordercolor=BORDER_COLOR,
    )

    # Combobox
    style.configure(
        "Custom.TCombobox",
        fieldbackground=BG_LIGHTER,
        background=BG_LIGHTER,
        foreground=TEXT_COLOR,
        arrowcolor=TEXT_COLOR,
        bordercolor=BORDER_COLOR,
        selectbackground=ACCENT_COLOR,
        selectforeground="white",
        padding=12,
    )

    style.map(
        "Custom.TCombobox",
        fieldbackground=[("readonly", BG_LIGHTER)],
        foreground=[("readonly", TEXT_COLOR)],
        background=[("readonly", BG_LIGHTER)],
    )

    # Boutons
    style.configure(
        "TButton",
        background=ACCENT_COLOR,
        foreground="white",
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
        padding=12,
        borderwidth=0,
        relief="flat",
    )
    style.map(
        "TButton",
        background=[("active", ACCENT_HOVER)],
        foreground=[("active", "white")],
    )

    # Frames avec label
    style.configure(
        "Custom.TLabelframe",
        background=LABELFRAME_BG,
        foreground=TEXT_COLOR,
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
        borderwidth=1,
        relief="solid",
        padding=24,
    )
    style.configure(
        "Custom.TLabelframe.Label",
        background=LABELFRAME_BG,
        foreground=TEXT_COLOR,
        font=(FONT_FAMILY, FONT_SIZE_LABEL, "bold"),
    )

    # Checkbuttons
    style.configure(
        "Custom.TCheckbutton",
        background=BG_LIGHT,
        foreground=TEXT_COLOR,
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
    )

    # Bouton primaire
    style.configure(
        "Green.TButton",
        background=SUCCESS_COLOR,
        foreground="white",
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
        padding=12,
        borderwidth=0,
        relief="flat",
    )

    style.map(
        "Green.TButton",
        background=[("active", "#218838")],
        foreground=[("active", "white")],
    )

    # Bouton secondaire
    style.configure(
        "Red.TButton",
        background=ERROR_COLOR,
        foreground="white",
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
        padding=12,
        borderwidth=0,
        relief="flat",
    )

    style.map(
        "Red.TButton",
        background=[("active", "#c82333")],
        foreground=[("active", "white")],
    )


def make_label(parent, text, size=FONT_SIZE_LABEL, bold=False):
    """Crée un label stylisé avec les couleurs et polices de l'application."""
    font_weight = "bold" if bold else "normal"
    return tk.Label(
        parent,
        text=text,
        font=(FONT_FAMILY, size, font_weight),
        fg=TEXT_COLOR,
        bg=parent["bg"],
    )


def show_error_message(parent, message):
    """Display an error message in a dialog box."""
    logger.info("Displaying error message: %s", message)
    dialog = tk.Toplevel(parent)
    dialog.title("Error")
    dialog.geometry("500x200")
    dialog.configure(bg=BG_LIGHT)
    dialog.transient(parent)
    dialog.grab_set()

    # Center the window
    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f"{width}x{height}+{x}+{y}")

    # Error message
    error_label = make_label(
        dialog,
        message,
        size=12,
        bold=True,
    )
    error_label.pack(pady=(30, 20))

    # OK button
    ok_btn = ttk.Button(
        dialog,
        text="OK",
        command=dialog.destroy,
        style="TButton",
    )
    ok_btn.pack()

    dialog.wait_window()


def setup_main_interface(root, dev_mode=False):
    """Construit l'interface utilisateur principale : formulaires, champs et boutons."""
    entities_data = {}  # {entity_name: {fields: [field_data]}}
    entity_editors = {}  # {entity_name: EntityEditorWindow}

    # --- Fonctions internes (doivent être définies avant l'utilisation) ---
    def open_entity_editor(entity_name):
        logger.info("Opening editor for %s", entity_name)
        if entity_name in entity_editors:
            try:
                entity_editors[entity_name].lift()
                logger.info("Editor %s is already open, it is raised", entity_name)
                return
            except tk.TclError:
                logger.info("Editor %s is already open, it is closed", entity_name)
                del entity_editors[entity_name]

        editor = EntityEditorWindow(
            root,
            entity_name,
            on_name_change=update_entity_name,
            dev_mode=dev_mode,
        )
        entity_editors[entity_name] = editor

    def create_entity():
        """Crée une nouvelle entité avec un nom par défaut,
        puis ouvre directement l'éditeur."""
        base_name = "NouvelleEntite"
        suffix = 1
        name = base_name

        # Générer un nom unique
        while name in entities_data:
            name = f"{base_name}{suffix}"
            suffix += 1

        logger.info("Creating entity %s", name)
        entities_data[name] = []
        entity_board.add_entity(name)
        open_entity_editor(name)

    # Ajoute un set pour suivre les opérations en cours
    operations_in_progress = set()

    def handle_delete_entity(entity_name):
        """Supprime une entité et ses ressources associées."""
        operation_key = f"delete_{entity_name}"
        if operation_key in operations_in_progress:
            logger.info("Skipping recursive deletion of %s", entity_name)
            return

        operations_in_progress.add(operation_key)
        try:
            logger.info("Deleting entity %s", entity_name)

            # Fermer l'éditeur s'il est ouvert
            if entity_name in entity_editors:
                try:
                    editor = entity_editors[entity_name]
                    editor._is_being_deleted = (
                        True  # Marquer l'éditeur comme en cours de suppression
                    )
                    editor.destroy()
                except tk.TclError:
                    pass  # L'éditeur est déjà fermé
                del entity_editors[entity_name]

            # Supprimer les données de l'entité
            if entity_name in entities_data:
                del entities_data[entity_name]

            # Supprimer le fichier JSON temporaire
            json_path = f"temp/{entity_name}.json"
            if os.path.exists(json_path):
                logger.info("Deleting temporary JSON file %s", json_path)
                try:
                    os.remove(json_path)
                except OSError as e:
                    logger.error("Error deleting JSON file: %s", e)

            # Supprimer l'entité du board
            if entity_name in entity_board.entities:
                entity_board.delete_entity(entity_name)
                logger.info("Entity %s deleted from board", entity_name)
        finally:
            operations_in_progress.remove(operation_key)

    def generate_all_entities():
        logger.info("Generating all entities")
        company = header.get_company()
        project = header.get_project()

        if not company:
            show_error_message(root, "The company name cannot be empty")
            return
        if not project:
            show_error_message(root, "The project name cannot be empty")
            return

        for entity_name, editor in list(entity_editors.items()):
            try:
                # Vérifier si l'éditeur existe toujours
                try:
                    editor.winfo_exists()
                except tk.TclError:
                    logger.info(
                        "Editor %s does not exist, deleting reference", entity_name
                    )
                    del entity_editors[entity_name]
                    continue

                # Récupérer les données depuis le fichier JSON temporaire
                json_path = f"temp/{entity_name}.json"
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if not data:
                    show_error_message(
                        root,
                        f"The entity '{entity_name}' has no fields. "
                        "Please add at least one field before generating.",
                    )
                    logger.error("No data found for %s", entity_name)
                    return
                if not os.path.exists(json_path):
                    logger.error("File JSON not found for %s", entity_name)
                    continue

                logger.info("Generating templates for %s", entity_name)
                generate_all_templates(json_path=json_path)
            except Exception as e:
                logger.error("Error generating %s: %s", entity_name, e)
                show_error_message(root, f"Error generating {entity_name}: {e}")
                return
        messagebox.showinfo(
            "Generation completed", "All entities have been generated successfully"
        )

    def update_entity_name(old_name, new_name):
        operation_key = f"rename_{old_name}_{new_name}"
        if operation_key in operations_in_progress:
            logger.info("Skipping recursive update from %s to %s", old_name, new_name)
            return

        logger.info("Updating entity name from %s to %s", old_name, new_name)
        operations_in_progress.add(operation_key)

        try:
            if old_name in entity_editors:
                try:
                    editor = entity_editors.pop(old_name)
                    entity_editors[new_name] = editor
                    editor.entity_name = new_name
                    editor.title(f"Editing {new_name}")
                except tk.TclError:
                    if old_name in entity_editors:
                        del entity_editors[old_name]

            if old_name in entities_data:
                entities_data[new_name] = entities_data.pop(old_name)

            # Renommer le fichier JSON si nécessaire
            old_json_path = f"temp/{old_name}.json"
            new_json_path = f"temp/{new_name}.json"
            if os.path.exists(old_json_path):
                os.rename(old_json_path, new_json_path)

            if old_name in entity_board.entities:
                box = entity_board.entities.pop(old_name)
                box.rename(new_name)
                entity_board.entities[new_name] = box

        finally:
            operations_in_progress.remove(operation_key)

    # --- Layout principal ---
    main_container = tk.Frame(root, bg=BG_DARK)
    main_container.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    main_container.grid_rowconfigure(0, weight=0)
    main_container.grid_rowconfigure(1, weight=1)
    main_container.grid_columnconfigure(0, weight=1)

    # Ligne pour le titre
    title_frame = tk.Frame(main_container, bg=BG_DARK)
    title_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
    title_label = make_label(
        title_frame,
        "HexAPI Generator",
        size=12,
        bold=True,
    )
    title_label.pack(pady=(8, 0), anchor="center")

    # --- Zone haute divisée en 2 parties ---
    top_frame = tk.Frame(main_container, bg=BG_DARK)
    top_frame.grid(row=1, column=0, sticky="nsew")
    top_frame.grid_rowconfigure(0, weight=1)
    top_frame.grid_columnconfigure(0, weight=0, minsize=420)
    top_frame.grid_columnconfigure(1, weight=2)

    # --- Colonne gauche : project header ---
    header = ProjectHeader(top_frame, width=360, height=400)
    header.grid(row=0, column=0, sticky="n", padx=(PADDING * 2, PADDING), pady=PADDING)
    header.grid_propagate(False)

    # --- Colonne droite : entités ---
    entity_section_container = tk.Frame(top_frame, bg=BG_LIGHT, padx=24, pady=24)
    entity_section_container.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(PADDING, PADDING * 2),
        pady=PADDING,
    )
    entity_section_container.grid_rowconfigure(0, weight=1)

    entity_board = EntityBoard(
        entity_section_container,
        on_entity_click=open_entity_editor,
        on_add_entity=create_entity,
        on_entity_delete=handle_delete_entity,
    )
    entity_board.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

    # --- Zone basse : bouton de génération et version (fixe) ---
    bottom_frame = tk.Frame(main_container, bg=BG_DARK)
    bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
    bottom_frame.grid_columnconfigure(0, weight=1)  # Pour centrer le contenu

    # Container pour le bouton et la version
    bottom_content = tk.Frame(bottom_frame, bg=BG_DARK)
    bottom_content.pack(pady=(20, 10))

    generate_btn = ttk.Button(
        bottom_content,
        text="🚀 Generate all entities",
        command=generate_all_entities,
        style="TButton",
    )
    generate_btn.pack(pady=(0, 8))

    version_label = make_label(
        bottom_content,
        f"Version {VERSION}",
        size=10,
    )
    version_label.pack()

    # Injection des callbacks dans entity_board
    entity_board.update_entity_name = update_entity_name
    entity_board.handle_delete_entity = handle_delete_entity


def main():
    """Point d'entrée principal de l'interface :
    initialise la fenêtre et les composants."""
    logger.info("Starting application")
    clean_folders()
    root = create_main_window()
    apply_style(root)
    load_icons()
    setup_main_interface(root, dev_mode=True)
    create_menu_bar(root)
    root.mainloop()
    logger.info("Stopping application")
