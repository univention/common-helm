# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import subprocess

import pytest

from univention.testing.helm.base import Labels, Namespace
from yaml import safe_load


class SecretPasswords(Labels, Namespace):
    """
    Verify a password Secret in the Client role.

    Test harness class to validate kubernetes secret helm templates
    focussed on password templating.
    Supporting:
    - Generated passwords
    - Injected passwords via helm values
    - Passwords via configured existingSecretsSecret
    """

    secret_key = "password"
    """
    The key within the generated Secret under which the password value is stored.
    """

    def values(self, localpart: dict) -> dict:
        return localpart

    def test_auth_plain_values_generate_secret(self, helm, chart_path):
        values = self.values(
            safe_load("""
            auth:
              password: "stub-password"
        """),
        )
        result = self.helm_template_file(helm, chart_path, values, self.template_file)
        assert result.findone(f"stringData.{self.secret_key}") == "stub-password"

    def test_auth_plain_values_password_is_not_templated(self, helm, chart_path):
        values = self.values(
            safe_load("""
            auth:
              password: "{{ value }}"
        """),
        )
        result = self.helm_template_file(helm, chart_path, values, self.template_file)
        assert result.findone(f"stringData.{self.secret_key}") == "{{ value }}"

    def test_auth_plain_values_password_is_required(self, helm, chart_path):
        """
        Only relevant for secrets that don't have generated password support
        """
        values = self.values(
            safe_load("""
            auth:
              password: null
        """),
        )
        with pytest.raises(subprocess.CalledProcessError):
            self.helm_template_file(helm, chart_path, values, self.template_file)

    def test_auth_plain_values_password_has_no_default_value(self, helm, chart_path):
        """
        Only relevant for secrets that don't have generated password support
        """
        values = {}
        helm.values = []

        with pytest.raises(subprocess.CalledProcessError):
            self.helm_template_file(helm, chart_path, values, self.template_file)

    def test_auth_existing_secret_does_not_generate_a_secret(
        self,
        helm,
        chart_path,
    ):
        values = self.values(
            safe_load(
                """
            auth:
              existingSecret:
                name: "stub-secret-name"
        """,
            ),
        )
        result = self.helm_template_file(helm, chart_path, values, self.template_file)
        assert result == {}

    def test_auth_existing_secret_does_not_require_plain_password(
        self,
        helm,
        chart_path,
    ):
        values = self.values(
            safe_load(
                """
            auth:
              password: null
              existingSecret:
                name: "stub-secret-name"
        """,
            ),
        )
        result = self.helm_template_file(helm, chart_path, values, self.template_file)
        assert result == {}

    def test_auth_existing_secret_has_precedence(self, helm, chart_path):
        values = self.values(
            safe_load(
                """
            auth:
              password: stub-plain-password
              existingSecret:
                name: "stub-secret-name"
                keyMapping:
                  password: "stub_password_key"
        """,
            ),
        )
        result = self.helm_template_file(helm, chart_path, values, self.template_file)
        assert result == {}

    def test_global_secrets_keep_is_ignored(self, helm, chart_path):
        """
        Keeping Secrets shall not be supported in Client role.

        Random values for a password will never be generated when in Client
        role. This is why the configuration `global.secrets.keep` shall not
        have any effect on Secrets in Client role.
        """
        values = safe_load(
            """
            global:
              secrets:
                keep: true
            """,
        )
        result = self.helm_template_file(helm, chart_path, values, self.template_file)
        annotations = result.findone("metadata.annotations") or {}
        helm_resource_policy = annotations.get("helm.sh/resource-policy")
        assert helm_resource_policy != "keep"
