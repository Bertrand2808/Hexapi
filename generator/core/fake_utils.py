from faker import Faker

faker = Faker("fr_FR")  # ou "en_US"


def get_fake_value(field_type: str) -> str:
    match field_type:
        case "String":
            return faker.first_name()
        case "Integer":
            return str(faker.random_int(min=1, max=100))
        case "Long":
            return str(faker.random_number(digits=10))
        case "Boolean":
            return "true"
        case "Double":
            return str(
                round(faker.pyfloat(left_digits=2, right_digits=2, positive=True), 2)
            )
        case "BigDecimal":
            return str(round(faker.pydecimal(left_digits=4, right_digits=2), 2))
        case "ZonedDateTime" | "LocalDateTime":
            return faker.iso8601()
        case "LocalDate":
            return faker.date()
        case "UUID":
            return str(faker.uuid4())
        case _:
            return ""
