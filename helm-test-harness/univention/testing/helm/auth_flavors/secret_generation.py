# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import subprocess
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
              existingSecret:
                name: null
            """)
        result = chart.helm_template(values)
        self.assert_password_value(result, "stub-password")

    def test_auth_plain_values_password_is_not_templated(self, chart):
        values = self.load_and_map(
            """
            auth:
              username: "stub-username"
              password: "{{ value }}"
              existingSecret:
                name: null
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


class AuthSecretGenerationOwner(AuthSecretGeneration):
    """
    Partial client test focused only on the Secret generation.

    Should be used in cases where the password is **used and owned** by the helm chart.
    In those cases a secret value is generated
    if neither a custom-secret-value nor an existing-secret is configured.

    Checks the following values:

    - `auth.password`
    """

    is_secret_owner = True

    derived_password = "stub-derived-value"

    def test_auth_password_has_random_value(self, chart):
        if not self.is_secret_owner:
            pytest.skip(reason="Chart is not the Secret owner.")
        values = self.load_and_map(
            """
            global:
              secrets:
                masterPassword: ""
            auth:
              password: null
              existingSecret:
                name: null
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

            auth:
              password: null
              existingSecret:
                name: null
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

            auth:
              password: "stub-password"
              existingSecret:
                name: null
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        annotations = secret.findone("metadata.annotations", default={})
        helm_resource_policy = annotations.get("helm.sh/resource-policy")
        assert helm_resource_policy == "keep"


class AuthSecretGenerationUser(AuthSecretGeneration):
    """
    Partial client test focused only on the Secret generation.

    Should be used in cases where the password is used by the helm chart but not owned by it.
    In those cases either a custom-secret-value or an existing-secret is required.
    Secret generation is not supported.

    Checks the following values:

    - `auth.password`
    """

    secret_name = "release-name-test-nubus-common"
    path_password = "stringData.password"

    def test_auth_plain_values_password_is_required(self, chart):
        values = self.load_and_map(
            """
            auth:
              username: "stub-username"
              password: null
              existingSecret:
                name: null
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "password is required" in error.value.stderr

    def test_global_secrets_keep_is_ignored(self, chart):
        """
        Keeping Secrets shall not be supported in pasword User role.

        Random values for a password will never be generated when in User
        role. This is why the configuration `global.secrets.keep` shall not
        have any effect on Secrets in Client role.
        """
        values = self.load_and_map(
            """
            global:
              secrets:
                keep: true

            auth:
              password: "stub-password"
              existingSecret:
                name: null
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        annotations = secret.findone("metadata.annotations", default={})
        helm_resource_policy = annotations.get("helm.sh/resource-policy")
        assert helm_resource_policy != "keep"
