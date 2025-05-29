import yaml

from pytest_helm._yaml import CustomSafeLoader
from pytest_helm.models import HelmTemplateResult

stub_helm_output = """
---
kind: Deployment
metadata:
    name: "stub-deployment"

---
kind: ConfigMap
metadata:
    name: "stub-config-map"
"""


def test_records_resource_access():
    data = yaml.load_all(stub_helm_output, Loader=CustomSafeLoader)
    result = HelmTemplateResult(data)
    deployment = result.get_resource(kind="Deployment")

    assert result._accessed_resources == [deployment]
