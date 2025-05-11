from unittest.mock import MagicMock, patch

from generator.gui.widgets import BG_COLOR


@patch("generator.gui.widgets.tk.Frame")
@patch("generator.gui.widgets.tk.Label")
@patch("generator.gui.widgets.ttk.Entry")
@patch("generator.gui.widgets.ttk.Combobox")
@patch("generator.gui.widgets.ttk.Checkbutton")
@patch("generator.gui.widgets.tk.BooleanVar")
@patch("generator.gui.widgets.tk.StringVar")
def test_add_field_smoke(
    mock_stringvar,
    mock_booleanvar,
    mock_checkbutton,
    mock_combobox,
    mock_entry,
    mock_label,
    mock_frame,
):
    mock_root = MagicMock()
    mock_stringvar.return_value = MagicMock()
    mock_booleanvar.return_value = MagicMock()

    mock_frame_instance = MagicMock()
    mock_frame.return_value = mock_frame_instance
    mock_frame_instance.__getitem__.return_value = BG_COLOR

    mock_label_instance = MagicMock()
    mock_entry_instance = MagicMock()
    mock_combobox_instance = MagicMock()
    mock_checkbutton_instance = MagicMock()

    mock_label.return_value = mock_label_instance
    mock_entry.return_value = mock_entry_instance
    mock_combobox.return_value = mock_combobox_instance
    mock_checkbutton.return_value = mock_checkbutton_instance

    import generator.gui.widgets as widgets

    widgets.add_field(mock_root, index=1)

    # Vérifie que Label est appelé 5 fois
    # (index + Nom, Type, Commentaire, Valeur de test)
    assert mock_label.call_count == 5
    mock_label_instance.grid.assert_called()

    # Vérifie que Entry est appelé 4 fois (champs de saisie)
    assert mock_entry.call_count == 3
    mock_entry_instance.grid.assert_called()
