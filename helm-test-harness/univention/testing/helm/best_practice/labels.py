# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from collections.abc import Iterable

from pytest_helm.models import HelmTemplateResult
from pytest_helm.utils import load_yaml


class Labels:
    """
    Checks the common labels behavior expected for all chart resources.

    This is based on the suggestion from the best practices chart of openDesk:
    https://gitlab.opencode.de/bmi/opendesk/components/platform-development/charts/opendesk-best-practises
    """

    def test_additional_labels_add_another_label(self, chart, subtests):
        values = load_yaml(
            """
            additionalLabels:
              local.test/name: "value"
            """)
        result = chart.helm_template(values)
        for resource in self.resources_to_check(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                labels = resource.findone("metadata.labels")
                assert labels["local.test/name"] == "value"

    def test_additional_labels_modify_a_common_label(self, chart, subtests):
        values = load_yaml(
            """
            additionalLabels:
              app.kubernetes.io/name: "replaced value"
            """)
        result = chart.helm_template(values)
        for resource in self.resources_to_check(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                labels = resource.findone("metadata.labels")
                assert labels["app.kubernetes.io/name"] == "replaced value"

    def test_additional_labels_value_is_templated(self, chart, subtests):
        values = load_yaml(
            """
            global:
              test: "stub-value"
            additionalLabels:
              local.test/name: "{{ .Values.global.test }}"
            """)
        result = chart.helm_template(values)
        for resource in self.resources_to_check(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                labels = resource.findone("metadata.labels")
                assert labels["local.test/name"] == "stub-value"

    def resources_to_check(self, resources: HelmTemplateResult) -> Iterable[HelmTemplateResult]:
        """
        Allows to filter resources in subclasses.
        """
        return resources
