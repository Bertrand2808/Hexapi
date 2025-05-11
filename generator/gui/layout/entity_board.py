import tkinter as tk
from tkinter import ttk

FONT_FAMILY = "Segoe UI"
FONT_SIZE = 10
BG_COLOR = "#1e1e2f"
BOX_COLOR = "#2e2e3e"


class EntityBox(tk.Frame):
    """
    Représente une boîte cliquable pour une entité spécifique.
    """

    def __init__(self, parent, entity_name, on_click):
        super().__init__(parent, bg=BOX_COLOR, bd=1, relief="groove", padx=10, pady=10)
        self.entity_name = entity_name
        self.on_click = on_click
        self._build_ui()

    def _build_ui(self):
        self.label = tk.Label(
            self,
            text=self.entity_name,
            font=(FONT_FAMILY, 12, "bold"),
            fg="white",
            bg=BOX_COLOR,
        )
        self.label.pack(anchor="w")

        open_btn = ttk.Button(self, text="✏️ Modifier", command=self._on_click)
        open_btn.pack(anchor="e", pady=(5, 0))

    def _on_click(self):
        self.on_click(self.entity_name)


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
            text="Entités définies dans le projet",
            font=(FONT_FAMILY, 13, "bold"),
            fg="white",
            bg=BG_COLOR,
            pady=10,
        )
        self.title.pack(anchor="w")

        self.boxes_frame = tk.Frame(self, bg=BG_COLOR)
        self.boxes_frame.pack(fill="both", expand=True)

        self.add_button = ttk.Button(
            self, text="+ Ajouter une entité", command=self._handle_add
        )
        self.add_button.pack(anchor="w", pady=10)

    def add_entity(self, entity_name):
        """
        Ajoute visuellement une entité sous forme de box.
        """
        if entity_name in self.entity_boxes:
            return  # Eviter les doublons

        box = EntityBox(self.boxes_frame, entity_name, self.on_entity_click)
        box.pack(fill="x", pady=5)
        self.entity_boxes[entity_name] = box

    def update_entity_name(self, old_name, new_name):
        """
        Met à jour le nom d'une entité dans la liste.
        """
        if old_name in self.entity_boxes:
            box = self.entity_boxes.pop(old_name)
            box.entity_name = new_name
            box.label.configure(text=new_name)
            self.entity_boxes[new_name] = box

    def _handle_add(self):
        self.on_add_entity()
