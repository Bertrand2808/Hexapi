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
    FONT_SIZE_TITLE,
    LABELFRAME_BG,
    PADDING,
    SUCCESS_COLOR,
    TEXT_COLOR,
)
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
        borderwidth=1,
        relief="flat",
        padding=8,
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
        selectforeground=TEXT_COLOR,
        padding=8,
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
        padding=12,
        borderwidth=0,
        relief="flat",
    )
    style.map(
        "TButton",
        background=[("active", ACCENT_HOVER)],
        foreground=[("active", TEXT_COLOR)],
        relief=[("active", "groove")],
    )

    # Frames avec label
    style.configure(
        "Custom.TLabelframe",
        background=LABELFRAME_BG,
        foreground=TEXT_COLOR,
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
        borderwidth=1,
        padding=16,
        relief="ridge",
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
        foreground=TEXT_COLOR,
        font=(FONT_FAMILY, FONT_SIZE_LABEL, "bold"),
        padding=12,
        borderwidth=0,
        relief="flat",
    )

    style.map(
        "Green.TButton",
        background=[("active", "#2ecc71")],
        foreground=[("active", TEXT_COLOR)],
        relief=[("active", "groove")],
    )

    # Bouton secondaire
    style.configure(
        "Red.TButton",
        background=ERROR_COLOR,
        foreground="white",
        font=(FONT_FAMILY, FONT_SIZE_LABEL, "bold"),
        padding=12,
        borderwidth=0,
        relief="flat",
    )

    style.map(
        "Red.TButton",
        background=[("active", "#c0392b")],
        foreground=[("active", TEXT_COLOR)],
        relief=[("active", "groove")],
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

        editor = EntityEditorWindow(root, entity_name, header, dev_mode=dev_mode)
        entity_editors[entity_name] = editor

    def create_entity():
        logger.info("Creating new entity")
        dialog = tk.Toplevel(root)
        dialog.title("New entity")
        dialog.geometry("400x200")
        dialog.configure(bg=BG_LIGHT)
        dialog.transient(root)
        dialog.grab_set()

        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        title = make_label(
            dialog,
            "New entity name",
            size=14,
            bold=True,
        )
        title.pack(pady=(30, 20))

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
            if not name:
                show_error_message(dialog, "The entity name cannot be empty")
                return
            logger.info("Creating entity %s", name)
            dialog.destroy()
            entities_data[name] = []
            entity_board.add_entity(name)
            open_entity_editor(name)

        validate_btn = ttk.Button(
            dialog,
            text="Create",
            command=validate_and_create,
            style="TButton",
        )
        validate_btn.pack()

        dialog.bind("<Return>", lambda e: validate_and_create())
        dialog.wait_window()

    def delete_entity(entity_name):
        logger.info("Deleting entity %s", entity_name)
        if entity_name in entity_editors:
            try:
                entity_editors[entity_name].destroy()
            except tk.TclError:
                pass
            del entity_editors[entity_name]

        if entity_name in entities_data:
            del entities_data[entity_name]

        json_path = f"temp/{entity_name}.json"
        if os.path.exists(json_path):
            logger.info("Deleting temporary JSON file %s", json_path)
            os.remove(json_path)

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
        logger.info("Updating entity name from %s to %s", old_name, new_name)
        if old_name in entity_editors:
            try:
                editor = entity_editors.pop(old_name)
                entity_editors[new_name] = editor
                editor.entity_name = new_name
                editor.title(f"Editing {new_name}")
            except tk.TclError:
                if old_name in entity_editors:
                    logger.info("Deleting old editor %s", old_name)
                    del entity_editors[old_name]

        if old_name in entities_data:
            entities_data[new_name] = entities_data.pop(old_name)
            logger.info("Updating entity data for %s", new_name)

        entity_board.update_entity_name(old_name, new_name)
        logger.info("Updating entity %s", new_name)

    # --- Conteneur principal avec grid ---
    main_container = tk.Frame(root, bg=BG_DARK)
    main_container.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    main_container.grid_rowconfigure(0, weight=1)
    main_container.grid_rowconfigure(1, weight=0)
    main_container.grid_columnconfigure(0, weight=1)

    # --- Partie haute : header + section entités (scrollable) ---
    top_frame = tk.Frame(main_container, bg=BG_DARK)
    top_frame.grid(row=0, column=0, sticky="nsew")
    top_frame.grid_rowconfigure(0, weight=0)
    top_frame.grid_rowconfigure(1, weight=1)
    top_frame.grid_columnconfigure(0, weight=1)

    # --- Partie basse : bouton de génération (fixe) ---
    bottom_frame = tk.Frame(main_container, bg=BG_DARK)
    bottom_frame.grid(row=1, column=0, sticky="ew")

    # Frame principal avec padding (dans top_frame)
    main_frame = tk.Frame(top_frame, bg=BG_DARK, padx=PADDING, pady=PADDING)
    main_frame.grid(row=0, column=0, sticky="ew")

    # Titre principal
    title_label = make_label(
        main_frame,
        "HEXAPI GENERATOR",
        size=FONT_SIZE_TITLE,
        bold=True,
    )
    title_label.pack(pady=(0, 30))

    # En-tête du projet
    header = ProjectHeader(main_frame)
    header.pack(anchor="w", fill="x", pady=(0, 30))

    # --- Section des entités scrollable ---
    entity_section_container = tk.Frame(top_frame, bg=BG_DARK)
    entity_section_container.grid(row=1, column=0, sticky="nsew")
    entity_section_container.grid_rowconfigure(0, weight=1)
    entity_section_container.grid_columnconfigure(0, weight=1)

    # Canvas + Scrollbar
    entity_canvas = tk.Canvas(
        entity_section_container, bg=BG_DARK, highlightthickness=0
    )
    entity_canvas.grid(row=0, column=0, sticky="nsew")
    entity_scrollbar = ttk.Scrollbar(
        entity_section_container, orient="vertical", command=entity_canvas.yview
    )
    entity_scrollbar.grid(row=0, column=1, sticky="ns")
    entity_canvas.configure(yscrollcommand=entity_scrollbar.set)

    # Frame réelle qui contient les entités
    entity_section = ttk.LabelFrame(
        entity_canvas,
        text="Entities",
        padding=(20, 20),
        style="Custom.TLabelframe",
    )
    entity_window = entity_canvas.create_window(
        (0, 0), window=entity_section, anchor="nw"
    )

    def on_entity_frame_configure(event):
        # Mettre à jour la région de défilement
        entity_canvas.configure(scrollregion=entity_canvas.bbox("all"))

        # Vérifier si la scrollbar est nécessaire
        bbox = entity_canvas.bbox("all")
        if bbox:
            canvas_height = entity_canvas.winfo_height()
            content_height = bbox[3] - bbox[1]
            if content_height <= canvas_height:
                entity_scrollbar.grid_remove()  # Cacher la scrollbar
            else:
                entity_scrollbar.grid()  # Afficher la scrollbar

    entity_section.bind("<Configure>", on_entity_frame_configure)

    def on_entity_canvas_configure(event):
        # Adapter la largeur de la frame à celle du canvas
        canvas_width = event.width
        entity_canvas.itemconfig(entity_window, width=canvas_width)

        # Vérifier à nouveau si la scrollbar est nécessaire
        bbox = entity_canvas.bbox("all")
        if bbox:
            canvas_height = event.height
            content_height = bbox[3] - bbox[1]
            if content_height <= canvas_height:
                entity_scrollbar.grid_remove()  # Cacher la scrollbar
            else:
                entity_scrollbar.grid()  # Afficher la scrollbar

    entity_canvas.bind("<Configure>", on_entity_canvas_configure)

    # Scroll à la molette
    def on_mouse_wheel(event):
        try:
            # Vérifier si la souris est dans la zone des entités
            x = event.x_root - entity_section_container.winfo_rootx()
            y = event.y_root - entity_section_container.winfo_rooty()

            if (
                0 <= x <= entity_section_container.winfo_width()
                and 0 <= y <= entity_section_container.winfo_height()
            ):
                # Sur Windows, event.delta est en multiples de 120
                # Sur Linux/Mac, event.delta est en pixels
                if event.num == 4:  # Linux scroll up
                    entity_canvas.yview_scroll(-1, "units")
                elif event.num == 5:  # Linux scroll down
                    entity_canvas.yview_scroll(1, "units")
                else:  # Windows/Mac
                    entity_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            # Ignorer l'erreur si le canvas a été détruit
            pass

    # Lier l'événement de défilement à la fenêtre principale
    root.bind_all("<MouseWheel>", on_mouse_wheel)  # Windows
    root.bind_all("<Button-4>", on_mouse_wheel)  # Linux scroll up
    root.bind_all("<Button-5>", on_mouse_wheel)  # Linux scroll down

    def on_destroy(_event):
        root.unbind_all("<MouseWheel>")
        root.unbind_all("<Button-4>")
        root.unbind_all("<Button-5>")

    entity_canvas.bind("<Destroy>", on_destroy)

    # --- Board des entités ---
    entity_board = EntityBoard(
        entity_section,
        on_entity_click=open_entity_editor,
        on_add_entity=create_entity,
    )
    entity_board.pack(fill="both", expand=True)

    # --- Bouton de génération (fixe en bas) ---
    generate_btn = ttk.Button(
        bottom_frame,
        text="🚀 Generate all entities",
        command=generate_all_entities,
        style="TButton",
    )
    generate_btn.pack(pady=(30, 20), anchor="center")

    # Version label
    version_label = make_label(
        bottom_frame,
        f"Version {VERSION}",
        size=10,
    )
    version_label.pack(pady=(0, 10), anchor="center")

    # Exposer les fonctions de mise à jour
    entity_board.update_entity_name = update_entity_name
    entity_board.delete_entity = delete_entity


def main():
    """Point d'entrée principal de l'interface :
    initialise la fenêtre et les composants."""
    logger.info("Starting application")

    clean_folders()

    root = create_main_window()
    apply_style(root)
    setup_main_interface(root, dev_mode=True)
    create_menu_bar(root)
    root.mainloop()
    logger.info("Stopping application")
