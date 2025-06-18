# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import subprocess

import pytest
from pytest_helm.models import HelmTemplateResult

from .base import BaseTest


class Password(BaseTest):
    """
    Tests a password.

    Combine with the mixin `PasswordOwner` when checking a managed password
    value.

    An example is the initial password of the user "Administrator". This has
    only the password value and does not support to point to an existing
    `Secret` object.
    """

    secret_name = "release-name-test-nubus-common-password"

    path_password = "stringData.password"

    def get_password(self, result: HelmTemplateResult):
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        return secret.findone(self.path_password)

    def assert_password_value(self, result: HelmTemplateResult, value: str):
        password = self.get_password(result)
        assert password == value

    def test_secret_is_generated(self, chart):
        values = self.load_and_map(
            """
            password: "stub-password"
            """)
        result = chart.helm_template(values)
        self.assert_password_value(result, "stub-password")

    def test_password_is_not_templated(self, chart):
        values = self.load_and_map(
            """
            password: "{{ value }}"
            """)
        result = chart.helm_template(values)
        self.assert_password_value(result, "{{ value }}")

    def test_password_is_required(self, chart):
        if self.is_secret_owner:
            pytest.skip(reason="Chart is Secret owner.")
        values = self.load_and_map(
            """
            password: null
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "password has to be supplied" in error.value.stderr

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

            password: "stub-password"
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        annotations = secret.findone("metadata.annotations", default={})
        helm_resource_policy = annotations.get("helm.sh/resource-policy")
        assert helm_resource_policy != "keep"


class PasswordOwner:
    """
    Mixin to configure the test template class for the `Owner` role.

    See: `DefaultAttributes.is_secret_owner`
    """

    is_secret_owner = True

    derived_password = "stub-derived-value"

    def test_password_has_random_value(self, chart):
        if not self.is_secret_owner:
            pytest.skip(reason="Chart is not the Secret owner.")
        values = self.load_and_map(
            """
            password: null
            """)
        result = chart.helm_template(values)
        password = self.get_password(result)
        result_2 = chart.helm_template(values)
        password_2 = self.get_password(result_2)

        assert password != password_2

    def test_password_is_derived_from_master_password(self, chart):
        if not self.is_secret_owner:
            pytest.skip(reason="Chart is not the Secret owner.")
        values = self.load_and_map(
            """
            global:
              secrets:
                masterPassword: "stub-master-password"

            password: null
            """)
        result = chart.helm_template(values)
        self.assert_password_value(result, self.derived_password)

    def test_global_secrets_keep_is_respected(self, chart):
        if not self.is_secret_owner:
            pytest.skip(reason="Chart is not the Secret owner.")
        values = self.load_and_map(
            """
            global:
              secrets:
                keep: true

            password: "stub-password"
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        annotations = secret.findone("metadata.annotations", default={})
        helm_resource_policy = annotations.get("helm.sh/resource-policy")
        assert helm_resource_policy == "keep"
