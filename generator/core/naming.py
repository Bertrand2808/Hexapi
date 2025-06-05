"""
Module containing the naming.

date: 05/06/2025
"""

import re
import unicodedata


def clean_string(s: str) -> str:
    """
    Clean the string.
    """
    nfkd = unicodedata.normalize("NFKD", s)
    no_accents = "".join(c for c in nfkd if not unicodedata.combining(c))
    cleaned = re.sub(r"[^a-zA-Z0-9 ]", "", no_accents)
    return cleaned.strip()


def to_pascal_case(s: str) -> str:
    """
    Convert the string to PascalCase.
    """
    s = clean_string(s)
    return "".join(word.capitalize() for word in s.split())


def to_camel_case(s: str) -> str:
    """
    Convert the string to camelCase.
    """
    s = clean_string(s)
    parts = s.split()
    return (
        parts[0].lower() + "".join(w.capitalize() for w in parts[1:]) if parts else ""
    )


def to_kebab_case(s: str) -> str:
    """
    Convert the string to kebab-case.
    """
    s = clean_string(s)
    kebab = re.sub(r"(?<!^)(?=[A-Z])", "-", s).lower()
    return kebab + "s"  # Pluralisation naïve


def generate_name_variants(name: str) -> dict:
    """
    Generate several formats from a raw name.
    """
    s = clean_string(name)
    pascal = to_pascal_case(s)
    camel = to_camel_case(s)
    lower = s.lower().replace(" ", "")
    return {
        "original": s,
        "PascalCase": pascal,
        "camelCase": camel,
        "lowercase": lower,
    }
