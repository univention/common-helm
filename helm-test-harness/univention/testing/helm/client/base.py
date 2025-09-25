# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from collections.abc import Sequence

from pytest_helm.utils import load_yaml

from univention.testing.helm.utils import apply_mapping, PrefixMapping


class DefaultAttributes:
    """
    Default attributes and attribute names used in test classes.

    This class serves mainly documentation purposes.
    """

    kinds: Sequence = tuple()
    """
    List of Kubernetes object types to check.

    Some tests check multiple types like the image configuration related tests.
    The list of types to look up is configured via this attribute.

    See also:

    - The attribute `kind` within Kubernetes objects.
    """

    workload_kind: str = "Deployment"
    """
    Workloads can be deployed via multiple types in Kubernetes.

    This attribute allows to specify which workload kind shall be looked up.
    This way a test template can be used to check a `Deployment`, a
    `StatefulSet` and also a `Job` or `CronJob`.

    See also:

    - The attribute `kind` within Kubernetes objects.
    """

    workload_name: str | None = None
    """
    The name to use when looking up the workload object.

    Specification of a name in the lookup is needed for cases when a Helm chart
    deploys multiple workloads of the same kind. In other cases it can be kept
    as `None` so that no filtering by name is applied.

    See also:

    - The attribute `metadata.name` within Kubernetes objects.
    - The method `HelmTemplateResult.get_resources` in `pytest-helm`.
    """

    path_container = "..spec.template.spec.containers[?@.name=='main']"
    """
    Path to find the container under test.

    Typically we focus on the main container, ideally this container is called
    "main".
    """

    """
    Name of the volume in `volumes` and `volumeMounts`.

    Used to template `path_volume` and `sub_path_volume_mount`.

    Examples::
        volume_name = "test-volume-name"
    """

    volume_name: str

    path_volume: str
    """
    Overrides automatic path volume templating with volume_name.
    For backwards-compatibility and edge-cases

    Path to the related volume when testing something in the context of a workload.

    When testing in the context of a Secret, then this path should point to the
    volume mount in the workload under test.

    Examples::

        # Secret focused test
        path_volume = "..spec.template.spec.volumes[?@.name=='secret-ldap']"

    See also:

    - The attribute `sub_path_volume_mount` is related.
    """

    sub_path_volume_mount: str
    """
    Overrides automatic sub path volume mount templating with volume_name.
    For backwards-compatibility and edge-cases

    Sub path to find a volume mount inside of a container.

    Examples::

        # Secret focused test
        sub_path_volume_mount = "volumeMounts[?@.name=='secret-ldap']"

    See also:

    - The attribute `path_volume` is related.
    """

    is_secret_owner = False
    """
    Flag to indicate if the Helm chart under test owns the secret.

    Different behavior is expected if the secret is owned by the chart. The
    main aspect is that a random or derived value is generated automatically if
    the chart is the owner of the secret.
    """


class BaseTest(DefaultAttributes):
    """
    Base class for client configuration focused tests.

    The class groups common base functionality to avoid repetition.

    Be aware, that this class is focused on client based testing. Currently we
    do have two different approaches in `helm-test-harness`. See also the lass
    `univention.testing.helm.base.Base` which is used for test templates which
    focus on a single Kubernetes resource.
    """

    prefix_mapping: PrefixMapping = {}
    """
    Allows to map the default prefix into a different place.

    This is intended for special cases when the default prefix cannot be used.
    One example would be a case where two UDM Rest API clients are configured
    in one chart::

        class TestSourceUdmClient(UdmClient):

            prefix_mapping = {
                "sourceUdm": "udm",
                "global.sourceUdm": "global.udm",
            }

    """

    def load_and_map(self, values_yaml: str):
        '''
        Parse `values_yaml` and apply the prefix mapping.

        This shall be used in sub-classes in the following way::

            def test_example(self):
                values = self.load_and_map("""
                        exampleKey: "value"
                    """)
                # ...
        '''
        values = load_yaml(values_yaml)
        apply_mapping(values, self.prefix_mapping)
        return values
