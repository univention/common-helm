# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH



import pytest
from .secret_generation_base import AuthSecretGeneration


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
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        annotations = secret.findone("metadata.annotations", default={})
        helm_resource_policy = annotations.get("helm.sh/resource-policy")
        assert helm_resource_policy == "keep"
