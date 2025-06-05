"""
Module containing the generator.

date: 05/06/2025
"""

import json
import os

from generator.core.naming import to_camel_case, to_kebab_case, to_pascal_case


def build_entity_data(entity_name: str, fields_raw: list[tuple]) -> dict:
    """
    Build the entity data.
    """
    entity_pascal = to_pascal_case(entity_name)
    entity_camel = to_camel_case(entity_name)
    entity_kebab = to_kebab_case(entity_name)
    table_plural = entity_camel + "s"
    capital_table_plural = table_plural.capitalize()

    result = {
        "Table": entity_pascal,
        "table": entity_camel,
        "tables": table_plural,
        "capitalTables": capital_table_plural,
        "camelTable": entity_camel,
        "endpoint": entity_kebab,
        "fields": [],
    }

    for (
        name_entry,
        type_combobox,
        comment_entry,
        test_entry,
        is_id,
        nullable_checkbox,
        _,
    ) in fields_raw:
        name = to_camel_case(name_entry.get())
        typ = type_combobox.get().strip()
        comment = comment_entry.get().strip()
        test_val = test_entry.get().strip()
        is_id_value = is_id.get()
        nullable = nullable_checkbox.get()

        if not name:
            continue

        result["fields"].append(
            {
                "nom": name,
                "type": typ,
                "isId": is_id_value,
                "nullable": nullable,
                "comment": comment,
                "testValue": test_val,
            }
        )

    return result


def save_entity_json(entity_name: str, data: dict, output_dir="output") -> str:
    """
    Save the entity data to a JSON file.
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{entity_name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return filepath
