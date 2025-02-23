# TODO: Move this module into installable package

from contextlib import nullcontext as does_not_raise
from collections.abc import Mapping

import pytest
from yaml import safe_load, safe_dump

from utils import findone


type JSONPath = str
type PrefixMapping = Mapping[JSONPath, JSONPath]


# NOTE: We want to have the values + linter_values always be passing the
# schema validation and required checks. So in some way we have to "unset"
# a value to verify that something is required. At the same time we want to
# be sure that nothing else is missing so that we check exactly for the
# item under test.


class UdmClient:
    """
    UDM Rest API Client configuration

    Checks of the expected behavior around the configuration of the UDM Rest
    API client.
    """

    prefix_mapping: PrefixMapping = {}

    path_udm_api_url: str = "data.UDM_API_URL"

    def load_and_map(self, values_yaml: str):
        values = safe_load(values_yaml)
        apply_mapping(values, self.prefix_mapping)
        return values

    def test_connection_url_is_required(self, helm, chart_path):
        # TODO: Ensure that "client.connection.url" is removed from linter values
        values = self.load_and_map(
            """
            udm:
              connection:
                url: null
              auth:
                username: "stub-username"
                password: "stub-password"
            """)
        with pytest.raises(RuntimeError):
            helm.helm_template(chart_path, values)

    def test_connection_url_is_templated(self, helm, chart_path):
        values = self.load_and_map(
            """
            global:
              test: "stub_value"
            udm:
              connection:
                url: "{{ .Values.global.test }}"
              auth:
                username: "stub-username"
                password: "stub-password"
            """)
        result = helm.helm_template(chart_path, values)
        config_map = helm.get_resource(result, kind="ConfigMap")
        assert findone(config_map, self.path_udm_api_url) == "stub_value"

    def test_connection_url_supports_global_default(self, helm, chart_path):
        values = self.load_and_map(
            """
            global:
              udm:
                connection:
                  url: "global_stub"
            udm:
              connection:
                url: null
              auth:
                username: "stub-username"
                password: "stub-password"
        """)
        result = helm.helm_template(chart_path, values)
        config_map = helm.get_resource(result, kind="ConfigMap")
        assert findone(config_map, self.path_udm_api_url) == "global_stub"

    def test_connection_url_local_overrides_global(self, helm, chart_path):
        values = self.load_and_map(
            """
            global:
              udm:
                connection:
                  url: "global_stub"
            udm:
              connection:
                url: "local_stub"
              auth:
                username: "stub-username"
                password: "stub-password"
        """)
        result = helm.helm_template(chart_path, values)
        config_map = helm.get_resource(result, kind="ConfigMap")
        assert config_map["data"]["CLIENT_API_URL"] == "local_stub"


    def test_auth_plain_values_generate_secret(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                username: "stub-username"
                password: "stub-password"
        """)
        result = helm.helm_template(chart_path, values)
        secret = helm.get_resource(result, kind="Secret", name="release-name-test-nubus-common-client")

        assert findone(secret, "stringData.password") == "stub-password"


    def test_auth_plain_values_provide_username_via_config_map(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                username: "stub-username"
                password: "stub-password"
        """)
        result = helm.helm_template(chart_path, values)
        config_map = helm.get_resource(result, kind="ConfigMap")
        assert findone(config_map, "data.CLIENT_API_USERNAME") == "stub-username"


    def test_auth_plain_values_username_is_templated(self, helm, chart_path):
        values = self.load_and_map(
            """
            global:
              test: "stub-value"
            udm:
              connection:
                url: "local_stub"
              auth:
                username: "{{ .Values.global.test }}"
                password: "stub-password"
        """)
        result = helm.helm_template(chart_path, values)
        config_map = helm.get_resource(result, kind="ConfigMap")
        assert findone(config_map, "data.CLIENT_API_USERNAME") == "stub-value"


    def test_auth_plain_values_password_is_not_templated(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                username: "stub-username"
                password: "{{ value }}"
        """)
        result = helm.helm_template(chart_path, values)
        secret = helm.get_resource(result, kind="Secret", name="release-name-test-nubus-common-client")
        assert findone(secret, "stringData.password") == "{{ value }}"


    def test_auth_plain_values_password_is_required(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                username: "stub-username"
                password: null
        """)
        with pytest.raises(RuntimeError):
            helm.helm_template(chart_path, values)


    def test_auth_username_is_required(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                username: null
        """)
        with pytest.raises(RuntimeError):
            helm.helm_template(chart_path, values)


    def test_auth_username_has_default(self, helm, chart_path):
        # TODO: Ensure that "client.auth.username" is removed from linter-values before applying
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                password: "stub-password"
        """)
        result = helm.helm_template(chart_path, values)
        config_map = helm.get_resource(result, kind="ConfigMap")
        assert findone(config_map, "data.CLIENT_API_USERNAME") == "stub-values-username"


    def test_auth_existing_secret_does_not_generate_a_secret(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                existingSecret:
                  name: "stub-secret-name"
        """)
        result = helm.helm_template(chart_path, values)
        with pytest.raises(LookupError):
            helm.get_resource(result, kind="Secret", name="release-name-test-nubus-common-client")


    def test_auth_existing_secret_does_not_require_plain_password(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                password: null
                existingSecret:
                  name: "stub-secret-name"
        """)
        with does_not_raise():
            helm.helm_template(chart_path, values)


    def test_auth_existing_secret_mounts_password(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                existingSecret:
                  name: "stub-secret-name"
        """)
        result = helm.helm_template(chart_path, values)
        deployment = helm.get_resource(result, kind="Deployment")
        secret_udm_volume = findone(deployment, "spec.template.spec.volumes[?@.name=='secret-client']")
        assert findone(secret_udm_volume, "secret.secretName") == "stub-secret-name"


    def test_auth_existing_secret_mounts_correct_default_key(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                existingSecret:
                  name: "stub-secret-name"
        """)
        result = helm.helm_template(chart_path, values)
        deployment = helm.get_resource(result, kind="Deployment")
        main_container = findone(deployment, "spec.template.spec.containers[?@.name=='main']")
        secret_udm_volume_mount = findone(main_container, "volumeMounts[?@.name=='secret-client']")

        assert secret_udm_volume_mount["subPath"] == "password"


    def test_auth_disabling_existing_secret_by_setting_it_to_null(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                username: "stub-username"
                password: "stub-password"
                existingSecret: null
        """)
        result = helm.helm_template(chart_path, values)
        deployment = helm.get_resource(result, kind="Deployment")
        secret_udm_volume = findone(deployment, "spec.template.spec.volumes[?@.name=='secret-client']")
        main_container = findone(deployment, "spec.template.spec.containers[?@.name=='main']")
        secret_udm_volume_mount = findone(main_container, "volumeMounts[?@.name=='secret-client']")

        assert secret_udm_volume_mount["subPath"] == "password"
        assert findone(
            secret_udm_volume,
            "secret.secretName") == "release-name-test-nubus-common-client"


    def test_auth_existing_secret_mounts_correct_custom_key(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                existingSecret:
                  name: "stub-secret-name"
                  keyMapping:
                    password: "stub_password_key"
        """)
        result = helm.helm_template(chart_path, values)
        deployment = helm.get_resource(result, kind="Deployment")
        main_container = findone(deployment, "spec.template.spec.containers[?@.name=='main']")
        secret_udm_volume_mount = findone(main_container, "volumeMounts[?@.name=='secret-client']")

        assert secret_udm_volume_mount["subPath"] == "stub_password_key"


    def test_auth_existing_secret_has_precedence(self, helm, chart_path):
        values = self.load_and_map(
            """
            udm:
              connection:
                url: "local_stub"
              auth:
                password: stub-plain-password
                existingSecret:
                  name: "stub-secret-name"
                  keyMapping:
                    password: "stub_password_key"
        """)
        # TODO: Fix upstream, always return a list
        result = list(helm.helm_template(chart_path, values))
        with pytest.raises(LookupError):
            helm.get_resource(result, kind="Secret", name="release-name-test-nubus-common-client")

        deployment = helm.get_resource(result, kind="Deployment")
        secret_udm_volume = findone(deployment, "spec.template.spec.volumes[?@.name=='secret-client']")
        main_container = findone(deployment, "spec.template.spec.containers[?@.name=='main']")
        secret_udm_volume_mount = findone(main_container, "volumeMounts[?@.name=='secret-client']")

        assert secret_udm_volume_mount["subPath"] == "stub_password_key"
        assert findone(secret_udm_volume, "secret.secretName") == "stub-secret-name"


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
    else:
        return values[source_path[0]]


def _set_value(values: Mapping, target_path: list[str], value: any) -> None:
    if len(target_path) >= 2:
        sub_values = values.setdefault(target_path[0], {})
        sub_path = target_path[1:]
        _set_value(sub_values, sub_path, value)
    else:
        values[target_path[0]] = value
