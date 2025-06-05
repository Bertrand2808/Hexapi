"""
Module containing the ThemeManager class.

date: 05/06/2025
"""

from generator.core.config_manager import load_settings, save_settings
from generator.core.logger import logger
from generator.gui.style import THEMES, apply_style


class ThemeManager:
    """
    Class managing the theme of the application.
    """

    def __init__(self):
        """
        Initialize the ThemeManager.
        """
        settings = load_settings()
        self.current_theme = settings.get("theme", "light")
        self.subscribers = []

    def get(self, key):
        """
        Get the value of a theme key.
        """
        return THEMES[self.current_theme][key]

    def toggle_theme(self):
        """
        Toggle the theme.
        """
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        save_settings({"theme": self.current_theme})
        self._notify_subscribers()

    def subscribe(self, callback):
        """
        Subscribe to the theme change.
        """
        self.subscribers.append(callback)

    def unsubscribe(self, callback):
        """
        Unsubscribe from the theme change.
        """
        self.subscribers.remove(callback)

    def _notify_subscribers(self):
        """
        Notify the subscribers of the theme change.
        """
        for callback in self.subscribers:
            callback()


def notify_theme_change(root):
    """
    Notify the subscribers of the theme change.
    """
    apply_style(root)
    root.configure(bg=theme_manager.get("BG"))

    def refresh_recursively(widget):
        """
        Refresh the widget recursively.
        """
        try:
            if hasattr(widget, "apply_theme"):
                widget.apply_theme()
        except Exception as e:
            logger.warning("Theme refresh failed for %s: %s", widget, e)

        for child in widget.winfo_children():
            refresh_recursively(child)

    refresh_recursively(root)


# Singleton instance
theme_manager = ThemeManager()
