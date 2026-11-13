# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


from pytest_helm.utils import load_yaml

from .base import BestPracticeBase


POD_TEMPLATE_PATHS = {
    "CronJob": "spec.jobTemplate.spec.template.metadata.labels",
    "DaemonSet": "spec.template.metadata.labels",
    "Deployment": "spec.template.metadata.labels",
    "Job": "spec.template.metadata.labels",
    "ReplicaSet": "spec.template.metadata.labels",
    "StatefulSet": "spec.template.metadata.labels",
}

SELECTOR_LABELS = ("app.kubernetes.io/name", "app.kubernetes.io/instance")


class Labels(BestPracticeBase):
    """
    Checks the common labels behavior expected for all chart resources.

    This is based on the suggestion from the best practices chart of openDesk:
    https://gitlab.opencode.de/bmi/opendesk/components/platform-development/charts/opendesk-best-practises

    The pod template of a workload counts as a resource of its own,
    because NetworkPolicies and Services select pods by these labels.
    """

    def labels_to_check(self, result, pod_templates=True):
        """
        Yields the resource and the path of its labels, plus the pod template's labels of every workload.
        """
        for resource in self.resources_to_check(result):
            yield resource, "metadata.labels"
            if pod_templates and resource["kind"] in POD_TEMPLATE_PATHS:
                yield resource, POD_TEMPLATE_PATHS[resource["kind"]]

    def test_additional_labels_add_another_label(self, chart, subtests):
        values = load_yaml(
            """
            additionalLabels:
              local.test/name: "value"
            """)
        result = chart.helm_template(values)
        for resource, path in self.labels_to_check(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"], path=path):
                labels = resource.findone(path)
                assert labels["local.test/name"] == "value"

    def test_additional_labels_modify_a_common_label(self, chart, subtests):
        values = load_yaml(
            """
            additionalLabels:
              app.kubernetes.io/name: "replaced value"
            """)
        result = chart.helm_template(values)
        # Selectors, Services and NetworkPolicies match pods by their name label, so pods keep it.
        for resource, path in self.labels_to_check(result, pod_templates=False):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"], path=path):
                labels = resource.findone(path)
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
        for resource, path in self.labels_to_check(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"], path=path):
                labels = resource.findone(path)
                assert labels["local.test/name"] == "stub-value"

    def test_additional_labels_keep_the_selector_labels_of_pods(self, chart, subtests):
        # Selectors, Services and NetworkPolicies match pods by these, and a Deployment's selector is immutable.
        default = {
            (resource["kind"], resource["metadata"]["name"]): resource
            for resource in self.resources_to_check(chart.helm_template())
        }
        values = load_yaml(
            """
            additionalLabels:
              app.kubernetes.io/name: "replaced value"
              app.kubernetes.io/instance: "replaced value"
            """)
        result = chart.helm_template(values)
        for resource, path in self.labels_to_check(result):
            if path == "metadata.labels":
                continue
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"], path=path):
                labels = resource.findone(path)
                expected = default[(resource["kind"], resource["metadata"]["name"])].findone(path)
                for key in SELECTOR_LABELS:
                    assert labels[key] == expected[key]
