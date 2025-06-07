# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from pytest_helm.utils import load_yaml

from univention.testing.helm.utils import apply_mapping, PrefixMapping


class DefaultAttributes:
    """
    Default attributes and attribute names used in test classes.

    This class serves mainly documentation purposes.
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
