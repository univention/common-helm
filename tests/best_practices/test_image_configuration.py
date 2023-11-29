from yaml import safe_load

from utils import findone


def test_global_registry_is_used_as_default(helm, chart_path):
    values = safe_load("""
        global:
          imageRegistry: "stub-global-registry"
    """)
    result = helm.helm_template(chart_path, values)
    deployment = helm.get_resource(result, kind="Deployment")

    expected_registry = "stub-global-registry"
    image = findone(deployment, "spec.template.spec.containers[0].image")
    assert image.startswith(expected_registry + "/")
