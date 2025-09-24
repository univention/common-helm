# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import subprocess

import pytest

from .base import BaseTest


class SecretUsageViaVolume:
    """
    Mixin which implements the expected Secret usage via volume mounts.
    """

    path_volume= "..spec.template.spec.volumes[?@.name=='secret-nats']"

    sub_path_volume_mount = "volumeMounts[?@.name=='secret-nats']"

    def assert_correct_secret_usage(self, result, *, name=None, key=None):
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        secret_volume = workload.findone(self.path_volume)
        container = workload.findone(self.path_container)
        secret_volume_mount = container.findone(self.sub_path_volume_mount)

        if name:
            assert secret_volume.findone("secret.secretName") == name

        if key:
            assert secret_volume_mount["subPath"] == key


class Connection(BaseTest):
    """
    Test related to the connection configuration of Nats.

    Tests for the following values:

    - `nats.connection.host`
    - `nats.connection.port`
    """

    default_port = "4222"
    """
    Default client port of Nats.

    See: https://docs.nats.io/running-a-nats-service/nats_docker
    """

    def test_connection_host_is_required(self, chart):
        values = self.load_and_map(
            """
            nats:
              connection:
                host: null
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "connection has to be configured" in error.value.stderr

    @pytest.mark.parametrize("value", [
        "stub-hostname",
        # This value is invalid, but will ensure that "quote" is correctly used
        ":",
    ])
    def test_connection_host_can_be_configured(self, chart, value):
        values = self.load_and_map(
            f"""
            nats:
              connection:
                host: "{value}"
            """)
        result = chart.helm_template(values)
        self.assert_host_value(result, value)

    def test_connection_host_is_templated(self, chart):
        values = self.load_and_map(
            """
            global:
              test: "stub_value"
            nats:
              connection:
                host: "{{ .Values.global.test }}"
            """)
        result = chart.helm_template(values)
        self.assert_host_value(result, "stub_value")

    def test_connection_host_supports_global_default(self, chart):
        values = self.load_and_map(
            """
            global:
              nats:
                connection:
                  host: "global_stub"
            nats:
              connection:
                host: null
        """)
        result = chart.helm_template(values)
        self.assert_host_value(result, "global_stub")

    def test_connection_host_local_overrides_global(self, chart):
        values = self.load_and_map(
            """
            global:
              nats:
                connection:
                  host: "global_stub"
            nats:
              connection:
                host: "local_stub"
        """)
        result = chart.helm_template(values)
        self.assert_host_value(result, "local_stub")

    def test_connection_port_has_default(self, chart):
        values = self.load_and_map(
            """
            nats:
              connection:
                port: null
            """)
        result = chart.helm_template(values)
        self.assert_port_value(result, self.default_port)

    @pytest.mark.parametrize("value", [
        "1234",
        # This value is invalid, but will ensure that "quote" is correctly used
        ":",
    ])
    def test_connection_port_can_be_configured(self, chart, value):
        values = self.load_and_map(
            f"""
            nats:
              connection:
                port: "{value}"
            """)
        result = chart.helm_template(values)
        self.assert_port_value(result, value)

    def test_connection_port_is_templated(self, chart):
        values = self.load_and_map(
            """
            global:
              test: "stub_value"
            nats:
              connection:
                port: "{{ .Values.global.test }}"
            """)
        result = chart.helm_template(values)
        self.assert_port_value(result, "stub_value")

    def test_connection_port_supports_global_default(self, chart):
        values = self.load_and_map(
            """
            global:
              nats:
                connection:
                  port: "global_stub"
            nats:
              connection:
                port: null
        """)
        result = chart.helm_template(values)
        self.assert_port_value(result, "global_stub")

    def test_connection_port_local_overrides_global(self, chart):
        values = self.load_and_map(
            """
            global:
              nats:
                connection:
                  port: "global_stub"
            nats:
              connection:
                port: "local_stub"
        """)
        result = chart.helm_template(values)
        self.assert_port_value(result, "local_stub")

    def assert_host_value(self, result, value):
        raise NotImplementedError("Use a usage mixin or provide your own implementation.")

    def assert_port_value(self, result, value):
        raise NotImplementedError("Use a usage mixin or provide your own implementation.")


class ConnectionViaConfigMap:

    config_map_name = "release-name-test-nubus-common"

    path_host = "data.NATS_HOST"
    path_port = "data.NATS_PORT"

    def assert_host_value(self, result, value):
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        assert value == config_map.findone(self.path_host)

    def assert_port_value(self, result, value):
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        assert value == config_map.findone(self.path_port)
