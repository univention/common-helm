import pytest
from pytest_helm.utils import load_yaml


def test_renders_output(chart):
    values = load_yaml(
        """
        additionalAnnotations:
          local.test: stub-local-test
        """)
    result = chart.helm_template(values, template_file="templates/annotations/test_render.yaml")
    resource = result.get_resource()
    annotations = resource.findone("metadata.annotations")

    assert annotations["local.test"] == "stub-local-test"


@pytest.mark.parametrize("value", [
    "{}",
    "null",
    # NOTE: Setting an empty string is technically invalid, people tend to
    # use the empty string at times to unset a value. This ensures that the
    # implementation is robust in this case.
    '""',
])
def test_omits_key_when_no_annotations(chart, value):
    values = load_yaml(
        f"""
        additionalAnnotations: {value}
        """)
    result = chart.helm_template(values, template_file="templates/annotations/test_render.yaml")
    resource = result.get_resource()

    with pytest.raises(KeyError):
        resource.findone("metadata.annotations")


def test_allows_to_use_values_without_wrapping_in_a_list(chart):
    values = load_yaml(
        """
        additionalAnnotations:
          local.test: stub-local-test
        """)
    result = chart.helm_template(values, template_file="templates/annotations/test_render_single_value.yaml")
    resource = result.get_resource()
    annotations = resource.findone("metadata.annotations")

    assert annotations["local.test"] == "stub-local-test"
