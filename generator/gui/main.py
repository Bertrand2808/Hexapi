"""Module principal de l'interface graphique HexAPI Generator."""

# === Imports ===
import tkinter as tk
from tkinter import ttk

from generator.core.generator import build_entity_data, save_entity_json
from generator.core.naming import generate_name_variants
from generator.gui.menubar import create_menu_bar
from generator.gui.widgets import add_field, create_scrollable_fields_frame
from generator.scripts.generate_entity import generate_all_templates

BG_DARK = "#1e1e2f"
FONT_FAMILY = "Segoe UI"
FONT_SIZE_LABEL = 11


def create_main_window():
    """Crée et configure la fenêtre principale de l'application."""

    root = tk.Tk()
    root.title("HexAPI Generator")
    root.geometry("1200x800")
    root.configure(bg=BG_DARK)
    return root


def apply_style(root):
    """Applique le thème sombre et les styles personnalisés aux composants Tkinter."""

    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(
        "TLabel",
        foreground="#f0f0f0",
        background="#2e2e3e",
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
    )
    style.configure(
        "TEntry", foreground="white", fieldbackground="#3a3a4a", borderwidth=0
    )
    style.configure(
        "Custom.TCombobox",
        fieldbackground="#3a3a4a",  # couleur de fond du champ
        background="#3a3a4a",  # couleur de fond du menu déroulant
        foreground="white",  # texte
        arrowcolor="white",  # couleur de la flèche
        bordercolor="#4F8EF7",  # optionnel si tu veux border bleue
        selectbackground="#4F8EF7",  # couleur de sélection
        selectforeground="white",
        padding=4,
    )

    style.map(
        "Custom.TCombobox",
        fieldbackground=[("readonly", "#3a3a4a")],
        foreground=[("readonly", "white")],
        background=[("readonly", "#3a3a4a")],
    )

    style.configure(
        "TButton",
        background="#4F8EF7",
        foreground="white",
        font=(FONT_FAMILY, FONT_SIZE_LABEL, "bold"),
        padding=6,
        borderwidth=0,
    )
    style.map("TButton", background=[("active", "#6fa5f7")])
    style.configure(
        "Custom.TLabelframe",
        background="#2e2e3e",
        foreground="white",
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
        borderwidth=1,
    )
    style.configure(
        "Custom.TLabelframe.Label",
        background="#2e2e3e",
        foreground="white",
        font=(FONT_FAMILY, FONT_SIZE_LABEL, "bold"),
    )


def make_label(parent, text):
    """Crée un label stylisé avec les couleurs et polices de l'application."""

    return tk.Label(
        parent,
        text=text,
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
        fg="white",
        bg=parent["bg"],
    )


