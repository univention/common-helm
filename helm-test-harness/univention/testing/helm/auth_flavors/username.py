# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import subprocess
import pytest
from pytest_helm.models import HelmTemplateResult

from ..client.base import BaseTest


class AuthUsername(BaseTest):
    """
    Partial client test focused on the username configuration.

    Checks the following values:

    - `auth.username`
    """

    default_username = "stub-values-username"

    path_username = "data.USERNAME"

    def get_username(self, result: HelmTemplateResult):
        raise NotImplementedError("Use one of the concrete username implementations")

    def assert_username_value(self, result, value):
        username = self.get_username(result)
        assert username == value

    def test_auth_plain_values_provide_username(self, chart):
        values = self.load_and_map(
            """
            auth:
              username: "stub-username"
              password: "stub-password"
            """)
        result = chart.helm_template(values)
        self.assert_username_value(result, "stub-username")

    def test_auth_plain_values_username_is_templated(self, chart):
        values = self.load_and_map(
            """
            global:
              test: "stub-value"
            auth:
              username: "{{ .Values.global.test }}"
              password: "stub-password"
            """)
        result = chart.helm_template(values)
        self.assert_username_value(result, "stub-value")

    def test_auth_username_is_required(self, chart):
        values = self.load_and_map(
            """
            auth:
              username: null
              password: "stub-password"
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "username has to be supplied" in error.value.stderr

    def test_auth_username_has_default(self, chart):
        values = self.load_and_map(
            """
            auth:
              password: "stub-password"
            """)
        result = chart.helm_template(values)
        self.assert_username_value(result, self.default_username)


class AuthUsernameViaEnv(AuthUsername):
    """
    Mixin which checks the username usage as embedded environment variable.
    """

    sub_path_env_username = "env[?@name=='PROVISIONING_API_USERNAME']"

    def get_username(self, result: HelmTemplateResult):
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        container = workload.findone(self.path_container)
        username = container.findone(self.sub_path_env_username)
        return username["value"]


class AuthUsernameViaConfigMap(AuthUsername):
    """
    Partial client test focused on the username configuration.

    Checks the following values:

    - `auth.username`
    """
    config_map_name = None

    def get_username(self, result: HelmTemplateResult):
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        return config_map.findone(self.path_username)
