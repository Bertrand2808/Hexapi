# === Imports ===
import tkinter as tk
from tkinter import ttk

from generator.core.generator import build_entity_data, save_entity_json
from generator.gui.widgets import add_field

BG_DARK = "#1e1e2f"


def create_main_window():
    root = tk.Tk()
    root.title("HexAPI Generator")
    root.geometry("800x600")
    root.configure(bg=BG_DARK)
    return root


def setup_main_interface(root):
    fields = []

    main_frame = tk.Frame(root, bg="#2e2e3e", padx=40, pady=30)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = tk.Label(
        root,
        text="Créateur de classe Entity",
        font=("Helvetica Neue", 18, "bold"),
        fg="white",
        bg=BG_DARK,
    )
    title_label.pack(pady=(30, 20))

    entity_name_label = tk.Label(
        main_frame,
        text="Nom Entity (sans 'Entity')",
        font=("Segoe UI", 12),
        fg="white",
        bg=main_frame["bg"],
    )
    entity_name_label.pack(anchor="w")

    entity_name_entry = ttk.Entry(main_frame, width=40, font=("Segoe UI", 11))
    entity_name_entry.pack(pady=(5, 20), anchor="w")

    fields_frame = tk.Frame(main_frame, bg=main_frame["bg"])
    fields_frame.pack(anchor="w", fill="x")

    def handle_add_field():
        widgets = add_field(fields_frame)
        fields.append(widgets)
        fields_frame._fields_list = fields

    def generate_class():
        entity_name = entity_name_entry.get().strip()
        if not entity_name:
            print("Erreur : nom de l'Entity vide.")
            return
        data = build_entity_data(entity_name, fields)
        filepath = save_entity_json(entity_name, data)
        print(f"[OK] Class {entity_name} was generated in : {filepath}")

    add_field_button = ttk.Button(
        main_frame, text="Ajouter un champ", command=handle_add_field
    )
    add_field_button.pack(pady=(20, 0), anchor="w")

    generate_button = ttk.Button(
        main_frame, text="Générer la classe", command=generate_class
    )
    generate_button.pack(pady=(30, 0), anchor="center")


def main():
    root = create_main_window()
    setup_main_interface(root)
    root.mainloop()
