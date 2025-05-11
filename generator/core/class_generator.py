"""Module for rendering Jinja2 templates into Java class files based on JSON input."""

import json
import os
import re

from jinja2 import Environment, FileSystemLoader

from generator.core.java_imports import get_required_imports


def render_template_to_output(
    json_path: str, template_path: str, output_root: str = "output"
):
    """
    Render a Jinja2 template to a Java file, based on the content of a JSON file.

    Args:
        json_path (str): Path to the JSON input file.
        template_path (str): Path to the Jinja2 template file.
        output_root (str): Root directory where the rendered file will be written.
    """
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    company = data["company"]["lowercase"]
    project = data["project"]["lowercase"]
    table = data["table"]
    Table = data["Table"]

    template_rel_path = template_path.replace("generator/templates/", "")

    # Supprimer uniquement le .j2 en toute sécurité
    if template_rel_path.endswith(".j2"):
        template_rel_path = template_rel_path[:-3]

    # Remplacer les éléments dynamiques
    dynamic_path = (
        template_rel_path.replace("company", company)
        .replace("project", project)
        .replace("xxx", table)
        .replace("Xxx", Table)
    )

    if dynamic_path.endswith(".j2"):
        dynamic_path = dynamic_path[:-3]

    # Créer le chemin de sortie avec company/project comme préfixe
    output_path = os.path.join(output_root, company, project, dynamic_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    env = Environment(
        loader=FileSystemLoader("generator/templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["replaceCamelCaseWithUnderscore"] = lambda s: re.sub(
        r"(?<!^)(?=[A-Z])", "_", s
    ).lower()

    template_path_in_templates = template_path.replace("generator/templates/", "")
    template = env.get_template(template_path_in_templates)
    print(template_path_in_templates)

    rendered = template.render(**data, get_required_imports=get_required_imports)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"[OK] Fichier généré : {output_path}")
