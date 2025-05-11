"""
Gestion des imports Java en fonction des types de champs.
"""

# Mapping des types Java vers leurs imports nécessaires
TYPE_IMPORTS = {
    "ZonedDateTime": "java.time.ZonedDateTime",
    "LocalDate": "java.time.LocalDate",
    "LocalDateTime": "java.time.LocalDateTime",
    "UUID": "java.util.UUID",
    "List": "import java.util.List",
    "BigDecimal": "java.math.BigDecimal",
}

# Imports communs à toutes les entités
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
    Retourne la liste des imports nécessaires en fonction des types de champs.

    Args:
        fields: Liste des champs de l'entité

    Returns:
        Liste des imports nécessaires
    """
    imports = set(COMMON_IMPORTS)

    for field in fields:
        field_type = field["type"]
        if field_type in TYPE_IMPORTS:
            imports.add(TYPE_IMPORTS[field_type])

    return sorted(list(imports))
