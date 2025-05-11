from generator.core.java_imports import get_required_imports


def test_get_required_imports_with_special_types():
    """Teste la génération des imports pour différents types de champs."""
    fields = [
        {"type": "String", "nom": "name", "comment": "nom", "testValue": "test"},
        {
            "type": "ZonedDateTime",
            "nom": "createdAt",
            "comment": "date",
            "testValue": "2024",
        },
        {
            "type": "LocalDate",
            "nom": "birthDate",
            "comment": "date",
            "testValue": "2024",
        },
        {"type": "UUID", "nom": "uuid", "comment": "id", "testValue": "123"},
        {
            "type": "BigDecimal",
            "nom": "balance",
            "comment": "solde",
            "testValue": "100",
        },
    ]

    imports = get_required_imports(fields)

    # Vérifie que les imports communs sont présents
    assert "java.io.Serializable" in imports
    assert "jakarta.persistence.Entity" in imports
    assert "lombok.Data" in imports
    assert "jakarta.annotation.Nullable" in imports

    # Vérifie que les imports spécifiques sont présents
    assert "java.time.ZonedDateTime" in imports
    assert "java.time.LocalDate" in imports
    assert "java.util.UUID" in imports
    assert "java.math.BigDecimal" in imports

    # Vérifie que les imports sont triés
    assert imports == sorted(imports)


def test_get_required_imports_without_special_types():
    """Teste la génération des imports pour des types basiques."""
    fields = [
        {"type": "String", "nom": "name", "comment": "nom", "testValue": "test"},
        {"type": "Long", "nom": "id", "comment": "id", "testValue": "1"},
        {"type": "Boolean", "nom": "active", "comment": "actif", "testValue": "true"},
    ]

    imports = get_required_imports(fields)

    # Vérifie que seuls les imports communs sont présents
    assert "java.io.Serializable" in imports
    assert "jakarta.persistence.Entity" in imports
    assert "lombok.Data" in imports
    assert "jakarta.annotation.Nullable" in imports

    # Vérifie qu'aucun import spécial n'est présent
    assert "java.time.ZonedDateTime" not in imports
    assert "java.time.LocalDate" not in imports
    assert "java.util.UUID" not in imports
    assert "java.math.BigDecimal" not in imports


def test_get_required_imports_with_nullable_fields():
    """Teste la génération des imports avec des champs nullable."""
    fields = [
        {
            "type": "String",
            "nom": "description",
            "comment": "description optionnelle",
            "testValue": "test",
            "nullable": True,
        },
        {
            "type": "LocalDate",
            "nom": "endDate",
            "comment": "date de fin optionnelle",
            "testValue": "2024-12-31",
            "nullable": True,
        },
        {
            "type": "Long",
            "nom": "id",
            "comment": "identifiant",
            "testValue": "1",
            "nullable": False,
        },
    ]

    imports = get_required_imports(fields)

    # Vérifie que l'import pour @Nullable est présent
    assert "jakarta.annotation.Nullable" in imports
    # Vérifie que l'import pour LocalDate est présent
    assert "java.time.LocalDate" in imports
    # Vérifie que les imports communs sont présents
    assert "java.io.Serializable" in imports
    assert "jakarta.persistence.Entity" in imports
    assert "lombok.Data" in imports
