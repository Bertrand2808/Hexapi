import pytest

from generator.core.fake_utils import get_fake_value


@pytest.mark.parametrize(
    "field_type",
    [
        "String",
        "Integer",
        "Long",
        "Boolean",
        "Double",
        "BigDecimal",
        "ZonedDateTime",
        "LocalDate",
        "LocalDateTime",
        "UUID",
    ],
)
def test_get_fake_value_generates_data(field_type):
    value = get_fake_value(field_type)
    assert isinstance(value, str)
    assert value != ""
