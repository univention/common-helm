# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from contextlib import nullcontext as does_not_raise
import subprocess

import pytest

from .base import ClientTestBase


# NOTE: We want to have the values + linter_values always be passing the
# schema validation and required checks. So in some way we have to "unset"
# a value to verify that something is required. At the same time we want to
# be sure that nothing else is missing so that we check exactly for the
# item under test.


class UdmClient(ClientTestBase):
    """
    UDM Rest API Client configuration

    Checks of the expected behavior around the configuration of the UDM Rest
    API client.
    """

    default_username = "stub-values-username"
    path_udm_api_url = "data.UDM_API_URL"
    path_udm_api_username = "data.UDM_API_USERNAME"
    path_volume_secret_udm = "spec.template.spec.volumes[?@.name=='secret-udm']"
    path_main_container = "spec.template.spec.containers[?@.name=='main']"
    sub_path_udm_volume_mount = "volumeMounts[?@.name=='secret-udm']"
    secret_name = "release-name-test-nubus-common-udm"

    def test_connection_url_is_required(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: null
              auth:
                username: "stub-username"
                password: "stub-password"
            """,
        )
        with pytest.raises(subprocess.CalledProcessError) as error:
            helm.helm_template(chart_path, values)
        assert "connection has to be configured" in error.value.stderr

    def test_connection_url_is_templated(self, helm, chart_path):
        values = self.load_and_map(
            """
            global:
              test: "stub_value"
            udm:
              connection:
                url: "{{ .Values.global.test }}"
              auth:
                username: "stub-username"
                password: "stub-password"
            """,
        )
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        assert config_map.findone(self.path_udm_api_url) == "stub_value"

    def test_connection_url_supports_global_default(self, helm, chart_path):
        values = self.load_and_map(
            """
            global:
              udm:
                connection:
                  url: "global_stub"
            udm:
              connection:
                url: null
              auth:
                username: "stub-username"
                password: "stub-password"
        """,
        )
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        assert config_map.findone(self.path_udm_api_url) == "global_stub"

    def test_connection_url_local_overrides_global(self, helm, chart_path):
        values = self.load_and_map(
            """
            global:
              udm:
                connection:
                  url: "global_stub"
            udm:
              connection:
                url: "local_stub"
              auth:
                username: "stub-username"
                password: "stub-password"
        """,
        )
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        assert config_map.findone(self.path_udm_api_url) == "local_stub"

    def test_auth_plain_values_generate_secret(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                username: "stub-username"
                password: "stub-password"
        """,
        )
        result = helm.helm_template(chart_path, values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)

        assert secret.findone("stringData.password") == "stub-password"

    def test_auth_plain_values_provide_username_via_config_map(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                username: "stub-username"
                password: "stub-password"
        """,
        )
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        assert config_map.findone(self.path_udm_api_username) == "stub-username"

    def test_auth_plain_values_username_is_templated(self, helm, chart_path):
        values = self.load_and_map(
            """
            global:
              test: "stub-value"
            udm:
              connection:
                url: "local_stub"
              auth:
                username: "{{ .Values.global.test }}"
                password: "stub-password"
        """,
        )
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        assert config_map.findone(self.path_udm_api_username) == "stub-value"

    def test_auth_plain_values_password_is_not_templated(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                username: "stub-username"
                password: "{{ value }}"
        """,
        )
        result = helm.helm_template(chart_path, values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        assert secret.findone("stringData.password") == "{{ value }}"

    def test_auth_plain_values_password_is_required(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                username: "stub-username"
                password: null
        """,
        )
        with pytest.raises(subprocess.CalledProcessError) as error:
            helm.helm_template(chart_path, values)
        assert "password has to be supplied" in error.value.stderr

    def test_auth_username_is_required(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                username: null
                password: "stub-password"
        """,
        )
        with pytest.raises(subprocess.CalledProcessError) as error:
            helm.helm_template(chart_path, values)
        assert "username has to be supplied" in error.value.stderr

    def test_auth_username_has_default(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                password: "stub-password"
        """,
        )
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        assert config_map.findone(self.path_udm_api_username) == self.default_username

    def test_auth_existing_secret_does_not_generate_a_secret(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                existingSecret:
                  name: "stub-secret-name"
        """,
        )
        result = helm.helm_template(chart_path, values)
        with pytest.raises(LookupError):
            result.get_resource(kind="Secret", name=self.secret_name)

    def test_auth_existing_secret_does_not_require_plain_password(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                password: null
                existingSecret:
                  name: "stub-secret-name"
        """,
        )
        with does_not_raise():
            helm.helm_template(chart_path, values)

    def test_auth_existing_secret_mounts_password(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                existingSecret:
                  name: "stub-secret-name"
        """,
        )
        result = helm.helm_template(chart_path, values)
        deployment = result.get_resource(kind="Deployment")
        secret_udm_volume = deployment.findone(self.path_volume_secret_udm)
        assert secret_udm_volume.findone("secret.secretName") == "stub-secret-name"

    def test_auth_existing_secret_mounts_correct_default_key(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                existingSecret:
                  name: "stub-secret-name"
        """,
        )
        result = helm.helm_template(chart_path, values)
        deployment = result.get_resource(kind="Deployment")
        main_container = deployment.findone(self.path_main_container)
        secret_udm_volume_mount = main_container.findone(self.sub_path_udm_volume_mount)

        assert secret_udm_volume_mount["subPath"] == "password"

    def test_auth_disabling_existing_secret_by_setting_it_to_null(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                username: "stub-username"
                password: "stub-password"
                existingSecret: null
        """,
        )
        result = helm.helm_template(chart_path, values)
        deployment = result.get_resource(kind="Deployment")
        secret_udm_volume = deployment.findone(self.path_volume_secret_udm)
        main_container = deployment.findone(self.path_main_container)
        secret_udm_volume_mount = main_container.findone(self.sub_path_udm_volume_mount)

        assert secret_udm_volume_mount["subPath"] == "password"
        assert secret_udm_volume.findone("secret.secretName") == self.secret_name

    def test_auth_existing_secret_mounts_correct_custom_key(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                existingSecret:
                  name: "stub-secret-name"
                  keyMapping:
                    password: "stub_password_key"
        """,
        )
        result = helm.helm_template(chart_path, values)
        deployment = result.get_resource(kind="Deployment")
        main_container = deployment.findone(self.path_main_container)
        secret_udm_volume_mount = main_container.findone(self.sub_path_udm_volume_mount)

        assert secret_udm_volume_mount["subPath"] == "stub_password_key"

    def test_auth_existing_secret_has_precedence(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "stub-url"
              auth:
                password: stub-plain-password
                existingSecret:
                  name: "stub-secret-name"
                  keyMapping:
                    password: "stub_password_key"
        """,
        )
        result = helm.helm_template(chart_path, values)
        with pytest.raises(LookupError):
            result.get_resource(kind="Secret", name=self.secret_name)

        deployment = result.get_resource(kind="Deployment")
        secret_udm_volume = deployment.findone(self.path_volume_secret_udm)
        main_container = deployment.findone(self.path_main_container)
        secret_udm_volume_mount = main_container.findone(self.sub_path_udm_volume_mount)

        assert secret_udm_volume_mount["subPath"] == "stub_password_key"
        assert secret_udm_volume.findone("secret.secretName") == "stub-secret-name"

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

            udm:
              connection:
                url: "stub-url"
              auth:
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        annotations = secret.findone("metadata.annotations", default={})
        helm_resource_policy = annotations.get("helm.sh/resource-policy")
        assert helm_resource_policy != "keep"
