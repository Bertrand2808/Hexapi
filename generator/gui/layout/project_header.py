"""
Module containing the ProjectHeader class.

date: 05/06/2025
"""

import tkinter as tk
from tkinter import ttk

from generator.gui.style import FONT_FAMILY, FONT_SIZE_LABEL, SECTION_SPACING
from generator.gui.theme_manager import theme_manager


class ProjectHeader(tk.Frame):
    """
    Class representing the project header.
    """

    def __init__(self, parent, **kwargs):
        """
        Initialize the project header.
        """
        super().__init__(parent, bg=theme_manager.get("BG"), **kwargs)
        self.project_name = None
        self.company_name = None
        self.package_name = None
        self.entry_wrappers = []
        self._build_ui()
        theme_manager.subscribe(self.apply_theme)

    def apply_theme(self):
        """
        Apply the theme to the project header.
        """
        self.configure(bg=theme_manager.get("BG"))
        for child in self.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=theme_manager.get("BG_BOX"))
                for sub in child.winfo_children():
                    if isinstance(sub, tk.Label):
                        sub.configure(
                            bg=theme_manager.get("BG_BOX"),
                            fg=theme_manager.get("TEXT_COLOR"),
                        )
                    elif isinstance(sub, tk.Frame):
                        sub.configure(bg=theme_manager.get("BG_INPUT"))
                        for entry in sub.winfo_children():
                            if isinstance(entry, ttk.Entry):
                                entry.configure(style="CleanDark.TEntry")
                                # Update the text color if it's not a placeholder
                                current_text = entry.get()
                                if current_text not in [
                                    "Ex: My Company",
                                    "Ex: my-project",
                                    "Ex: com.mycompany.project",
                                ]:
                                    entry.configure(
                                        foreground=theme_manager.get("TEXT_COLOR")
                                    )

    def _build_ui(self):
        """
        Build the UI of the project header.
        """
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        fields = [
            ("Company Name", "company_name", "Ex: My Company"),
            ("Project Name", "project_name", "Ex: my-project"),
            ("Package Name", "package_name", "Ex: com.mycompany.project"),
        ]

        for i, (label_text, field_name, placeholder) in enumerate(fields):
            card = tk.Frame(self, bg=theme_manager.get("BG_BOX"), pady=10)
            card.grid(row=i, column=0, sticky="ew", pady=(0, SECTION_SPACING))
            card.grid_columnconfigure(0, weight=1)

            label = tk.Label(
                card,
                text=label_text,
                font=(FONT_FAMILY, FONT_SIZE_LABEL),
                fg=theme_manager.get("TEXT_COLOR"),
                bg=theme_manager.get("BG_BOX"),
            )
            label.grid(row=0, column=0, sticky="w", pady=(0, 10), padx=12)

            entry_wrapper = tk.Frame(
                card,
                bg=theme_manager.get("BG_INPUT"),
                padx=3,
                pady=1,
            )
            entry_wrapper.grid(row=1, column=0, sticky="ew", padx=12)
            entry_wrapper.grid_columnconfigure(0, weight=1)
            self.entry_wrappers.append(entry_wrapper)

            entry = ttk.Entry(entry_wrapper, style="CleanDark.TEntry")
            entry.grid(row=0, column=0, sticky="ew")
            entry.insert(0, placeholder)
            entry.bind("<FocusIn>", lambda e, p=placeholder: self._on_focus_in(e, p))
            entry.bind("<FocusOut>", lambda e, p=placeholder: self._on_focus_out(e, p))
            setattr(self, field_name, entry)

    def _on_focus_in(self, event, placeholder):
        """
        Clear the placeholder when the field receives the focus.
        """
        if event.widget.get() == placeholder:
            event.widget.delete(0, "end")
            event.widget.configure(foreground=theme_manager.get("TEXT_COLOR"))

    def _on_focus_out(self, event, placeholder):
        """
        Restore the placeholder if the field is empty.
        """
        if not event.widget.get():
            event.widget.insert(0, placeholder)
            event.widget.configure(foreground=theme_manager.get("TEXT_COLOR"))

    def get_company(self):
        """
        Get the company name.
        """
        value = self.company_name.get()
        return value if value != "Ex: My Company" else ""

    def get_project(self):
        """
        Get the project name.
        """
        value = self.project_name.get()
        return value if value != "Ex: my-project" else ""

    def get_package(self):
        """
        Get the package name.
        """
        value = self.package_name.get()
        return value if value != "Ex: com.mycompany.project" else ""
