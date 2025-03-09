from pytest_helm.utils import resolve

def test_resolve():
    values = resolve("config.logLevel", None)
    assert values == {"config": {"logLevel": None}}


