"""
Module containing the EntityEditorWindow class.

date: 05/06/2025
"""

import json
import os
import tkinter as tk
from tkinter import ttk

from generator.core.fake_utils import get_fake_value
from generator.core.logger import logger
from generator.gui.style import FONT_FAMILY, FONT_SIZE_LABEL, PADDING
from generator.gui.theme_manager import theme_manager
from generator.gui.utils.theme_utils import apply_theme_recursive
from generator.gui.widgets import add_field, create_scrollable_fields_frame


class EntityEditorWindow(tk.Toplevel):
    """
    Class representing the entity editor window.
    """

    def __init__(self, master, entity_name, on_name_change, dev_mode=False):
        """
        Initialize the entity editor window.
        """
        super().__init__(master)
        self.title(f"Édition - {entity_name}")
        self.geometry("1000x600")
        self.entity_name = entity_name
        self.on_name_change = on_name_change
        self.dev_mode = dev_mode
        self.fields = []
        self._name_changed = False
        self._theme_callback = self.apply_theme
        self._build_ui()
        self._load_data()
        self.apply_theme()
        theme_manager.subscribe(self._theme_callback)

        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def apply_theme(self):
        """
        Apply the theme to the entity editor.
        """
        if not self.winfo_exists():
            logger.warning("apply_theme() called on destroyed window")
            return
        logger.info("apply_theme() called on %s", self.entity_name)
        self.configure(bg=theme_manager.get("BG"))
        apply_theme_recursive(self)

    def _build_ui(self):
        """
        Build the UI of the entity editor.
        """
        main_container = tk.Frame(
            self,
            bg=theme_manager.get("BG_BOX"),
            padx=PADDING,
            pady=PADDING,
        )
        main_container.pack(fill="both", expand=True)

        # === Top row : entity name
        top_row = tk.Frame(main_container, bg=theme_manager.get("BG_BOX"))
        top_row.pack(fill="x", pady=(0, PADDING))

        name_label = tk.Label(
            top_row,
            text="Entity Name :",
            font=(FONT_FAMILY, FONT_SIZE_LABEL, "bold"),
            fg=theme_manager.get("TEXT_COLOR"),
            bg=theme_manager.get("BG_BOX"),
        )
        name_label.pack(side="left", padx=(0, 8))

        self.name_entry = ttk.Entry(
            top_row,
            width=30,
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            style="CleanDark.TEntry",
        )
        self.name_entry.insert(0, self.entity_name)
        self.name_entry.pack(side="left", fill="x", expand=True)

        # === Fields section
        fields_section = tk.LabelFrame(
            main_container,
            text="Fields",
            padx=PADDING,
            pady=PADDING,
            font=(FONT_FAMILY, FONT_SIZE_LABEL, "bold"),
            bg=theme_manager.get("BG_BOX"),
            fg=theme_manager.get("TEXT_COLOR"),
        )
        fields_section.pack(fill="both", expand=True, pady=(0, PADDING))

        self.fields_frame = create_scrollable_fields_frame(
            fields_section,
            bg_color=theme_manager.get("BG_BOX"),
            entity_name=self.entity_name,
        )

        # === Footer with buttons
        buttons_frame = tk.Frame(main_container, bg=theme_manager.get("BG_BOX"))
        buttons_frame.pack(fill="x", pady=(PADDING, 0))

        def add_auto_field():
            default_type = "String"
            field_data = {
                "name": "",
                "type": default_type,
                "comment": "",
                "test_value": get_fake_value(default_type),
                "is_id": False,
                "nullable": True,
            }
            add_field(self.fields_frame, field_data)

        ttk.Button(
            buttons_frame,
            text="➕ Add Field",
            command=add_auto_field,
            style="TButton",
            cursor="hand2",
        ).pack(side="left", padx=(0, 8))

        if self.dev_mode:
            ttk.Button(
                buttons_frame,
                text="[DEV] Generate auto",
                command=self._generate_fake_data,
                style="TButton",
                cursor="hand2",
            ).pack(side="left", padx=(0, 8))

        ttk.Button(
            buttons_frame,
            text="🧹 Clean",
            command=self._clear_fields,
            style="Red.TButton",
            cursor="hand2",
        ).pack(side="right", padx=(8, 0))

        ttk.Button(
            buttons_frame,
            text="✅ Validate",
            command=self._save_data,
            style="Green.TButton",
            cursor="hand2",
        ).pack(side="right")

    def _load_data(self):
        """
        Load the data from the JSON file.
        """
        json_path = f"temp/{self.entity_name}.json"
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for field_data in data:
                        add_field(self.fields_frame, field_data)
            except Exception as e:
                logger.error("Error loading JSON %s: %s", self.entity_name, e)

    def _save_data(self):
        """
        Save the data to the JSON file.
        """
        try:
            new_name = self.name_entry.get().strip()
            name_changed = new_name and new_name != self.entity_name
            old_name = self.entity_name
            if name_changed:
                self.entity_name = new_name

            fields_data = []
            for field_widget in self.fields_frame.winfo_children():
                if isinstance(field_widget, tk.Frame):
                    field_data = {
                        "name": field_widget.name_entry.get(),
                        "type": field_widget.type_combobox.get(),
                        "comment": field_widget.comment_entry.get(),
                        "test_value": field_widget.test_entry.get(),
                        "is_id": field_widget.is_id_var.get(),
                        "nullable": field_widget.nullable_var.get(),
                    }
                    fields_data.append(field_data)

            # Save in the new file first
            new_json_path = f"temp/{self.entity_name}.json"
            with open(new_json_path, "w", encoding="utf-8") as f:
                json.dump(fields_data, f, indent=2)

            # If the name has changed, delete the old file
            if name_changed:
                old_json_path = f"temp/{old_name}.json"
                if os.path.exists(old_json_path):
                    try:
                        os.remove(old_json_path)
                    except OSError as e:
                        logger.warning(
                            "Could not delete old file %s: %s",
                            old_json_path,
                            e,
                        )

            if name_changed and not self._name_changed:
                self._name_changed = True
                self.on_name_change(old_name, new_name)

            logger.info("Data saved for %s", self.entity_name)
            self.destroy()

        except Exception as e:
            logger.error("Error saving %s: %s", self.entity_name, e)

    def _on_closing(self):
        """
        Handle the closing event of the entity editor.
        """
        try:
            theme_manager.unsubscribe(self._theme_callback)
            if not hasattr(self, "_is_being_deleted"):
                self._save_data()
        except Exception as e:
            logger.error("Error closing %s: %s", self.entity_name, e)
        finally:
            self.destroy()

    def _clear_fields(self):
        """
        Clear the fields of the entity editor.
        """
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

    def _generate_fake_data(self):
        """
        Generate fake data for the entity editor.
        """
        self._clear_fields()

        # Create a custom modal dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Generate fake data")
        dialog.geometry("300x150")
        dialog.configure(bg=theme_manager.get("BG_BOX"))
        dialog.transient(self)  # Make the window stay on top of its parent
        dialog.grab_set()  # Make the window modal

        # Center the window
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        # Message
        message = tk.Label(
            dialog,
            text="Do you want to generate fake data?",
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            bg=theme_manager.get("BG_BOX"),
            fg=theme_manager.get("TEXT_COLOR"),
        )
        message.pack(pady=(20, 20))

        # Buttons
        buttons_frame = tk.Frame(dialog, bg=theme_manager.get("BG_BOX"))
        buttons_frame.pack(pady=(0, 20))

        def on_yes():
            dialog.destroy()
            fake_fields = [
                {
                    "name": "id",
                    "type": "Long",
                    "comment": "Unique ID",
                    "test_value": get_fake_value("Long"),
                    "is_id": True,
                    "nullable": False,
                },
                {
                    "name": "name",
                    "type": "String",
                    "comment": "Entity name",
                    "test_value": get_fake_value("String"),
                    "is_id": False,
                    "nullable": True,
                },
                {
                    "name": "description",
                    "type": "String",
                    "comment": "Entity description",
                    "test_value": get_fake_value("String"),
                    "is_id": False,
                    "nullable": True,
                },
                {
                    "name": "created_at",
                    "type": "LocalDateTime",
                    "comment": "Creation date",
                    "test_value": get_fake_value("LocalDateTime"),
                    "is_id": False,
                    "nullable": True,
                },
                {
                    "name": "updated_at",
                    "type": "LocalDateTime",
                    "comment": "Update date",
                    "test_value": get_fake_value("LocalDateTime"),
                    "is_id": False,
                    "nullable": True,
                },
            ]
            for field_data in fake_fields:
                add_field(self.fields_frame, field_data)

        def on_no():
            dialog.destroy()

        ttk.Button(
            buttons_frame,
            text="Yes",
            command=on_yes,
            style="Green.TButton",
            cursor="hand2",
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            buttons_frame, text="No", command=on_no, style="TButton", cursor="hand2"
        ).pack(side="left")

        # Wait for the window to be closed
        dialog.wait_window()
