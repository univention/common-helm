
# SPDX-FileCopyrightText: 2024 Univention GmbH
# SPDX-License-Identifier: AGPL-3.0-only

from yaml import safe_load

from utils import findone


def test_adds_extra_volumes_to_pod(helm, chart_path):
    values = safe_load(
        """
      extraVolumes:
        - name: custom-entrypoints
          configMap:
            name: ums-umc-customization
            defaultMode: 0555
    """,
    )
    result = helm.helm_template(chart_path, values)
    deployment = result.get_resource(kind="Deployment")

    expected_volumes = values["extraVolumes"]
    assert findone(deployment, "spec.template.spec.volumes") == expected_volumes


def test_adds_extra_volume_mounts_to_containers(helm, chart_path):
    values = safe_load(
        """
      extraVolumeMounts:
        - name: custom-entrypoints
          mountPath: /entrypoint.d/10-pre-entrypoint.sh
          subPath: pre-entrypoint.sh
        - name: custom-entrypoints
          mountPath: /entrypoint.d/90-post-entrypoint.sh
          subPath: post-entrypoint.sh
    """,
    )
    result = helm.helm_template(chart_path, values)
    deployment = result.get_resource(kind="Deployment")

    expected_volume_mounts = values["extraVolumeMounts"]
    assert (
        findone(deployment, "spec.template.spec.containers[0].volumeMounts") ==
        expected_volume_mounts
    )
