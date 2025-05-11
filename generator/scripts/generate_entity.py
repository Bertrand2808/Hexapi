# generator/core/generate_entity.py

from generator.core.class_generator import render_template_to_output

TEMPLATES_TO_GENERATE = [
    "generator/templates/src/main/java/com/company/project/api/adapters/"
    "datasources/xxx/model/XxxEntity.java.j2",
    "generator/templates/src/main/java/com/company/project/api/adapters/"
    "datasources/xxx/XxxMapper.java.j2",
    "generator/templates/src/main/java/com/company/project/api/adapters/"
    "datasources/xxx/XxxPanacheAdapter.java.j2",
    "generator/templates/src/main/java/com/company/project/api/adapters/"
    "rest/controllers/xxx/XxxController.java.j2",
    "generator/templates/src/main/java/com/company/project/api/adapters/"
    "rest/controllers/xxx/XxxMapper.java.j2",
    "generator/templates/src/main/java/com/company/project/api/adapters/"
    "rest/controllers/xxx/model/XxxSchema.java.j2",
    "generator/templates/src/main/java/com/company/project/api/application/"
    "xxx/XxxDatasourcePort.java.j2",
    "generator/templates/src/main/java/com/company/project/api/application/"
    "xxx/XxxService.java.j2",
    "generator/templates/src/main/java/com/company/project/api/application/"
    "xxx/model/Xxx.java.j2",
    "generator/templates/src/main/resources/application.properties.j2",
    "generator/templates/src/main/java/com/company/project/Application.java.j2",
]


def generate_all_templates(json_path: str):
    for template_path in TEMPLATES_TO_GENERATE:
        render_template_to_output(json_path=json_path, template_path=template_path)
