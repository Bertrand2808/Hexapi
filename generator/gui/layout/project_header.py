"""
En-tête du projet avec les champs de configuration.
"""

import tkinter as tk
from tkinter import ttk

from generator.gui.style import (
    BG_COLOR,
    BG_LIGHT,
    FONT_FAMILY,
    FONT_SIZE_LABEL,
    SECTION_SPACING,
    TEXT_COLOR,
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
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        fields = [
            ("Nom Entreprise", "company_name", "Ex: My Company"),
            ("Nom Projet", "project_name", "Ex: my-project"),
            ("Nom Package", "package_name", "Ex: com.mycompany.project"),
        ]

        for i, (label_text, field_name, placeholder) in enumerate(fields):
            wrapper = tk.Frame(self, bg=BG_LIGHT, padx=24, pady=16)
            wrapper.grid(
                row=i, column=0, sticky="ew", pady=(0, SECTION_SPACING), padx=0
            )
            wrapper.grid_columnconfigure(0, weight=1)

            label = tk.Label(
                wrapper,
                text=label_text,
                font=(FONT_FAMILY, FONT_SIZE_LABEL),
                fg=TEXT_COLOR,
                bg=BG_LIGHT,
            )
            label.grid(row=0, column=0, sticky="w", pady=(0, 8))

            entry = ttk.Entry(wrapper)
            entry.grid(row=1, column=0, sticky="ew")
            entry.insert(0, placeholder)
            entry.bind("<FocusIn>", lambda e, p=placeholder: self._on_focus_in(e, p))
            entry.bind("<FocusOut>", lambda e, p=placeholder: self._on_focus_out(e, p))
            setattr(self, field_name, entry)

    def _on_focus_in(self, event, placeholder):
        """Efface le placeholder quand le champ reçoit le focus."""
        if event.widget.get() == placeholder:
            event.widget.delete(0, "end")
            event.widget.configure(foreground=TEXT_COLOR)

    def _on_focus_out(self, event, placeholder):
        """Restaure le placeholder si le champ est vide."""
        if not event.widget.get():
            event.widget.insert(0, placeholder)
            event.widget.configure(foreground="gray")

    def get_company(self):
        """Retourne le nom de l'entreprise."""
        value = self.company_name.get()
        return value if value != "Ex: My Company" else ""

    def get_project(self):
        """Retourne le nom du projet."""
        value = self.project_name.get()
        return value if value != "Ex: my-project" else ""

    def get_package(self):
        """Retourne le nom du package."""
        value = self.package_name.get()
        return value if value != "Ex: com.mycompany.project" else ""
