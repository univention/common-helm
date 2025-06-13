# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from contextlib import nullcontext as does_not_raise
import subprocess

import pytest

from .base import BaseTest


class Auth(BaseTest):
    """
    Memcached Client configuration.
    """

    config_map_name = "release-name-test-client-config"
    secret_name = "release-name-test-client-config-memcached"

    default_username = "stub-values-username"
    secret_default_key = "password"

    path_main_container = "spec.template.spec.containers[?@.name=='main']"
    path_username = "data.MEMCACHED_USERNAME"

    def get_username(self, result):
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        return config_map.findone(self.path_username)

    def assert_username_value(self, result, value):
        username = self.get_username(result)
        assert username == value

    def assert_correct_secret_usage(self, result, *, name=None, key=None):
        raise NotImplementedError("Use one of the mixins or implement this method.")

    def test_auth_plain_values_generate_secret(self, chart):
        values = self.load_and_map(
            """
            memcached:
              auth:
                username: "stub-username"
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        assert secret.findone("stringData.password") == "stub-password"

    def test_auth_plain_values_provide_username(self, chart):
        values = self.load_and_map(
            """
            memcached:
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

            memcached:
              auth:
                username: "{{ .Values.global.test }}"
                password: "stub-password"
        """,
        )
        result = chart.helm_template(values)
        self.assert_username_value(result, "stub-value")

    def test_auth_plain_values_password_is_not_templated(self, chart):
        values = self.load_and_map(
            """
            memcached:
              auth:
                username: "stub-username"
                password: "{{ value }}"
        """,
        )
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        assert secret.findone("stringData.password") == "{{ value }}"

    def test_auth_plain_values_password_is_required(self, chart):
        values = self.load_and_map(
            """
            memcached:
              auth:
                username: "stub-username"
                password: null
        """,
        )
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "password has to be supplied" in error.value.stderr

    def test_auth_username_is_required(self, chart):
        values = self.load_and_map(
            """
            memcached:
              auth:
                username: null
                password: "stub-password"
        """,
        )
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "username has to be supplied" in error.value.stderr

    def test_auth_username_has_default(self, chart):
        values = self.load_and_map(
            """
            memcached:
              auth:
                password: "stub-password"
        """,
        )
        result = chart.helm_template(values)
        self.assert_username_value(result, self.default_username)

    def test_auth_existing_secret_does_not_generate_a_secret(self, chart):
        values = self.load_and_map(
            """
            memcached:
              auth:
                username: "stub-username"
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        with pytest.raises(LookupError):
            result.get_resource(kind="Secret", name=self.secret_name)

    def test_auth_existing_secret_does_not_require_plain_password(self, chart):
        values = self.load_and_map(
            """
            memcached:
              auth:
                password: null
                existingSecret:
                  name: "stub-secret-name"
            """)
        with does_not_raise():
            chart.helm_template(values)

    def test_auth_existing_secret_uses_password(self, chart):
        values = self.load_and_map(
            """
            memcached:
              auth:
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, name="stub-secret-name")

    def test_auth_existing_secret_uses_correct_default_key(self, chart):
        values = self.load_and_map(
            """
            memcached:
              auth:
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, key=self.secret_default_key)

    def test_auth_existing_secret_uses_correct_custom_key(self, chart):
        values = self.load_and_map(
            """
            memcached:
              auth:
                existingSecret:
                  name: "stub-secret-name"
                  keyMapping:
                    password: "stub_password_key"
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, key="stub_password_key")

    def test_auth_disabling_existing_secret_by_setting_it_to_null(self, chart):
        values = self.load_and_map(
            """
            memcached:
              auth:
                username: "stub-username"
                password: "stub-password"
                existingSecret: null
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, name=self.secret_name, key=self.secret_default_key)

    def test_auth_existing_secret_has_precedence(self, chart):
        values = self.load_and_map(
            """
            memcached:
              auth:
                password: "stub-plain-password"
                existingSecret:
                  name: "stub-secret-name"
                  keyMapping:
                    password: "stub_password_key"
            """)
        result = chart.helm_template(values)
        with pytest.raises(LookupError):
            result.get_resource(kind="Secret", name=self.secret_name)

        self.assert_correct_secret_usage(result, name="stub-secret-name", key="stub_password_key")

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

            memcached:
              auth:
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        annotations = secret.findone("metadata.annotations", default={})
        helm_resource_policy = annotations.get("helm.sh/resource-policy")
        assert helm_resource_policy != "keep"


class SecretUsageViaEnv:
    """
    Mixin which implements the expected Secret usage via environment variables.
    """

    sub_path_env_password = "env[?@name=='MEMCACHED_PASSWORD']"

    def assert_correct_secret_usage(self, result, *, name=None, key=None):
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        main_container = workload.findone(self.path_main_container)
        password = main_container.findone(self.sub_path_env_password)

        if name:
            assert password.findone("valueFrom.secretKeyRef.name") == name

        if key:
            assert password.findone("valueFrom.secretKeyRef.key") == key


class SecretUsageViaVolume:
    """
    Mixin which implements the expected Secret usage via volume mounts.
    """

    path_volume_secret = "..spec.template.spec.volumes[?@.name=='secret-memcached']"

    sub_path_volume_mount = "volumeMounts[?@.name=='secret-memcached']"

    def assert_correct_secret_usage(self, result, *, name=None, key=None):
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        secret_volume = workload.findone(self.path_volume_secret)
        main_container = workload.findone(self.path_main_container)
        secret_volume_mount = main_container.findone(self.sub_path_volume_mount)

        if name:
            assert secret_volume.findone("secret.secretName") == name

        if key:
            assert secret_volume_mount["subPath"] == key
