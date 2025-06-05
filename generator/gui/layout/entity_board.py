"""
Module containing the EntityBox and EntityBoard classes.

date: 05/06/2025
"""

import tkinter as tk
from tkinter import ttk

from generator.core.logger import logger
from generator.gui.style import FONT_FAMILY, FONT_SIZE_LABEL, PADDING
from generator.gui.theme_manager import theme_manager

# === Classes ===
# === EntityBox Class ===


class EntityBox(tk.Frame):
    """
    Class representing an entity box in the table.
    """

    def __init__(self, parent, entity_name, on_click, on_delete=None):
        super().__init__(
            parent,
            bg=theme_manager.get("BG_BOX"),
            highlightbackground=theme_manager.get("BORDER_COLOR"),
            highlightthickness=1,
            padx=16,
            pady=12,
        )
        self.pack_propagate(False)
        self.entity_name = entity_name
        self.on_click = on_click
        self.on_delete = on_delete
        self._build_ui()
        theme_manager.subscribe(self.apply_theme)

    def apply_theme(self):
        """
        Apply the theme to the entity box.
        """
        self.configure(
            bg=theme_manager.get("BG_BOX"),
            highlightbackground=theme_manager.get("BORDER_COLOR"),
        )
        for widget in self.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(
                    bg=theme_manager.get("BG_BOX"), fg=theme_manager.get("TEXT_COLOR")
                )
            elif isinstance(widget, ttk.Button):
                widget.configure(style="TButton")

    def _build_ui(self):
        """
        Build the UI of the entity box.
        """
        self.columnconfigure(0, weight=1)

        self.label = tk.Label(
            self,
            text=self.entity_name,
            font=(FONT_FAMILY, FONT_SIZE_LABEL, "bold"),
            bg=theme_manager.get("BG_BOX"),
            fg=theme_manager.get("TEXT_COLOR"),
        )
        self.label.grid(row=0, column=0, sticky="w")

        modify_btn = ttk.Button(
            self,
            text="Modifier",
            command=self._on_click,
            style="TButton",
            cursor="hand2",
            width=8,  # Réduit la largeur du bouton
        )
        modify_btn.grid(row=0, column=1, padx=(10, 4), sticky="e")

        delete_btn = ttk.Button(
            self,
            text="Supprimer",
            command=self._on_delete,
            style="Red.TButton",
            cursor="hand2",
            width=9,  # Réduit la largeur du bouton
        )
        delete_btn.grid(row=0, column=2, padx=(0, 0), sticky="e")

    def _on_click(self):
        """
        Handle the click event on the entity box.
        """
        self.on_click(self.entity_name)

    def _on_delete(self):
        """
        Handle the delete event on the entity box.
        """
        if self.on_delete is not None:
            self.on_delete(self.entity_name)

    def rename(self, new_name):
        """
        Rename the entity box.
        """
        logger.info("Renaming entity box from %s to %s", self.entity_name, new_name)
        self.entity_name = new_name
        self.label.config(text=new_name)


# === EntityBoard Class ===


class EntityBoard(tk.Frame):
    """
    Class representing the entity board.
    """

    def __init__(
        self,
        parent,
        on_entity_click=None,
        on_add_entity=None,
        on_entity_delete=None,
    ):
        super().__init__(parent, bg=theme_manager.get("BG_BOX"))
        self.on_entity_click = on_entity_click
        self.on_add_entity = on_add_entity
        self.on_entity_delete = on_entity_delete
        self.entities = {}
        self._build_ui()
        theme_manager.subscribe(self.apply_theme)

    def _build_ui(self):
        """
        Build the UI of the entity board.
        """
        self.title = tk.Label(
            self,
            text="Entities",
            font=(FONT_FAMILY, FONT_SIZE_LABEL, "bold"),
            fg=theme_manager.get("TEXT_COLOR"),
            bg=theme_manager.get("BG_BOX"),
        )
        self.title.pack(anchor="w", pady=(0, 10), fill="x")

        self.add_btn = ttk.Button(
            self,
            text="➕ Add Entity",
            command=self.on_add_entity,
            style="TButton",
            cursor="hand2",
        )
        self.add_btn.pack(anchor="w", padx=24, pady=(0, PADDING))

        # Frame contenant le canvas + scrollbar
        canvas_frame = tk.Frame(self, bg=theme_manager.get("BG_BOX"))
        canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg=theme_manager.get("BG_BOX"))
        self.scrollbar = ttk.Scrollbar(
            canvas_frame,
            orient="vertical",
            command=self.canvas.yview,
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.entity_container = tk.Frame(self.canvas, bg=theme_manager.get("BG_BOX"))
        self.container_window = self.canvas.create_window(
            (0, 0),
            window=self.entity_container,
            anchor="nw",
        )
        self.canvas.bind("<Configure>", self._resize_entity_container)

        def on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            self._update_scrollbar_visibility()

        self.entity_container.bind("<Configure>", on_frame_configure)

        def _on_mousewheel(event):
            if self.canvas.bbox("all")[3] > self.canvas.winfo_height():
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind(
            "<Enter>",
            lambda e: self.canvas.bind_all("<MouseWheel>", _on_mousewheel),
        )
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

    def _resize_entity_container(self, event):
        """
        Resize the entity container.
        """
        canvas_width = event.width
        self.canvas.itemconfig(self.container_window, width=canvas_width)

    def apply_theme(self):
        """
        Apply the theme to the entity board.
        """
        self.configure(bg=theme_manager.get("BG_BOX"))
        self.title.configure(
            bg=theme_manager.get("BG_BOX"), fg=theme_manager.get("TEXT_COLOR")
        )
        self.canvas.configure(bg=theme_manager.get("BG_BOX"))
        self.entity_container.configure(bg=theme_manager.get("BG_BOX"))

    def add_entity(self, entity_name):
        """
        Add an entity to the entity board.
        """
        if entity_name in self.entities:
            return
        box = EntityBox(
            self.entity_container,
            entity_name,
            self.on_entity_click,
            on_delete=self.on_entity_delete,
        )
        box.pack(fill="x", pady=(0, PADDING))
        self.entities[entity_name] = box

    def delete_entity(self, entity_name):
        """
        Delete an entity from the entity board.
        """
        if entity_name in self.entities:
            entity_box = self.entities[entity_name]
            entity_box.destroy()
            del self.entities[entity_name]
            self.entity_container.update_idletasks()
            self.update_idletasks()

    def update_entity_name(self, old_name, new_name):
        """
        Update the name of an entity.
        """
        if old_name in self.entities:
            box = self.entities.pop(old_name)
            box.rename(new_name)
            self.entities[new_name] = box

    def _update_scrollbar_visibility(self):
        """
        Update the visibility of the scrollbar.
        """
        self.update_idletasks()
        if self.canvas.bbox("all"):
            needs_scroll = self.canvas.bbox("all")[3] > self.canvas.winfo_height()
            if needs_scroll:
                self.scrollbar.pack(side="right", fill="y")
            else:
                self.scrollbar.pack_forget()
