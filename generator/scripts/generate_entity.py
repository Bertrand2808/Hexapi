# generator/core/generate_entity.py

from generator.core.class_generator import render_template_to_output
from generator.core.logger import logger

TEMPLATES_TO_GENERATE = [
    "generator/templates/src/main/java/api/adapters/"
    "datasources/xxx/model/XxxEntity.java.j2",
    "generator/templates/src/main/java/api/adapters/"
    "datasources/xxx/XxxMapper.java.j2",
    "generator/templates/src/main/java/api/adapters/"
    "datasources/xxx/XxxPanacheAdapter.java.j2",
    "generator/templates/src/main/java/api/adapters/"
    "rest/controllers/xxx/XxxController.java.j2",
    "generator/templates/src/main/java/api/adapters/"
    "rest/controllers/xxx/XxxMapper.java.j2",
    "generator/templates/src/main/java/api/adapters/"
    "rest/controllers/xxx/model/XxxSchema.java.j2",
    "generator/templates/src/main/java/api/application/"
    "xxx/XxxDatasourcePort.java.j2",
    "generator/templates/src/main/java/api/application/" "xxx/XxxService.java.j2",
    "generator/templates/src/main/java/api/application/" "xxx/model/Xxx.java.j2",
    "generator/templates/src/main/resources/application.properties.j2",
    "generator/templates/src/main/java/api/Application.java.j2",
]


def generate_all_templates(json_path: str):
    """Génère tous les templates pour une entité."""
    logger.info("Début de la génération des templates pour %s", json_path)
    try:
        for template_path in TEMPLATES_TO_GENERATE:
            logger.info("Génération du template: %s", template_path)
            try:
                render_template_to_output(
                    json_path=json_path, template_path=template_path
                )
                logger.info("Template généré avec succès: %s", template_path)
            except Exception as e:
                logger.error(
                    "Erreur lors de la génération du template %s: %s", template_path, e
                )
                raise
        logger.info("Génération des templates terminée pour %s", json_path)
    except Exception as e:
        logger.error("Erreur lors de la génération des templates: %s", e)
        raise
