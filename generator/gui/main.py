"""Module principal de l'interface graphique HexAPI Generator."""

# === Imports ===
import os
import shutil
import tkinter as tk
from tkinter import ttk

from generator.core.generator import save_entity_json
from generator.gui.layout.entity_board import EntityBoard
from generator.gui.layout.entity_editor import EntityEditorWindow
from generator.gui.layout.project_header import ProjectHeader
from generator.gui.menubar import create_menu_bar
from generator.scripts.generate_entity import generate_all_templates

# === Constantes de style ===
BG_DARK = "#1e1e2f"
BG_LIGHT = "#2e2e3e"
BG_LIGHTER = "#3a3a4a"
ACCENT_COLOR = "#4F8EF7"
ACCENT_HOVER = "#6fa5f7"
TEXT_COLOR = "#f0f0f0"
FONT_FAMILY = "Segoe UI"
FONT_SIZE_LABEL = 11
FONT_SIZE_TITLE = 24
FONT_SIZE_SUBTITLE = 18
PADDING = 20
BORDER_RADIUS = 8


def clean_temp_folder():
    """Nettoie le dossier temp au lancement de l'application."""
    temp_dir = "temp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)


def create_main_window():
    """Crée et configure la fenêtre principale de l'application."""
    root = tk.Tk()
    root.title("HexAPI Generator")
    root.geometry("1200x800")
    root.configure(bg=BG_DARK)
    root.minsize(1000, 700)  # Taille minimale de la fenêtre
    return root


def apply_style(root):
    """Applique le thème sombre et les styles personnalisés aux composants Tkinter."""
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
        borderwidth=0,
        padding=5,
    )

    # Combobox
    style.configure(
        "Custom.TCombobox",
        fieldbackground=BG_LIGHTER,
        background=BG_LIGHTER,
        foreground=TEXT_COLOR,
        arrowcolor=TEXT_COLOR,
        bordercolor=ACCENT_COLOR,
        selectbackground=ACCENT_COLOR,
        selectforeground=TEXT_COLOR,
        padding=5,
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
        foreground=TEXT_COLOR,
        font=(FONT_FAMILY, FONT_SIZE_LABEL, "bold"),
        padding=10,
        borderwidth=0,
    )
    style.map(
        "TButton",
        background=[("active", ACCENT_HOVER)],
        foreground=[("active", TEXT_COLOR)],
    )

    # Frames avec label
    style.configure(
        "Custom.TLabelframe",
        background=BG_LIGHT,
        foreground=TEXT_COLOR,
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
        borderwidth=1,
        padding=10,
    )
    style.configure(
        "Custom.TLabelframe.Label",
        background=BG_LIGHT,
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


def setup_main_interface(root, dev_mode=False):
    """Construit l'interface utilisateur principale : formulaires, champs et boutons."""
    entities_data = {}  # {entity_name: {fields: [field_data]}}
    entity_editors = {}  # {entity_name: EntityEditorWindow}

    def open_entity_editor(entity_name):
        print(f"Opening editor for {entity_name}")
        if entity_name in entity_editors:
            try:
                entity_editors[entity_name].lift()
                return
            except tk.TclError:
                del entity_editors[entity_name]

        editor = EntityEditorWindow(root, entity_name, header, dev_mode=dev_mode)
        entity_editors[entity_name] = editor

    def create_entity():
        """Crée une nouvelle entité avec un nom personnalisé."""
        dialog = tk.Toplevel(root)
        dialog.title("Nouvelle entité")
        dialog.geometry("400x200")
        dialog.configure(bg=BG_LIGHT)
        dialog.transient(root)
        dialog.grab_set()

        # Centrer la fenêtre
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        # Titre
        title = make_label(
            dialog,
            "Nom de la nouvelle entité",
            size=14,
            bold=True,
        )
        title.pack(pady=(30, 20))

        # Champ de saisie
        name_var = tk.StringVar()
        name_entry = ttk.Entry(
            dialog,
            textvariable=name_var,
            width=30,
            font=(FONT_FAMILY, 12),
        )
        name_entry.pack(pady=(0, 30))
        name_entry.focus_set()

        def validate_and_create():
            name = name_var.get().strip()
            if name:
                dialog.destroy()
                entities_data[name] = []
                entity_board.add_entity(name)
                open_entity_editor(name)

        # Bouton de validation
        validate_btn = ttk.Button(
            dialog,
            text="Créer",
            command=validate_and_create,
            style="TButton",
        )
        validate_btn.pack()

        dialog.bind("<Return>", lambda e: validate_and_create())
        dialog.wait_window()

    def generate_all_entities():
        """Génère toutes les entités ouvertes."""
        for entity_name, editor in list(entity_editors.items()):
            try:
                data = editor.get_entity_data()
                filepath = save_entity_json(entity_name, data)
                print(f"[OK] JSON généré pour {entity_name} : {filepath}")
                generate_all_templates(json_path=filepath)
            except tk.TclError:
                del entity_editors[entity_name]

    def update_entity_name(old_name, new_name):
        """Met à jour le nom d'une entité dans l'interface."""
        if old_name in entity_editors:
            try:
                editor = entity_editors.pop(old_name)
                entity_editors[new_name] = editor
                editor.entity_name = new_name
                editor.title(f"Édition de {new_name}")
            except tk.TclError:
                if old_name in entity_editors:
                    del entity_editors[old_name]

        if old_name in entities_data:
            entities_data[new_name] = entities_data.pop(old_name)

        entity_board.update_entity_name(old_name, new_name)

    # Frame principal avec padding
    main_frame = tk.Frame(root, bg=BG_DARK, padx=PADDING, pady=PADDING)
    main_frame.pack(fill="both", expand=True)

    # Titre principal
    title_label = make_label(
        main_frame,
        "Créateur de classes HexAPI",
        size=FONT_SIZE_TITLE,
        bold=True,
    )
    title_label.pack(pady=(0, 30))

    # En-tête du projet
    header = ProjectHeader(main_frame)
    header.pack(anchor="w", fill="x", pady=(0, 30))

    # Section des entités
    entity_section = ttk.LabelFrame(
        main_frame,
        text="Entités",
        padding=(20, 20),
        style="Custom.TLabelframe",
    )
    entity_section.pack(fill="both", expand=True)

    entity_board = EntityBoard(
        entity_section,
        on_entity_click=open_entity_editor,
        on_add_entity=create_entity,
    )
    entity_board.pack(fill="both", expand=True)

    # Bouton de génération
    generate_btn = ttk.Button(
        main_frame,
        text="🚀 Générer toutes les entités",
        command=generate_all_entities,
        style="TButton",
    )
    generate_btn.pack(pady=(30, 0), anchor="center")

    # Exposer la fonction de mise à jour du nom
    entity_board.update_entity_name = update_entity_name


def main():
    """Point d'entrée principal de l'interface :
    initialise la fenêtre et les composants."""

    clean_temp_folder()

    root = create_main_window()
    apply_style(root)
    setup_main_interface(root, dev_mode=True)
    create_menu_bar(root)
    root.mainloop()
