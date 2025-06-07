"""
Module containing the main window.

date: 05/06/2025
"""

# === Imports ===
import json
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from generator.core.config_manager import load_settings, save_settings
from generator.core.logger import logger
from generator.gui.intro import show_intro_popup
from generator.gui.layout.entity_board import EntityBoard
from generator.gui.layout.entity_editor import EntityEditorWindow
from generator.gui.layout.project_header import ProjectHeader
from generator.gui.menubar import create_menu_bar
from generator.gui.style import FONT_FAMILY, FONT_SIZE_LABEL, PADDING, apply_style
from generator.gui.theme_manager import theme_manager
from generator.gui.widgets import load_icons
from generator.scripts.generate_entity import generate_all_templates

# === Constants ===
VERSION = "0.1.0"  # Version of the application
WINDOW_TITLE = "HexAPI Generator"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 700

ui_refs = {}  # References to the UI elements


def clean_folders():
    """
    Clean the temp and output folders.
    """
    temp_dir = "temp"
    output_dir = "output"
    if os.path.exists(temp_dir):
        logger.info("Cleaning temp folder: %s", temp_dir)
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    logger.info("Temp folder created: %s", temp_dir)

    if os.path.exists(output_dir):
        logger.info("Cleaning output folder: %s", output_dir)
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    logger.info("Output folder created: %s", output_dir)


def create_main_window():
    """
    Create and configure the main window.
    """
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.configure(bg=theme_manager.get("BG"))
    root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
    return root


def make_label(parent, text, size=FONT_SIZE_LABEL, bold=False):
    """
    Create a styled label with the colors and fonts of the application.
    """
    font_weight = "bold" if bold else "normal"
    return tk.Label(
        parent,
        text=text,
        font=(FONT_FAMILY, size, font_weight),
        fg=theme_manager.get("TEXT_COLOR"),
        bg=parent["bg"],
    )


def show_error_message(parent, message):
    """Display an error message in a dialog box."""
    logger.info("Displaying error message: %s", message)
    dialog = tk.Toplevel(parent)
    dialog.title("Error")
    dialog.geometry("500x200")
    dialog.configure(bg=theme_manager.get("BG_BOX"))
    dialog.transient(parent)
    dialog.grab_set()

    # Center the window
    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f"{width}x{height}+{x}+{y}")

    # Error message
    error_label = make_label(
        dialog,
        message,
        size=12,
        bold=True,
    )
    error_label.pack(pady=(30, 20))

    # OK button
    ok_btn = ttk.Button(
        dialog,
        text="OK",
        command=dialog.destroy,
        style="TButton",
    )
    ok_btn.pack()

    dialog.wait_window()


