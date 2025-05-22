# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from contextlib import nullcontext as does_not_raise
from collections.abc import Mapping
import subprocess

import pytest
from yaml import safe_load

# TODO: Change once the Python version has been upgraded in the test runner to >= 3.12
JSONPath = str
PrefixMapping = Mapping[JSONPath, JSONPath]
# type JSONPath = str
# type PrefixMapping = Mapping[JSONPath, JSONPath]


class ObjectStorage:
    """
    Client configuration for an S3 based object storage.
    """

    prefix_mapping: PrefixMapping = {}

    path_main_container = "spec.template.spec.containers[?@.name=='main']"
    env_access_key_id = "OBJECT_STORAGE_ACCESS_KEY_ID"
    env_secret_access_key = "OBJECT_STORAGE_SECRET_ACCESS_KEY"
    secret_name = "release-name-test-nubus-common-object-storage"

    def load_and_map(self, values_yaml: str):
        values = safe_load(values_yaml)
        apply_mapping(values, self.prefix_mapping)
        return values

    def test_auth_plain_values_generate_secret(self, helm, chart_path):
        values = self.load_and_map(
            """
            objectStorage:
              endpoint: "local_stub"
              bucketName: "local_stub"
              auth:
                accessKeyId: "stub-access-key"
                secretAccessKey: "stub-secret-key"
        """,
        )
        result = helm.helm_template(chart_path, values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        assert secret.findone("stringData.accessKeyId") == "stub-access-key"
        assert secret.findone("stringData.secretAccessKey") == "stub-secret-key"

    def test_auth_plain_values_access_key_id_is_templated(self, helm, chart_path):
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
        """,
        )
        result = helm.helm_template(chart_path, values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        assert secret.findone("stringData.accessKeyId") == "stub-value"

    def test_auth_plain_values_secret_key_is_not_templated(self, helm, chart_path):
        values = self.load_and_map(
            """
            objectStorage:
              endpoint: "local_stub"
              bucketName: "local_stub"
              auth:
                accessKeyId: "stub-access-key-id"
                secretAccessKey: "{{ value }}"
        """,
        )
        result = helm.helm_template(chart_path, values)
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        assert secret.findone("stringData.secretAccessKey") == "{{ value }}"

    def test_auth_plain_values_secret_key_is_required(self, helm, chart_path, capsys):
        values = self.load_and_map(
            """
            objectStorage:
              endpoint: "local_stub"
              bucketName: "local_stub"
              auth:
                accessKeyId: "stub-access-key"
                secretAccessKey: null
        """,
        )
        with pytest.raises(subprocess.CalledProcessError) as error:
            helm.helm_template(chart_path, values)
        assert "Object Storage credentials have to be supplied" in error.value.stderr

    def test_auth_plain_values_access_key_is_required(self, helm, chart_path):
        values = self.load_and_map(
            """
            objectStorage:
              endpoint: "local_stub"
              bucketName: "local_stub"
              auth:
                accessKeyId: null
                secretAccessKey: "stub-secret-key"
        """,
        )
        with pytest.raises(subprocess.CalledProcessError) as error:
            helm.helm_template(chart_path, values)
        assert "Object Storage credentials have to be supplied" in error.value.stderr

    def test_auth_existing_secret_does_not_generate_a_secret(self, helm, chart_path):
        values = self.load_and_map(
            """
            objectStorage:
              endpoint: "local_stub"
              bucketName: "local_stub"
              auth:
                existingSecret:
                  name: "stub-secret-name"
        """,
        )
        result = helm.helm_template(chart_path, values)
        with pytest.raises(LookupError):
            result.get_resource(kind="Secret", name=self.secret_name)

    def test_auth_existing_secret_does_not_require_plain_password(self, helm, chart_path):
        values = self.load_and_map(
            """
            objectStorage:
              endpoint: "local_stub"
              bucketName: "local_stub"
              auth:
                secretAccessKey: null
                existingSecret:
                  name: "stub-secret-name"
        """,
        )
        with does_not_raise():
            helm.helm_template(chart_path, values)

    def test_auth_existing_secret_env_password(self, helm, chart_path):
        values = self.load_and_map(
            """
            objectStorage:
              endpoint: "local_stub"
              bucketName: "local_stub"
              auth:
                existingSecret:
                  name: "stub-secret-name"

        """,
        )
        result = helm.helm_template(chart_path, values)
        deployment = result.get_resource(kind="Deployment")
        main_container = deployment.findone(self.path_main_container)

        access_key_id = main_container.findone(f"env[?@name=='{self.env_access_key_id}']")
        assert access_key_id.findone("valueFrom.secretKeyRef.name") == "stub-secret-name"

        secret_access_key = main_container.findone(f"env[?@name=='{self.env_secret_access_key}']")
        assert secret_access_key.findone("valueFrom.secretKeyRef.name") == "stub-secret-name"

    def test_auth_existing_secret_mounts_correct_custom_key(self, helm, chart_path):
        values = self.load_and_map(
            """
            objectStorage:
              auth:
                existingSecret:
                  name: "stub-secret-name"
                  keyMapping:
                    accessKeyId: "stub_access_key_id_key"
                    secretAccessKey: "stub_secret_access_key_key"
        """,
        )
        result = helm.helm_template(chart_path, values)
        deployment = result.get_resource(kind="Deployment")
        main_container = deployment.findone(self.path_main_container)

        access_key_id = main_container.findone(f"env[?@name=='{self.env_access_key_id}']")
        assert access_key_id.findone("valueFrom.secretKeyRef.key") == "stub_access_key_id_key"

        secret_access_key = main_container.findone(f"env[?@name=='{self.env_secret_access_key}']")
        assert secret_access_key.findone(
            "valueFrom.secretKeyRef.key",
        ) == "stub_secret_access_key_key"

    def test_auth_existing_secret_has_precedence(self, helm, chart_path):
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
        """,
        )
        result = helm.helm_template(chart_path, values)
        with pytest.raises(LookupError):
            result.get_resource(kind="Secret", name=self.secret_name)

        deployment = result.get_resource(kind="Deployment")
        main_container = deployment.findone(self.path_main_container)

        access_key_id = main_container.findone(f"env[?@name=='{self.env_access_key_id}']")
        assert access_key_id.findone("valueFrom.secretKeyRef.name") == "stub-secret-name"

        secret_access_key = main_container.findone(f"env[?@name=='{self.env_secret_access_key}']")
        assert secret_access_key.findone("valueFrom.secretKeyRef.name") == "stub-secret-name"


def apply_mapping(values: Mapping, prefix_mapping: PrefixMapping) -> None:
    for target, source in prefix_mapping.items():
        _move(values, target, source)


def _move(values: Mapping, target: JSONPath, source: JSONPath) -> None:
    target_path = target.split(".")
    source_path = source.split(".")
    try:
        value = _pop_value(values, source_path)
    except KeyError:
        # Source does not exist, there is nothing to map.
        pass
    else:
        _set_value(values, target_path, value)


def _pop_value(values: Mapping, source_path: list[str]) -> any:
    if len(source_path) >= 2:
        sub_values = values[source_path[0]]
        sub_path = source_path[1:]
        return _pop_value(sub_values, sub_path)
    return values[source_path[0]]


def _set_value(values: Mapping, target_path: list[str], value: any) -> None:
    if len(target_path) >= 2:
        sub_values = values.setdefault(target_path[0], {})
        sub_path = target_path[1:]
        _set_value(sub_values, sub_path, value)
    else:
        values[target_path[0]] = value
