# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from contextlib import nullcontext as does_not_raise
import subprocess

import pytest

from .base import BaseTest


class ObjectStorage(BaseTest):
    """
    Client configuration for an S3 based object storage.

    We decided to have the access key id inside the generated `Secret` even
    though it is comparable to a username. The rationale is that people tend to
    prefer keeping the access key id also private.
    """

    path_main_container = "spec.template.spec.containers[?@.name=='main']"
    env_access_key_id = "OBJECT_STORAGE_ACCESS_KEY_ID"
    env_secret_access_key = "OBJECT_STORAGE_SECRET_ACCESS_KEY"
    secret_name = "release-name-test-nubus-common-object-storage"

    def test_auth_plain_values_generate_secret(self, chart):
        values = self.load_and_map(
            """
            objectStorage:
              endpoint: "local_stub"
              bucketName: "local_stub"
              auth:
                accessKeyId: "stub-access-key"
                secretAccessKey: "stub-secret-key"
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        assert secret.findone("stringData.accessKeyId") == "stub-access-key"
        assert secret.findone("stringData.secretAccessKey") == "stub-secret-key"

    def test_auth_plain_values_access_key_id_is_templated(self, chart):
        values = self.load_and_map(
            """
            global:
              test: "stub-value"
            objectStorage:
              endpoint: "local_stub"
              bucketName: "local_stub"
              auth:
                accessKeyId: "{{ .Values.global.test }}"
                secretAccessKey: "stub-password"
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        assert secret.findone("stringData.accessKeyId") == "stub-value"

    def test_auth_plain_values_secret_key_is_not_templated(self, chart):
        values = self.load_and_map(
            """
            objectStorage:
              endpoint: "local_stub"
              bucketName: "local_stub"
              auth:
                accessKeyId: "stub-access-key-id"
                secretAccessKey: "{{ value }}"
            """)
        result = chart.helm_template(values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        assert secret.findone("stringData.secretAccessKey") == "{{ value }}"

    def test_auth_plain_values_secret_key_is_required(self, chart, capsys):
        values = self.load_and_map(
            """
            objectStorage:
              endpoint: "local_stub"
              bucketName: "local_stub"
              auth:
                accessKeyId: "stub-access-key"
                secretAccessKey: null
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "Object Storage credentials have to be supplied" in error.value.stderr

    def test_auth_plain_values_access_key_is_required(self, chart):
        values = self.load_and_map(
            """
            objectStorage:
              endpoint: "local_stub"
              bucketName: "local_stub"
              auth:
                accessKeyId: null
                secretAccessKey: "stub-secret-key"
            """)
        with pytest.raises(subprocess.CalledProcessError) as error:
            chart.helm_template(values)
        assert "Object Storage credentials have to be supplied" in error.value.stderr

    def test_auth_existing_secret_does_not_generate_a_secret(self, chart):
        values = self.load_and_map(
            """
            objectStorage:
              endpoint: "local_stub"
              bucketName: "local_stub"
              auth:
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        with pytest.raises(LookupError):
            result.get_resource(kind="Secret", name=self.secret_name)

    def test_auth_existing_secret_does_not_require_plain_password(self, chart):
        values = self.load_and_map(
            """
            objectStorage:
              endpoint: "local_stub"
              bucketName: "local_stub"
              auth:
                secretAccessKey: null
                existingSecret:
                  name: "stub-secret-name"
            """)
        with does_not_raise():
            chart.helm_template(values)

    def test_auth_existing_secret_used_to_populate_environment_variables(self, chart):
        values = self.load_and_map(
            """
            objectStorage:
              endpoint: "local_stub"
              bucketName: "local_stub"
              auth:
                existingSecret:
                  name: "stub-secret-name"

            """)
        result = chart.helm_template(values)
        deployment = result.get_resource(kind="Deployment")
        main_container = deployment.findone(self.path_main_container)

        access_key_id = main_container.findone(f"env[?@name=='{self.env_access_key_id}']")
        assert access_key_id.findone("valueFrom.secretKeyRef.name") == "stub-secret-name"

        secret_access_key = main_container.findone(f"env[?@name=='{self.env_secret_access_key}']")
        assert secret_access_key.findone("valueFrom.secretKeyRef.name") == "stub-secret-name"

    def test_auth_existing_secret_uses_correct_default_key(self, chart):
        values = self.load_and_map(
            """
            objectStorage:
              auth:
                existingSecret:
                  name: "stub-secret-name"
            """)
        result = chart.helm_template(values)
        deployment = result.get_resource(kind="Deployment")
        main_container = deployment.findone(self.path_main_container)

        access_key_id = main_container.findone(f"env[?@name=='{self.env_access_key_id}']")
        assert access_key_id.findone("valueFrom.secretKeyRef.key") == "access_key_id"

        secret_access_key = main_container.findone(f"env[?@name=='{self.env_secret_access_key}']")
        assert secret_access_key.findone(
            "valueFrom.secretKeyRef.key",
        ) == "secret_access_key"

    def test_auth_existing_secret_uses_correct_custom_key(self, chart):
        values = self.load_and_map(
            """
            objectStorage:
              auth:
                existingSecret:
                  name: "stub-secret-name"
                  keyMapping:
                    access_key_id: "stub_access_key_id_key"
                    secret_access_key: "stub_secret_access_key_key"
            """)
        result = chart.helm_template(values)
        deployment = result.get_resource(kind="Deployment")
        main_container = deployment.findone(self.path_main_container)

        access_key_id = main_container.findone(f"env[?@name=='{self.env_access_key_id}']")
        assert access_key_id.findone("valueFrom.secretKeyRef.key") == "stub_access_key_id_key"

        secret_access_key = main_container.findone(f"env[?@name=='{self.env_secret_access_key}']")
        assert secret_access_key.findone(
            "valueFrom.secretKeyRef.key",
        ) == "stub_secret_access_key_key"

    def test_auth_existing_secret_has_precedence(self, chart):
        values = self.load_and_map(
            """
            objectStorage:
              auth:
                accessKeyId: stub-access-key
                secretAccessKey: stub-secret-key
                existingSecret:
                  name: "stub-secret-name"
                  keyMapping:
                    accessKeyId: "stub_access_key_id_key"
                    secretAccessKey: "stub_secret_access_key_key"
            """)
        result = chart.helm_template(values)
        with pytest.raises(LookupError):
            result.get_resource(kind="Secret", name=self.secret_name)

        deployment = result.get_resource(kind="Deployment")
        main_container = deployment.findone(self.path_main_container)

        access_key_id = main_container.findone(f"env[?@name=='{self.env_access_key_id}']")
        assert access_key_id.findone("valueFrom.secretKeyRef.name") == "stub-secret-name"

        secret_access_key = main_container.findone(f"env[?@name=='{self.env_secret_access_key}']")
        assert secret_access_key.findone("valueFrom.secretKeyRef.name") == "stub-secret-name"

    def test_global_secrets_keep_is_ignored(self, chart):
        """
        Keeping Secrets shall not be supported in Client role.

        Random values for a password will never be generated when in Client
        role. This is why the configuration `global.secrets.keep` shall not
        have any effect on Secrets in Client role.
        """
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
