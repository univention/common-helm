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


def test_image_registry_overrides_global_default_registry(helm, chart_path):
    values = safe_load("""
        global:
          imageRegistry: "stub-global-registry"

        image:
          registry: "stub-registry"
    """)
    result = helm.helm_template(chart_path, values)
    deployment = helm.get_resource(result, kind="Deployment")

    expected_registry = "stub-registry"
    image = findone(deployment, "spec.template.spec.containers[0].image")
    assert image.startswith(expected_registry + "/")


def test_global_registry_is_using_knut_registry_per_default(helm, chart_path):
    """
    The UMS Charts point to the internal registry in the knut domain.

    This shall change once the public registry for the publication of UMS stack
    artifacts is in place. Until then the default configuration of all plain
    UMS charts shall use the knut registry by default.
    """
    values = {}
    result = helm.helm_template(chart_path, values)
    deployment = helm.get_resource(result, kind="Deployment")

    expected_registry = "gitregistry.knut.univention.de"
    image = findone(deployment, "spec.template.spec.containers[0].image")
    assert image.startswith(expected_registry + "/")


def test_image_pull_secrets_can_be_provided(helm, chart_path):
    values = safe_load("""
        global:
          imagePullSecrets:
            - "stub-secret-a"
            - "stub-secret-b"
    """)
    result = helm.helm_template(chart_path, values)
    deployment = helm.get_resource(result, kind="Deployment")

    expected_secrets = ["stub-secret-a", "stub-secret-b"]
    image_pull_secrets = findone(deployment, "spec.template.spec.imagePullSecrets")
    assert image_pull_secrets == expected_secrets
