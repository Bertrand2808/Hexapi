"""
Module containing the style constants for the GUI.

date: 05/06/2025
"""

import tkinter as tk
from tkinter import ttk

from generator.core.config_manager import load_settings, save_settings

# === Couleurs ===
BG_DARK = "#ffffff"  # White background
BG_LIGHT = "#f5f5f5"  # Very light gray
BG_LIGHTER = "#ffffff"  # White for the fields
BG_HOVER = "#f0f0f0"  # Light gray on hover
BG_COLOR = BG_LIGHTER  # Background color for the widgets
BOX_COLOR = BG_LIGHT  # Background color for the entity boxes
LABELFRAME_BG = "#ffffff"  # Background color for the LabelFrame
ACCENT_COLOR = "#0066ff"  # Bright blue
ACCENT_HOVER = "#0052cc"  # Dark blue on hover
TEXT_COLOR = "#333333"  # Dark gray text
BORDER_COLOR = "#e0e0e0"  # Light gray border
HOVER_LIGHT = "#f8f9fa"
SUCCESS_COLOR = "#28a745"
ERROR_COLOR = "#dc3545"


THEMES = {
    "light": {
        "BG": "#ffffff",
        "BG_BOX": "#f5f5f5",
        "BG_INPUT": "#ffffff",
        "TEXT_COLOR": "#333333",
        "ACCENT_COLOR": "#0066ff",
        "ACCENT_HOVER": "#0052cc",
        "BORDER_COLOR": "#e0e0e0",
        "HOVER_LIGHT": "#f8f9fa",
        "SUCCESS_COLOR": "#28a745",
        "ERROR_COLOR": "#dc3545",
    },
    "dark": {
        "BG": "#19242B",
        "BG_BOX": "#252B30",
        "BG_INPUT": "#333A3F",
        "TEXT_COLOR": "#f5f5f5",
        "ACCENT_COLOR": "#3399ff",
        "ACCENT_HOVER": "#0077cc",
        "BORDER_COLOR": "#444444",
        "HOVER_LIGHT": "#252B30",
        "SUCCESS_COLOR": "#28a745",
        "ERROR_COLOR": "#dc3545",
    },
}

CURRENT_THEME = load_settings().get("theme", "light")

# === Polices ===
FONT_FAMILY = "Segoe UI"
FONT_SIZE_LABEL = 12
FONT_SIZE_TITLE = 24
FONT_SIZE_SUBTITLE = 18

# === Dimensions ===
PADDING = 24  # General padding increased
BORDER_RADIUS = 8
SHADOW_COLOR = "rgba(0, 0, 0, 0.1)"
BOX_SHADOW = "0 2px 8px rgba(0,0,0,0.1)"

# === Espacement ===
LABEL_ENTRY_SPACING = 8  # Spacing between label and field
SECTION_SPACING = 24  # Spacing between sections
BUTTON_SPACING = 12  # Spacing between buttons


def get_style(name):
    """
    Get the style for a given name.
    """
    return THEMES[CURRENT_THEME][name]


def switch_theme():
    """
    Switch the theme.
    """
    global CURRENT_THEME
    CURRENT_THEME = "dark" if CURRENT_THEME == "light" else "light"
    save_settings({"theme": CURRENT_THEME})


def get_current_theme():
    """
    Get the current theme.
    """
    return CURRENT_THEME


def apply_style(root):
    """
    Apply the theme and the custom styles to the Tkinter components.
    """
    from generator.gui.style import FONT_FAMILY, FONT_SIZE_LABEL
    from generator.gui.theme_manager import theme_manager

    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(
        ".",
        background=theme_manager.get("BG_BOX"),
        foreground=theme_manager.get("TEXT_COLOR"),
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
    )

    style.configure(
        "TEntry",
        fieldbackground=theme_manager.get("BG_INPUT"),
        foreground=theme_manager.get("TEXT_COLOR"),
        borderwidth=1,
        relief="solid",
        padding=12,
        bordercolor=theme_manager.get("BORDER_COLOR"),
    )

    style.configure(
        "Custom.TCombobox",
        fieldbackground=theme_manager.get("BG_INPUT"),
        background=theme_manager.get("BG_INPUT"),
        foreground=theme_manager.get("TEXT_COLOR"),
        arrowcolor=theme_manager.get("TEXT_COLOR"),
        bordercolor=theme_manager.get("BORDER_COLOR"),
        selectbackground=theme_manager.get("ACCENT_COLOR"),
        selectforeground="white",
        padding=12,
    )

    style.map(
        "Custom.TCombobox",
        fieldbackground=[("readonly", theme_manager.get("BG_INPUT"))],
        foreground=[("readonly", theme_manager.get("TEXT_COLOR"))],
        background=[("readonly", theme_manager.get("ACCENT_COLOR"))],
    )

    style.configure(
        "TButton",
        background=theme_manager.get("ACCENT_COLOR"),
        foreground="white",
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
        padding=12,
        borderwidth=0,
        relief="flat",
    )
    style.map("TButton", background=[("active", theme_manager.get("ACCENT_HOVER"))])

    style.configure(
        "Green.TButton",
        background=theme_manager.get("SUCCESS_COLOR"),
        foreground="white",
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
        padding=12,
        borderwidth=0,
        relief="flat",
    )
    style.map(
        "Green.TButton",
        background=[("active", theme_manager.get("SUCCESS_COLOR"))],
    )

    style.configure(
        "Red.TButton",
        background=theme_manager.get("ERROR_COLOR"),
        foreground="white",
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
        padding=12,
        borderwidth=0,
        relief="flat",
    )
    style.map("Red.TButton", background=[("active", theme_manager.get("ERROR_COLOR"))])

    style.configure(
        "CleanDark.TEntry",
        fieldbackground=theme_manager.get("BG_INPUT"),
        background=theme_manager.get("ACCENT_COLOR"),
        foreground=theme_manager.get("TEXT_COLOR"),
        relief="flat",
        borderwidth=0,
        padding=10,
        insertcolor=theme_manager.get("TEXT_COLOR"),
    )
    style.map(
        "CleanDark.TEntry",
        fieldbackground=[("active", theme_manager.get("BG_INPUT"))],
    )


def make_label(parent, text, size=FONT_SIZE_SUBTITLE, bold=False):
    """
    Create a styled label with the colors and fonts of the application.
    """
    font_weight = "bold" if bold else "normal"
    # Use BG_COLOR for the ttk widgets
    bg_color = BG_COLOR if isinstance(parent, ttk.Widget) else parent["bg"]
    return tk.Label(
        parent,
        text=text,
        font=(FONT_FAMILY, size, font_weight),
        fg=TEXT_COLOR,
        bg=bg_color,
    )
