import json
import os
import tkinter as tk
from tkinter import ttk

from generator.core.fake_utils import get_fake_value
from generator.core.logger import logger
from generator.gui.style import (
    BG_DARK,
    BG_LIGHT,
    FONT_FAMILY,
    FONT_SIZE_LABEL,
    PADDING,
    TEXT_COLOR,
)
from generator.gui.widgets import add_field, create_scrollable_fields_frame


class EntityEditorWindow(tk.Toplevel):
    """
    Fenêtre d'édition pour une entité.
    Permet d'ajouter/modifier des champs.
    """

    def __init__(self, master, entity_name, on_name_change, dev_mode=False):
        logger.info("Création de la fenêtre d'édition pour %s", entity_name)
        super().__init__(master)
        self.title(f"Édition - {entity_name}")
        self.geometry("1000x600")
        self.configure(bg=BG_DARK)
        self._name_changed = False
        self.entity_name = entity_name
        self.on_name_change = on_name_change
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

        # Section Nom Entité en ligne
        top_row = tk.Frame(main_container, bg=self["bg"])
        top_row.pack(fill="x", pady=(0, PADDING))

        name_label = tk.Label(
            top_row,
            text="Nom Entité :",
            font=(FONT_FAMILY, FONT_SIZE_LABEL, "bold"),
            fg=TEXT_COLOR,
            bg=self["bg"],
        )
        name_label.pack(side="left", padx=(0, 8))

        self.name_entry = ttk.Entry(
            top_row,
            width=30,
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
        )
        self.name_entry.pack(side="left", fill="x", expand=True)
        self.name_entry.insert(0, self.entity_name)

        # Section des champs
        fields_section = tk.LabelFrame(
            main_container,
            text="Champs",
            padx=PADDING,
            pady=PADDING,
            bg=BG_LIGHT,
            font=(FONT_FAMILY, FONT_SIZE_LABEL, "bold"),
        )
        fields_section.pack(fill="both", expand=True, pady=(0, PADDING))

        # Frame scrollable pour les champs
        self.fields_frame = create_scrollable_fields_frame(
            fields_section,
            bg_color=BG_LIGHT,
            entity_name=self.entity_name,
        )

        buttons_frame = tk.Frame(main_container, bg=self["bg"])
        buttons_frame.pack(fill="x", pady=(PADDING, 0))

        def add_auto_field():
            default_type = "String"
            field_data = {
                "name": "",
                "type": default_type,
                "comment": "",
                "test_value": get_fake_value(default_type),
                "is_id": False,
                "nullable": True,
            }
            add_field(self.fields_frame, field_data)

        # Ajouter Entité (icône + texte)
        add_field_btn = ttk.Button(
            buttons_frame,
            text="➕ Add Field",
            command=add_auto_field,
            style="TButton",
            cursor="hand2",
        )
        add_field_btn.pack(side="left", padx=(0, 8))

        # Géné auto
        if self.dev_mode:
            generate_btn = ttk.Button(
                buttons_frame,
                text="[DEV] Générer auto",
                style="TButton",
                cursor="hand2",
                command=self._generate_fake_data,
            )
            generate_btn.pack(side="left", padx=(0, 8))

        # Nettoyer
        clear_btn = ttk.Button(
            buttons_frame,
            text="🧹 Nettoyer",
            command=lambda: self._clear_fields(),
            style="Red.TButton",
            cursor="hand2",
        )
        clear_btn.pack(side="right", padx=(8, 0))

        # Valider
        validate_btn = ttk.Button(
            buttons_frame,
            text="✅ Valider",
            command=self._save_data,
            style="Green.TButton",
            cursor="hand2",
        )
        validate_btn.pack(side="right")

    def _load_data(self):
        """Charge les données de l'entité depuis le fichier JSON."""
        json_path = f"temp/{self.entity_name}.json"
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for field_data in data:
                        add_field(self.fields_frame, field_data)
            except Exception as e:
                logger.error("Erreur lors du chargement des données: %s", e)

    def _save_data(self):
        """Sauvegarde les données de l'entité dans un fichier JSON."""
        try:
            # Récupérer le nom de l'entité
            new_name = self.name_entry.get().strip()
            # Vérifie si le nom a changé
            name_changed = new_name and new_name != self.entity_name
            old_name = self.entity_name
            if name_changed:
                # On change tout de suite pour éviter conflits de fichiers
                self.entity_name = new_name

            # Récupérer les données des champs
            fields_data = []
            for field_widget in self.fields_frame.winfo_children():
                if isinstance(field_widget, tk.Frame):
                    field_data = {
                        "name": field_widget.name_entry.get(),
                        "type": field_widget.type_combobox.get(),
                        "comment": field_widget.comment_entry.get(),
                        "test_value": field_widget.test_entry.get(),
                        "is_id": field_widget.is_id_var.get(),
                        "nullable": field_widget.nullable_var.get(),
                    }
                    fields_data.append(field_data)

            # Sauvegarder dans un fichier JSON
            json_path = f"temp/{self.entity_name}.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(fields_data, f, indent=2)

            if name_changed and not self._name_changed:
                self._name_changed = True
                self.on_name_change(old_name, new_name)

            logger.info("Données sauvegardées pour %s", self.entity_name)
            self.destroy()

        except Exception as e:
            logger.error("Erreur lors de la sauvegarde des données: %s", e)

    def _on_closing(self):
        """Appelé quand la fenêtre est fermée."""
        try:
            if not hasattr(self, "_is_being_deleted"):
                self._save_data()
        except Exception as e:
            logger.error("Erreur lors de la fermeture: %s", e)
        finally:
            self.destroy()

    def _clear_fields(self):
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

    def _generate_fake_data(self):
        """Génère des données fake pour les champs."""
        self._clear_fields()
        from generator.core.fake_utils import get_fake_value

        fake_fields = [
            {
                "name": "id",
                "type": "Long",
                "comment": "ID unique",
                "test_value": get_fake_value("Long"),
                "is_id": True,
                "nullable": False,
            },
            {
                "name": "name",
                "type": "String",
                "comment": "Nom de l'entité",
                "test_value": get_fake_value("String"),
                "is_id": False,
                "nullable": True,
            },
            {
                "name": "description",
                "type": "String",
                "comment": "Description de l'entité",
                "test_value": get_fake_value("String"),
                "is_id": False,
                "nullable": True,
            },
            {
                "name": "created_at",
                "type": "LocalDateTime",
                "comment": "Date de création",
                "test_value": get_fake_value("LocalDateTime"),
                "is_id": False,
                "nullable": True,
            },
            {
                "name": "updated_at",
                "type": "LocalDateTime",
                "comment": "Date de mise à jour",
                "test_value": get_fake_value("LocalDateTime"),
                "is_id": False,
                "nullable": True,
            },
        ]
        for field_data in fake_fields:
            add_field(self.fields_frame, field_data)
