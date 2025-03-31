def test_add_field_smoke():
    import tkinter as tk

    root = tk.Tk()
    from generator.gui.widgets import add_field

    frame = tk.Frame(root)
    widgets = add_field(frame)
    assert len(widgets) == 5
