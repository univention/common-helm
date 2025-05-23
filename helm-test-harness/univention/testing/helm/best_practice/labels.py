# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from yaml import safe_load


class Labels:
    """
    Checks the common labels behavior expected for all chart resources.
    """

    def test_additional_labels_add_another_label(self, chart, subtests):
        values = safe_load(
            """
            additionalLabels:
              local.test/name: "value"
            """)
        result = chart.helm_template(values)
        for resource in result:
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                labels = resource.findone("metadata.labels")
                assert labels["local.test/name"] == "value"

    def test_additional_labels_modify_a_common_label(self, chart, subtests):
        values = safe_load(
            """
            additionalLabels:
              app.kubernetes.io/name: "replaced value"
            """)
        result = chart.helm_template(values)
        for resource in result:
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                labels = resource.findone("metadata.labels")
                assert labels["app.kubernetes.io/name"] == "replaced value"

    def test_additional_labels_value_is_templated(self, chart, subtests):
        values = safe_load(
            """
            global:
              test: "stub-value"
            additionalLabels:
              local.test/name: "{{ .Values.global.test }}"
            """)
        result = chart.helm_template(values)
        for resource in result:
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                labels = resource.findone("metadata.labels")
                assert labels["local.test/name"] == "stub-value"
