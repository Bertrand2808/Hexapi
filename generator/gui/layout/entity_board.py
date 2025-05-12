import tkinter as tk
from tkinter import ttk

from generator.core.logger import logger
from generator.gui.style import BG_COLOR, BOX_COLOR, FONT_FAMILY


class EntityBox(tk.Frame):
    """
    Représente une boîte cliquable pour une entité spécifique.
    """

    def __init__(self, parent, entity_name, on_click):
        logger.info("Création de la boîte pour %s", entity_name)
        super().__init__(parent, bg=BOX_COLOR, bd=1, relief="groove", padx=10, pady=10)
        self.entity_name = entity_name
        self.on_click = on_click
        self._build_ui()

    def _build_ui(self):
        logger.info("Construction de la boîte pour %s", self.entity_name)
        self.label = tk.Label(
            self,
            text=self.entity_name,
            font=(FONT_FAMILY, 12, "bold"),
            fg="white",
            bg=BOX_COLOR,
        )
        self.label.pack(anchor="w")

        buttons_frame = tk.Frame(self, bg=BOX_COLOR)
        buttons_frame.pack(anchor="e", pady=(5, 0))

        open_btn = ttk.Button(buttons_frame, text="✏️ Modifier", command=self._on_click)
        open_btn.pack(side="left", padx=(0, 5))

        delete_btn = ttk.Button(
            buttons_frame, text="🗑️ Supprimer", command=self._on_delete
        )
        delete_btn.pack(side="left")

    def _on_click(self):
        logger.info("Ouverture de la boîte pour %s", self.entity_name)
        self.on_click(self.entity_name)

    def _on_delete(self):
        logger.info("Suppression de la boîte pour %s", self.entity_name)
        if hasattr(self, "on_delete"):
            self.on_delete(self.entity_name)


class EntityBoard(tk.Frame):
    """
    Contient l'ensemble des boxes d'entités + bouton d'ajout.
    """

    def __init__(self, parent, on_entity_click, on_add_entity):
        super().__init__(parent, bg=BG_COLOR)
        self.on_entity_click = on_entity_click
        self.on_add_entity = on_add_entity
        self.entity_boxes = {}
        self._build_ui()

    def _build_ui(self):
        self.title = tk.Label(
            self,
            text="Defined entities in the project",
            font=(FONT_FAMILY, 13, "bold"),
            fg="white",
            bg=BG_COLOR,
            pady=10,
        )
        self.title.pack(anchor="w", pady=(0, 12))

        self.boxes_frame = tk.Frame(self, bg=BG_COLOR)
        self.boxes_frame.pack(fill="both", expand=True)

        self.add_button = ttk.Button(
            self, text="+ Add an entity", command=self._handle_add
        )
        self.add_button.pack(anchor="w", pady=10)

    def add_entity(self, entity_name):
        """
        Ajoute visuellement une entité sous forme de box.
        """
        logger.info("Adding entity %s to the table", entity_name)
        if entity_name in self.entity_boxes:
            return  # Eviter les doublons

        box = EntityBox(self.boxes_frame, entity_name, self.on_entity_click)
        box.on_delete = self._handle_delete
        box.pack(fill="x", pady=5)
        self.entity_boxes[entity_name] = box

    def update_entity_name(self, old_name, new_name):
        """
        Met à jour le nom d'une entité dans la liste.
        """
        logger.info("Updating entity name %s", old_name)
        if old_name in self.entity_boxes:
            box = self.entity_boxes.pop(old_name)
            box.entity_name = new_name
            box.label.configure(text=new_name)
            self.entity_boxes[new_name] = box

    def _handle_add(self):
        logger.info("Adding an entity")
        self.on_add_entity()

    def _handle_delete(self, entity_name):
        """
        Gère la suppression d'une entité.
        """
        logger.info("Deleting entity %s", entity_name)
        if entity_name in self.entity_boxes:
            if hasattr(self, "delete_entity"):
                self.delete_entity(entity_name)
            box = self.entity_boxes.pop(entity_name)
            box.destroy()
