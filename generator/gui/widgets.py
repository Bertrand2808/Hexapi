import tkinter as tk
from tkinter import ttk

from generator.core.fake_utils import get_fake_value

# === Constantes ===
FONT_FAMILY = "Segoe UI"
FONT_SIZE_LABEL = 9
TEXT_COLOR = "white"
BG_COLOR = "#3a3a4a"


def add_field(parent_frame):
    """
    Ajoute dynamiquement une ligne de champ (nom + type + comment + testValue)
    dans une section encadrée.
    """
    # Conteneur visuel de la ligne
    row = tk.Frame(parent_frame, bg=BG_COLOR, padx=10, pady=10)
    row.pack(fill="x", pady=10)

    # Frame interne pour le layout en grille
    content = tk.Frame(row, bg=row["bg"])
    content.pack()

    # Préparation du type et de sa valeur par défaut
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

    # --- Label + Entry : Nom ---
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

    # --- Label + ComboBox : Type ---
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
    )
    type_combobox.grid(row=1, column=1, padx=(0, 10))

    # --- Label + Entry : Commentaire ---
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

    # --- Label + Entry : Valeur de test ---
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

    # --- MàJ auto de la valeur de test quand le type change ---
    def update_test_value(*args):
        test_value.set(get_fake_value(selected_type.get()))

    selected_type.trace_add("write", update_test_value)

    # --- Bouton supprimer ---
    def remove_row():
        row.destroy()
        if hasattr(parent_frame, "_fields_list"):
            parent_frame._fields_list.remove(
                (name_entry, type_combobox, comment_entry, test_entry, row)
            )

    delete_button = ttk.Button(content, text="🗑", width=3, command=remove_row)
    delete_button.grid(row=1, column=4, padx=(15, 0))

    return name_entry, type_combobox, comment_entry, test_entry, row
