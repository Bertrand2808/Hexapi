"""
Widgets pour l'interface de génération d'entités Java.
Inclut les champs dynamiques (nom, type, commentaire, valeur de test)
ainsi qu'une frame scrollable personnalisée.
"""

import tkinter as tk
from tkinter import ttk

from generator.core.fake_utils import get_fake_value
from generator.core.logger import logger
from generator.gui.style import (
    BG_COLOR,
    BUTTON_SPACING,
    FONT_FAMILY,
    FONT_SIZE_LABEL,
    LABEL_ENTRY_SPACING,
    PADDING,
    SECTION_SPACING,
    TEXT_COLOR,
)


def add_field(parent_frame, index=None):
    """
    Ajoute dynamiquement une ligne de champ (nom + type + commentaire + testValue).
    Chaque champ est inséré dans la scrollable frame et stylisé.
    """
    logger.info("Ajout d'un champ pour %s", parent_frame.entity_name)

    # Container principal avec ombre et coins arrondis
    row = tk.Frame(parent_frame, bg=BG_COLOR, padx=PADDING, pady=PADDING)
    row.pack(fill="x", pady=SECTION_SPACING)

    # En-tête avec numéro et bouton de suppression
    header = tk.Frame(row, bg=BG_COLOR)
    header.pack(fill="x", pady=(0, 8))

    if index is not None:
        index_label = tk.Label(
            header,
            text=f"#{index}",
            font=(FONT_FAMILY, FONT_SIZE_LABEL, "bold"),
            fg=TEXT_COLOR,
            bg=BG_COLOR,
            width=4,
        )
        index_label.pack(side="left")

    delete_button = ttk.Button(
        header,
        text="🗑",
        width=3,
        command=lambda: remove_row(),
        style="Red.TButton",
        cursor="hand2",
    )
    delete_button.pack(side="right")

    # Contenu du champ
    content = tk.Frame(row, bg=BG_COLOR)
    content.pack(fill="x")

    type_options = [
        "String",
        "Integer",
        "Long",
        "Boolean",
        "Double",
        "BigDecimal",
        "ZonedDateTime",
        "LocalDate",
        "LocalDateTime",
        "UUID",
    ]
    selected_type = tk.StringVar(value=type_options[0])
    test_value = tk.StringVar(value=get_fake_value(selected_type.get()))
    is_id = tk.BooleanVar(value=False)
    nullable_var = tk.BooleanVar(value=False)

    # Grille des champs
    fields = [
        ("Nom", "name", 0),
        ("Type", "type", 1),
        ("Commentaire", "comment", 2),
        ("Valeur de test", "test", 3),
    ]

    # Initialiser les variables pour éviter les erreurs de linter
    name_entry = None
    type_combobox = None
    comment_entry = None
    test_entry = None

    for label_text, field_type, col in fields:
        field_frame = tk.Frame(content, bg=BG_COLOR)
        field_frame.grid(row=0, column=col, padx=(0, PADDING), sticky="ew")

        label = tk.Label(
            field_frame,
            text=label_text,
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            fg=TEXT_COLOR,
            bg=BG_COLOR,
        )
        label.pack(anchor="w", pady=(0, LABEL_ENTRY_SPACING))

        if field_type == "name":
            entry = ttk.Entry(field_frame, width=20)
            entry.pack(fill="x")
            name_entry = entry
        elif field_type == "type":
            combobox = ttk.Combobox(
                field_frame,
                values=type_options,
                width=15,
                state="readonly",
                textvariable=selected_type,
                style="Custom.TCombobox",
            )
            combobox.pack(fill="x")
            type_combobox = combobox
        elif field_type == "comment":
            entry = ttk.Entry(field_frame, width=20)
            entry.pack(fill="x")
            comment_entry = entry
        else:  # test
            entry = ttk.Entry(field_frame, textvariable=test_value, width=20)
            entry.pack(fill="x")
            test_entry = entry

    # Options
    options_frame = tk.Frame(content, bg=BG_COLOR)
    options_frame.grid(row=0, column=4, padx=(PADDING, 0), sticky="ew")

    id_checkbox = ttk.Checkbutton(
        options_frame,
        text="ID",
        variable=is_id,
        style="Custom.TCheckbutton",
        cursor="hand2",
    )
    id_checkbox.pack(side="left", padx=(0, BUTTON_SPACING))

    nullable_checkbox = ttk.Checkbutton(
        options_frame,
        text="nullable",
        variable=nullable_var,
        style="Custom.TCheckbutton",
        cursor="hand2",
    )
    nullable_checkbox.pack(side="left")

    def update_test_value(_varname=None, _index=None, _mode=None):
        logger.info(
            "Mise à jour de la valeur de test pour %s", parent_frame.entity_name
        )
        test_value.set(get_fake_value(selected_type.get()))

    selected_type.trace_add("write", update_test_value)

    def remove_row():
        logger.info("Suppression de la ligne pour %s", parent_frame.entity_name)
        if isinstance(parent_frame, ScrollableFieldsFrame):
            fields_list = parent_frame.get_fields_list()
            # Trouver l'index du champ à supprimer
            for i, field in enumerate(fields_list):
                if field[-1] == row:  # Le dernier élément est la row
                    fields_list.pop(i)
                    break
            parent_frame.set_fields_list(fields_list)
        row.destroy()

    return (
        name_entry,
        type_combobox,
        comment_entry,
        test_entry,
        is_id,
        nullable_var,
        row,
    )


