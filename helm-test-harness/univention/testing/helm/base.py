# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from pytest_helm.helm import Helm
from pytest_helm.utils import findone
from yaml import safe_load


class Base:
    manifest = ""

    def test_add_another_label(self, helm, chart_path):
        values = safe_load(
            """
            additionalLabels:
              local.test/name: "value"
        """,
        )
        result = helm.helm_template_file(chart_path, values, self.manifest)
        labels = findone(result, "metadata.labels")

        assert labels["local.test/name"] == "value"

    def test_modify_a_common_label(self, helm, chart_path):
        values = safe_load(
            """
            additionalLabels:
              app.kubernetes.io/name: "replaced value"
        """,
        )
        result = helm.helm_template_file(chart_path, values, self.manifest)
        labels = findone(result, "metadata.labels")

        assert labels["app.kubernetes.io/name"] == "replaced value"

    def test_value_is_templated(self, helm: Helm, chart_path):
        values = safe_load(
            """
            global:
              test: "stub-value"
            additionalLabels:
              local.test/name: "{{ .Values.global.test }}"
        """,
        )
        result = helm.helm_template_file(chart_path, values, self.manifest)
        labels = findone(result, "metadata.labels")

        assert labels["local.test/name"] == "stub-value"

    def test_namespaceoverride_takes_precedence_over_release_namespace(self, helm: Helm, chart_path):
        values = {"namespaceOverride": "stub-namespace"}

        result = helm.helm_template_file(chart_path, values, self.manifest)
        assert findone(result, "metadata.namespace")== "stub-namespace"

    def test_namespace_is_release_namespace(self, helm: Helm, chart_path):

        result = helm.helm_template_file(chart_path, {}, self.manifest, ["--set", "namespaceOverride=stub-namespace"])
        assert findone(result, "metadata.namespace")== "stub-namespace"
