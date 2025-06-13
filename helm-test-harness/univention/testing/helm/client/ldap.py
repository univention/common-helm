# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from contextlib import nullcontext as does_not_raise
import subprocess

import pytest
from pytest_helm.models import HelmTemplateResult

from .base import BaseTest


class LdapAuth(BaseTest):
    """
    Tests for the value `ldap.auth` of the LDAP client configuration.

    Per default the test template will assume the password to be mounted out of
    a secret and the other parameters to be provided via the `envFrom`
    attribute of the container configuration.
    """

    config_map_name = None
    secret_name = "release-name-test-nubus-common-ldap"

    default_bind_dn = "cn=admin,dc=univention-organization,dc=intranet"

    path_ldap_bind_dn = "data.LDAP_HOST_DN"
    path_main_container = "..spec.template.spec.containers[?@.name=='main']"
    path_volume = "..spec.template.spec.volumes[?@.name=='secret-ldap']"

    sub_path_volume_mount = "volumeMounts[?@.name=='secret-ldap']"

    def get_bind_dn(self, result: HelmTemplateResult):
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        return config_map.findone(self.path_ldap_bind_dn)

    def assert_bind_dn_value(self, result: HelmTemplateResult, value: str):
        bind_dn = self.get_bind_dn(result)
        assert bind_dn == value

    def assert_correct_secret_usage(self, result, *, name=None, key=None):
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        secret_volume = workload.findone(self.path_volume)
        main_container = workload.findone(self.path_main_container)
        secret_volume_mount = main_container.findone(self.sub_path_volume_mount)

        if name:
            assert secret_volume.findone("secret.secretName") == name

        if key:
            assert secret_volume_mount["subPath"] == key

    def test_auth_plain_values_generate_secret(self, chart):
        values = self.load_and_map(
            """
            ldap:
              auth:
                bindDn: "stub-bind-dn"
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)

        assert secret.findone("stringData.password") == "stub-password"

    def test_auth_plain_values_provide_bind_dn(self, chart):
        values = self.load_and_map(
            """
            ldap:
              auth:
                bindDn: "stub-bind-dn"
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        self.assert_bind_dn_value(result, "stub-bind-dn")

    def test_auth_plain_values_bind_dn_is_templated(self, chart):
        values = self.load_and_map(
            """
            global:
              test: "stub-value"
            ldap:
              auth:
                bindDn: "{{ .Values.global.test }}"
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        self.assert_bind_dn_value(result, "stub-value")

    @pytest.mark.parametrize("value", [
        "null",
        '""',
    ])
    def test_auth_bind_dn_is_required(self, chart, value):
        values = self.load_and_map(
            f"""
            ldap:
              auth:
                bindDn: {value}
                password: "stub-password"
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert '"ldap.auth.bindDn" is required.' in error.value.stderr

    def test_auth_bind_dn_has_default(self, chart):
        values = self.load_and_map(
            """
            ldap:
              auth:
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        self.assert_bind_dn_value(result, self.default_bind_dn)

    def test_auth_plain_values_password_is_not_templated(self, chart):
        values = self.load_and_map(
            """
            ldap:
              auth:
                bindDn: "stub-bind-dn"
                password: "{{ value }}"
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        assert secret.findone("stringData.password") == "{{ value }}"

    def test_auth_plain_values_password_is_required(self, chart):
        values = self.load_and_map(
            """
            ldap:
              auth:
                bindDn: "stub-bind-dn"
                password: null
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "password has to be supplied" in error.value.stderr

    def test_auth_existing_secret_does_not_generate_a_secret(self, chart):
        values = self.load_and_map(
            """
            ldap:
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
            ldap:
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
            ldap:
              auth:
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, name="stub-secret-name")

    def test_auth_existing_secret_uses_correct_default_key(self, chart):
        values = self.load_and_map(
            """
            ldap:
              auth:
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, key="password")

    def test_auth_disabling_existing_secret_by_setting_it_to_null(self, chart):
        values = self.load_and_map(
            """
            ldap:
              auth:
                bindDn: "stub-bind-dn"
                password: "stub-password"
                existingSecret: null
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, name=self.secret_name, key="password")

    def test_auth_existing_secret_uses_correct_custom_key(self, chart):
        values = self.load_and_map(
            """
            ldap:
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
            ldap:
              auth:
                password: stub-plain-password
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

            ldap:
              auth:
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        annotations = secret.findone("metadata.annotations", default={})
        helm_resource_policy = annotations.get("helm.sh/resource-policy")
        assert helm_resource_policy != "keep"


class LdapAuthUsageViaEnv:
    """
    Mixin to change the expected behavior to be based on env configuration.

    Both the `bindDn` and the `password` out of `ldap.auth` are expected to be
    used via the attribute `env` within the container configuration.
    """

    sub_path_env_bind_dn = "env[?@.name=='LDAP_ADMIN_USER']"
    sub_path_env_password = "env[?@.name=='LDAP_ADMIN_PASSWORD']"

    def get_bind_dn(self, result: HelmTemplateResult):
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        main_container = workload.findone(self.path_main_container)
        env_basn_dn = main_container.findone(self.sub_path_env_bind_dn)
        return env_basn_dn["value"]

    def assert_correct_secret_usage(self, result, *, name=None, key=None):
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        main_container = workload.findone(self.path_main_container)
        env_password = main_container.findone(self.sub_path_env_password)

        if name:
            assert env_password.findone("valueFrom.secretKeyRef.name") == name

        if key:
            assert env_password.findone("valueFrom.secretKeyRef.key") == key


class LdapConnectionHostAndPort(BaseTest):
    """
    Tests related to the usage `host` and `port` in the connection.

    Tests for the following values:

    - `ldap.connection.host`
    - `ldap.connection.port`
    """
    config_map_name = None

    default_port = "389"

    path_ldap_host = "data.LDAP_HOST"
    path_ldap_port = "data.LDAP_PORT"

    def test_connection_host_is_required(self, chart):
        values = self.load_and_map(
            """
            ldap:
              connection:
                host: null
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "connection has to be configured" in error.value.stderr

    @pytest.mark.parametrize("value", [
        "stub-hostname",
        # This value is invalid, but will ensure that "quote" is correctly used
        ":",
    ])
    def test_connection_host_can_be_configured(self, chart, value):
        values = self.load_and_map(
            f"""
            ldap:
              connection:
                host: "{value}"
            """)
        result = chart.helm_template(values)
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        ldap_host = config_map.findone(self.path_ldap_host)
        assert value in ldap_host

    def test_connection_host_is_templated(self, chart):
        values = self.load_and_map(
            """
            global:
              test: "stub_value"
            ldap:
              connection:
                host: "{{ .Values.global.test }}"
            """)
        result = chart.helm_template(values)
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        ldap_host = config_map.findone(self.path_ldap_host)
        assert "stub_value" in ldap_host

    def test_connection_host_supports_global_default(self, chart):
        values = self.load_and_map(
            """
            global:
              ldap:
                connection:
                  host: "global_stub"
            ldap:
              connection:
                host: null
            """)
        result = chart.helm_template(values)
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        ldap_host = config_map.findone(self.path_ldap_host)
        assert "global_stub" in ldap_host

    def test_connection_host_local_overrides_global(self, chart):
        values = self.load_and_map(
            """
            global:
              ldap:
                connection:
                  host: "global_stub"
            ldap:
              connection:
                host: "local_stub"
        """)
        result = chart.helm_template(values)
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        ldap_host = config_map.findone(self.path_ldap_host)
        assert "local_stub" in ldap_host

    def test_connection_port_has_default(self, chart):
        values = self.load_and_map(
            """
            ldap:
              connection:
                port: null
            """)
        result = chart.helm_template(values)
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        ldap_port = config_map.findone(self.path_ldap_port)
        assert self.default_port == ldap_port

    @pytest.mark.parametrize("value", [
        "1234",
        # This value is invalid, but will ensure that "quote" is correctly used
        ":",
    ])
    def test_connection_port_can_be_configured(self, chart, value):
        values = self.load_and_map(
            f"""
            ldap:
              connection:
                port: "{value}"
            """)
        result = chart.helm_template(values)
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        ldap_port = config_map.findone(self.path_ldap_port)
        assert value == ldap_port

    def test_connection_port_is_templated(self, chart):
        values = self.load_and_map(
            """
            global:
              test: "stub_value"
            ldap:
              connection:
                port: "{{ .Values.global.test }}"
            """)
        result = chart.helm_template(values)
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        ldap_port = config_map.findone(self.path_ldap_port)
        assert "stub_value" == ldap_port

    def test_connection_port_supports_global_default(self, chart):
        values = self.load_and_map(
            """
            global:
              ldap:
                connection:
                  port: "global_stub"
            ldap:
              connection:
                port: null
            """)
        result = chart.helm_template(values)
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        ldap_port = config_map.findone(self.path_ldap_port)
        assert "global_stub" == ldap_port

    def test_connection_port_local_overrides_global(self, chart):
        values = self.load_and_map(
            """
            global:
              ldap:
                connection:
                  port: "global_stub"
            ldap:
              connection:
                port: "local_stub"
            """)
        result = chart.helm_template(values)
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        ldap_port = config_map.findone(self.path_ldap_port)
        assert "local_stub" == ldap_port


class LdapConnectionUri(BaseTest):
    """
    Tests related to the usage of `ldap.connection.uri`.
    """

    path_main_container = "spec.template.spec.containers[?@.name=='main']"

    sub_path_env_connection_uri = "env[?@name=='LDAP_URI']"

    def test_connection_uri_is_required(self, chart):
        values = self.load_and_map(
            """
            ldap:
              connection:
                uri: null
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "connection has to be configured" in error.value.stderr

    def test_connection_uri_is_templated(self, chart):
        values = self.load_and_map(
            """
            global:
              test: "stub_value"
            ldap:
              connection:
                uri: "{{ .Values.global.test }}"
            """)
        result = chart.helm_template(values)
        self.assert_connection_uri_value(result, "stub_value")

    def test_connection_uri_supports_global_default(self, chart):
        values = self.load_and_map(
            """
            global:
              ldap:
                connection:
                  uri: "global_stub"
            ldap:
              connection:
                uri: null
            """)
        result = chart.helm_template(values)
        self.assert_connection_uri_value(result, "global_stub")

    def test_connection_uri_local_overrides_global(self, chart):
        values = self.load_and_map(
            """
            global:
              ldap:
                connection:
                  uri: "global_stub"
            ldap:
              connection:
                uri: "local_stub"
        """)
        result = chart.helm_template(values)
        self.assert_connection_uri_value(result, "local_stub")

    def assert_connection_uri_value(self, result, value):
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        main_container = workload.findone(self.path_main_container)
        env_connection_uri = main_container.findone(self.sub_path_env_connection_uri)

        assert env_connection_uri["value"] == value


class LdapConnectionUriViaConfigMap:
    """
    Mixin which expects the connection URI in a ConfigMap.
    """

    config_map_name = None

    path_ldap_uri = "data.LDAP_URI"

    def get_ldap_uri(self, result: HelmTemplateResult):
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        uri = config_map.findone(self.path_ldap_uri)
        return uri

    def assert_connection_uri_value(self, result, value):
        uri = self.get_ldap_uri(result)
        assert uri == value
