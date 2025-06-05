"""
Module containing the ConfigManager class.

date: 05/06/2025
"""

import json
import os

SETTINGS_FILE = "generator/config/settings.json"


def load_settings():
    """
    Load the settings from the settings file.
    """
    if not os.path.exists(SETTINGS_FILE):
        return {"theme": "light"}
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_settings(settings):
    """
    Save the settings to the settings file.
    """
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
