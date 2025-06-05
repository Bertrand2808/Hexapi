"""
Module containing the theme utils.

date: 05/06/2025
"""

import tkinter as tk
from tkinter import ttk

from generator.core.logger import logger
from generator.gui.theme_manager import theme_manager


def apply_theme_recursive(widget):
    """
    Apply the theme to the widget recursively.
    """
    try:
        # Appliquer sur le widget lui-même
        if isinstance(widget, tk.Frame) or isinstance(widget, tk.LabelFrame):
            widget.configure(bg=theme_manager.get("BG_BOX"))
        elif isinstance(widget, tk.Label):
            widget.configure(
                bg=theme_manager.get("BG_BOX"),
                fg=theme_manager.get("TEXT_COLOR"),
            )
        elif isinstance(widget, tk.Entry):
            widget.configure(
                fg=theme_manager.get("TEXT_COLOR"),
                insertbackground=theme_manager.get("TEXT_COLOR"),
            )
        elif isinstance(widget, tk.Canvas):
            widget.configure(bg=theme_manager.get("BG_BOX"))
        elif isinstance(widget, ttk.Entry):
            # nothing here, the style is managed via ttk.Style
            pass
        elif isinstance(widget, ttk.Button):
            pass
        elif isinstance(widget, tk.Scrollbar):
            widget.configure(bg=theme_manager.get("BG_BOX"))

        # Apply recursively on the children
        for child in widget.winfo_children():
            apply_theme_recursive(child)

    except Exception as e:
        logger.warning(f"Widget {widget} could not be themed: {e}")