def setup_main_interface(root, dev_mode=False):
    """
    Setup the main interface.
    """

    entities_data = {}  # {entity_name: {fields: [field_data]}}
    entity_editors = {}  # {entity_name: EntityEditorWindow}

    # --- Internal functions (must be defined before use) ---
    def open_entity_editor(entity_name):
        logger.info("Opening editor for %s", entity_name)
        if entity_name in entity_editors:
            try:
                entity_editors[entity_name].lift()
                logger.info("Editor %s is already open, it is raised", entity_name)
                return
            except tk.TclError:
                logger.info("Editor %s is already open, it is closed", entity_name)
                del entity_editors[entity_name]

        editor = EntityEditorWindow(
            root,
            entity_name,
            on_name_change=update_entity_name,
            dev_mode=dev_mode,
        )
        entity_editors[entity_name] = editor

    def create_entity():
        """
        Create a new entity with a default name,
        then open the editor directly.
        """
        base_name = "NouvelleEntite"
        suffix = 1
        name = base_name

        # Generate a unique name
        while name in entities_data:
            name = f"{base_name}{suffix}"
            suffix += 1

        logger.info("Creating entity %s", name)
        entities_data[name] = []
        entity_board.add_entity(name)
        open_entity_editor(name)

    # Add a set to track the operations in progress
    operations_in_progress = set()

    def handle_delete_entity(entity_name):
        """
        Delete an entity and its associated resources.
        """
        operation_key = f"delete_{entity_name}"
        if operation_key in operations_in_progress:
            logger.info("Skipping recursive deletion of %s", entity_name)
            return

        operations_in_progress.add(operation_key)
        try:
            logger.info("Deleting entity %s", entity_name)

            # Close the editor if it is open
            if entity_name in entity_editors:
                try:
                    editor = entity_editors[entity_name]
                    editor._is_being_deleted = True  # Mark the editor as being deleted
                    editor.destroy()
                except tk.TclError:
                    pass  # The editor is already closed
                del entity_editors[entity_name]

            # Delete the entity data
            if entity_name in entities_data:
                del entities_data[entity_name]

            # Delete the temporary JSON file
            json_path = f"temp/{entity_name}.json"
            if os.path.exists(json_path):
                logger.info("Deleting temporary JSON file %s", json_path)
                try:
                    os.remove(json_path)
                except OSError as e:
                    logger.error("Error deleting JSON file: %s", e)

            # Delete the entity from the board
            if entity_name in entity_board.entities:
                entity_board.delete_entity(entity_name)
                logger.info("Entity %s deleted from board", entity_name)
        finally:
            operations_in_progress.remove(operation_key)

    def generate_all_entities():
        """
        Generate all entities.
        """
        logger.info("Generating all entities")
        company = header.get_company()
        project = header.get_project()
        package = header.get_package()
        if not company:
            show_error_message(root, "The company name cannot be empty")
            return
        if not project:
            show_error_message(root, "The project name cannot be empty")
            return

        # Check if entities are set
        if not entities_data:
            show_error_message(root, "No entities have been created yet")
            return

        # Ask the user to choose the output directory
        output_dir = filedialog.askdirectory(
            title="Choisir le dossier de destination",
            initialdir=os.path.abspath("output"),
        )

        if not output_dir:  # If the user cancels the selection
            return

        for entity_name, editor in list(entity_editors.items()):
            try:
                # Check if the editor still exists
                try:
                    editor.winfo_exists()
                except tk.TclError:
                    logger.info(
                        "Editor %s does not exist, deleting reference", entity_name
                    )
                    del entity_editors[entity_name]
                    continue

                # Get the data from the temporary JSON file
                json_path = f"temp/{entity_name}.json"
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Inject meta datas
                data = {
                    "company": {
                        "lowercase": company.lower(),
                        "uppercase": company.upper(),
                    },
                    "project": {
                        "lowercase": project.lower(),
                        "uppercase": project.upper(),
                    },
                    "package_name": package,
                    "table": entity_name.lower(),
                    "Table": entity_name[0].upper() + entity_name[1:],
                    "fields": data,
                }
                logger.info("Injecting meta datas for %s", entity_name)

                # Save the data
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)

                if not data:
                    show_error_message(
                        root,
                        f"The entity '{entity_name}' has no fields. "
                        "Please add at least one field before generating.",
                    )
                    logger.error("No data found for %s", entity_name)
                    return
                if not os.path.exists(json_path):
                    logger.error("File JSON not found for %s", entity_name)
                    continue
                logger.info("Generating templates for %s", entity_name)
                generate_all_templates(json_path=json_path, output_root=output_dir)
            except Exception as e:
                logger.error("Error generating %s: %s", entity_name, e)
                show_error_message(root, f"Error generating {entity_name}: {e}")
                return
        messagebox.showinfo(
            "Generation completed",
            f"All entities have been generated successfully in {output_dir}",
        )

    def update_entity_name(old_name, new_name):
        """
        Update the name of an entity.
        """
        operation_key = f"rename_{old_name}_{new_name}"
        if operation_key in operations_in_progress:
            logger.info("Skipping recursive update from %s to %s", old_name, new_name)
            return

        logger.info("Updating entity name from %s to %s", old_name, new_name)
        operations_in_progress.add(operation_key)

        try:
            if old_name in entity_editors:
                try:
                    editor = entity_editors.pop(old_name)
                    entity_editors[new_name] = editor
                    editor.entity_name = new_name
                    editor.title(f"Editing {new_name}")
                except tk.TclError:
                    if old_name in entity_editors:
                        del entity_editors[old_name]

            if old_name in entities_data:
                entities_data[new_name] = entities_data.pop(old_name)

            # Rename the JSON file if necessary
            old_json_path = f"temp/{old_name}.json"
            new_json_path = f"temp/{new_name}.json"
            if os.path.exists(old_json_path):
                os.rename(old_json_path, new_json_path)

            if old_name in entity_board.entities:
                box = entity_board.entities.pop(old_name)
                box.rename(new_name)
                entity_board.entities[new_name] = box

        finally:
            operations_in_progress.remove(operation_key)

    # --- Main layout ---
    main_container = tk.Frame(root, bg=theme_manager.get("ACCENT_COLOR"))
    print(main_container["bg"])
    main_container.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    main_container.grid_rowconfigure(0, weight=0)
    main_container.grid_rowconfigure(1, weight=1)
    main_container.grid_columnconfigure(0, weight=1)

    # Line for the title
    title_frame = tk.Frame(main_container, bg=theme_manager.get("BG"))
    title_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
    title_label = make_label(
        title_frame,
        "HexAPI Generator",
        size=12,
        bold=True,
    )
    title_label.pack(pady=(8, 0), anchor="center")

    # --- Top zone divided into 2 parts ---
    top_frame = tk.Frame(main_container, bg=theme_manager.get("BG"))
    top_frame.grid(row=1, column=0, sticky="nsew")
    top_frame.grid_rowconfigure(0, weight=1)
    top_frame.grid_columnconfigure(0, weight=0, minsize=420)
    top_frame.grid_columnconfigure(1, weight=2)

    # --- Left column : project header ---
    header = ProjectHeader(top_frame, width=360, height=400)
    header.grid(row=0, column=0, sticky="n", padx=(PADDING * 2, PADDING), pady=PADDING)
    header.grid_propagate(False)

    # --- Right column : entities ---
    entity_section_container = tk.Frame(
        top_frame,
        bg=theme_manager.get("BG_BOX"),
        padx=24,
        pady=24,
    )
    entity_section_container.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(PADDING, PADDING * 2),
        pady=PADDING,
    )
    entity_section_container.grid_rowconfigure(0, weight=1)
    entity_section_container.grid_columnconfigure(0, weight=1)

    entity_board = EntityBoard(
        entity_section_container,
        on_entity_click=open_entity_editor,
        on_add_entity=create_entity,
        on_entity_delete=handle_delete_entity,
    )
    entity_board.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

    # --- Bottom zone : generation button and version (fixed) ---
    bottom_frame = tk.Frame(main_container, bg=theme_manager.get("BG"))
    bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
    bottom_frame.grid_columnconfigure(0, weight=1)  # Pour centrer le contenu

    # Container for the button and the version
    bottom_content = tk.Frame(bottom_frame, bg=theme_manager.get("BG"))
    bottom_content.pack(pady=(20, 10))

    generate_btn = ttk.Button(
        bottom_content,
        text="🚀 Generate all entities",
        command=generate_all_entities,
        style="TButton",
    )
    generate_btn.pack(pady=(0, 8))

    version_label = make_label(
        bottom_content,
        f"Version {VERSION}",
        size=10,
    )
    version_label.pack()

    # Injection of the callbacks in entity_board
    entity_board.update_entity_name = update_entity_name
    entity_board.handle_delete_entity = handle_delete_entity

    ui_refs["main_container"] = main_container
    ui_refs["title_frame"] = title_frame
    ui_refs["top_frame"] = top_frame
    ui_refs["bottom_frame"] = bottom_frame
    ui_refs["bottom_content"] = bottom_content
    ui_refs["entity_section_container"] = entity_section_container
    ui_refs["entity_board"] = entity_board
    ui_refs["header"] = header
    ui_refs["title_label"] = title_label
    ui_refs["generate_btn"] = generate_btn
    ui_refs["version_label"] = version_label


