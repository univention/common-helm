# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


import subprocess
import pytest
from .secret_generation_base import AuthSecretGeneration


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
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        annotations = secret.findone("metadata.annotations", default={})
        helm_resource_policy = annotations.get("helm.sh/resource-policy")
        assert helm_resource_policy != "keep"
