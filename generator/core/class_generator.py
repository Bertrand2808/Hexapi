"""
Module for rendering Jinja2 templates into Java class files based on JSON input.

date: 05/06/2025
"""

import json
import os
import re

from jinja2 import Environment, FileSystemLoader

from generator.core.logger import logger


def render_template_to_output(
    json_path: str,
    template_path: str,
    output_root: str = "output",
    get_required_imports: bool = False,
):
    """
    Render a Jinja2 template to a Java file, based on the content of a JSON file.

    Args:
        json_path (str): Path to the JSON input file.
        template_path (str): Path to the Jinja2 template file.
        output_root (str): Root directory where the rendered file will be written.
    """
    logger.info(
        "Starting template rendering %s with data from %s", template_path, json_path
    )
    try:
        # Charger les données JSON
        logger.info("Loading JSON file: %s", json_path)
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info("JSON data loaded: %s", data)

        company = data["company"]["lowercase"]
        project = data["project"]["lowercase"]
        package_name = data["package_name"]
        table = data["table"]
        Table = data["Table"]

        # Convert the package name to a path
        package_path = package_name.replace(".", "/")
        logger.info("Package path: %s", package_path)

        # Determine if it's a resource file
        is_resource = "application.properties" in template_path

        if is_resource:
            # For resources, place in src/main/resources
            template_rel_path = template_path.replace(
                "generator/templates/src/main/resources/", ""
            )
            output_path = os.path.join(
                output_root,
                company,
                project,
                "src/main/resources",
                template_rel_path.replace(".j2", ""),
            )
        else:
            template_rel_path = template_path.replace(
                "generator/templates/src/main/java/", ""
            )
            dynamic_path = (
                template_rel_path.replace("xxx", table).replace("Xxx", Table)
            ).replace(".j2", "")
            output_path = os.path.join(
                output_root,
                company,
                project,
                "src/main/java",
                package_path,
                dynamic_path,
            )

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        logger.info("Directories created if necessary: %s", output_path)

        # Configure the Jinja2 environment
        logger.info("Configuring Jinja2 environment")
        env = Environment(
            loader=FileSystemLoader("generator/templates"),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        env.filters["replaceCamelCaseWithUnderscore"] = lambda s: re.sub(
            r"(?<!^)(?=[A-Z])", "_", s
        ).lower()

        # Load and render the template
        logger.info("Loading template: %s", template_path)
        template_path_in_templates = template_path.replace("generator/templates/", "")
        template = env.get_template(template_path_in_templates)
        logger.info("Rendering template with data")
        rendered = template.render(**data, get_required_imports=get_required_imports)
        logger.info("Template rendered successfully")

        # Write the output file
        logger.info("Writing output file: %s", output_path)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        logger.info("File written successfully")

    except Exception as e:
        logger.error("Error rendering template: %s", e)
        raise

    logger.info("File generated: %s", output_path)
