# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from contextlib import nullcontext as does_not_raise
import subprocess

import pytest

from .base import BaseTest


class PostgresqlClient(BaseTest):
    """
    Postgresql Client configuration

    Checks of the expected behavior around the configuration of the Postgresql
    client.
    """

    default_username = "stub-values-username"
    default_port = "5432"
    secret_name = "release-name-test-nubus-common-postgresql"
    secret_default_key = "password"
    path_main_container = "spec.template.spec.containers[?@.name=='main']"
    path_postgresql_username = "data.DB_USERNAME"
    path_postgresql_url = "data.DATABASE_URL"
    sub_path_env_db_password = "env[?@name=='DB_PASSWORD']"

    def test_connection_host_is_required(self, helm, chart_path):
        values = self.load_and_map(
            """
            postgresql:
              connection:
                host: null
              auth:
                password: "stub-password"
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            helm.helm_template(chart_path, values)
        assert "connection has to be configured" in error.value.stderr

    def test_connection_host_is_templated(self, helm, chart_path):
        values = self.load_and_map(
            """
            global:
              test: "stub_value"
            postgresql:
              connection:
                host: "{{ .Values.global.test }}"
              auth:
                password: "stub-password"
            """)
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        postgresql_url = config_map.findone(self.path_postgresql_url)
        assert "stub_value" in postgresql_url

    def test_connection_host_supports_global_default(self, helm, chart_path):
        values = self.load_and_map(
            """
            global:
              postgresql:
                connection:
                  host: "global_stub"
            postgresql:
              connection:
                host: null
              auth:
                password: "stub-password"
        """)
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        postgresql_url = config_map.findone(self.path_postgresql_url)
        assert "global_stub" in postgresql_url

    def test_connection_host_local_overrides_global(self, helm, chart_path):
        values = self.load_and_map(
            """
            global:
              postgresql:
                connection:
                  host: "global_stub"
            postgresql:
              connection:
                host: "local_stub"
              auth:
                password: "stub-password"
        """)
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        postgresql_url = config_map.findone(self.path_postgresql_url)
        assert "local_stub" in postgresql_url

    def test_connection_port_has_default(self, helm, chart_path):
        values = self.load_and_map(
            """
            postgresql:
              connection:
                port: null
              auth:
                password: "stub-password"
            """)
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        postgresql_url = config_map.findone(self.path_postgresql_url)
        assert self.default_port in postgresql_url

    def test_connection_port_is_templated(self, helm, chart_path):
        values = self.load_and_map(
            """
            global:
              test: "stub_value"
            postgresql:
              connection:
                port: "{{ .Values.global.test }}"
              auth:
                password: "stub-password"
            """)
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        postgresql_url = config_map.findone(self.path_postgresql_url)
        assert "stub_value" in postgresql_url

    def test_connection_port_supports_global_default(self, helm, chart_path):
        values = self.load_and_map(
            """
            global:
              postgresql:
                connection:
                  port: "global_stub"
            postgresql:
              connection:
                port: null
              auth:
                password: "stub-password"
        """)
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        postgresql_url = config_map.findone(self.path_postgresql_url)
        assert "global_stub" in postgresql_url

    def test_connection_port_local_overrides_global(self, helm, chart_path):
        values = self.load_and_map(
            """
            global:
              postgresql:
                connection:
                  port: "global_stub"
            postgresql:
              connection:
                port: "local_stub"
              auth:
                password: "stub-password"
        """)
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        postgresql_url = config_map.findone(self.path_postgresql_url)
        assert "local_stub" in postgresql_url

    def test_auth_plain_values_generate_secret(self, helm, chart_path):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                username: "stub-username"
                database: "stub-database"
                password: "stub-password"
        """,
        )
        result = helm.helm_template(chart_path, values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)

        assert secret.findone("stringData.password") == "stub-password"

    def test_auth_plain_values_provide_username_in_database_url_via_config_map(self, helm, chart_path):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                username: "stub-username"
                database: "stub-database"
                password: "stub-password"
        """,
        )
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        assert "stub-username" in config_map.findone(self.path_postgresql_url)

    def test_auth_plain_values_username_is_templated(self, helm, chart_path):
        values = self.load_and_map(
            """
            global:
              test: "stub-value"
            postgresql:
              auth:
                username: "{{ .Values.global.test }}"
                database: "stub-database"
                password: "stub-password"
        """,
        )
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        assert "stub-value" in config_map.findone(self.path_postgresql_url)

    def test_auth_plain_values_password_is_not_templated(self, helm, chart_path):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                username: "stub-username"
                database: "stub-database"
                password: "{{ value }}"
        """,
        )
        result = helm.helm_template(chart_path, values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        assert secret.findone("stringData.password") == "{{ value }}"

    def test_auth_plain_values_password_is_required(self, helm, chart_path):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                username: "stub-username"
                database: "stub-database"
                password: null
        """,
        )
        with pytest.raises(subprocess.CalledProcessError) as error:
            helm.helm_template(chart_path, values)
        assert "password has to be supplied" in error.value.stderr

    def test_auth_username_is_required(self, helm, chart_path):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                username: null
                database: "stub-database"
                password: "stub-password"
        """,
        )
        with pytest.raises(subprocess.CalledProcessError) as error:
            helm.helm_template(chart_path, values)
        assert "username has to be supplied" in error.value.stderr

    def test_auth_username_has_default(self, helm, chart_path):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                password: "stub-password"
        """,
        )
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        assert self.default_username in config_map.findone(self.path_postgresql_url)

    def test_auth_database_is_required(self, helm, chart_path):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                username: "stub-username"
                database: null
                password: "stub-password"
        """,
        )
        with pytest.raises(subprocess.CalledProcessError) as error:
            helm.helm_template(chart_path, values)
        assert "database has to be supplied" in error.value.stderr

    def test_auth_database_has_default(self, helm, chart_path):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                password: "stub-password"
        """,
        )
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        assert self.default_database in config_map.findone(self.path_postgresql_url)

    def test_auth_database_is_templated(self, helm, chart_path):
        values = self.load_and_map(
            """
            global:
              test: "stub-value"
            postgresql:
              auth:
                username: "stub-username"
                database: "{{ .Values.global.test }}"
                password: "stub-password"
        """,
        )
        result = helm.helm_template(chart_path, values)
        config_map = result.get_resource(kind="ConfigMap")
        assert "stub-value" in config_map.findone(self.path_postgresql_url)


    def test_auth_existing_secret_does_not_generate_a_secret(self, helm, chart_path):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                username: "stub-username"
                database: "stub-database"
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
            postgresql:
              auth:
                password: null
                existingSecret:
                  name: "stub-secret-name"
        """,
        )
        with does_not_raise():
            helm.helm_template(chart_path, values)

    def test_auth_existing_secret_used_to_populate_environment_variables(self, helm, chart_path):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = helm.helm_template(chart_path, values)
        deployment = result.get_resource(kind="Deployment")
        main_container = deployment.findone(self.path_main_container)

        password = main_container.findone(self.sub_path_env_db_password)
        assert password.findone("valueFrom.secretKeyRef.name") == "stub-secret-name"

    def test_auth_existing_secret_uses_correct_default_key(self, helm, chart_path):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = helm.helm_template(chart_path, values)
        deployment = result.get_resource(kind="Deployment")
        main_container = deployment.findone(self.path_main_container)

        password = main_container.findone(self.sub_path_env_db_password)
        assert password.findone("valueFrom.secretKeyRef.key") == self.secret_default_key

    def test_auth_existing_secret_uses_correct_custom_key(self, helm, chart_path):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                existingSecret:
                  name: "stub-secret-name"
                  keyMapping:
                    password: "stub_password_key"
            """)
        result = helm.helm_template(chart_path, values)
        deployment = result.get_resource(kind="Deployment")
        main_container = deployment.findone(self.path_main_container)

        password = main_container.findone(self.sub_path_env_db_password)
        assert password.findone("valueFrom.secretKeyRef.key") == "stub_password_key"

    def test_auth_plain_values_uses_correct_secret(self, helm, chart_path):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                username: "stub-username"
                database: "stub-database"
                password: "stub-password"
                existingSecret: null
            """)
        result = helm.helm_template(chart_path, values)
        deployment = result.get_resource(kind="Deployment")
        main_container = deployment.findone(self.path_main_container)
        password = main_container.findone(self.sub_path_env_db_password)
        expected_value = {"name": self.secret_name, "key": self.secret_default_key}
        assert password.findone("valueFrom.secretKeyRef") == expected_value

    def test_auth_existing_secret_has_precedence(self, helm, chart_path):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                password: "stub-plain-password"
                existingSecret:
                  name: "stub-secret-name"
                  keyMapping:
                    password: "stub_password_key"
            """)
        result = helm.helm_template(chart_path, values)
        with pytest.raises(LookupError):
            result.get_resource(kind="Secret", name=self.secret_name)

        deployment = result.get_resource(kind="Deployment")
        main_container = deployment.findone(self.path_main_container)
        password = main_container.findone(self.sub_path_env_db_password)
        expected_value = {"name": "stub-secret-name", "key": "stub_password_key"}
        assert password.findone("valueFrom.secretKeyRef") == expected_value

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

            postgresql:
              auth:
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        annotations = secret.findone("metadata.annotations", default={})
        helm_resource_policy = annotations.get("helm.sh/resource-policy")
        assert helm_resource_policy != "keep"
