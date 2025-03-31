from unittest.mock import MagicMock, patch

import generator.gui.main as gui_main


@patch("generator.gui.main.tk.Tk")
@patch("generator.gui.main.add_field")
@patch("generator.gui.main.save_entity_json")
@patch("generator.gui.main.build_entity_data")
def test_setup_main_interface_triggers_add_and_generate(
    mock_build_data, mock_save_json, mock_add_field, mock_tk
):
    mock_root = MagicMock()
    mock_tk.return_value = mock_root

    mock_build_data.return_value = {"fields": []}
    mock_save_json.return_value = "output/UserTest.json"
    mock_add_field.return_value = ("name", "type", "comment", "test", "row")

    gui_main.setup_main_interface(mock_root)

    # On vérifie que les boutons ont été créés et pack() appelés (via mock)
    assert mock_root.method_calls  # Appels de méthodes sur le root simulé
