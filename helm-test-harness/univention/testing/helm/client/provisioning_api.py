# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from contextlib import nullcontext as does_not_raise
import subprocess

import pytest

from .base import BaseTest


class ProvisioningApi(BaseTest):
    """
    Provisioning API Client configuration checks.
    """

    # TODO: Check what's needed
    config_map_name = None
    secret_name = "release-name-test-nubus-common-provisioning-api"

    default_username = "stub-values-username"

    path_main_container = "spec.template.spec.containers[?@.name=='main']"
    path_provisioning_api_url = "data.PROVISIONING_API_URL"
    path_provisioning_api_username = "data.PROVISIONING_API_USERNAME"

    env_password = "PROVISIONING_API_PASSWORD"

    def test_connection_url_is_required(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              connection:
                url: null
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "connection has to be configured" in error.value.stderr

    def test_connection_url_is_templated(self, chart):
        values = self.load_and_map(
            """
            global:
              test: "stub_value"
            provisioningApi:
              connection:
                url: "{{ .Values.global.test }}"
            """)
        result = chart.helm_template(values)
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        assert config_map.findone(self.path_provisioning_api_url) == "stub_value"

    def test_auth_plain_values_generate_secret(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              auth:
                username: "stub-username"
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)

        assert secret.findone("stringData.password") == "stub-password"

    def test_auth_plain_values_provide_username_via_config_map(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              auth:
                username: "stub-username"
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        assert config_map.findone(self.path_provisioning_api_username) == "stub-username"

    def test_auth_plain_values_username_is_templated(self, chart):
        values = self.load_and_map(
            """
            global:
              test: "stub-value"
            provisioningApi:
              auth:
                username: "{{ .Values.global.test }}"
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        assert config_map.findone(self.path_provisioning_api_username) == "stub-value"

    def test_auth_plain_values_password_is_not_templated(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              auth:
                username: "stub-username"
                password: "{{ value }}"
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        assert secret.findone("stringData.password") == "{{ value }}"

    def test_auth_plain_values_password_is_required(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              auth:
                username: "stub-username"
                password: null
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "password has to be supplied" in error.value.stderr

    def test_auth_username_is_required(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
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
            provisioningApi:
              auth:
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        assert config_map.findone(self.path_provisioning_api_username) == self.default_username

    def test_auth_existing_secret_does_not_generate_a_secret(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              auth:
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        with pytest.raises(LookupError):
            result.get_resource(kind="Secret", name=self.secret_name)

    def test_auth_existing_secret_does_not_require_plain_password(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              auth:
                password: null
                existingSecret:
                  name: "stub-secret-name"
            """)
        with does_not_raise():
            chart.helm_template(values)

    def test_auth_existing_secret_used_to_populate_environment_variables(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              auth:
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        main_container = workload.findone(self.path_main_container)

        password = main_container.findone(f"env[?@name=='{self.env_password}']")
        assert password.findone("valueFrom.secretKeyRef.name") == "stub-secret-name"

    def test_auth_existing_secret_uses_correct_default_key(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              auth:
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        main_container = workload.findone(self.path_main_container)

        password = main_container.findone(f"env[?@name=='{self.env_password}']")
        assert password.findone("valueFrom.secretKeyRef.key") == "password"

    def test_auth_existing_secret_uses_correct_custom_key(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              auth:
                existingSecret:
                  name: "stub-secret-name"
                  keyMapping:
                    password: "stub_password_key"
            """)
        result = chart.helm_template(values)
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        main_container = workload.findone(self.path_main_container)

        password = main_container.findone(f"env[?@name=='{self.env_password}']")
        assert password.findone("valueFrom.secretKeyRef.key") == "stub_password_key"

    def test_auth_existing_secret_has_precedence(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              auth:
                password: "stub-password"
                existingSecret:
                  name: "stub-secret-name"
                  keyMapping:
                    password: "stub_password_key"
            """)
        result = chart.helm_template(values)
        with pytest.raises(LookupError):
            result.get_resource(kind="Secret", name=self.secret_name)

        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        main_container = workload.findone(self.path_main_container)

        password = main_container.findone(f"env[?@name=='{self.env_password}']")
        assert password.findone("valueFrom.secretKeyRef.key") == "stub_password_key"

    def test_auth_disabling_existing_secret_by_setting_it_to_null(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              auth:
                username: "stub-username"
                password: "stub-password"
                existingSecret: null
            """)
        result = chart.helm_template(values)
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        main_container = workload.findone(self.path_main_container)

        password = main_container.findone(f"env[?@name=='{self.env_password}']")
        assert password.findone("valueFrom.secretKeyRef.name") == self.secret_name
        assert password.findone("valueFrom.secretKeyRef.key") == "password"

    def test_global_secrets_keep_is_ignored(self, chart):
        """
        Keeping Secrets shall not be supported in Client role.

        Random values for a password will never be generated when in Client
        role. This is why the configuration `global.secrets.keep` shall not
        have any effect on Secrets in Client role.
        """
        values = self.load_and_map(
            """
            global:
              secrets:
                keep: true

            provisioningApi:
              auth:
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        annotations = secret.findone("metadata.annotations", default={})
        helm_resource_policy = annotations.get("helm.sh/resource-policy")
        assert helm_resource_policy != "keep"
