# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from pytest_helm.utils import add_jsonpath_prefix, get_containers
from univention.testing.helm.base import Base, Labels, Namespace
from pytest_helm.utils import load_yaml


class Deployment(Labels, Namespace):

    def test_pod_security_context_can_be_disabled(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                """
            podSecurityContext:
              enabled: false
              fsGroup: 1000
              fsGroupChangePolicy: "Always"
            """,
            ),
        )
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        pod_spec = deployment["spec"]["template"]["spec"]

        assert "securityContext" not in pod_spec.keys()

    def test_pod_security_context_is_applied(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                """
            podSecurityContext:
              enabled: true
              fsGroup: 1000
              fsGroupChangePolicy: "Always"
              sysctls: null
            """,
            ),
        )
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        pod_security_context = deployment["spec"]["template"]["spec"]["securityContext"]
        expected_security_context = {
            "fsGroup": 1000,
            "fsGroupChangePolicy": "Always",
            "sysctls": None,
        }
        _compare_dict(pod_security_context, expected_security_context, 'pod')

    def test_container_security_context_can_be_disabled(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                """
            containerSecurityContext:
              enabled: false
              capabilities:
                drop: []
              runAsUser: 9876
            """,
            ),
        )
        expected_security_context = {}
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        containers = get_containers(deployment)
        _assert_all_have_security_context(containers, expected_security_context)

    def test_container_security_context_is_applied(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                """
            containerSecurityContext:
              enabled: true
              capabilities:
                drop: []
              runAsUser: 9876
            """,
            ),
        )
        expected_security_context = {
            "capabilities": {
                "drop": [],
            },
            "runAsUser": 9876,
        }

        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        containers = get_containers(deployment)
        _assert_all_have_security_context(containers, expected_security_context)

    def test_has_configuable_service_account(self, helm, chart_path):
        values = load_yaml(
            """
            serviceAccount:
              create: true
            """)
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        service_account_name = deployment["spec"]["template"]["spec"]["serviceAccountName"]
        assert service_account_name.startswith("release-name-"), f"unexpected serviceAccountName: {service_account_name}"


def _assert_all_have_security_context(containers, expected_security_context):
    for container in containers:
        security_context = container.get("securityContext", {})
        name = container["name"]

        _compare_dict(security_context, expected_security_context, name)


def _compare_dict(actual: dict, expected: dict, container: str, invalid_keys: set = ['enabled']):
    '''Compare values in actual dict with value in expected

       We do not know which keys are set from outside so ignore additional keys.
       Also make sure that if a value is None it is the same as if the key is missing,
       helm templates has some special handling here if a key is overriden with null. If
       it was available previously the key will be removed but if it was not available the
       key will be available with value None.
    '''
    for key in invalid_keys:
        assert (key not in actual), f'Invalid key {key} in {container} security context'

    for key, value in expected.items():
        assert (
            key in actual or value is None
        ), f'Failed to find expected key {key} in {container} security context'

        if key not in actual:
            continue

        if isinstance(value, dict):
            _compare_dict(actual[key], value, container, [])
        else:
            assert (
                actual[key] == value
            ), f'Values of {key} in {container} security context do not match: actual: {actual[key]}, expected: {value}'


