"""
Module containing the Java imports.

date: 05/06/2025
"""

# Mapping of Java types to their necessary imports
TYPE_IMPORTS = {
    "ZonedDateTime": "java.time.ZonedDateTime",
    "LocalDate": "java.time.LocalDate",
    "LocalDateTime": "java.time.LocalDateTime",
    "UUID": "java.util.UUID",
    "List": "import java.util.List",
    "BigDecimal": "java.math.BigDecimal",
}

# Common imports for all entities
COMMON_IMPORTS = [
    "java.io.Serializable",
    "jakarta.persistence.Entity",
    "jakarta.persistence.Id",
    "jakarta.persistence.GeneratedValue",
    "jakarta.persistence.GenerationType",
    "jakarta.persistence.Column",
    "jakarta.annotation.Nullable",
    "lombok.Data",
    "lombok.NoArgsConstructor",
    "lombok.AllArgsConstructor",
    "lombok.Builder",
]


def get_required_imports(fields):
    """
    Get the required imports for a given list of fields.

    Args:
        fields: List of fields of the entity

    Returns:
        List of required imports
    """
    imports = set(COMMON_IMPORTS)

    for field in fields:
        field_type = field["type"]
        if field_type in TYPE_IMPORTS:
            imports.add(TYPE_IMPORTS[field_type])

    return sorted(list(imports))
