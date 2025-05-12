"""
Constantes de style pour l'interface graphique.
"""

import tkinter as tk
from tkinter import ttk

# === Couleurs ===
BG_DARK = "#1e1e2e"
BG_LIGHT = "#2e2e3e"
BG_LIGHTER = "#3e3e4e"
BG_HOVER = "#2b2b3f"
BG_COLOR = BG_LIGHTER  # Couleur de fond pour les widgets
BOX_COLOR = BG_LIGHT  # Couleur des boîtes d'entités
LABELFRAME_BG = "#45455a"  # Couleur de fond pour les LabelFrame
ACCENT_COLOR = "#7289da"
ACCENT_HOVER = "#677bc4"
TEXT_COLOR = "#f0f0f0"
BORDER_COLOR = "#5e5e6e"  # Bordure plus claire pour plus de contraste
HOVER_LIGHT = "#3d3d5c"
SUCCESS_COLOR = "#43b581"
ERROR_COLOR = "#f04747"

# === Polices ===
FONT_FAMILY = "Segoe UI"
FONT_SIZE_LABEL = 10
FONT_SIZE_TITLE = 16
FONT_SIZE_SUBTITLE = 18

# === Dimensions ===
PADDING = 20  # Augmentation du padding général
BORDER_RADIUS = 6
SHADOW_COLOR = "rgba(0, 0, 0, 0.15)"
BOX_SHADOW = "0 2px 8px rgba(0,0,0,0.15)"

# === Espacement ===
LABEL_ENTRY_SPACING = 5  # Espacement entre label et champ
SECTION_SPACING = 20  # Espacement entre les sections
BUTTON_SPACING = 10  # Espacement entre les boutons


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
