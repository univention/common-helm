# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from pytest_helm.helm import Helm
from pytest_helm.utils import findone
from yaml import safe_load


class Base:
    """
    Base class for helm test harness classes
    It implements utility functions
    that may be overwritten by child classes to adapt a Deployment, Secret... harness.
    To adapt the test to specifics or exceptions of a specific helm chart.
    """
    template_file = ""

    def add_prefix(self, localpart: dict) -> dict:
        """
        Override this method in your subclass to add a prefix to all content of the the test_values.yaml
        a prefix could be for example `{"udm": localpart}` or {"provisioning-api": {"config": localpart}}
        """
        return localpart


    def helm_template_file(self, helm: Helm, chart, values: dict, template_file: str, helm_args: list[str] | None = None) -> dict:
        """
        Templates exactly one helm template yaml file,
        enforces that this one template file renders exactly one kubernetes manifest
        and returns this one kubernetes manifest.

        One manifest per template files is our best-practice.
        Among other things, this makes our tests simpler
        because they don't have to select a specific manifest from a list of manifests.

        For cases where this constraint is not practical, this method can be overwritten by a subclass.
        """
        assert template_file
        result = [ i for i in helm.helm_template(chart, values, template_file, helm_args) if i is not None ]
        assert len(result) <= 1
        if not result:
            return {}
        return result[0]


class Labels(Base):
    """
    Test harness class to validate that an arbitrary kubernetes manifests
    conforms to our standards around `additionalLabels`
    """
    def test_add_another_label(self, helm, chart_path):
        values = self.add_prefix(safe_load(
            """
            additionalLabels:
              local.test/name: "value"
        """,
        ))
        result = self.helm_template_file(helm, chart_path, values, self.template_file)
        labels = findone(result, "metadata.labels")

        assert labels["local.test/name"] == "value"

    def test_modify_a_common_label(self, helm, chart_path):
        values = self.add_prefix(safe_load(
            """
            additionalLabels:
              app.kubernetes.io/name: "replaced value"
        """,
        ))
        result = self.helm_template_file(helm, chart_path, values, self.template_file)
        labels = findone(result, "metadata.labels")

        assert labels["app.kubernetes.io/name"] == "replaced value"

    def test_value_is_templated(self, helm: Helm, chart_path):
        values = self.add_prefix(safe_load(
            """
            global:
              test: "stub-value"
            additionalLabels:
              local.test/name: "{{ .Values.global.test }}"
        """,
        ))
        result = self.helm_template_file(helm, chart_path, values, self.template_file)
        labels = findone(result, "metadata.labels")

        assert labels["local.test/name"] == "stub-value"


class Namespace(Base):

    def test_namespaceoverride_takes_precedence_over_release_namespace(self, helm: Helm, chart_path):
        values = {"namespaceOverride": "stub-namespace"}

        result = self.helm_template_file(helm, chart_path, values, self.template_file)
        assert findone(result, "metadata.namespace")== "stub-namespace"

    def test_namespace_is_release_namespace(self, helm: Helm, chart_path):

        result = self.helm_template_file(helm, chart_path, {}, self.template_file, ["--set", "namespaceOverride=stub-namespace"])
        assert findone(result, "metadata.namespace")== "stub-namespace"
