# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from pytest_helm.utils import findone, resolve
from yaml import safe_load


class Container:
    manifest = ""
    name = ""

    def test_auth_existing_secret_custom_name( self, helm, chart_path, key, env_var,):
        values = resolve(
            key,
            safe_load(
                """
                auth:
                  existingSecret:
                    name: "stub-secret-name"
            """,
            ),
        )
        deployment = helm.helm_template_file(chart_path, values, self.manifest)
        env = findone(
            deployment,
            f"spec.template.spec.containers[?@.name=='{self.name}'].env[?@.name=='{env_var}']",
        )
        assert env["valueFrom"]["secretKeyRef"]["name"] == "stub-secret-name"
        assert env["valueFrom"]["secretKeyRef"]["key"] == "password"

    def test_auth_disabling_existing_secret( self, helm, chart_path, key, env_var):
        values = resolve(
            key,
            safe_load(
                """
                auth:
                  existingSecret: null
            """,
            ),
        )
        deployment = helm.helm_template_file(chart_path, values, self.manifest)
        env = findone(
            deployment,
            f"spec.template.spec.containers[?@.name=='{self.name}'].env[?@.name=='{env_var}']",
        )
        assert env["valueFrom"]["secretKeyRef"]["name"].startswith(
            f"release-name-{self.name}",
        )
        assert env["valueFrom"]["secretKeyRef"]["key"] == "password"

    def test_auth_existing_secret_custom_key( self, helm, chart_path, key, env_var,):
        values = resolve(
            key,
            safe_load(
                """
                auth:
                  existingSecret:
                    name: "stub-secret-name"
                    keyMapping:
                      password: "stub_password_key"
            """,
            ),
        )
        deployment = helm.helm_template_file(chart_path, values, self.manifest)
        env = findone(
            deployment,
            f"spec.template.spec.containers[?@.name=='{self.name}'].env[?@.name=='{env_var}']",
        )
        assert env["valueFrom"]["secretKeyRef"]["name"] == "stub-secret-name"
        assert env["valueFrom"]["secretKeyRef"]["key"] == "stub_password_key"

    def test_auth_existing_secret_has_precedence( self, helm, chart_path, key, env_var,):
        values = resolve(
            key,
            safe_load(
                """
                auth:
                  password: stub-plain-password
                  existingSecret:
                    name: "stub-secret-name"
                    keyMapping:
                      password: "stub_password_key"
            """,
            ),
        )
        deployment = helm.helm_template_file(chart_path, values, self.manifest)
        env = findone(
            deployment,
            f"spec.template.spec.containers[?@.name=='{self.name}'].env[?@.name=='{env_var}']",
        )
        assert env["valueFrom"]["secretKeyRef"]["name"] == "stub-secret-name"
        assert env["valueFrom"]["secretKeyRef"]["key"] == "stub_password_key"

