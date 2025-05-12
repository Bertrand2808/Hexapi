"""
En-tête du projet avec les champs de configuration.
"""

import tkinter as tk
from tkinter import ttk

from generator.core.logger import logger
from generator.gui.style import (
    BG_COLOR,
    FONT_FAMILY,
    FONT_SIZE_LABEL,
    FONT_SIZE_TITLE,
    LABEL_ENTRY_SPACING,
    PADDING,
    SECTION_SPACING,
    TEXT_COLOR,
    make_label,
)


class ProjectHeader(tk.Frame):
    """En-tête du projet avec les champs de configuration."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=BG_COLOR, **kwargs)
        # Initialiser les attributs pour éviter les erreurs de linter
        self.project_name = None
        self.company_name = None
        self.package_name = None
        self._build_ui()

    def _build_ui(self):
        """Construit l'interface utilisateur."""
        # Titre
        title = make_label(
            self, "Project configuration", size=FONT_SIZE_TITLE, bold=True
        )
        title.pack(pady=(0, SECTION_SPACING))

        # Groupe 1 : Informations du projet
        project_group = tk.Frame(self, bg=BG_COLOR)
        project_group.pack(fill="x", pady=(0, SECTION_SPACING))

        group_title = make_label(
            project_group, "Project informations", size=FONT_SIZE_LABEL, bold=True
        )
        group_title.pack(anchor="w", pady=(0, LABEL_ENTRY_SPACING))

        # Champs de configuration du projet
        fields = [
            ("Project name", "project_name", "Ex: my-project"),
            ("Company name", "company_name", "Ex: My Company"),
        ]

        for label_text, field_name, placeholder in fields:
            field_frame = tk.Frame(project_group, bg=BG_COLOR)
            field_frame.pack(fill="x", pady=(0, SECTION_SPACING))

            label = tk.Label(
                field_frame,
                text=label_text,
                font=(FONT_FAMILY, FONT_SIZE_LABEL),
                fg=TEXT_COLOR,
                bg=BG_COLOR,
            )
            label.pack(anchor="w", pady=(0, LABEL_ENTRY_SPACING))

            # Frame intermédiaire pour le padding horizontal
            entry_frame = tk.Frame(field_frame, bg=BG_COLOR)
            entry_frame.pack(fill="x", padx=PADDING)

            entry = ttk.Entry(entry_frame, width=40)
            entry.pack(fill="x")
            entry.insert(0, placeholder)
            entry.bind("<FocusIn>", lambda e, p=placeholder: self._on_focus_in(e, p))
            entry.bind("<FocusOut>", lambda e, p=placeholder: self._on_focus_out(e, p))
            setattr(self, field_name, entry)

        # Séparateur
        separator = ttk.Separator(self, orient="horizontal")
        separator.pack(fill="x", pady=SECTION_SPACING)

        # Groupe 2 : Configuration technique
        tech_group = tk.Frame(self, bg=BG_COLOR)
        tech_group.pack(fill="x")

        group_title = make_label(
            tech_group, "Technical configuration", size=FONT_SIZE_LABEL, bold=True
        )
        group_title.pack(anchor="w", pady=(0, LABEL_ENTRY_SPACING))

        # Champ package
        field_frame = tk.Frame(tech_group, bg=BG_COLOR)
        field_frame.pack(fill="x", pady=(0, SECTION_SPACING))

        label = tk.Label(
            field_frame,
            text="Package name",
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            fg=TEXT_COLOR,
            bg=BG_COLOR,
        )
        label.pack(anchor="w", pady=(0, LABEL_ENTRY_SPACING))

        # Frame intermédiaire pour le padding horizontal
        entry_frame = tk.Frame(field_frame, bg=BG_COLOR)
        entry_frame.pack(fill="x", padx=PADDING)

        entry = ttk.Entry(entry_frame, width=40)
        entry.pack(fill="x")
        entry.insert(0, "Ex: com.mycompany.project")
        placeholder = "Ex: com.mycompany.project"
        entry.bind("<FocusIn>", lambda e, p=placeholder: self._on_focus_in(e, p))
        entry.bind("<FocusOut>", lambda e, p=placeholder: self._on_focus_out(e, p))
        self.package_name = entry

    def _on_focus_in(self, event, placeholder):
        """Gère l'événement de focus sur un champ."""
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)

    def _on_focus_out(self, event, placeholder):
        """Gère l'événement de perte de focus sur un champ."""
        if not event.widget.get():
            event.widget.insert(0, placeholder)

    def get_values(self):
        """Récupère les valeurs des champs."""
        return {
            "project_name": self.project_name.get(),
            "company_name": self.company_name.get(),
            "package_name": self.package_name.get(),
        }

    def get_company(self) -> str:
        """Retourne la valeur de l'entreprise (str)."""
        logger.info("Récupération de la valeur de l'entreprise")
        value = self.company_name.get().strip()
        return "" if value in ["Ex: My Company"] else value

    def get_project(self) -> str:
        """Retourne la valeur du projet (str)."""
        logger.info("Récupération de la valeur du projet")
        value = self.project_name.get().strip()
        return "" if value in ["Ex: my-project"] else value

    def set_company(self, value: str):
        logger.info("Mise à jour de la valeur de l'entreprise")
        self.company_name.delete(0, tk.END)
        self.company_name.insert(0, value or "Ex: My Company")

    def set_project(self, value: str):
        logger.info("Mise à jour de la valeur du projet")
        self.project_name.delete(0, tk.END)
        self.project_name.insert(0, value or "Ex: my-project")

    def get_package(self) -> str:
        """Retourne la valeur du package (str)."""
        logger.info("Récupération de la valeur du package")
        value = self.package_name.get().strip()
        return "" if value in ["Ex: com.mycompany.project"] else value

    def set_package(self, value: str):
        logger.info("Mise à jour de la valeur du package")
        self.package_name.delete(0, tk.END)
        self.package_name.insert(0, value or "Ex: com.mycompany.project")
