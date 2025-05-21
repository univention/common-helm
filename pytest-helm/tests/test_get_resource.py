import pytest

from pytest_helm.models import HelmTemplateResult


@pytest.fixture
def resources():
    return HelmTemplateResult(
        [
            {
                "apiVersion": "test/v1alpha1",
                "kind": "kind1",
                "metadata": {
                    "name": "test1",
                },
                "id": 1,
            },
            {
                "apiVersion": "test/v1",
                "kind": "kind1",
                "metadata": {
                    "name": "test2",
                },
                "id": 2,
            },
            {
                "apiVersion": "test/v1",
                "kind": "kind2",
                "metadata": {
                    "name": "test1",
                },
                "id": 3,
            },
        ],
    )


def test_get_resources_by_api_version(helm, resources):
    resources = resources.get_resources(api_version="test/v1")
    assert len(resources) == 2
    assert resources[0]["id"] == 2
    assert resources[1]["id"] == 3


def test_get_resources_by_kind(helm, resources):
    resources = resources.get_resources(kind="kind1")
    assert len(resources) == 2
    assert resources[0]["id"] == 1
    assert resources[1]["id"] == 2


def test_get_resources_by_name(helm, resources):
    resources = resources.get_resources(name="test1")
    assert len(resources) == 2
    assert resources[0]["id"] == 1
    assert resources[1]["id"] == 3


def test_get_resources_by_predicate(helm, resources):
    resources = resources.get_resources(predicate=lambda doc: doc["id"] == 2)
    assert len(resources) == 1
    assert resources[0]["id"] == 2


def test_get_resources(helm, resources):
    resources = resources.get_resources(kind="kind1")
    assert len(resources) == 2


def test_get_resource(helm, resources):
    resource = resources.get_resource(kind="kind1", name="test2")
    assert resource["kind"] == "kind1"
    assert resource["metadata"]["name"] == "test2"
    assert resource["id"] == 2


def test_get_resource_not_found(helm, resources):
    with pytest.raises(LookupError) as e:
        resources.get_resource(kind="kind1", name="notfound")
    assert "No manifest found" in str(e)


def test_get_resource_multiple_found(helm, resources):
    with pytest.raises(LookupError) as e:
        resources.get_resource(kind="kind1")
    assert "More than one manifest found" in str(e)
