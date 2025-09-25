# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.auth_flavors.password_usage_base import AuthPasswordUsage


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
