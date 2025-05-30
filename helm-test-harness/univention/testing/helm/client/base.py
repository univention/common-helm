# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from collections.abc import Mapping
from pytest_helm.utils import load_yaml


# TODO: Change once the Python version has been upgraded in the test runner to >= 3.12
JSONPath = str
PrefixMapping = Mapping[JSONPath, JSONPath]
# type JSONPath = str
# type PrefixMapping = Mapping[JSONPath, JSONPath]


class BaseTest:
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


def apply_mapping(values: Mapping, prefix_mapping: PrefixMapping, *, copy=False) -> None:
    op = "get" if copy else "pop"
    for target, source in prefix_mapping.items():
        _map(values, target, source, op=op)


def _map(values: Mapping, target: JSONPath, source: JSONPath, *, op="pop") -> None:
    target_path = target.split(".")
    source_path = source.split(".")
    try:
        value = _get_or_pop_value(values, source_path, op=op)
    except KeyError:
        # Source does not exist, there is nothing to map.
        pass
    else:
        _set_value(values, target_path, value)


def _get_or_pop_value(values: Mapping, source_path: list[str], *, op) -> any:
    if len(source_path) >= 2:
        sub_values = values[source_path[0]]
        sub_path = source_path[1:]
        return _get_or_pop_value(sub_values, sub_path, op=op)
    return getattr(values, op)(source_path[0])


def _set_value(values: Mapping, target_path: list[str], value: any) -> None:
    if len(target_path) >= 2:
        sub_values = values.setdefault(target_path[0], {})
        sub_path = target_path[1:]
        _set_value(sub_values, sub_path, value)
    else:
        values[target_path[0]] = value
