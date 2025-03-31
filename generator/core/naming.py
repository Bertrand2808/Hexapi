import re
import unicodedata


def clean_string(s: str) -> str:
    # Supprimer les accents, les caractères spéciaux, etc.
    nfkd = unicodedata.normalize("NFKD", s)
    no_accents = "".join(c for c in nfkd if not unicodedata.combining(c))
    cleaned = re.sub(r"[^a-zA-Z0-9 ]", "", no_accents)
    return cleaned.strip()


def to_pascal_case(s: str) -> str:
    s = clean_string(s)
    return "".join(word.capitalize() for word in s.split())


def to_camel_case(s: str) -> str:
    s = clean_string(s)
    parts = s.split()
    return (
        parts[0].lower() + "".join(w.capitalize() for w in parts[1:]) if parts else ""
    )


def to_kebab_case(s: str) -> str:
    s = clean_string(s)
    kebab = re.sub(r"(?<!^)(?=[A-Z])", "-", s).lower()
    return kebab + "s"  # Pluralisation naïve
