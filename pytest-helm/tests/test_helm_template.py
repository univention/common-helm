import textwrap

import pytest

from pytest_helm._yaml import KubernetesResource, YamlMapping
from pytest_helm.helm import Helm


class StubCompletedProcess:

    stdout = textwrap.dedent("""
        ---
        apiVersion: testing.local/v1
        kind: Stub
        metadata:
          name: first

        ---
        apiVersion: testing.local/v1
        kind: Stub
        metadata:
          name: second
        """)

    stderr = ""


@pytest.fixture(autouse=True)
def mock_run_command(mocker):
    mocker.patch("pytest_helm.helm._run_command", return_value=StubCompletedProcess())


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
    assert StubCompletedProcess.stdout not in output.out


def test_helm_template_dumps_output_when_enabled(mocker, capsys):
    helm = Helm(debug=True)

    helm.helm_template("stub-chart")
    output = capsys.readouterr()
    assert StubCompletedProcess.stdout in output.out


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
