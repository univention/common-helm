from utils import findone


def test_adds_extra_volumes_to_pod(helm, chart_test_deployment):
    values = {
        "extraVolumes": [
            {
                "name": "custom-entrypoints",
                "configMap": {
                    "name": "ums-umc-customization",
                    "defaultMode": 0o555,
                },
            },
        ],
    }
    result = helm.helm_template(chart_test_deployment, values)

    deployment = helm.get_resource(
        result,
        kind="Deployment",
        name="release-name-test-deployment",
    )

    expected_volumes = [
        {
            "configMap": {
                "name": "ums-umc-customization",
                "defaultMode": 0o555,
            },
            "name": "custom-entrypoints",
        },
    ]
    assert findone(deployment, "spec.template.spec.volumes") == expected_volumes


def test_adds_extra_volume_mounts_to_containers(helm, chart_test_deployment):
    values = {
        "extraVolumeMounts": [
            {
                "name": "custom-entrypoints",
                "mountPath": "/entrypoint.d/10-pre-entrypoint.sh",
                "subPath": "pre-entrypoint.sh",
            },
            {
                "name": "custom-entrypoints",
                "mountPath": "/entrypoint.d/90-post-entrypoint.sh",
                "subPath": "post-entrypoint.sh",
            },
        ],
    }

    result = helm.helm_template(chart_test_deployment, values)

    deployment = helm.get_resource(
        result,
        kind="Deployment",
        name="release-name-test-deployment",
    )

    expected_volume_mounts = values["extraVolumeMounts"]
    assert findone(deployment, "spec.template.spec.containers[0].volumeMounts") == expected_volume_mounts
