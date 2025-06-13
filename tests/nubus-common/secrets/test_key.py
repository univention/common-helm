# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from pytest_helm.utils import load_yaml


def test_uses_key_name_as_default_in_key_mapping(chart):
    values = load_yaml(
        """
        client:
          auth:
            existingSecret:
              name: "stub-name"
              keyMapping:
                password: null
        """)
    result = chart.helm_template(values, template_file="templates/secrets/test_key.yaml")
    resource = result.get_resource()
    data = resource["data"]

    assert data["secretKey"] == "password"

def test_handles_key_mapping_as_null_gracefully(chart):
    values = load_yaml(
        """
        client:
          auth:
            existingSecret:
              name: ""
              keyMapping: null
        """)
    result = chart.helm_template(values, template_file="templates/secrets/test_key.yaml")
    resource = result.get_resource()
    data = resource["data"]

    assert data["secretKey"] == "password"
