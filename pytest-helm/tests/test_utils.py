from pytest_helm.utils import add_jsonpath_prefix, get_containers, load_yaml


def test_add_jsonpath_prefix():
    values = add_jsonpath_prefix("config.logLevel", None)
    assert values == {"config": {"logLevel": None}}


def test_get_containers_without_init_containers():
    resource = load_yaml(
        """
        spec:
          template:
            spec:
              containers: []
        """)
    result = get_containers(resource)
    assert result == []

def test_get_containers_returns_init_containers_and_containers():
    resource = load_yaml(
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


def test_get_containers_finds_cron_job_containers():
    resource = load_yaml(
        """
        spec:
          jobTemplate:
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


def test_load_yaml():
    data = load_yaml(
        """
        key: value
        """)
    assert data == {"key": "value"}
