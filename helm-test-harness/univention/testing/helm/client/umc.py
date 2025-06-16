# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import subprocess

import pytest

from .base import BaseTest


class Connection(BaseTest):

    config_map_name = "release-name-test-nubus-common"

    path_url = "data.UMC_SERVER_URL"

    def test_connection_url_is_required(self, chart):
        values = self.load_and_map(
            """
            umc:
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
            umc:
              connection:
                url: "{{ .Values.global.test }}"
            """)
        result = chart.helm_template(values)
        self.assert_connection_url_value(result, "stub_value")

    def test_connection_url_supports_global_default(self, chart):
        values = self.load_and_map(
            """
            global:
              umc:
                connection:
                  url: "global_stub"
            umc:
              connection:
                url: null
            """)
        result = chart.helm_template(values)
        self.assert_connection_url_value(result, "global_stub")

    def test_connection_url_local_overrides_global(self, chart):
        values = self.load_and_map(
            """
            global:
              umc:
                connection:
                  url: "global_stub"
            umc:
              connection:
                url: "local_stub"
        """)
        result = chart.helm_template(values)
        self.assert_connection_url_value(result, "local_stub")

    def assert_connection_url_value(self, result, value):
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        assert config_map.findone(self.path_url) == value
