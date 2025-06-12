# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from contextlib import nullcontext as does_not_raise
import subprocess

import pytest

from .base import BaseTest


class PostgresqlAuth(BaseTest):
    """
    Postgresql Client configuration

    Checks of the expected behavior around the configuration of the Postgresql
    client.
    """

    secret_name = "release-name-test-nubus-common-postgresql"

    default_username = "stub-values-username"
    secret_default_key = "password"

    path_main_container = "spec.template.spec.containers[?@.name=='main']"
    path_postgresql_username = "data.DB_USERNAME"

    sub_path_database_url = "env[?@name=='DATABASE_URL'].value"
    sub_path_env_db_password = "env[?@name=='DB_PASSWORD']"

    def test_auth_plain_values_generate_secret(self, chart):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                username: "stub-username"
                database: "stub-database"
                password: "stub-password"
        """,
        )
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)

        assert secret.findone("stringData.password") == "stub-password"

    def test_auth_plain_values_provide_username_in_database_url_via_config_map(self, chart):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                username: "stub-username"
                database: "stub-database"
                password: "stub-password"
        """,
        )
        result = chart.helm_template(values)
        database_url = self._get_database_url(result)
        assert "stub-username" in database_url

    def test_auth_plain_values_username_is_templated(self, chart):
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
        result = chart.helm_template(values)
        database_url = self._get_database_url(result)
        assert "stub-value" in database_url

    def test_auth_plain_values_password_is_not_templated(self, chart):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                username: "stub-username"
                database: "stub-database"
                password: "{{ value }}"
        """,
        )
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        assert secret.findone("stringData.password") == "{{ value }}"

    def test_auth_plain_values_password_is_required(self, chart):
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
            chart.helm_template(values)
        assert "password has to be supplied" in error.value.stderr

    def test_auth_username_is_required(self, chart):
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
            chart.helm_template(values)
        assert "username has to be supplied" in error.value.stderr

    def test_auth_username_has_default(self, chart):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                password: "stub-password"
        """,
        )
        result = chart.helm_template(values)
        database_url = self._get_database_url(result)
        assert self.default_username in database_url

    def test_auth_database_is_required(self, chart):
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
            chart.helm_template(values)
        assert "database has to be supplied" in error.value.stderr

    def test_auth_database_has_default(self, chart):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                password: "stub-password"
        """,
        )
        result = chart.helm_template(values)
        database_url = self._get_database_url(result)
        assert self.default_database in database_url

    def test_auth_database_is_templated(self, chart):
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
        result = chart.helm_template(values)
        database_url = self._get_database_url(result)
        assert "stub-value" in database_url

    def test_auth_existing_secret_does_not_generate_a_secret(self, chart):
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
        result = chart.helm_template(values)
        with pytest.raises(LookupError):
            result.get_resource(kind="Secret", name=self.secret_name)

    def test_auth_existing_secret_does_not_require_plain_password(self, chart):
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
            chart.helm_template(values)

    def test_auth_existing_secret_used_to_populate_environment_variables(self, chart):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        main_container = workload.findone(self.path_main_container)

        password = main_container.findone(self.sub_path_env_db_password)
        assert password.findone("valueFrom.secretKeyRef.name") == "stub-secret-name"

    def test_auth_existing_secret_uses_correct_default_key(self, chart):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        main_container = workload.findone(self.path_main_container)

        password = main_container.findone(self.sub_path_env_db_password)
        assert password.findone("valueFrom.secretKeyRef.key") == self.secret_default_key

    def test_auth_existing_secret_uses_correct_custom_key(self, chart):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                existingSecret:
                  name: "stub-secret-name"
                  keyMapping:
                    password: "stub_password_key"
            """)
        result = chart.helm_template(values)
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        main_container = workload.findone(self.path_main_container)

        password = main_container.findone(self.sub_path_env_db_password)
        assert password.findone("valueFrom.secretKeyRef.key") == "stub_password_key"

    def test_auth_plain_values_uses_correct_secret(self, chart):
        values = self.load_and_map(
            """
            postgresql:
              auth:
                username: "stub-username"
                database: "stub-database"
                password: "stub-password"
                existingSecret: null
            """)
        result = chart.helm_template(values)
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        main_container = workload.findone(self.path_main_container)
        password = main_container.findone(self.sub_path_env_db_password)
        expected_value = {"name": self.secret_name, "key": self.secret_default_key}
        assert password.findone("valueFrom.secretKeyRef") == expected_value

    def test_auth_existing_secret_has_precedence(self, chart):
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
        result = chart.helm_template(values)
        with pytest.raises(LookupError):
            result.get_resource(kind="Secret", name=self.secret_name)

        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        main_container = workload.findone(self.path_main_container)
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

    def _get_database_url(self, result):
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        main_container = workload.findone(self.path_main_container)
        database_url = main_container.findone(self.sub_path_database_url)
        return database_url


class PostgresqlConnection(BaseTest):
    """
    Test related to the connection configuration of postgresql.

    Tests for the following values:

    - `postgresql.connection.host`
    - `postgresql.connection.port`
    """

    default_port = "5432"

    path_main_container = "spec.template.spec.containers[?@.name=='main']"

    sub_path_database_url = "env[?@name=='DATABASE_URL'].value"

    def test_connection_host_is_required(self, chart):
        values = self.load_and_map(
            """
            postgresql:
              connection:
                host: null
              auth:
                password: "stub-password"
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "connection has to be configured" in error.value.stderr

    def test_connection_host_is_templated(self, chart):
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
        result = chart.helm_template(values)
        database_url = self._get_database_url(result)
        assert "stub_value" in database_url

    def test_connection_host_supports_global_default(self, chart):
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
        result = chart.helm_template(values)
        database_url = self._get_database_url(result)
        assert "global_stub" in database_url

    def test_connection_host_local_overrides_global(self, chart):
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
        result = chart.helm_template(values)
        database_url = self._get_database_url(result)
        assert "local_stub" in database_url

    def test_connection_port_has_default(self, chart):
        values = self.load_and_map(
            """
            postgresql:
              connection:
                port: null
              auth:
                password: "stub-password"
            """)
        result = chart.helm_template(values)
        database_url = self._get_database_url(result)
        assert self.default_port in database_url

    def test_connection_port_is_templated(self, chart):
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
        result = chart.helm_template(values)
        database_url = self._get_database_url(result)
        assert "stub_value" in database_url

    def test_connection_port_supports_global_default(self, chart):
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
        result = chart.helm_template(values)
        database_url = self._get_database_url(result)
        assert "global_stub" in database_url

    def test_connection_port_local_overrides_global(self, chart):
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
        result = chart.helm_template(values)
        database_url = self._get_database_url(result)
        assert "local_stub" in database_url

    def _get_database_url(self, result):
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        main_container = workload.findone(self.path_main_container)
        database_url = main_container.findone(self.sub_path_database_url)
        return database_url
