from unittest.mock import MagicMock

from generator.core.generator import build_entity_data, save_entity_json


def mock_field(name, type_, comment="", test_value="", is_id=False):
    return (
        MagicMock(get=MagicMock(return_value=name)),
        MagicMock(get=MagicMock(return_value=type_)),
        MagicMock(get=MagicMock(return_value=comment)),
        MagicMock(get=MagicMock(return_value=test_value)),
        MagicMock(get=MagicMock(return_value=is_id)),
        None,  # row
    )


def test_build_entity_data():
    fields = [mock_field("nom", "String", "Nom de l'utilisateur", "Jean", False)]
    result = build_entity_data("User", fields)
    assert result["Table"] == "User"
    assert result["camelTable"] == "user"
    assert result["endpoint"] == "user" + "s"
    assert len(result["fields"]) == 1
    assert result["fields"][0]["nom"] == "nom"
    assert result["fields"][0]["type"] == "String"
    assert result["fields"][0]["isId"] is False


def test_save_entity_json(tmp_path):
    filepath = save_entity_json("Test", {"test": 123}, output_dir=tmp_path)
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    assert '"test": 123' in content
