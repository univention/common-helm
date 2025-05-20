import pytest

from pytest_helm.utils import _findall, _findone, add_jsonpath_prefix


def test_add_jsonpath_prefix():
    values = add_jsonpath_prefix("config.logLevel", None)
    assert values == {"config": {"logLevel": None}}


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
    result = _findone(stub_data, path)
    assert result == expected_value


def test_findone_raises_in_case_of_missing_value():
    with pytest.raises(AttributeError):
        _findone(stub_data, "a.missing-key")


@pytest.mark.parametrize(
    "path,expected_value",
    [
        ("a.b", ["value"]),
        ("a.c", [None]),
        ("a.*", ["value", None]),
    ],
)
def test_findall_returns_all_found_objects_in_a_list(path, expected_value):
    result = _findall(stub_data, path)
    assert result == expected_value


def test_findall_returns_empty_list_in_case_of_missing_value():
    result = _findall(stub_data, "a.missing-key")
    assert result == []
