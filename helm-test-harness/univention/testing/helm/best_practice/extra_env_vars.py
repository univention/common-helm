# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from pytest_helm.utils import get_containers

from .base import BestPracticeBase


class ExtraEnvVars(BestPracticeBase):
    """
    Checks extraEnvVars behaviour expected for all chart resources.
    """

    kinds = ("Deployment", "Job", "CronJob")
    """
    Which resource kinds to verify.
    """

    def test_extra_env_vars_can_be_configured(self, chart, subtests):
        """Test that extraEnvVars can be configured"""
        values = self._load_and_map(
            """
            extraEnvVars:
              - name: "FOO"
                value: "bar"
            """,
        )
        result = chart.helm_template(values)
        for containers, resource in self._generate_containers_of_resource_kinds(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                _assert_env_var_exists(containers, "FOO", "bar", resource["metadata"]["name"])

    def test_extra_env_vars_empty_by_default(self, chart, subtests):
        """Test that env sections are omitted when no extraEnvVars are configured"""
        result = chart.helm_template()
        for containers, resource in self._generate_containers_of_resource_kinds(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                _assert_no_empty_env_sections(containers)

    def test_extra_env_vars_multiple_values(self, chart, subtests):
        """Test that multiple extraEnvVars can be configured"""
        values = self._load_and_map(
            """
            extraEnvVars:
              - name: "FOO"
                value: "bar"
              - name: "BAZ"
                value: "qux"
            """,
        )
        result = chart.helm_template(values)
        for containers, resource in self._generate_containers_of_resource_kinds(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                _assert_env_var_exists(containers, "FOO", "bar", resource["metadata"]["name"])
                _assert_env_var_exists(containers, "BAZ", "qux", resource["metadata"]["name"])

    def _generate_containers_of_resource_kinds(self, result):
        for kind in self.kinds:
            resources = result.get_resources(kind=kind)
            for resource in resources:
                containers = get_containers(resource)
                yield containers, resource


def _assert_env_var_exists(containers, name, value, workload_name):
    """Assert all containers have the specified env var with correct value"""
    for container in containers:
        env_var = container.findone(f"env[?@.name=='{name}']")

        assert env_var, (
            f"Container: {container.name} in Workload: {workload_name} does not have extraEnvVars configured correctly."
        )
        assert env_var.get("value") == value, (
            f"{name} has wrong value in container {container.get('name')}"
        )


def _assert_no_empty_env_sections(containers):
    """Assert containers either have no env section or have actual env vars"""
    for container in containers:
        container_name = container.get("name", "")

        if "env" in container:
            env_vars = container.get("env", [])
            assert len(env_vars) > 0, (
                f"Container {container_name} has empty env section - should be omitted"
            )
