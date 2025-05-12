import tkinter as tk
from tkinter import ttk

from generator.core.logger import logger
from generator.gui.style import (
    BG_COLOR,
    BG_LIGHT,
    FONT_FAMILY,
    FONT_SIZE_LABEL,
    PADDING,
    TEXT_COLOR,
)


class EntityBox(tk.Frame):
    def __init__(self, parent, entity_name, on_click, on_delete=None):
        super().__init__(
            parent,
            bg=BG_COLOR,
            bd=1,
            relief="solid",
            padx=PADDING,
            pady=PADDING,
        )
        self.entity_name = entity_name
        self.on_click = on_click
        self.on_delete = on_delete
        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)

        self.label = tk.Label(
            self,
            text=self.entity_name,
            font=(FONT_FAMILY, FONT_SIZE_LABEL, "bold"),
            fg=TEXT_COLOR,
            bg=BG_COLOR,
        )
        self.label.grid(row=0, column=0, sticky="w")

        modify_btn = ttk.Button(
            self,
            text="Modifier",
            command=self._on_click,
            style="TButton",
            cursor="hand2",
        )
        modify_btn.grid(row=0, column=1, padx=(10, 4), sticky="e")

        delete_btn = ttk.Button(
            self,
            text="Supprimer",
            command=self._on_delete,
            style="Red.TButton",
            cursor="hand2",
        )
        delete_btn.grid(row=0, column=2, padx=(0, 0), sticky="e")

    def _on_click(self):
        self.on_click(self.entity_name)

    def _on_delete(self):
        if self.on_delete is not None:
            self.on_delete(self.entity_name)

    def rename(self, new_name):
        logger.info("Renaming entity box from %s to %s", self.entity_name, new_name)
        self.entity_name = new_name
        self.label.config(text=new_name)


class EntityBoard(tk.Frame):
    def __init__(
        self, parent, on_entity_click=None, on_add_entity=None, on_entity_delete=None
    ):
        super().__init__(parent, bg=BG_LIGHT)
        self.on_entity_click = on_entity_click
        self.on_add_entity = on_add_entity
        self.on_entity_delete = on_entity_delete
        self.entities = {}
        self._build_ui()

    def _build_ui(self):
        # Titre
        title = tk.Label(
            self,
            text="Entities",
            font=(FONT_FAMILY, FONT_SIZE_LABEL, "bold"),
            fg=TEXT_COLOR,
            bg=BG_LIGHT,
        )
        title.pack(anchor="w", pady=(0, 10), fill="x")

        # Bouton stylé
        add_btn = ttk.Button(
            self,
            text="➕ Add Entity",
            command=self.on_add_entity,
            style="TButton",
            cursor="hand2",
        )
        add_btn.pack(anchor="w", pady=(0, PADDING))

        # Conteneur des entités
        self.entity_container = tk.Frame(self, bg=BG_LIGHT)
        self.entity_container.pack(fill="both", expand=True, pady=(PADDING, 0))

    def add_entity(self, entity_name):
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
        """Supprime une entité du board (UI + registre)."""
        if entity_name in self.entities:
            logger.info(
                "[UI] Avant suppression: %d widgets dans le conteneur",
                len(self.entity_container.winfo_children()),
            )

            entity_box = self.entities[entity_name]
            entity_box.destroy()  # Supprime le widget de l'interface
            del self.entities[entity_name]  # Supprime la référence
            self.entity_container.pack_propagate(False)
            for widget in self.entity_container.winfo_children():
                widget.pack_configure()
            self.entity_container.update_idletasks()
            self.update_idletasks()

            logger.info(
                "[UI] Après suppression: %d widgets dans le conteneur",
                len(self.entity_container.winfo_children()),
            )

    def update_entity_name(self, old_name, new_name):
        if old_name in self.entities:
            box = self.entities.pop(old_name)
            box.rename(new_name)
            self.entities[new_name] = box
