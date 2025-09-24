# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from ..client.base import BaseTest


class AuthPasswordUsage(BaseTest):
    """
    Partial client test focused only on the Secret usage.

    Should not be directly used.
    Instead use AuthPasswordUsageEnvVar, AuthPasswordUsageVolume or AuthPasswordUsageProjectedVolume

    Checks the following values:

    - `auth.existingSecret`
    """

    secret_name = "release-name-test-nubus-common"
    secret_default_key = "password"

    def assert_correct_secret_usage(self, result, *, name=None, key=None):
        raise NotImplementedError("Use one of the mixins or implement this method.")

    def test_auth_existing_secret_used(self, chart):
        values = self.load_and_map(
            """
            auth:
              existingSecret:
                name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, name="stub-secret-name")

    def test_auth_existing_secret_uses_correct_default_key(self, chart):
        values = self.load_and_map(
            """
            auth:
              existingSecret:
                name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, key=self.secret_default_key)

    def test_auth_existing_secret_uses_correct_custom_key(self, chart):
        values = self.load_and_map(
            """
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
            auth:
              username: "stub-username"
              password: "stub-password"
              existingSecret: null
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, name=self.secret_name, key="password")
