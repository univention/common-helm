# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import pytest

from univention.testing.helm.base import Labels
from pytest_helm.utils import findone
from yaml import safe_load


class Secret(Labels):
    def values(self, localpart: dict) -> dict:
        return localpart

    def test_udm_plain_values_generate_secret(self, helm, chart_path):
        values = self.values(safe_load(
            """
            auth:
              password: "stub-password"
        """,
        ))
        result = helm.helm_template_file(chart_path, values, self.manifest)
        assert findone(result, "stringData.password") == "stub-password"

    def test_auth_plain_values_password_is_not_templated(self, helm, chart_path):
        values = self.values(safe_load(
            """
            auth:
              password: "{{ value }}"
        """,
        ))
        result = helm.helm_template_file(chart_path, values, self.manifest)
        assert findone(result, "stringData.password") == "{{ value }}"

    def test_auth_plain_values_password_is_required(self, helm, chart_path):
        """
        Only relevant for secrets that don't have generated password support
        """
        values = self.values(safe_load(
            """
            auth:
              password: null
        """,
        ))
        with pytest.raises(RuntimeError):
            helm.helm_template_file(chart_path, values, self.manifest)

    def test_auth_existing_secret_does_not_generate_a_secret(
        self,
        helm,
        chart_path,
    ):
        values = self.values(safe_load(
            """
            auth:
              existingSecret:
                name: "stub-secret-name"
        """,
        ))
        result = helm.helm_template_file(chart_path, values, self.manifest)
        assert result == {}

    def test_auth_existing_secret_does_not_require_plain_password(
        self,
        helm,
        chart_path,
    ):
        values = self.values(safe_load(
            """
            auth:
              password: null
              existingSecret:
                name: "stub-secret-name"
        """,
        ))
        result = helm.helm_template_file(chart_path, values, self.manifest)
        assert result == {}

    def test_auth_existing_secret_has_precedence(self, helm, chart_path):
        values = self.values(safe_load(
            """
            auth:
              password: stub-plain-password
              existingSecret:
                name: "stub-secret-name"
                keyMapping:
                  password: "stub_password_key"
        """,
        ))
        result = helm.helm_template_file(chart_path, values, self.manifest)
        assert result == {}
