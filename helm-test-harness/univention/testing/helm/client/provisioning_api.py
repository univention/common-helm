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


class RegistrationSecretUsage(BaseTest):
    """
    Checks the correct secret usage around the user registration.

    This Secret usage check is special because the registration requires an
    existing secret to be configured. Most other implementations support to
    provide also a value in a key like `password` directly.
    """

    secret_name = "stub-secret-name"
    secret_default_key = "registration"
    path_registration = "stringData.registration"

    def assert_correct_secret_usage(self, result, *, name=None, key=None):
        raise NotImplementedError("Use one of the mixins or implement this method.")

    def test_auth_existing_secret_used(self, chart):
        values = self.load_and_map(
            """
            registerConsumers:
              createUsers:
                consumerName:
                  existingSecret:
                    name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, name="stub-secret-name")

    def test_auth_existing_secret_uses_correct_default_key(self, chart):
        values = self.load_and_map(
            """
            registerConsumers:
              createUsers:
                consumerName:
                  existingSecret:
                    name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, key=self.secret_default_key)

    def test_auth_existing_secret_uses_correct_custom_key(self, chart):
        values = self.load_and_map(
            """
            registerConsumers:
              createUsers:
                consumerName:
                  existingSecret:
                    name: "stub-secret-name"
                    keyMapping:
                      registration: "stub_registration_key"
            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, key="stub_registration_key")

    def test_auth_existing_secret_is_required(self, chart):
        values = self.load_and_map(
            """
            registerConsumers:
              createUsers:
                consumerName:
                  existingSecret: null
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "Consumer secrets can only be configured as existing secret" in error.value.stderr


class SecretViaProjectedVolume:
    """
    Mixin which checks the expected Secret usage via a projected volume.
    """

    path_volume= "..spec.template.spec.volumes[?@.name=='consumer-secrets']"

    sub_path_volume_mount = "volumeMounts[?@.name=='consumer-secrets']"

    def assert_correct_secret_usage(self, result, *, name=None, key=None):
        # A projected volume can combine many secrets, that's why this has to
        # use the defaults. This is a difference from the other mixins.
        name = name or self.secret_name
        key = key or self.secret_default_key

        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        secret_volume = workload.findone(self.path_volume)
        assert "projected" in secret_volume
        secret_projection = secret_volume.findone(f"projected.sources[?@secret.name=='{name}']")
        container = workload.findone(self.path_container)
        secret_volume_mount = container.findone(self.sub_path_volume_mount)

        # The projection has to be configured for this secret and it has to
        # have an entry for the key.
        assert secret_projection
        assert secret_projection.findone(f"secret.items[?@key=='{key}']")

        # On the container side we only want to be sure that the volume is mounted.
        assert secret_volume_mount
