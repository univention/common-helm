# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from contextlib import nullcontext as does_not_raise

import pytest
from pytest_helm.models import HelmTemplateResult

from ..client.base import BaseTest


class AuthSecretGeneration(BaseTest):
    """
    Partial client test focused only on the Secret generation.

    Should not be directly used.
    Instead use AuthSecretGenerationOwner or AuthSecretGenerationUser

    Checks the following values:

    - `auth.password`
    """

    secret_name = "release-name-test-nubus-common"
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
            auth:
              username: "stub-username"
              password: "stub-password"
            """)
        result = chart.helm_template(values)
        self.assert_password_value(result, "stub-password")

    def test_auth_plain_values_password_is_not_templated(self, chart):
        values = self.load_and_map(
            """
            auth:
              username: "stub-username"
              password: "{{ value }}"
            """)
        result = chart.helm_template(values)
        self.assert_password_value(result, "{{ value }}")

    def test_auth_existing_secret_does_not_generate_a_secret(self, chart):
        values = self.load_and_map(
            """
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
