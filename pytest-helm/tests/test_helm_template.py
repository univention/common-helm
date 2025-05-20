from pytest_helm._yaml import HelmResource
from pytest_helm.helm import Helm

stub_output = b"""
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
"""


def test_get_resource_can_be_used_multiple_times_on_the_same_result(mocker):
    mocker.patch("pytest_helm.helm.Helm.run_command", return_value=stub_output)
    helm = Helm()

    result = helm.helm_template("stub-chart")
    first_resource = helm.get_resources(result, name="first")
    second_resource = helm.get_resources(result, name="second")

    assert first_resource
    assert second_resource


def test_helm_template_does_not_dump_output(mocker, capsys):
    mocker.patch("pytest_helm.helm.Helm.run_command", return_value=stub_output)
    helm = Helm()

    helm.helm_template("stub-chart")
    output = capsys.readouterr()
    assert stub_output.decode() not in output.out


def test_helm_template_dumps_output_when_enabled(mocker, capsys):
    mocker.patch("pytest_helm.helm.Helm.run_command", return_value=stub_output)
    helm = Helm(debug=True)

    helm.helm_template("stub-chart")
    output = capsys.readouterr()
    assert stub_output.decode() in output.out


def test_helm_template_returns_helm_resources_for_maps(mocker):
    mocker.patch("pytest_helm.helm.Helm.run_command", return_value=stub_output)
    helm = Helm()

    result = helm.helm_template("stub-chart")
    resource = helm.get_resource(result, name="first")
    assert isinstance(resource, HelmResource)
    assert isinstance(resource["metadata"], HelmResource)
