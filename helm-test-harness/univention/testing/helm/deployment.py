# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import pytest
from yaml import safe_load

from pytest_helm.utils import get_containers


class Deployment:  # Labels): # TODO: Decide if we want labels on Deployments and statefulsets
    manifest = ""

    def values(self, localpart: dict) -> dict:
        return localpart

    def test_pod_security_context_can_be_disabled(self, helm, chart_path):
        values = self.values(
            safe_load(
                """
            podSecurityContext:
              enabled: false
              fsGroup: 1000
              fsGroupChangePolicy: "Always"
            """,
            ),
        )
        deployment = helm.helm_template_file(chart_path, values, self.manifest)
        pod_spec = deployment["spec"]["template"]["spec"]

        with pytest.raises(KeyError):
            pod_spec["securityContext"]

    def test_pod_security_context_is_applied(self, helm, chart_path):
        values = self.values(
            safe_load(
                """
            podSecurityContext:
              enabled: true
              fsGroup: 1000
              fsGroupChangePolicy: "Always"
              sysctls: null
            """,
            ),
        )
        deployment = helm.helm_template_file(chart_path, values, self.manifest)
        pod_security_context = deployment["spec"]["template"]["spec"]["securityContext"]
        expected_security_context = {
            "enabled": True,
            "fsGroup": 1000,
            "fsGroupChangePolicy": "Always",
            "sysctls": None,
        }
        assert pod_security_context == expected_security_context

    def test_container_security_context_can_be_disabled(self, helm, chart_path):
        values = self.values(
            safe_load(
                """
            containerSecurityContext:
              enabled: false
              capabilities:
                drop: []
              runAsUser: 9876
            """,
            ),
        )
        expected_security_context = {}
        deployment = helm.helm_template_file(chart_path, values, self.manifest)
        containers = get_containers(deployment)
        self._assert_all_have_security_context(containers, expected_security_context)

    def test_container_security_context_is_applied(self, helm, chart_path):
        values = self.values(
            safe_load(
                """
            containerSecurityContext:
              enabled: true
              capabilities:
                drop: []
              runAsUser: 9876
            """,
            ),
        )
        expected_security_context = {
            "capabilities": {
                "drop": [],
            },
            "enabled": True,
            "runAsUser": 9876,
        }

        deployment = helm.helm_template_file(chart_path, values, self.manifest)
        containers = get_containers(deployment)
        self._assert_all_have_security_context(containers, expected_security_context)

    def _assert_all_have_security_context(self, containers, expected_security_context):
        for container in containers:
            security_context = container.get("securityContext", {})
            name = container["name"]
            assert (
                security_context.keys() >= expected_security_context.keys()
            ), f'Wrong securityContext in container "{name}"'
            assert (
                security_context.items() >= expected_security_context.items()
            ), f'Wrong securityContext in container "{name}"'
