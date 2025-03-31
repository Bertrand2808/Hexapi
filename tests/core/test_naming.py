from generator.core.naming import to_camel_case, to_kebab_case, to_pascal_case


def test_to_pascal_case():
    assert to_pascal_case("test de classe") == "TestDeClasse"


def test_to_camel_case():
    assert to_camel_case("nom de famille") == "nomDeFamille"


def test_to_kebab_case():
    assert to_kebab_case("FreezePeriod") == "freeze-periods"
