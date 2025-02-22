# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from yaml import safe_load

from utils import findone


def test_client_auth_plain_values_generate_secret(helm, chart_path):
    values = safe_load(
        """
        client:
          connection:
            url: "local_stub"
          auth:
            username: "stub-username"
            password: "stub-password"
    """)
    result = helm.helm_template(chart_path, values)
    secret = helm.get_resource(result, kind="Secret", name="release-name-test-nubus-common-client")

    assert findone(secret, "stringData.password") == "stub-password"
