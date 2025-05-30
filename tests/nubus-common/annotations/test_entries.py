import pytest
from pytest_helm.utils import load_yaml


def test_merges_values(chart):
    values = load_yaml(
        """
        additionalAnnotations:
          local.test: stub-local-test

        ingress:
          annotations:
            local.test/ingress: stub-ingress
        """)
    result = chart.helm_template(values, template_file="templates/annotations/test_entries.yaml")
    resource = result.get_resource()
    annotations = resource.findone("metadata.annotations")

    assert annotations["local.test"] == "stub-local-test"
    assert annotations["local.test/ingress"] == "stub-ingress"


def test_merged_values_override(chart):
    values = load_yaml(
        """
        additionalAnnotations:
          local.test: stub-additional-annotations

        ingress:
          annotations:
            local.test: stub-ingress-annotations
        """)
    result = chart.helm_template(values, template_file="templates/annotations/test_entries.yaml")
    resource = result.get_resource()
    annotations = resource.findone("metadata.annotations")

    assert annotations["local.test"] == "stub-ingress-annotations"


def test_allows_to_use_values_without_wrapping_in_a_list(chart):
    values = load_yaml(
        """
        additionalAnnotations:
          local.test: stub-local-test
        """)
    result = chart.helm_template(values, template_file="templates/annotations/test_entries_single_value.yaml")
    resource = result.get_resource()
    annotations = resource.findone("metadata.annotations")

    assert annotations["local.test"] == "stub-local-test"


@pytest.mark.parametrize("value, expected_value", [
    ("null", None),
    ("{}", None),
    # NOTE: Setting an empty string is technically invalid, people tend to
    # use the empty string at times to unset a value. This ensures that the
    # implementation is robust in this case.
    ('""', None),
])
def test_renders_no_annotations(chart, value, expected_value):
    values = load_yaml(
        f"""
        additionalAnnotations: {value}
        """)
    result = chart.helm_template(values, template_file="templates/annotations/test_entries_single_value.yaml")
    resource = result.get_resource()
    annotations = resource.findone("metadata.annotations")
    assert annotations == expected_value


def test_values_are_templated(chart):
    values = load_yaml(
        """
        global:
          test: global-value

        additionalAnnotations:
          local.test: "{{ .Values.global.test }}"
        """)
    result = chart.helm_template(values, template_file="templates/annotations/test_entries_single_value.yaml")
    resource = result.get_resource()
    annotations = resource.findone("metadata.annotations")

    assert annotations["local.test"] == "global-value"
