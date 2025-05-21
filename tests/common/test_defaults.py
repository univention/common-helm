
# SPDX-FileCopyrightText: 2024 Univention GmbH
# SPDX-License-Identifier: AGPL-3.0-only


def test_nothing_is_mounted_by_default(helm, chart_path):
    result = helm.helm_template(chart_path)
    deployment = result.get_resource(kind="Deployment")

    assert not deployment.findone("spec.template.spec.volumes")
    assert not deployment.findone("spec.template.spec.containers[0].volumeMounts")