class ScrollableFieldsFrame(tk.Frame):
    """Frame avec liste de champs dynamiques et accès à l'état interne."""

    def __init__(self, parent, bg_color, entity_name="Unknown"):
        super().__init__(parent, bg=bg_color)
        self._fields_list = []
        self.entity_name = entity_name

    def set_fields_list(self, fields_list):
        """Met à jour la liste des widgets de champs."""
        logger.info(
            "Mise à jour de la liste des widgets de champs pour %s", self.entity_name
        )
        self._fields_list = fields_list

    def get_fields_list(self):
        """Retourne la liste des widgets de champs."""
        logger.info(
            "Récupération de la liste des widgets de champs pour %s", self.entity_name
        )
        return self._fields_list


def create_scrollable_fields_frame(parent, bg_color, entity_name="Unknown"):
    """Crée une section scrollable pour accueillir les champs dynamiques."""
    logger.info("Création du frame scrollable pour %s", entity_name)
    container = tk.Frame(parent, bg=bg_color)
    container.pack(fill="both", expand=True, pady=(10, 0))

    canvas = tk.Canvas(container, bg=bg_color, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame = ScrollableFieldsFrame(canvas, bg_color, entity_name)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_frame_configure(_event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_mouse_wheel(event):
        """Gère le défilement de la souris."""
        try:
            # Sur Windows, event.delta est en multiples de 120
            # Sur Linux/Mac, event.delta est en pixels
            if event.num == 4:  # Linux scroll up
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:  # Linux scroll down
                canvas.yview_scroll(1, "units")
            else:  # Windows/Mac
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            # Ignorer l'erreur si le canvas a été détruit
            pass

    scrollable_frame.bind("<Configure>", on_frame_configure)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Lier l'événement de défilement au canvas uniquement
    canvas.bind("<MouseWheel>", on_mouse_wheel)  # Windows
    canvas.bind("<Button-4>", on_mouse_wheel)  # Linux scroll up
    canvas.bind("<Button-5>", on_mouse_wheel)  # Linux scroll down

    # Nettoyer l'événement lors de la destruction
    def on_destroy(_event):
        canvas.unbind("<MouseWheel>")
        canvas.unbind("<Button-4>")
        canvas.unbind("<Button-5>")

    canvas.bind("<Destroy>", on_destroy)

    return scrollable_frame
