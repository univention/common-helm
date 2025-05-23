import pytest

from pytest_helm.models import YamlMapping


def test_findone_raises_if_key_is_missing():
    value = YamlMapping()

    with pytest.raises(AttributeError):
        value.findone("test.path")


@pytest.mark.parametrize("value", [
    "default",
    None,
])
def test_findone_returns_default_if_key_is_missing(value):
    value = YamlMapping()
    result = value.findone("test.path", default=value)
    assert result == value
