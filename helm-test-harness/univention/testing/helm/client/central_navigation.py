# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from contextlib import nullcontext as does_not_raise
import subprocess

import pytest
from pytest_helm.models import HelmTemplateResult

from .base import BaseTest


class CentralNavigationClient(BaseTest):
    """
    Client part of the Central Navigation API of the portal server.
    """

    secret_name = "release-name-test-nubus-common-central-navigation"

    path_main_container = "spec.template.spec.containers[?@.name=='main']"

    path_shared_secret = "stringData.shared_secret"
    path_volume = "spec.template.spec.volumes[?@.name=='secret-central-navigation']"

    sub_path_volume_mount = "volumeMounts[?@.name=='secret-central-navigation']"

    def get_shared_secret(self, result: HelmTemplateResult):
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        return secret.findone(self.path_shared_secret)

    def test_auth_plain_values_does_not_generate_secret_if_disabled(self, chart):
        values = self.load_and_map(
            """
            centralNavigation:
              enabled: false
              auth:
                sharedSecret: "stub-secret"
            """)
        result = chart.helm_template(values)
        with pytest.raises(LookupError):
            result.get_resource(kind="Secret", name=self.secret_name)

    def test_auth_plain_values_generate_secret(self, chart):
        values = self.load_and_map(
            """
            centralNavigation:
              auth:
                sharedSecret: "stub-secret"
            """)
        result = chart.helm_template(values)
        shared_secret = self.get_shared_secret(result)
        assert shared_secret == "stub-secret"

    def test_auth_plain_values_shared_secret_is_not_templated(self, chart):
        values = self.load_and_map(
            """
            centralNavigation:
              auth:
                sharedSecret: "{{ value }}"
        """)
        result = chart.helm_template(values)
        shared_secret = self.get_shared_secret(result)
        assert shared_secret == "{{ value }}"

    def test_auth_plain_values_shared_secret_is_required(self, chart):
        if self.is_secret_owner:
            pytest.skip(reason="Chart is Secret owner.")
        values = self.load_and_map(
            """
            centralNavigation:
              auth:
                sharedSecret: null
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "shared secret has to be supplied" in error.value.stderr

    def test_auth_existing_secret_does_not_generate_a_secret(self, chart):
        values = self.load_and_map(
            """
            centralNavigation:
              auth:
                existingSecret:
                  name: "stub-secret-name"
        """,
        )
        result = chart.helm_template(values)
        with pytest.raises(LookupError):
            result.get_resource(kind="Secret", name=self.secret_name)

    def test_auth_existing_secret_does_not_require_plain_shared_secret(self, chart):
        values = self.load_and_map(
            """
            centralNavigation:
              auth:
                sharedSecret: null
                existingSecret:
                  name: "stub-secret-name"
        """,
        )
        with does_not_raise():
            chart.helm_template(values)

    def test_auth_existing_secret_mounts_shared_secret(self, chart):
        values = self.load_and_map(
            """
            centralNavigation:
              auth:
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        deployment = result.get_resource(kind="Deployment")
        secret_central_navigation_volume = deployment.findone(self.path_volume)
        assert secret_central_navigation_volume.findone("secret.secretName") == "stub-secret-name"

    def test_auth_existing_secret_mounts_correct_default_key(self, chart):
        values = self.load_and_map(
            """
            centralNavigation:
              auth:
                existingSecret:
                  name: "stub-secret-name"
        """,
        )
        result = chart.helm_template(values)
        deployment = result.get_resource(kind="Deployment")
        main_container = deployment.findone(self.path_main_container)
        secret_central_navigation_volume_mount = main_container.findone(self.sub_path_volume_mount)

        assert secret_central_navigation_volume_mount["subPath"] == "shared_secret"

    def test_auth_disabling_existing_secret_by_setting_it_to_null(self, chart):
        values = self.load_and_map(
            """
            centralNavigation:
              auth:
                sharedSecret: "stub-shared-secret"
                existingSecret: null
        """)
        result = chart.helm_template(values)
        deployment = result.get_resource(kind="Deployment")
        secret_central_navigation_volume = deployment.findone(self.path_volume)
        main_container = deployment.findone(self.path_main_container)
        secret_central_navigation_volume_mount = main_container.findone(self.sub_path_volume_mount)

        assert secret_central_navigation_volume_mount["subPath"] == "shared_secret"
        assert secret_central_navigation_volume.findone("secret.secretName") == self.secret_name

    def test_auth_existing_secret_mounts_correct_custom_key(self, chart):
        values = self.load_and_map(
            """
            centralNavigation:
              auth:
                existingSecret:
                  name: "stub-secret-name"
                  keyMapping:
                    shared_secret: "stub_shared_secret_key"
        """,
        )
        result = chart.helm_template(values)
        deployment = result.get_resource(kind="Deployment")
        main_container = deployment.findone(self.path_main_container)
        secret_central_navigation_volume_mount = main_container.findone(self.sub_path_volume_mount)

        assert secret_central_navigation_volume_mount["subPath"] == "stub_shared_secret_key"

    def test_auth_existing_secret_has_precedence(self, chart):
        values = self.load_and_map(
            """
            centralNavigation:
              auth:
                sharedSecret: stub-plain-shared-secret
                existingSecret:
                  name: "stub-secret-name"
                  keyMapping:
                    shared_secret: "stub_shared_secret_key"
        """,
        )
        result = chart.helm_template(values)
        with pytest.raises(LookupError):
            result.get_resource(kind="Secret", name=self.secret_name)

        deployment = result.get_resource(kind="Deployment")
        secret_central_navigation_volume = deployment.findone(self.path_volume)
        main_container = deployment.findone(self.path_main_container)
        secret_central_navigation_volume_mount = main_container.findone(self.sub_path_volume_mount)

        assert secret_central_navigation_volume_mount["subPath"] == "stub_shared_secret_key"
        assert secret_central_navigation_volume.findone("secret.secretName") == "stub-secret-name"

    def test_global_secrets_keep_is_ignored(self, chart):
        """
        Keeping Secrets shall not be supported in Client role.

        Random values for a password will never be generated when in Client
        role. This is why the configuration `global.secrets.keep` shall not
        have any effect on Secrets in Client role.
        """
        if self.is_secret_owner:
            pytest.skip(reason="Chart is Secret owner.")
        values = self.load_and_map(
            """
            global:
              secrets:
                keep: true
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        annotations = secret.findone("metadata.annotations", default={})
        helm_resource_policy = annotations.get("helm.sh/resource-policy")
        assert helm_resource_policy != "keep"


class CentralNavigationOwner(CentralNavigationClient):

    is_secret_owner = True

    derived_shared_secret = "stub-derived-value"

    def test_auth_shared_secret_has_random_value(self, chart):
        if not self.is_secret_owner:
            pytest.skip(reason="Chart is not the Secret owner.")
        values = self.load_and_map(
            """
            centralNavigation:
              auth:
                sharedSecret: null
            """)

        result = chart.helm_template(values, template_file="templates/secret-central-navigation.yaml")
        shared_secret = self.get_shared_secret(result)
        result_2 = chart.helm_template(values, template_file="templates/secret-central-navigation.yaml")
        shared_secret_2 = self.get_shared_secret(result_2)

        assert shared_secret != shared_secret_2

    def test_auth_shared_secret_is_derived_from_master_password(self, chart):
        if not self.is_secret_owner:
            pytest.skip(reason="Chart is not the Secret owner.")
        values = self.load_and_map(
            """
            global:
              secrets:
                masterPassword: "stub-master-password"

            centralNavigation:
              auth:
                sharedSecret: null
            """)
        result = chart.helm_template(values, template_file="templates/secret-central-navigation.yaml")
        shared_secret = self.get_shared_secret(result)
        assert shared_secret == self.derived_shared_secret

    def test_global_secrets_keep_is_respected(self, chart):
        if not self.is_secret_owner:
            pytest.skip(reason="Chart is not the Secret owner.")
        values = self.load_and_map(
            """
            global:
              secrets:
                keep: true

            centralNavigation:
              auth:
                sharedSecret: "stub-value"
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        annotations = secret.findone("metadata.annotations", default={})
        helm_resource_policy = annotations.get("helm.sh/resource-policy")
        assert helm_resource_policy == "keep"
