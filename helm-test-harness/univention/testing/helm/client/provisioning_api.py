# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import subprocess

import pytest

from .base import BaseTest


class Connection(BaseTest):

    config_map_name = None

    path_provisioning_api_url = "data.PROVISIONING_API_URL"

    def test_connection_url_is_required(self, chart):
        values = self.load_and_map(
            """
            provisioningApi:
              connection:
                url: null
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "connection has to be configured" in error.value.stderr

    def test_connection_url_is_templated(self, chart):
        values = self.load_and_map(
            """
            global:
              test: "stub_value"
            provisioningApi:
              connection:
                url: "{{ .Values.global.test }}"
            """)
        result = chart.helm_template(values)
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        assert config_map.findone(self.path_provisioning_api_url) == "stub_value"
