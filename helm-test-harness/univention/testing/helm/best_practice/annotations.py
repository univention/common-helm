# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from pytest_helm.utils import load_yaml


class Annotations:
    """
    Checks the common annotations behavior expected for all chart resources.

    This is based on the suggestion from the best practices chart of openDesk:
    https://gitlab.opencode.de/bmi/opendesk/components/platform-development/charts/opendesk-best-practises
    """

    def test_additional_annotations_add_another_annotation(self, chart, subtests):
        values = load_yaml(
            """
            additionalAnnotations:
              local.test/name: "value"
            """)
        result = chart.helm_template(values)
        for resource in result:
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                annotations = resource.findone("metadata.annotations", default={})
                assert annotations["local.test/name"] == "value"

    def test_additional_annotations_value_is_templated(self, chart, subtests):
        values = load_yaml(
            """
            global:
              test: "stub-value"
            additionalAnnotations:
              local.test/name: "{{ .Values.global.test }}"
            """)
        result = chart.helm_template(values)
        for resource in result:
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                annotations = resource.findone("metadata.annotations")
                assert annotations["local.test/name"] == "stub-value"
