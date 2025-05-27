import pytest

from pytest_helm.models import YamlMapping


def test_findone_raises_if_key_is_missing():
    value = YamlMapping()

    with pytest.raises(KeyError):
        value.findone("test.path")


@pytest.mark.parametrize("value", [
    "default",
    None,
])
def test_findone_returns_default_if_key_is_missing(value):
    value = YamlMapping()
    result = value.findone("test.path", default=value)
    assert result == value


def test_findone_raises_key_error_if_key_is_missing():
    value = YamlMapping()
    with pytest.raises(KeyError):
        value.findone("test.path")


stub_data = {
    "a": {
        "b": "value",
        "c": None,
    },
}


@pytest.mark.parametrize("path,expected_value", [
    ("a.b", "value"),
    ("a.c", None),
])
def test_findone_returns_found_object(path, expected_value):
    result = YamlMapping.findone(stub_data, path)
    assert result == expected_value


def test_findone_raises_in_case_of_missing_value():
    with pytest.raises(KeyError):
        YamlMapping.findone(stub_data, "a.missing-key")


@pytest.mark.parametrize(
    "path,expected_value",
    [
        ("a.b", ["value"]),
        ("a.c", [None]),
        ("a.*", ["value", None]),
    ],
)
def test_findall_returns_all_found_objects_in_a_list(path, expected_value):
    result = YamlMapping.findall(stub_data, path)
    assert result == expected_value


def test_findall_returns_empty_list_in_case_of_missing_value():
    result = YamlMapping.findall(stub_data, "a.missing-key")
    assert result == []
