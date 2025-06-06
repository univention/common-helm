
# SPDX-FileCopyrightText: 2024 Univention GmbH
# SPDX-License-Identifier: AGPL-3.0-only

import re

from pytest_helm.utils import load_yaml


def test_mounts_configmap_ucr(helm, chart_path):
    """Test that charts which have `mountUcr: true` get the UCR's base*.conf file mounted."""
    values = load_yaml(
        """
      mountUcr: true
      global:
        configMapUcrDefaults: test-configmap-defaults
        configMapUcr: test-configmap
        configMapUcrForced: test-configmap-forced
    """,
    )
    result = helm.helm_template(chart_path, values)
    deployment = result.get_resource(kind="Deployment")

    expected_volumes = [
        {
            "configMap": {
                "name": "test-configmap-defaults",
            },
            "name": "config-map-ucr-defaults",
        },
        {
            "configMap": {
                "name": "test-configmap",
            },
            "name": "config-map-ucr",
        },
        {
            "configMap": {
                "name": "test-configmap-forced",
            },
            "name": "config-map-ucr-forced",
        },
    ]
    assert deployment.findone("spec.template.spec.volumes") == expected_volumes

    expected_volume_mounts = [
        {
            "mountPath": "/etc/univention/base-defaults.conf",
            "name": "config-map-ucr-defaults",
            "subPath": "base.conf",
        },
        {
            "mountPath": "/etc/univention/base.conf",
            "name": "config-map-ucr",
            "subPath": "base.conf",
        },
        {
            "mountPath": "/etc/univention/base-forced.conf",
            "name": "config-map-ucr-forced",
            "subPath": "base.conf",
        },
    ]
    assert (
        deployment.findone("spec.template.spec.containers[0].volumeMounts") ==
        expected_volume_mounts
    )


def test_mounts_no_configmap_ucr(helm, chart_path):
    """Test that charts which have `mountUcr: false` do not get the UCR's base*.conf file mounted."""
    values = load_yaml(
        """
      mountUcr: false
    """,
    )
    result = helm.helm_template(chart_path, values)
    deployment = result.get_resource(kind="Deployment")

    volume_mounts = deployment.findone("spec.template.spec.containers[0].volumeMounts")
    for volume_mount in volume_mounts or []:
        assert not re.match(
            r"/etc/univention/base([^/]*).conf",
            volume_mount["mountPath"],
        )
