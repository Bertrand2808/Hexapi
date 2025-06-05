"""
Module containing the menu bar for the main window of HexAPI Generator.

date: 05/06/2025
"""

import os
import platform
import subprocess
import tkinter as tk
import webbrowser
from tkinter import messagebox, scrolledtext

from generator.core.logger import LOG_DIR, logger
from generator.gui.style import get_current_theme
from generator.gui.theme_manager import notify_theme_change, theme_manager

FONT_FAMILY = "Segoe UI"


def create_menu_bar(root):
    """
    Create and attach the menu bar to the main window.
    """

    menu_bar = tk.Menu(
        root,
        bg="#2e2e3e",
        fg="#f0f0f0",
        activebackground="#3f3f5a",
        activeforeground="#ffffff",
        tearoff=0,
        bd=0,
        relief="flat",
        font=(FONT_FAMILY, 10),
    )
    root.config(menu=menu_bar)

    _add_file_menu(menu_bar)
    _add_preferences_menu(menu_bar, root)
    _add_help_menu(menu_bar)


def _add_file_menu(menu_bar):
    """
    Add the file menu to the menu bar.
    """
    file_menu = tk.Menu(
        menu_bar,
        bg="#2e2e3e",
        fg="#f0f0f0",
        activebackground="#3f3f5a",
        activeforeground="#ffffff",
        tearoff=0,
        bd=0,
        relief="flat",
        font=(FONT_FAMILY, 10),
    )
    file_menu.add_command(label="New", command=_new_project)
    file_menu.add_command(label="Open a JSON project...", command=_open_project)
    file_menu.add_command(label="Save", command=_save_project)
    file_menu.add_separator()
    file_menu.add_command(label="Quit", command=_quit_app)
    menu_bar.add_cascade(label="File", menu=file_menu)


def _add_help_menu(menu_bar):
    """
    Add the help menu to the menu bar.
    """
    help_menu = tk.Menu(
        menu_bar,
        bg="#2e2e3e",
        fg="#f0f0f0",
        activebackground="#3f3f5a",
        activeforeground="#ffffff",
        tearoff=0,
        bd=0,
        relief="flat",
        font=(FONT_FAMILY, 10),
    )
    help_menu.add_command(label="About", command=_show_about)
    help_menu.add_command(label="Roadmap", command=_show_roadmap)
    help_menu.add_separator()
    help_menu.add_command(label="Open the logs", command=_open_logs)
    help_menu.add_command(label="Open the documentation", command=_open_docs)
    help_menu.add_command(label="Open the GitHub", command=_open_github)
    menu_bar.add_cascade(label="Help", menu=help_menu)


def _add_preferences_menu(menu_bar, root):
    """
    Add the preferences menu to the menu bar.
    """
    pref_menu = tk.Menu(
        menu_bar,
        bg="#2e2e3e",
        fg="#f0f0f0",
        activebackground="#3f3f5a",
        activeforeground="#ffffff",
        tearoff=0,
        bd=0,
        relief="flat",
        font=(FONT_FAMILY, 10),
    )
    current_theme = get_current_theme()
    toggle_theme_label = (
        "Switch Dark/Light Mode"
        if current_theme == "light"
        else "Switch Light/Dark Mode"
    )
    pref_menu.add_command(
        label=toggle_theme_label, command=lambda: on_toggle_theme(root)
    )
    menu_bar.add_cascade(label="Preferences", menu=pref_menu)


def on_toggle_theme(root):
    """
    Toggle the theme.
    """
    theme_manager.toggle_theme()
    notify_theme_change(root)


# === Callbacks ===


def _new_project():
    """
    Create a new project.
    """
    logger.info("Creation of a new project")
    messagebox.showinfo(
        "Feature not available yet",
        "This feature will be available in a future update.",
    )


def _open_project():
    """
    Open an existing project.
    """
    logger.info("Opening an existing project")
    messagebox.showinfo(
        "Feature not available yet",
        "This feature will be available in a future update.",
    )


def _save_project():
    """
    Save the current project.
    """
    logger.info("Saving the current project")
    messagebox.showinfo(
        "Feature not available yet",
        "This feature will be available in a future update.",
    )


def _quit_app():
    """
    Quit the application.
    """
    logger.info("Closing the application")
    exit(0)


def _show_about():
    """
    Show the about information.
    """
    logger.info("Displaying the information about the application")
    messagebox.showinfo("About", "HexAPI Generator\nVersion 1.0\n© 2025 BertrandCorp")


def _open_docs():
    """
    Open the documentation.
    """
    logger.info("Opening the documentation")
    # webbrowser.open_new_tab("https://tonsite/docs")
    messagebox.showinfo(
        "Feature not available yet",
        "This feature will be available in a future update.",
    )


def _open_github():
    """
    Open the GitHub.
    """
    logger.info("Opening the GitHub")
    webbrowser.open_new_tab("https://github.com/Bertrand2808/Hexapi")


def _open_logs():
    """
    Open the logs.
    """
    logger.info("Opening the logs")
    logger.info("Opening the logs folder: %s", LOG_DIR)

    if os.path.exists(LOG_DIR):
        if platform.system() == "Windows":
            subprocess.Popen(f'explorer "{LOG_DIR}"')
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", LOG_DIR])
        elif platform.system() == "Linux":
            subprocess.Popen(["xdg-open", LOG_DIR])
        else:
            logger.error("Operating system not supported: %s", platform.system())
            messagebox.showerror(
                "Error",
                f"Unable to open the logs folder on {platform.system()}",
            )
    else:
        logger.error("The logs folder does not exist: %s", LOG_DIR)
        messagebox.showerror("Error", "The logs folder does not exist")


def _show_roadmap():
    """
    Show the roadmap in a popup window.
    """
    logger.info("Displaying the roadmap")

    # Create a new window
    roadmap_window = tk.Toplevel()
    roadmap_window.title("Roadmap")
    roadmap_window.geometry("600x400")
    roadmap_window.configure(bg=theme_manager.get("BG_BOX"))
    roadmap_window.transient(
        roadmap_window.master
    )  # Make window stay on top of its parent
    roadmap_window.grab_set()  # Make window modal

    # Create a text widget with a scrollbar
    text_widget = scrolledtext.ScrolledText(
        roadmap_window,
        wrap=tk.WORD,
        width=70,
        height=20,
        font=(FONT_FAMILY, 10),
        bg=theme_manager.get("BG_BOX"),
        fg=theme_manager.get("TEXT_COLOR"),
    )
    text_widget.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Read and display the content of the roadmap file
    try:
        with open("generator/config/roadmap.txt", "r", encoding="utf-8") as f:
            content = f.read()
            text_widget.insert(tk.END, content)
            text_widget.configure(state="disabled")  # Make the text read-only
    except Exception as e:
        logger.error("Error during the reading of the roadmap: %s", e)
        text_widget.insert(tk.END, "Error during the loading of the roadmap.")
        text_widget.configure(state="disabled")
