from core.class_generator import render_template_to_output

render_template_to_output(
    json_path="output/User.json",
    template_path=(
        "generator/templates/src/main/java/com/company/project/api/"
        "adapters/datasources/xxx/model/XxxEntity.java.j2"
    ),
)
