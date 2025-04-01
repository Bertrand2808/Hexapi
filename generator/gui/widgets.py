"""
Widgets pour l'interface de génération d'entités Java.
Inclut les champs dynamiques (nom, type, commentaire, valeur de test)
ainsi qu'une frame scrollable personnalisée.
"""

import tkinter as tk
from tkinter import ttk

from generator.core.fake_utils import get_fake_value

# === Constantes ===
FONT_FAMILY = "Segoe UI"
FONT_SIZE_LABEL = 9
TEXT_COLOR = "white"
BG_COLOR = "#3a3a4a"


def add_field(parent_frame, index=None):
    """
    Ajoute dynamiquement une ligne de champ (nom + type + commentaire + testValue).
    Chaque champ est inséré dans la scrollable frame et stylisé.
    """
    row = tk.Frame(parent_frame, bg=BG_COLOR, padx=10, pady=10)
    row.pack(fill="x", pady=10)

    if index is not None:
        index_label = tk.Label(
            row,
            text=f"#{index}",
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            fg=TEXT_COLOR,
            bg=BG_COLOR,
            width=4,
        )
        index_label.pack(side="left", padx=(0, 10))

    content = tk.Frame(row, bg=row["bg"])
    content.pack()

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

    name_label = tk.Label(
        content,
        text="Nom",
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
        fg=TEXT_COLOR,
        bg=content["bg"],
    )
    name_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
    name_entry = ttk.Entry(content, width=20)
    name_entry.grid(row=1, column=0, padx=(0, 10))

    type_label = tk.Label(
        content,
        text="Type",
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
        fg=TEXT_COLOR,
        bg=content["bg"],
    )
    type_label.grid(row=0, column=1, sticky="w", padx=(0, 10))
    type_combobox = ttk.Combobox(
        content,
        values=type_options,
        width=15,
        state="readonly",
        textvariable=selected_type,
        style="Custom.TCombobox",
    )
    type_combobox.grid(row=1, column=1, padx=(0, 10))

    comment_label = tk.Label(
        content,
        text="Commentaire",
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
        fg=TEXT_COLOR,
        bg=content["bg"],
    )
    comment_label.grid(row=0, column=2, sticky="w", padx=(0, 10))
    comment_entry = ttk.Entry(content, width=20)
    comment_entry.grid(row=1, column=2, padx=(0, 10))

    test_label = tk.Label(
        content,
        text="Valeur de test",
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
        fg=TEXT_COLOR,
        bg=content["bg"],
    )
    test_label.grid(row=0, column=3, sticky="w")
    test_entry = ttk.Entry(content, textvariable=test_value, width=20)
    test_entry.grid(row=1, column=3)

    def update_test_value(_varname=None, _index=None, _mode=None):
        test_value.set(get_fake_value(selected_type.get()))

    selected_type.trace_add("write", update_test_value)

    def remove_row():
        row.destroy()
        if isinstance(parent_frame, ScrollableFieldsFrame):
            fields_list = parent_frame.get_fields_list()
            fields_list.remove(
                (name_entry, type_combobox, comment_entry, test_entry, row)
            )
            parent_frame.set_fields_list(fields_list)

    delete_button = ttk.Button(content, text="🗑", width=3, command=remove_row)
    delete_button.grid(row=1, column=4, padx=(15, 0))

    return name_entry, type_combobox, comment_entry, test_entry, row


class ScrollableFieldsFrame(tk.Frame):
    """Frame avec liste de champs dynamiques et accès à l'état interne."""

    def __init__(self, parent, bg_color):
        super().__init__(parent, bg=bg_color)
        self._fields_list = []

    def set_fields_list(self, fields_list):
        """Met à jour la liste des widgets de champs."""
        self._fields_list = fields_list

    def get_fields_list(self):
        """Retourne la liste des widgets de champs."""
        return self._fields_list


def create_scrollable_fields_frame(parent, bg_color):
    """Crée une section scrollable pour accueillir les champs dynamiques."""
    container = tk.Frame(parent, bg=bg_color)
    container.pack(fill="both", expand=True, pady=(10, 0))

    canvas = tk.Canvas(container, bg=bg_color, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame = ScrollableFieldsFrame(canvas, bg_color)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_frame_configure(_event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.bind_all(
        "<MouseWheel>",
        lambda _e: canvas.yview_scroll(int(-1 * (_e.delta / 120)), "units"),
    )

    return scrollable_frame