def setup_main_interface(root, dev_mode=False):
    """Construit l'interface utilisateur principale : formulaires, champs et boutons."""

    fields = []

    main_frame = tk.Frame(root, bg="#2e2e3e", padx=40, pady=30)
    main_frame.pack(fill="both", expand=True)

    title_label = tk.Label(
        main_frame,
        text="Créateur de classes HexAPI",
        font=("Helvetica Neue", 18, "bold"),
        fg="white",
        bg=main_frame["bg"],
    )
    title_label.pack(pady=(10, 20))

    # === Ligne horizontale pour Nom Entreprise et Nom Projet ===
    top_row_frame = tk.Frame(main_frame, bg=main_frame["bg"])
    top_row_frame.pack(anchor="w", pady=(0, 20), fill="x")
    top_row_frame.columnconfigure(1, weight=1)
    top_row_frame.columnconfigure(3, weight=1)

    make_label(top_row_frame, "Nom Entreprise").grid(
        row=0, column=0, sticky="w", padx=(0, 10)
    )
    company_entry = ttk.Entry(
        top_row_frame, width=25, font=(FONT_FAMILY, FONT_SIZE_LABEL)
    )
    company_entry.grid(row=0, column=1, sticky="ew", padx=(0, 30))

    make_label(top_row_frame, "Nom Projet").grid(
        row=0, column=2, sticky="w", padx=(0, 10)
    )
    project_entry = ttk.Entry(
        top_row_frame, width=25, font=(FONT_FAMILY, FONT_SIZE_LABEL)
    )
    project_entry.grid(row=0, column=3, sticky="ew")

    make_label(main_frame, "Nom Entity (sans 'Entity')").pack(anchor="w")
    entity_name_entry = ttk.Entry(
        main_frame, width=40, font=(FONT_FAMILY, FONT_SIZE_LABEL)
    )
    entity_name_entry.pack(pady=(5, 20), anchor="w")

    # === Cadre encadré pour les champs dynamiques ===
    fields_section = ttk.LabelFrame(
        main_frame,
        text="Champs de l'entité",
        padding=(20, 10),
        style="Custom.TLabelframe",
    )

    fields_section.pack(fill="both", expand=True, pady=(10, 20))
    fields_section.configure(style="TLabel")

    fields_frame = create_scrollable_fields_frame(fields_section, bg_color="#2e2e3e")

    def handle_add_field():
        index = len(fields) + 1
        widgets = add_field(fields_frame, index=index)
        fields.append(widgets)
        fields_frame.set_fields_list(fields)

    def generate_class():
        company_raw = company_entry.get().strip()
        project_raw = project_entry.get().strip()
        entity_name = entity_name_entry.get().strip()

        if not entity_name:
            print("Erreur : nom de l'Entity vide.")
            return

        company_variants = generate_name_variants(company_raw)
        project_variants = generate_name_variants(project_raw)

        data = build_entity_data(entity_name, fields)
        data["company"] = company_variants
        data["project"] = project_variants

        filepath = save_entity_json(entity_name, data)
        print(f"[OK] Json was generated in : {filepath}")

        generate_all_templates(json_path=filepath)

    add_field_button = ttk.Button(
        main_frame, text="Ajouter un champ", command=handle_add_field
    )
    add_field_button.pack(pady=(10, 10), anchor="w")

    # Ligne de séparation
    ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=10)

    generate_button = ttk.Button(
        main_frame, text="Générer la classe", command=generate_class
    )
    generate_button.pack(pady=(10, 0), anchor="center")

    if dev_mode:
        dev_button = ttk.Button(
            main_frame,
            text="Pré-remplir pour test 🧪",
            command=lambda: auto_fill_fields(
                company_entry,
                project_entry,
                entity_name_entry,
                fields,
                handle_add_field,
            ),
        )
        dev_button.pack(pady=(5, 0), anchor="w")


def auto_fill_fields(
    company_entry, project_entry, entity_name_entry, fields, handle_add_field
):
    """Préremplit les champs pour les tests en dev."""
    company_entry.delete(0, tk.END)
    company_entry.insert(0, "TestDemonEntreprise")

    project_entry.delete(0, tk.END)
    project_entry.insert(0, "MonSuperProjet")

    entity_name_entry.delete(0, tk.END)
    entity_name_entry.insert(0, "User")

    exemples = [
        ("id", "Long", "id de l'utilisateur", "42", True),
        ("name", "String", "nom complet", "Toto Bidule", False),
        ("mail", "String", "email principal", "toto@hexapi.dev", False),
    ]

    for nom, type_, comment, test_value, is_id_value in exemples:
        handle_add_field()
        name_entry, type_combobox, comment_entry, test_entry, is_id, _ = fields[-1]
        name_entry.insert(0, nom)
        type_combobox.set(type_)
        comment_entry.insert(0, comment)
        test_entry.insert(0, test_value)
        is_id.set(is_id_value)


def main():
    """Point d'entrée principal de l'interface :
    initialise la fenêtre et les composants."""

    root = create_main_window()
    apply_style(root)
    setup_main_interface(root, dev_mode=True)
    create_menu_bar(root)
    root.mainloop()