def main():
    """
    Main function.
    """
    logger.info("Starting application")
    clean_folders()
    root = create_main_window()
    apply_style(root)
    load_icons()
    settings = load_settings()
    if settings.get("first_launch"):
        show_intro_popup(root)
        settings["first_launch"] = False
        save_settings(settings)
    setup_main_interface(root, dev_mode=True)

    def on_theme_change():
        """
        Apply the theme to the main window.
        """
        apply_style(root)
        root.configure(bg=theme_manager.get("BG"))

        for key, widget in ui_refs.items():
            if widget:
                try:
                    if key == "entity_section_container":
                        widget.configure(bg=theme_manager.get("BG_BOX"))
                    elif key == "main_container":
                        widget.configure(bg=theme_manager.get("ACCENT_COLOR"))
                    elif isinstance(widget, (tk.Frame, tk.Label, tk.Toplevel)):
                        widget.configure(bg=theme_manager.get("BG"))
                except Exception as e:
                    logger.warning("Theme refresh failed for %s: %s", key, e)

        # Update the colors of the specific labels
        if "title_label" in ui_refs:
            ui_refs["title_label"].configure(
                bg=theme_manager.get("BG"), fg=theme_manager.get("TEXT_COLOR")
            )
        if "version_label" in ui_refs:
            ui_refs["version_label"].configure(
                bg=theme_manager.get("BG"), fg=theme_manager.get("TEXT_COLOR")
            )

        def refresh_recursively(widget):
            """
            Refresh the widget recursively.
            """
            try:
                if hasattr(widget, "apply_theme"):
                    widget.apply_theme()
                elif isinstance(widget, tk.Entry):
                    widget.configure(style="CleanDark.TEntry")
            except Exception as e:
                logger.warning("Theme refresh failed for %s: %s", widget, e)
            for child in widget.winfo_children():
                refresh_recursively(child)

        refresh_recursively(root)

    theme_manager.subscribe(on_theme_change)

    # Create the menu after the subscription
    create_menu_bar(root)

    root.mainloop()
    logger.info("Stopping application")
