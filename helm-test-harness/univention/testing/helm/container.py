# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from pytest_helm.manifests.base import Base
from pytest_helm.utils import findone, add_jsonpath_prefix
from yaml import safe_load


class ContainerEnvVarSecret(Base):
    """
    Test harness class to validate the `container` section of a kubernetes Pod manifest
    focussing on templating of paswords mounted as env values.
    The pod manifest must be embedded in a Deployment, StatefulSet or Job manifes.
    Supporting:
    - Injected passwords via helm values
    - Passwords via configured existingSecretsSecret
    - (optional) Generated passwords
    """
    container_name = ""

    def test_auth_existing_secret_custom_name( self, helm, chart_path, key, env_var,):
        values = add_jsonpath_prefix(
            key,
            safe_load(
                """
                auth:
                  existingSecret:
                    name: "stub-secret-name"
            """,
            ),
        )
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        env = findone(
            deployment,
            f"spec.template.spec.containers[?@.name=='{self.container_name}'].env[?@.name=='{env_var}']",
        )
        assert env["valueFrom"]["secretKeyRef"]["name"] == "stub-secret-name"
        assert env["valueFrom"]["secretKeyRef"]["key"] == "password"

    def test_auth_disabling_existing_secret( self, helm, chart_path, key, env_var):
        values = add_jsonpath_prefix(
            key,
            safe_load(
                """
                auth:
                  existingSecret: null
            """,
            ),
        )
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        env = findone(
            deployment,
            f"spec.template.spec.containers[?@.name=='{self.container_name}'].env[?@.name=='{env_var}']",
        )
        assert env["valueFrom"]["secretKeyRef"]["name"].startswith(
            f"release-name-{self.container_name}",
        )
        assert env["valueFrom"]["secretKeyRef"]["key"] == "password"

    def test_auth_existing_secret_custom_key( self, helm, chart_path, key, env_var,):
        values = add_jsonpath_prefix(
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
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        env = findone(
            deployment,
            f"spec.template.spec.containers[?@.name=='{self.container_name}'].env[?@.name=='{env_var}']",
        )
        assert env["valueFrom"]["secretKeyRef"]["name"] == "stub-secret-name"
        assert env["valueFrom"]["secretKeyRef"]["key"] == "stub_password_key"

    def test_auth_existing_secret_has_precedence( self, helm, chart_path, key, env_var,):
        values = add_jsonpath_prefix(
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
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        env = findone(
            deployment,
            f"spec.template.spec.containers[?@.name=='{self.container_name}'].env[?@.name=='{env_var}']",
        )
        assert env["valueFrom"]["secretKeyRef"]["name"] == "stub-secret-name"
        assert env["valueFrom"]["secretKeyRef"]["key"] == "stub_password_key"

