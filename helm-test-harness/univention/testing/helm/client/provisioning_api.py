# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from contextlib import nullcontext as does_not_raise
import subprocess

import pytest
from pytest_helm.models import HelmTemplateResult

from .base import BaseTest


class AuthPasswordSecret(BaseTest):
    """
    Partial client test focused only on the Secret generation.

    Checks the following values:

    - `provisioningApi.auth.password`
    """

    secret_name = "release-name-test-nubus-common-provisioning-api"
    path_password = "stringData.password"

    def get_password(self, result: HelmTemplateResult):
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        return secret.findone(self.path_password)

    def assert_password_value(self, result: HelmTemplateResult, value: str):
        password = self.get_password(result)
        assert password == value

    def test_auth_plain_values_generate_secret(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              auth:
                username: "stub-username"
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        self.assert_password_value(result, "stub-password")

    def test_auth_plain_values_password_is_not_templated(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              auth:
                username: "stub-username"
                password: "{{ value }}"
            """)
        result = chart.helm_template(values)
        self.assert_password_value(result, "{{ value }}")

    def test_auth_plain_values_password_is_required(self, chart):
        if self.is_secret_owner:
            pytest.skip(reason="Chart is Secret owner.")
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

    def test_auth_existing_secret_has_precedence_no_secret_generated(self, chart):
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

    def test_global_secrets_keep_is_ignored(self, chart):
        """
        Keeping Secrets shall not be supported in Client role.

        Random values for a password will never be generated when in Client
        role. This is why the configuration `global.secrets.keep` shall not
        have any effect on Secrets in Client role.
        """
        if self.is_secret_owner:
            pytest.skip(reason="Chart is Secret owner.")
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


class AuthPasswordUsage(BaseTest):
    """
    Partial client test focused only on the Secret usage.

    Checks the following values:

    - `provisioningApi.auth.existingSecret`
    """

    secret_name = "release-name-test-nubus-common-provisioning-api"
    secret_default_key = "password"

    def assert_correct_secret_usage(self, result, *, name=None, key=None):
        raise NotImplementedError("Use one of the mixins or implement this method.")

    def test_auth_existing_secret_used(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              auth:
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, name="stub-secret-name")

    def test_auth_existing_secret_uses_correct_default_key(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              auth:
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, key=self.secret_default_key)

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
        self.assert_correct_secret_usage(result, key="stub_password_key")

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
        self.assert_correct_secret_usage(result, name="stub-secret-name", key="stub_password_key")

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
        self.assert_correct_secret_usage(result, name=self.secret_name, key="password")


class AuthPassword(AuthPasswordSecret, AuthPasswordUsage):
    pass


class AuthPasswordOwner:
    """
    Mixin to configure the test template class to own the checked Secret.

    See: `DefaultAttributes.is_secret_owner`
    """

    is_secret_owner = True

    derived_password = "stub-derived-value"

    def test_auth_password_has_random_value(self, chart):
        if not self.is_secret_owner:
            pytest.skip(reason="Chart is not the Secret owner.")
        values = self.load_and_map(
            """
            provisioningApi:
              auth:
                password: null
            """)
        result = chart.helm_template(values)
        password = self.get_password(result)
        result_2 = chart.helm_template(values)
        password_2 = self.get_password(result_2)

        assert password != password_2

    def test_auth_password_is_derived_from_master_password(self, chart):
        if not self.is_secret_owner:
            pytest.skip(reason="Chart is not the Secret owner.")
        values = self.load_and_map(
            """
            global:
              secrets:
                masterPassword: "stub-master-password"

            provisioningApi:
              auth:
                password: null
            """)
        result = chart.helm_template(values)
        self.assert_password_value(result, self.derived_password)

    def test_global_secrets_keep_is_respected(self, chart):
        if not self.is_secret_owner:
            pytest.skip(reason="Chart is not the Secret owner.")
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
        assert helm_resource_policy == "keep"


class AuthUsername(BaseTest):
    """
    Partial client test focused on the username configuration.

    Checks the following values:

    - `provisioningApi.auth.username`
    """

    config_map_name = None

    default_username = "stub-values-username"

    path_username = "data.PROVISIONING_API_USERNAME"

    def get_username(self, result: HelmTemplateResult):
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        return config_map.findone(self.path_username)

    def assert_username_value(self, result, value):
        username = self.get_username(result)
        assert username == value

    def test_auth_plain_values_provide_username(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
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
            provisioningApi:
              auth:
                username: "{{ .Values.global.test }}"
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        self.assert_username_value(result, "stub-value")

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
        self.assert_username_value(result, self.default_username)


class UsernameViaEnv:
    """
    Mixin which checks the username usage as embedded environment variable.
    """

    sub_path_env_username = "env[?@name=='PROVISIONING_API_USERNAME']"

    def get_username(self, result: HelmTemplateResult):
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        container = workload.findone(self.path_container)
        username = container.findone(self.sub_path_env_username)
        return username["value"]


class Auth(AuthPassword, AuthUsername):
    pass


class SecretViaEnv:
    """
    Mixin which implements the expected Secret usage via environment variables.
    """

    sub_path_env_password = "env[?@name=='PROVISIONING_API_PASSWORD']"

    def assert_correct_secret_usage(self, result, *, name=None, key=None):
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        container = workload.findone(self.path_container)
        password = container.findone(self.sub_path_env_password)

        if name:
            assert password.findone("valueFrom.secretKeyRef.name") == name

        if key:
            assert password.findone("valueFrom.secretKeyRef.key") == key


class Connection(BaseTest):

    config_map_name = None

    path_provisioning_api_url = "data.PROVISIONING_API_URL"

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


class RegistrationSecretUsage(BaseTest):
    """
    Checks the correct secret usage around the user registration.

    This Secret usage check is special because the registration requires an
    existing secret to be configured. Most other implementations support to
    provide also a value in a key like `password` directly.
    """

    secret_name = "stub-secret-name"
    secret_default_key = "registration"
    path_registration = "stringData.registration"

    def assert_correct_secret_usage(self, result, *, name=None, key=None):
        raise NotImplementedError("Use one of the mixins or implement this method.")

    def test_auth_existing_secret_used(self, chart):
        values = self.load_and_map(
            """
            registerConsumers:
              createUsers:
                consumerName:
                  existingSecret:
                    name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, name="stub-secret-name")

    def test_auth_existing_secret_uses_correct_default_key(self, chart):
        values = self.load_and_map(
            """
            registerConsumers:
              createUsers:
                consumerName:
                  existingSecret:
                    name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, key=self.secret_default_key)

    def test_auth_existing_secret_uses_correct_custom_key(self, chart):
        values = self.load_and_map(
            """
            registerConsumers:
              createUsers:
                consumerName:
                  existingSecret:
                    name: "stub-secret-name"
                    keyMapping:
                      registration: "stub_registration_key"
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, key="stub_registration_key")

    def test_auth_existing_secret_is_required(self, chart):
        values = self.load_and_map(
            """
            registerConsumers:
              createUsers:
                consumerName:
                  existingSecret: null
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "Consumer secrets can only be configured as existing secret" in error.value.stderr


class SecretViaProjectedVolume:
    """
    Mixin which checks the expected Secret usage via a projected volume.
    """

    path_volume= "..spec.template.spec.volumes[?@.name=='consumer-secrets']"

    sub_path_volume_mount = "volumeMounts[?@.name=='consumer-secrets']"

    def assert_correct_secret_usage(self, result, *, name=None, key=None):
        # A projected volume can combine many secrets, that's why this has to
        # use the defaults. This is a difference from the other mixins.
        name = name or self.secret_name
        key = key or self.secret_default_key

        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        secret_volume = workload.findone(self.path_volume)
        assert "projected" in secret_volume
        secret_projection = secret_volume.findone(f"projected.sources[?@secret.name=='{name}']")
        container = workload.findone(self.path_container)
        secret_volume_mount = container.findone(self.sub_path_volume_mount)

        # The projection has to be configured for this secret and it has to
        # have an entry for the key.
        assert secret_projection
        assert secret_projection.findone(f"secret.items[?@key=='{key}']")

        # On the container side we only want to be sure that the volume is mounted.
        assert secret_volume_mount
