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

    def test_auth_existing_secret_is_templated(self, chart):
        values = self.load_and_map(
            """
            global:
              test: "global-stub-value"
            auth:
              username: "normal-user"
              existingSecret:
                name: "{{ .Values.global.test | quote }}"

            """)
        result = chart.helm_template(values)
        self.assert_correct_secret_usage(result, name="global-stub-value")


class AuthPasswordUsageViaEnv(AuthPasswordUsage):
    """
    Mixin which implements the expected Secret usage via environment variables.
    """

    sub_path_env_password = "env[?@name=='PASSWORD']"

    def assert_correct_secret_usage(self, result, *, name=None, key=None):
        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        container = workload.findone(self.path_container)
        password = container.findone(self.sub_path_env_password)

        if name:
            assert password.findone("valueFrom.secretKeyRef.name") == name

        if key:
            assert password.findone("valueFrom.secretKeyRef.key") == key


class AuthPasswordUsageViaVolume(AuthPasswordUsage):
    """
    Mixin which implements the expected Secret usage via volume mounts.

    You usually only need to configure:
    volume_name = "your-volume-name"

    In some cases when you are not testing a Deployment or StatefulSet manifest,
    you need to set the following values instead:

    path_volume= "..spec.template.spec.volumes[?@.name=='test-volume-name']"
    sub_path_volume_mount = "volumeMounts[?@.name=='test-volume-name']"
    """

    volume_name = "test-volume-name"
    path_volume = ""
    sub_path_volume_mount = ""

    def assert_correct_secret_usage(self, result, *, name=None, key=None):

        path_volume = self.path_volume or f"..spec.template.spec.volumes[?@.name=='{self.volume_name}']"
        sub_path_volume_mount = self.sub_path_volume_mount or f"volumeMounts[?@.name=='{self.volume_name}']"

        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        secret_volume = workload.findone(path_volume)
        container = workload.findone(self.path_container)
        secret_volume_mount = container.findone(sub_path_volume_mount)

        if name:
            assert secret_volume.findone("secret.secretName") == name

        if key:
            assert secret_volume_mount["subPath"] == key


class AuthPasswordUsageViaProjectedVolume(AuthPasswordUsage):
    """
    Mixin which checks the expected Secret usage via a projected volume.
    """

    path_volume = ""
    sub_path_volume_mount = ""

    def assert_correct_secret_usage(self, result, *, name=None, key=None):
        # A projected volume can combine many secrets, that's why this has to
        # use the defaults. This is a difference from the other mixins.
        name = name or self.secret_name
        key = key or self.secret_default_key

        path_volume = self.path_volume or f"..spec.template.spec.volumes[?@.name=='{self.volume_name}']"
        sub_path_volume_mount = self.sub_path_volume_mount or f"volumeMounts[?@.name=='{self.volume_name}']"


        workload = result.get_resource(kind=self.workload_kind, name=self.workload_name)
        secret_volume = workload.findone(path_volume)
        assert "projected" in secret_volume
        secret_projection = secret_volume.findone(f"projected.sources[?@secret.name=='{name}']")
        container = workload.findone(self.path_container)
        secret_volume_mount = container.findone(sub_path_volume_mount)

        # The projection has to be configured for this secret and it has to
        # have an entry for the key.
        assert secret_projection
        assert secret_projection.findone(f"secret.items[?@key=='{key}']")

        # On the container side we only want to be sure that the volume is mounted.
        assert secret_volume_mount
