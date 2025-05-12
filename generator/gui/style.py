"""
Constantes de style pour l'interface graphique.
"""

import tkinter as tk
from tkinter import ttk

# === Couleurs ===
BG_DARK = "#ffffff"  # Fond blanc
BG_LIGHT = "#f5f5f5"  # Gris très clair
BG_LIGHTER = "#ffffff"  # Blanc pour les champs
BG_HOVER = "#f0f0f0"  # Gris clair au survol
BG_COLOR = BG_LIGHTER  # Couleur de fond pour les widgets
BOX_COLOR = BG_LIGHT  # Couleur des boîtes d'entités
LABELFRAME_BG = "#ffffff"  # Couleur de fond pour les LabelFrame
ACCENT_COLOR = "#0066ff"  # Bleu vif
ACCENT_HOVER = "#0052cc"  # Bleu plus foncé au survol
TEXT_COLOR = "#333333"  # Texte gris foncé
BORDER_COLOR = "#e0e0e0"  # Bordure gris clair
HOVER_LIGHT = "#f8f9fa"
SUCCESS_COLOR = "#28a745"
ERROR_COLOR = "#dc3545"

# === Polices ===
FONT_FAMILY = "Segoe UI"
FONT_SIZE_LABEL = 12
FONT_SIZE_TITLE = 24
FONT_SIZE_SUBTITLE = 18

# === Dimensions ===
PADDING = 24  # Padding général augmenté
BORDER_RADIUS = 8
SHADOW_COLOR = "rgba(0, 0, 0, 0.1)"
BOX_SHADOW = "0 2px 8px rgba(0,0,0,0.1)"

# === Espacement ===
LABEL_ENTRY_SPACING = 8  # Espacement entre label et champ
SECTION_SPACING = 24  # Espacement entre les sections
BUTTON_SPACING = 12  # Espacement entre les boutons


def make_label(parent, text, size=FONT_SIZE_SUBTITLE, bold=False):
    """Crée un label stylisé avec les couleurs et polices de l'application."""
    font_weight = "bold" if bold else "normal"
    # Utiliser BG_COLOR pour les widgets ttk
    bg_color = BG_COLOR if isinstance(parent, ttk.Widget) else parent["bg"]
    return tk.Label(
        parent,
        text=text,
        font=(FONT_FAMILY, size, font_weight),
        fg=TEXT_COLOR,
        bg=bg_color,
    )