class DeploymentTlsDhparamBase(Base):
    """
    Test harness base class to validate the `volumes` section of a kubernetes manifest
    focusing on templating TLS or TLS dhparam secrets mounted as volumes.
    """
    volume_name = ""
    chart_name = ""

    @staticmethod
    def _create_tls_mount_items(
        tls_key="tls.key",
        tls_crt="tls.crt",
        ca_crt="ca.crt",
        dhparam_pem="dhparam.pem",
    ):
        return {
            "ca.crt": ca_crt,
            "tls.crt": tls_crt,
            "tls.key": tls_key,
            "dhparam.pem": dhparam_pem,
        }

    def _run_test(self, helm, chart_path, key, volume_item, mount_items, secret_name, values_yaml):
        values = add_jsonpath_prefix(key, load_yaml(values_yaml))
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)

        secret = deployment.findone(
            f"spec.template.spec.volumes[?@.name=='{self.volume_name}'].secret",
        )
        assert secret["secretName"].startswith(
            f"release-name-{secret_name}",
        ), f"Secret name: {secret['secretName']} does not start with release-name-{secret_name}"

        vol_item = deployment.findone(
            f"spec.template.spec.volumes[?@.name=='{self.volume_name}'].secret.items[?@.path=='{volume_item}']",
        )
        assert vol_item["key"] == mount_items[volume_item]

    def _test_volume_existing_secret_custom_name(
        self,
        helm,
        chart_path,
        key,
        volume_item,
    ):
        secret_name = "stub-secret-name"
        mount_items = self._create_tls_mount_items()
        values_yaml = """
        existingSecret:
          name: "stub-secret-name"
        """
        values = add_jsonpath_prefix(key, load_yaml(values_yaml))
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)

        secret = deployment.findone(
            f"spec.template.spec.volumes[?@.name=='{self.volume_name}'].secret",
        )
        assert secret["secretName"].startswith(
            secret_name,
        ), f"Secret name: {secret['secretName']} does not start with {secret_name}"

        vol_item = deployment.findone(
            f"spec.template.spec.volumes[?@.name=='{self.volume_name}'].secret.items[?@.path=='{volume_item}']",
        )
        assert vol_item["key"] == mount_items[volume_item]


class DeploymentTlsVolumeSecret(DeploymentTlsDhparamBase):
    """
    Test harness class to validate the `volumes` section of a kubernetes manifest
    focusing on templating TLS secrets mounted as volumes.
    The volumes section must be embedded in a Deployment, StatefulSet or Job manifest.
    Supporting:
    - TLS secrets via configured existingSecrets
    """
    test_volume_tls_existing_secret_custom_name = DeploymentTlsDhparamBase._test_volume_existing_secret_custom_name

    def test_volume_tls_existing_secret_custom_ca_cert(
        self,
        helm,
        chart_path,
        key,
        volume_item,
    ):
        secret_name = self.chart_name
        mount_items = self._create_tls_mount_items(ca_crt="stub-custom-ca.crt")
        values_yaml = f"""
        existingSecret:
          keyMapping:
            ca.crt: {mount_items["ca.crt"]}
        """
        self._run_test(helm, chart_path, key, volume_item, mount_items, secret_name, values_yaml)

    def test_volume_tls_existing_secret_custom_tls_cert(
        self,
        helm,
        chart_path,
        key,
        volume_item,
    ):
        secret_name = self.chart_name
        mount_items = self._create_tls_mount_items(tls_crt="stub-custom-tls.crt")
        values_yaml = f"""
        existingSecret:
          keyMapping:
            tls.crt: {mount_items["tls.crt"]}
        """
        self._run_test(helm, chart_path, key, volume_item, mount_items, secret_name, values_yaml)

    def test_volume_tls_existing_secret_custom_tls_key(
        self,
        helm,
        chart_path,
        key,
        volume_item,
    ):
        secret_name = self.chart_name
        mount_items = self._create_tls_mount_items(tls_key="stub-custom-tls.key")
        values_yaml = f"""
        existingSecret:
          keyMapping:
            tls.key: {mount_items["tls.key"]}
        """
        self._run_test(helm, chart_path, key, volume_item, mount_items, secret_name, values_yaml)


class DeploymentTlsDhparamVolumeSecret(DeploymentTlsDhparamBase):
    """
    Test harness class to validate the `volumes` section of a kubernetes manifest
    focusing on templating TLS dhparam secrets mounted as volumes.
    The volumes section must be embedded in a Deployment, StatefulSet or Job manifest.
    Supporting:
    - TLS/Dhparam secrets via configured existingSecrets
    """
    test_volume_tls_dhparam_existing_secret_custom_name = DeploymentTlsDhparamBase._test_volume_existing_secret_custom_name

    def test_volume_tls_existing_secret_custom_dhparam_pem(
        self,
        helm,
        chart_path,
        key,
        volume_item,
    ):
        secret_name = self.chart_name
        mount_items = self._create_tls_mount_items(dhparam_pem="stub-custom-dhparam.pem")
        values_yaml = f"""
        existingSecret:
          keyMapping:
            dhparam.pem: {mount_items["dhparam.pem"]}
        """
        self._run_test(helm, chart_path, key, volume_item, mount_items, secret_name, values_yaml)
