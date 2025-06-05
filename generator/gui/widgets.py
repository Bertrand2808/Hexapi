"""
Module containing the widgets for the GUI.

date: 05/06/2025
"""

import os
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from generator.core.fake_utils import get_fake_value
from generator.gui.style import FONT_FAMILY, FONT_SIZE_LABEL, SECTION_SPACING
from generator.gui.theme_manager import theme_manager

DELETE_ICON = None


def load_icons():
    """
    Load the icons.
    """
    global DELETE_ICON
    path = os.path.join("generator", "assets", "icons", "delete_light_mode.png")
    img = Image.open(path)
    img = img.resize((18, 18), Image.Resampling.LANCZOS)
    DELETE_ICON = ImageTk.PhotoImage(img)


def create_scrollable_fields_frame(parent, bg_color, entity_name):
    """
    Create a scrollable frame for the fields.
    """
    container = tk.Frame(parent, bg=bg_color)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg=bg_color, highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=bg_color)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind("<Destroy>", lambda e: canvas.unbind_all("<MouseWheel>"))

    return scrollable_frame


def add_field(parent_frame, field_data=None):
    """
    Add a field to the parent frame.
    """
    row = tk.Frame(parent_frame, bg=theme_manager.get("BG_BOX"), pady=4)
    row.pack(fill="x", pady=(0, SECTION_SPACING))

    number_label = tk.Label(
        row,
        text=f"#{len(parent_frame.winfo_children())}",
        font=(FONT_FAMILY, FONT_SIZE_LABEL),
        fg=theme_manager.get("TEXT_COLOR"),
        bg=theme_manager.get("BG_BOX"),
        width=4,
    )
    number_label.grid(row=0, column=0, padx=(0, 8), sticky="w")

    name_entry = ttk.Entry(row, style="CleanDark.TEntry")
    name_entry.grid(row=0, column=1, padx=(0, 8), sticky="ew")
    if field_data and field_data.get("name"):
        name_entry.insert(0, field_data["name"])
        name_entry.configure(foreground=theme_manager.get("TEXT_COLOR"))
    else:
        set_placeholder(name_entry, "Name of the field")
    row.name_entry = name_entry

    type_options = [
        "String",
        "Integer",
        "Long",
        "Boolean",
        "Double",
        "BigDecimal",
        "ZonedDateTime",
        "LocalDate",
        "LocalDateTime",
        "UUID",
    ]
    type_var = tk.StringVar(value=type_options[0])
    if field_data:
        type_var.set(field_data.get("type", type_options[0]))
    type_combobox = ttk.Combobox(
        row,
        values=type_options,
        textvariable=type_var,
        state="readonly",
        style="Custom.TCombobox",
        width=15,
    )
    type_combobox.grid(row=0, column=2, padx=(0, 8), sticky="ew")
    row.type_combobox = type_combobox

    def clear_selection(event):
        event.widget.icursor(tk.END)
        event.widget.selection_clear()

    def update_test_value(event=None):
        test_var.set(get_fake_value(type_var.get()))

    type_combobox.bind("<<ComboboxSelected>>", update_test_value)
    type_combobox.bind("<<ComboboxSelected>>", clear_selection, add="+")

    comment_entry = ttk.Entry(row, style="CleanDark.TEntry")
    comment_entry.grid(row=0, column=3, padx=(0, 8), sticky="ew")
    if field_data and field_data.get("comment"):
        comment_entry.insert(0, field_data["comment"])
        comment_entry.configure(foreground=theme_manager.get("TEXT_COLOR"))
    else:
        set_placeholder(comment_entry, "Comment")
    row.comment_entry = comment_entry

    test_var = tk.StringVar()
    test_entry = ttk.Entry(row, textvariable=test_var, style="CleanDark.TEntry")
    test_entry.grid(row=0, column=4, padx=(0, 8), sticky="ew")
    if field_data and field_data.get("test_value"):
        test_var.set(field_data["test_value"])
        test_entry.configure(foreground=theme_manager.get("TEXT_COLOR"))
    else:
        set_placeholder(test_entry, "Test value")
    row.test_entry = test_entry

    id_var = tk.BooleanVar()
    id_check = ttk.Checkbutton(
        row,
        text="id",
        variable=id_var,
        style="Custom.TCheckbutton",
    )
    id_check.grid(row=0, column=5, padx=(0, 8), sticky="w")
    row.is_id_var = id_var

    nullable_var = tk.BooleanVar()
    nullable_check = ttk.Checkbutton(
        row,
        text="Nullable",
        variable=nullable_var,
        style="Custom.TCheckbutton",
    )
    nullable_check.grid(row=0, column=6, padx=(0, 8), sticky="w")
    row.nullable_var = nullable_var

    delete_btn = ttk.Button(
        row,
        image=DELETE_ICON,
        command=lambda: row.destroy(),
        style="Red.TButton",
        width=1,
    )
    delete_btn.grid(row=0, column=7, padx=(0, 0), sticky="e")

    row.grid_columnconfigure(1, weight=2)
    row.grid_columnconfigure(2, weight=2)
    row.grid_columnconfigure(3, weight=3)
    row.grid_columnconfigure(4, weight=2)

    if field_data:
        id_var.set(field_data.get("is_id", False))
        nullable_var.set(field_data.get("nullable", False))


def set_placeholder(entry_widget, placeholder_text):
    """
    Set the placeholder for the entry widget.
    """

    def on_focus_in(event):
        """
        Handle the focus in event.
        """
        if getattr(entry_widget, "_has_placeholder", False):
            entry_widget.delete(0, tk.END)
            entry_widget.configure(foreground=theme_manager.get("TEXT_COLOR"))
            entry_widget._has_placeholder = False

    def on_focus_out(event):
        """
        Handle the focus out event.
        """
        if not entry_widget.get():
            entry_widget.insert(0, placeholder_text)
            entry_widget.configure(foreground="gray")
            entry_widget._has_placeholder = True

    def on_key_release(event):
        """
        Handle the key release event.
        """
        if not getattr(entry_widget, "_has_placeholder", False):
            entry_widget.configure(foreground=theme_manager.get("TEXT_COLOR"))

    entry_widget.bind("<FocusIn>", on_focus_in)
    entry_widget.bind("<FocusOut>", on_focus_out)
    entry_widget.bind("<KeyRelease>", on_key_release)

    entry_widget.insert(0, placeholder_text)
    entry_widget.configure(foreground="gray")
    entry_widget._has_placeholder = True
