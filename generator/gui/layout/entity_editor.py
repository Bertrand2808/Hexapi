import json
import os
import tkinter as tk
from tkinter import ttk

from generator.core.logger import logger
from generator.core.naming import generate_name_variants
from generator.gui.style import (
    BG_DARK,
    BG_LIGHT,
    FONT_FAMILY,
    FONT_SIZE_LABEL,
    FONT_SIZE_SUBTITLE,
    PADDING,
    TEXT_COLOR,
)
from generator.gui.widgets import add_field, create_scrollable_fields_frame


class EntityEditorWindow(tk.Toplevel):
    """
    Fenêtre d'édition pour une entité.
    Permet d'ajouter/modifier des champs.
    """

    def __init__(self, master, entity_name, header, dev_mode=False):
        logger.info("Création de la fenêtre d'édition pour %s", entity_name)
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
        logger.info("Fenêtre d'édition pour %s créée", entity_name)

    def _build_ui(self):
        logger.info("Construction de l'interface utilisateur pour %s", self.entity_name)

        # Container principal avec padding
        main_container = tk.Frame(self, bg=self["bg"], padx=PADDING, pady=PADDING)
        main_container.pack(fill="both", expand=True)

        # Section des métadonnées
        metadata_section = ttk.LabelFrame(
            main_container,
            text="Métadonnées de l'entité",
            padding=(PADDING, PADDING),
            style="Custom.TLabelframe",
        )
        metadata_section.pack(fill="x", pady=(0, PADDING))

        # Frame pour le nom de l'entité
        name_frame = tk.Frame(metadata_section, bg=BG_LIGHT)
        name_frame.pack(fill="x", pady=(0, PADDING))

        name_label = tk.Label(
            name_frame,
            text="Nom de l'entité",
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            fg=TEXT_COLOR,
            bg=BG_LIGHT,
        )
        name_label.pack(anchor="w", pady=(0, 4))

        self.name_entry = ttk.Entry(
            name_frame,
            width=30,
            font=(FONT_FAMILY, FONT_SIZE_SUBTITLE),
        )
        self.name_entry.pack(fill="x")
        self.name_entry.insert(0, self.entity_name)

        # Section des champs
        fields_section = ttk.LabelFrame(
            main_container,
            text="Champs de l'entité",
            padding=(PADDING, PADDING),
            style="Custom.TLabelframe",
        )
        fields_section.pack(fill="both", expand=True, pady=(0, PADDING))

        self.fields_frame = create_scrollable_fields_frame(
            fields_section,
            bg_color=BG_LIGHT,
            entity_name=self.entity_name,
        )

        # Boutons d'action
        buttons_frame = tk.Frame(main_container, bg=self["bg"])
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
                style="Red.TButton",
            )
            dev_btn.pack(side="left")

        # Bouton OK
        ok_btn = ttk.Button(
            buttons_frame,
            text="✅ Valider",
            command=self._on_closing,
            style="Green.TButton",
        )
        ok_btn.pack(side="right", padx=(0, 10))

        # Bouton Clean
        clean_btn = ttk.Button(
            buttons_frame,
            text="🧹 Nettoyer",
            command=self._clean_fields,
            style="Red.TButton",
        )
        clean_btn.pack(side="right", padx=(0, 10))

    def _add_field(self):
        logger.info("Ajout d'un champ pour %s", self.entity_name)
        index = len(self.fields) + 1
        widgets = add_field(self.fields_frame, index=index)
        self.fields.append(widgets)
        self.fields_frame.set_fields_list(self.fields)

    def _clean_fields(self):
        """Nettoie les champs de l'entité."""
        logger.info("Nettoyage des champs pour %s", self.entity_name)
        for widgets in self.fields:
            row = widgets[-1]
            row.destroy()
        self.fields = []
        self.fields_frame.set_fields_list([])

    def get_entity_data(self):
        """Retourne les données de l'entité pour la génération."""
        logger.info("Récupération des données de l'entité pour %s", self.entity_name)
        try:
            company_raw = self.header.get_company()
            project_raw = self.header.get_project()
            package_name = self.header.get_package()
            logger.info(
                "Entreprise: %s, Projet: %s, Package: %s",
                company_raw,
                project_raw,
                package_name,
            )

            company_variants = generate_name_variants(company_raw)
            project_variants = generate_name_variants(project_raw)
            entity_variants = generate_name_variants(self.name_entry.get().strip())
            logger.info("Variantes entreprise: %s", company_variants)
            logger.info("Variantes projet: %s", project_variants)
            logger.info("Variantes entité: %s", entity_variants)

            data = {
                "name": self.name_entry.get().strip(),
                "fields": [],
                "company": company_variants,
                "project": project_variants,
                "table": entity_variants["lowercase"],
                "Table": entity_variants["PascalCase"],
                "package_name": package_name,
            }
            logger.info("Structure de base créée pour %s", self.entity_name)

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
                        "name": name_entry.get().strip(),
                        "type": type_combobox.get().strip(),
                        "comment": comment_entry.get().strip(),
                        "testValue": test_entry.get().strip(),
                        "isId": is_id.get(),
                        "nullable": nullable.get(),
                    }
                    logger.info("Champ ajouté: %s", field_data)
                    data["fields"].append(field_data)
                except tk.TclError as e:
                    logger.error("Erreur TclError sur un champ: %s", e)
                    continue
                except Exception as e:
                    logger.error("Erreur inattendue sur un champ: %s", e)
                    continue

            logger.info("Données complètes générées pour %s", self.entity_name)
            return data
        except Exception as e:
            logger.error("Erreur dans get_entity_data: %s", e)
            raise

    def _save_data(self):
        """Sauvegarde les données de l'entité dans un fichier temporaire."""
        logger.info("Saving entity data for %s", self.entity_name)
        try:
            data = self.get_entity_data()

            # Créer le dossier temp s'il n'existe pas
            logger.info("Creating temp directory for %s", self.entity_name)
            os.makedirs("temp", exist_ok=True)

            # Sauvegarder dans un fichier temporaire
            logger.info(
                "Saving data in a temporary file for %s",
                self.entity_name,
            )
            with open(f"temp/{self.entity_name}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error("Error saving data: %s", e)

    def _load_data(self):
        """Charge les données de l'entité depuis le fichier temporaire."""
        logger.info("Loading entity data for %s", self.entity_name)
        try:
            with open(f"temp/{self.entity_name}.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            # Mettre à jour le nom
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, data["name"])
            logger.info("Entity name updated for %s", self.entity_name)

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
        logger.info("Fermeture de la fenêtre pour %s", self.entity_name)
        try:
            # Vérifier que le nom de l'entité n'est pas vide
            entity_name = self.name_entry.get().strip()
            if not entity_name:
                from generator.gui.main import show_error_message

                show_error_message(self, "The entity name cannot be empty")
                return

            # Vérifier que tous les champs ont un nom
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
                    if not name_entry.get().strip():
                        from generator.gui.main import show_error_message

                        show_error_message(self, "All fields must have a name")
                        return
                    if not nullable.get() and not test_entry.get().strip():
                        from generator.gui.main import show_error_message

                        msg = f"The field '{name_entry.get()}' cannot be empty"
                        show_error_message(self, msg)
                        return
                except tk.TclError:
                    continue

            self._save_data()
        except Exception as e:
            logger.error("Error closing window: %s", e)
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
        logger.info("Pré-remplissage des champs pour %s", self.entity_name)

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
