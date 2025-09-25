# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.auth_flavors.password_usage_base import AuthPasswordUsage


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
