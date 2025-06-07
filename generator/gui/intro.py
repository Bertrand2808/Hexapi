import os
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from generator.gui.style import FONT_FAMILY
from generator.gui.theme_manager import theme_manager

# Chemin absolu vers l'image d'illustration
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(
    CURRENT_DIR, "..", "assets", "images", "intro", "add_entity.png"
)


def show_intro_popup(parent):
    """
    Show the intro popup.
    """
    pages = [
        {
            "title": "Welcome in HexAPI Generator 🎉",
            "content": (
                "This tool allows you to generate a complete Java API by simply "
                "defining your entities."
            ),
        },
        {
            "title": "Step 1 : Create your entities",
            "content": (
                "Use the + button to add an entity, and define its fields "
                "(name, type, test value...)."
            ),
            "image": ASSETS_PATH,
        },
        {
            "title": "Step 2 : Automatic generation",
            "content": (
                "Click on '🚀 Generate all entities' to generate the Java architecture. "
                "You can then manually modify the files if needed."
            ),
        },
    ]

    current_page = {"index": 0}

    def show_page():
        """
        Show the current page.
        """
        data = pages[current_page["index"]]
        title_var.set(data["title"])
        content_var.set(data["content"])

        if "image" in data:
            try:
                pil_image = Image.open(data["image"])

                # Redimensionner proportionnellement (max 400px de large)
                max_width = 400
                width, height = pil_image.size
                if width > max_width:
                    ratio = max_width / width
                    pil_image = pil_image.resize(
                        (int(width * ratio), int(height * ratio)),
                        resample=Image.Resampling.LANCZOS,
                    )

                image = ImageTk.PhotoImage(pil_image)
                image_label.configure(image=image)
                image_label.image = image
            except Exception as e:
                print(f"Erreur lors du chargement de l'image: {e}")
                image_label.configure(image="")
        else:
            image_label.configure(image="")

        prev_btn.config(state="normal" if current_page["index"] > 0 else "disabled")
        next_btn.config(
            text="Next" if current_page["index"] < len(pages) - 1 else "Finish"
        )

        popup.update_idletasks()
        w = popup.winfo_reqwidth()
        h = popup.winfo_reqheight()
        x = (popup.winfo_screenwidth() // 2) - (w // 2)
        y = (popup.winfo_screenheight() // 2) - (h // 2)
        popup.geometry(f"{w}x{h}+{x}+{y}")

    def next_page():
        if current_page["index"] < len(pages) - 1:
            current_page["index"] += 1
            show_page()
        else:
            popup.destroy()

    def prev_page():
        if current_page["index"] > 0:
            current_page["index"] -= 1
            show_page()

    # === Création de la fenêtre popup ===
    popup = tk.Toplevel(parent)
    popup.title("Welcome in HexAPI Generator 🎉")
    popup.configure(bg=theme_manager.get("BG_BOX"))
    popup.transient(parent)
    popup.grab_set()

    # === Conteneur avec padding ===
    container = tk.Frame(popup, bg=theme_manager.get("BG_BOX"))
    container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # Variables dynamiques
    title_var = tk.StringVar()
    content_var = tk.StringVar()

    title_label = tk.Label(
        container,
        textvariable=title_var,
        font=(FONT_FAMILY, 16, "bold"),
        bg=theme_manager.get("BG_BOX"),
        fg=theme_manager.get("TEXT_COLOR"),
    )
    title_label.pack(pady=(20, 10))

    content_label = tk.Label(
        container,
        textvariable=content_var,
        font=(FONT_FAMILY, 12),
        wraplength=540,
        justify="center",
        bg=theme_manager.get("BG_BOX"),
        fg=theme_manager.get("TEXT_COLOR"),
    )
    content_label.pack(pady=(0, 20))

    image_label = tk.Label(container, bg=theme_manager.get("BG_BOX"))
    image_label.pack(pady=(0, 20))

    btn_frame = tk.Frame(container, bg=theme_manager.get("BG_BOX"))
    btn_frame.pack()

    prev_btn = ttk.Button(btn_frame, text="Previous", command=prev_page)
    prev_btn.pack(side="left", padx=10)

    next_btn = ttk.Button(btn_frame, text="Next", command=next_page)
    next_btn.pack(side="left", padx=10)

    show_page()
    popup.wait_window()
