from pytest_helm._yaml import CustomYAML
from pytest_helm.utils import add_jsonpath_prefix, get_containers


def test_add_jsonpath_prefix():
    values = add_jsonpath_prefix("config.logLevel", None)
    assert values == {"config": {"logLevel": None}}


def test_get_containers_without_init_containers():
    resource = CustomYAML().load(
        """
        spec:
          template:
            spec:
              containers: []
        """)
    result = get_containers(resource)
    assert result == []

def test_get_containers_returns_init_containers_and_containers():
    resource = CustomYAML().load(
        """
        spec:
          template:
            spec:
              initContainers:
                - stub-init-container
              containers:
                - stub-container
        """)
    result = get_containers(resource)
    assert result == ["stub-init-container", "stub-container"]
