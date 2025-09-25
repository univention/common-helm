# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import re
import subprocess

import pytest

from pytest_helm.models import HelmTemplateResult


class NatsCreateUserMixin:
    workload_kind = "StatefulSet"
    workload_name = "release-name-provisioning-nats"
    config_map_name = "release-name-provisioning-nats-config"
    env_password = "TESTUSER"

    def get_username(self, result: HelmTemplateResult):
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        config = config_map["data"]["nats.conf"]
        match = re.search(rf' +user: (.+)\n +password: \${self.env_password}\n', config)
        assert match
        return match.group(1)

    def test_password_env_in_nats_conf(self, chart):
        result = chart.helm_template()
        config_map = result.get_resource(kind="ConfigMap", name=self.config_map_name)
        config = config_map["data"]["nats.conf"]
        assert f"password: ${self.env_password}" in config

    @pytest.mark.skip("Nats secrets can only be configured as existing secret")
    def test_auth_disabling_existing_secret_by_setting_it_to_null(self, chart): ...

    def test_auth_existing_secret_is_required(self, chart):
        values = self.load_and_map(
            """
            auth:
              username: "normal-user"
              existingSecret: null
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "auth.existingSecret.name is required" in error.value.stderr
