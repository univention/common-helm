from subprocess import CompletedProcess

import pytest

from pytest_helm._yaml import KubernetesResource, YamlMapping
from pytest_helm.helm import Helm

stub_stdout = """
---
apiVersion: stub.test/v1
kind: Stub
metadata:
  name: first

---
apiVersion: stub.test/v1
kind: Stub
metadata:
  name: second
"""


@pytest.fixture
def run_result():
    return CompletedProcess(["helm", "template", "stub-chart"], 0, stdout=stub_stdout, stderr="")


@pytest.fixture(autouse=True)
def mock_run_command(mocker, run_result):
    mocker.patch("pytest_helm.helm.Helm._run_command", return_value=run_result)


def test_get_resource_can_be_used_multiple_times_on_the_same_result(mocker):
    helm = Helm()

    result = helm.helm_template("stub-chart")
    first_resource = result.get_resources(name="first")
    second_resource = result.get_resources(name="second")

    assert first_resource
    assert second_resource


def test_helm_template_does_not_dump_output(mocker, capsys):
    helm = Helm()

    helm.helm_template("stub-chart")
    output = capsys.readouterr()
    assert stub_stdout not in output.out


def test_helm_template_dumps_output_when_enabled(mocker, capsys):
    helm = Helm(debug=True)

    result = helm.helm_template("stub-chart")
    assert stub_stdout in result.stdout


def test_helm_template_returns_yaml_mappings_for_maps(mocker):
    helm = Helm()

    result = helm.helm_template("stub-chart")
    resource = result.get_resource(name="first")
    assert isinstance(resource, YamlMapping)
    assert isinstance(resource["metadata"], YamlMapping)


def test_helm_template_returns_kubernetes_resource(mocker):
    helm = Helm()

    result = helm.helm_template("stub-chart")
    resource = result.get_resource(name="first")
    assert isinstance(resource, KubernetesResource)
    assert isinstance(resource["metadata"], YamlMapping)


def test_helm_template_result_allows_to_get_resources(mocker):
    helm = Helm()

    result = helm.helm_template("stub-chart")
    resource = result.get_resources(kind="Stub")
    assert len(resource) == 2


def test_helm_template_result_allows_to_get_single_resource(mocker):
    helm = Helm()

    result = helm.helm_template("stub-chart")
    resource = result.get_resource(name="first")
    assert resource


def test_helm_template_result_has_values_as_yaml_string():
    helm = Helm()
    result = helm.helm_template("stub-chart", {"stub": "value"})
    assert result.values == "stub: value\n"
