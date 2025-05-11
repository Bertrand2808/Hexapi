import json
import os
import tkinter as tk
from tkinter import ttk

from generator.core.generator import build_entity_data
from generator.core.naming import generate_name_variants
from generator.gui.widgets import add_field, create_scrollable_fields_frame

# === Constantes de style ===
BG_DARK = "#1e1e2f"
BG_LIGHT = "#2e2e3e"
BG_LIGHTER = "#3a3a4a"
ACCENT_COLOR = "#4F8EF7"
ACCENT_HOVER = "#6fa5f7"
TEXT_COLOR = "#f0f0f0"
FONT_FAMILY = "Segoe UI"
FONT_SIZE_LABEL = 11
FONT_SIZE_TITLE = 20
FONT_SIZE_SUBTITLE = 16
PADDING = 20


class EntityEditorWindow(tk.Toplevel):
    """
    Fenêtre d'édition pour une entité.
    Permet d'ajouter/modifier des champs.
    """

    def __init__(self, master, entity_name, header, dev_mode=False):
        super().__init__(master)
        self.title(f"Édition de {entity_name}")
        self.geometry("1000x700")
        self.configure(bg=BG_DARK)
        self.minsize(800, 600)  # Taille minimale de la fenêtre

        self.entity_name = entity_name
        self.header = header
        self.dev_mode = dev_mode
        self.fields = []

        self._build_ui()
        self._load_data()

        # Sauvegarder les données quand la fenêtre est fermée
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _build_ui(self):
        # Frame pour le nom de l'entité
        name_frame = tk.Frame(self, bg=self["bg"])
        name_frame.pack(fill="x", pady=(PADDING, PADDING))

        name_label = tk.Label(
            name_frame,
            text="Nom de l'entité :",
            font=(FONT_FAMILY, FONT_SIZE_SUBTITLE),
            fg=TEXT_COLOR,
            bg=self["bg"],
        )
        name_label.pack(side="left", padx=(0, 10))

        self.name_entry = ttk.Entry(
            name_frame,
            width=30,
            font=(FONT_FAMILY, FONT_SIZE_SUBTITLE),
        )
        self.name_entry.pack(side="left")
        self.name_entry.insert(0, self.entity_name)

        # Section des champs
        fields_section = ttk.LabelFrame(
            self,
            text="Champs de l'entité",
            padding=(PADDING, PADDING),
            style="Custom.TLabelframe",
        )
        fields_section.pack(fill="both", expand=True, pady=(0, PADDING))

        self.fields_frame = create_scrollable_fields_frame(
            fields_section,
            bg_color=BG_LIGHT,
        )

        # Boutons d'action
        buttons_frame = tk.Frame(self, bg=self["bg"])
        buttons_frame.pack(fill="x", pady=(0, PADDING))

        # Bouton "Ajouter champ"
        add_btn = ttk.Button(
            buttons_frame,
            text="➕ Ajouter un champ",
            command=self._add_field,
            style="TButton",
        )
        add_btn.pack(side="left", padx=(0, 10))

        # Bouton dev
        if self.dev_mode:
            dev_btn = ttk.Button(
                buttons_frame,
                text="🧪 Pré-remplir pour test",
                command=self._auto_fill_fields,
                style="TButton",
            )
            dev_btn.pack(side="left")

    def _add_field(self):
        index = len(self.fields) + 1
        widgets = add_field(self.fields_frame, index=index)
        self.fields.append(widgets)
        self.fields_frame.set_fields_list(self.fields)

    def get_entity_data(self):
        """Retourne les données de l'entité pour la génération."""
        company_raw = self.header.get_company()
        project_raw = self.header.get_project()

        company_variants = generate_name_variants(company_raw)
        project_variants = generate_name_variants(project_raw)

        data = build_entity_data(self.entity_name, self.fields)
        data["company"] = company_variants
        data["project"] = project_variants

        return data

    def _save_data(self):
        """Sauvegarde les données de l'entité dans un fichier temporaire."""
        try:
            data = {
                "name": self.name_entry.get(),
                "fields": [],
            }

            for field in self.fields:
                try:
                    (
                        name_entry,
                        type_combobox,
                        comment_entry,
                        test_entry,
                        is_id,
                        nullable,
                        _,
                    ) = field
                    field_data = {
                        "name": name_entry.get(),
                        "type": type_combobox.get(),
                        "comment": comment_entry.get(),
                        "testValue": test_entry.get(),
                        "isId": is_id.get(),
                        "nullable": nullable.get(),
                    }
                    data["fields"].append(field_data)
                except tk.TclError:
                    # Ignorer les champs qui ont été détruits
                    continue

            # Créer le dossier temp s'il n'existe pas
            os.makedirs("temp", exist_ok=True)

            # Sauvegarder dans un fichier temporaire
            with open(f"temp/{self.entity_name}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des données : {e}")

    def _load_data(self):
        """Charge les données de l'entité depuis le fichier temporaire."""
        try:
            with open(f"temp/{self.entity_name}.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            # Mettre à jour le nom
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, data["name"])

            # Recréer les champs
            for field in data["fields"]:
                self._add_field()
                (
                    name_entry,
                    type_combobox,
                    comment_entry,
                    test_entry,
                    is_id,
                    nullable,
                    _,
                ) = self.fields[-1]
                name_entry.insert(0, field["name"])
                type_combobox.set(field["type"])
                comment_entry.insert(0, field["comment"])
                test_entry.insert(0, field["testValue"])
                is_id.set(field["isId"])
                nullable.set(field["nullable"])
        except FileNotFoundError:
            pass  # Pas de données sauvegardées

    def _on_closing(self):
        """Gère la fermeture de la fenêtre."""
        try:
            self._save_data()
        except Exception as e:
            print(f"Erreur lors de la fermeture de la fenêtre : {e}")
        self.destroy()

    def _auto_fill_fields(self):
        exemples = [
            ("id", "Long", "id de l'utilisateur", "42", True, False),
            ("name", "String", "nom complet", "Toto Bidule", False, False),
            ("mail", "String", "email principal", "toto@hexapi.dev", False, False),
            (
                "createdAt",
                "ZonedDateTime",
                "date de création",
                "2024-03-20T10:00:00Z",
                False,
                False,
            ),
            ("birthDate", "LocalDate", "date de naissance", "1990-01-01", False, False),
            (
                "lastLogin",
                "LocalDateTime",
                "dernière connexion",
                "2024-03-20T10:00:00",
                False,
                False,
            ),
            (
                "uuid",
                "UUID",
                "identifiant unique",
                "123e4567-e89b-12d3-a456-426614174000",
                False,
                False,
            ),
            ("balance", "BigDecimal", "solde du compte", "1234.56", False, True),
        ]

        for nom, type_, comment, test_value, is_id_value, nullable_value in exemples:
            self._add_field()
            name_entry, type_combobox, comment_entry, test_entry, is_id, nullable, _ = (
                self.fields[-1]
            )
            name_entry.insert(0, nom)
            type_combobox.set(type_)
            comment_entry.insert(0, comment)
            test_entry.insert(0, test_value)
            is_id.set(is_id_value)
            nullable.set(nullable_value)
