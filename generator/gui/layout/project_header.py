import tkinter as tk
from tkinter import ttk

FONT_FAMILY = "Segoe UI"
FONT_SIZE_LABEL = 11
BG_COLOR = "#2e2e3e"


class ProjectHeader(tk.Frame):
    """
    En-tête du projet contenant les champs globaux :
    - Nom de l'entreprise
    - Nom du projet

    Peut être réutilisé et interrogé pour obtenir les valeurs.
    """

    def __init__(self, parent):
        super().__init__(parent, bg=BG_COLOR, padx=10, pady=10)

        self.company_entry = ttk.Entry(
            self, width=25, font=(FONT_FAMILY, FONT_SIZE_LABEL)
        )
        self.project_entry = ttk.Entry(
            self, width=25, font=(FONT_FAMILY, FONT_SIZE_LABEL)
        )

        self._build_ui()

    def _build_ui(self):
        """Construit les widgets et leur placement."""

        label_entreprise = tk.Label(
            self,
            text="Nom Entreprise",
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            fg="white",
            bg=BG_COLOR,
        )
        label_entreprise.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.company_entry.grid(row=0, column=1, sticky="ew", padx=(0, 30))

        label_projet = tk.Label(
            self,
            text="Nom Projet",
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            fg="white",
            bg=BG_COLOR,
        )
        label_projet.grid(row=0, column=2, sticky="w", padx=(0, 10))
        self.project_entry.grid(row=0, column=3, sticky="ew")

        # Ajoute un poids aux colonnes pour élasticité
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)

    def get_company(self) -> str:
        """Retourne la valeur de l'entreprise (str)."""
        return self.company_entry.get().strip()

    def get_project(self) -> str:
        """Retourne la valeur du projet (str)."""
        return self.project_entry.get().strip()

    def set_company(self, value: str):
        self.company_entry.delete(0, tk.END)
        self.company_entry.insert(0, value)

    def set_project(self, value: str):
        self.project_entry.delete(0, tk.END)
        self.project_entry.insert(0, value)
