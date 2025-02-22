
# SPDX-FileCopyrightText: 2024 Univention GmbH
# SPDX-License-Identifier: AGPL-3.0-only

from utils import findone


def test_nothing_is_mounted_by_default(helm, chart_path):
    result = helm.helm_template(chart_path)
    deployment = helm.get_resource(result, kind="Deployment")

    assert not findone(deployment, "spec.template.spec.volumes")
    assert not findone(deployment, "spec.template.spec.containers[0].volumeMounts")
