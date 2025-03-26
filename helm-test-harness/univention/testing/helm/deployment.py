# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from yaml import safe_load

from pytest_helm.utils import get_containers
from univention.testing.helm.base import Labels, Namespace


class Deployment(Labels, Namespace):

    def test_pod_security_context_can_be_disabled(self, helm, chart_path):
        values = self.add_prefix(
            safe_load(
                """
            podSecurityContext:
              enabled: false
              fsGroup: 1000
              fsGroupChangePolicy: "Always"
            """,
            ),
        )
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        pod_spec = deployment["spec"]["template"]["spec"]

        assert "securityContext" not in pod_spec.keys()

    def test_pod_security_context_is_applied(self, helm, chart_path):
        values = self.add_prefix(
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
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        pod_security_context = deployment["spec"]["template"]["spec"]["securityContext"]
        expected_security_context = {
            "fsGroup": 1000,
            "fsGroupChangePolicy": "Always",
            "sysctls": None,
        }
        _compare_dict(pod_security_context, expected_security_context, 'pod')

    def test_container_security_context_can_be_disabled(self, helm, chart_path):
        values = self.add_prefix(
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
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        containers = get_containers(deployment)
        _assert_all_have_security_context(containers, expected_security_context)

    def test_container_security_context_is_applied(self, helm, chart_path):
        values = self.add_prefix(
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
            "runAsUser": 9876,
        }

        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        containers = get_containers(deployment)
        _assert_all_have_security_context(containers, expected_security_context)


def _assert_all_have_security_context(containers, expected_security_context):
    for container in containers:
        security_context = container.get("securityContext", {})
        name = container["name"]

        _compare_dict(security_context, expected_security_context, name)


def _compare_dict(actual: dict, expected: dict, container: str, invalid_keys: set = ['enabled']):
    '''Compare values in actual dict with value in expected

       We do not know which keys are set from outside so ignore additional keys.
       Also make sure that if a value is None it is the same as if the key is missing,
       helm templates has some special handling here if a key is overriden with null. If
       it was available previously the key will be removed but if it was not available the
       key will be available with value None.
    '''
    for key in invalid_keys:
        assert (key not in actual), f'Invalid key {key} in {container} security context'

    for key, value in expected.items():
        assert (
            key in actual or value is None
        ), f'Failed to find expected key {key} in {container} security context'

        if key not in actual:
            continue

        if isinstance(value, dict):
            _compare_dict(actual[key], value, container, [])
        else:
            assert (
                actual[key] == value
            ), f'Values of {key} in {container} security context do not match: actual: {actual[key]}, expected: {value}'
