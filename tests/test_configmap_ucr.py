from yaml import safe_load

from utils import findone


def test_mounts_configmap_ucr(helm, chart_test_deployment):
    values = safe_load("""
      global:
        configMapUcr: test-configmap
    """)
    result = helm.helm_template(chart_test_deployment, values)

    deployment = helm.get_resource(
        result,
        kind="Deployment",
        name="release-name-test-deployment",
    )

    expected_volumes = [
        {
            "configMap": {
                "name": "test-configmap",
            },
            "name": "config-map-ucr",
        },
    ]
    assert findone(deployment, "spec.template.spec.volumes") == expected_volumes

    expected_volume_mounts = [
        {
            "mountPath": "/etc/univention/base.conf",
            "name": "config-map-ucr",
            "subPath": "base.conf",
        },
    ]
    assert findone(deployment, "spec.template.spec.containers[0].volumeMounts") == expected_volume_mounts
