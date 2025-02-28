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
