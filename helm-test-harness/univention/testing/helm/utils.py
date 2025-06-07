# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from collections.abc import Mapping


# TODO: Change once the Python version has been upgraded in the test runner to >= 3.12
JSONPath = str
PrefixMapping = Mapping[JSONPath, JSONPath]
# type JSONPath = str
# type PrefixMapping = Mapping[JSONPath, JSONPath]


def apply_mapping(values: Mapping, prefix_mapping: PrefixMapping, *, copy=False) -> None:
    """
    Map one path in `values` to another path in `values`.

    Intended to help with test templates which have to adjust the values from a
    canonical structure towards a chart specific path.

    An example for `prefix_mapping`::

        prefix_mapping = {
            "sourceUdm": "udm",
            "global.sourceUdm": "global.udm",
        }

    By default the source values will be removed. Set `copy` to `True` in order
    to keep the source value.
    """
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
    if op == "pop":
        return values.pop(source_path[0])
    elif op == "get":
        return values[source_path[0]]
    else:
        raise RuntimeError(f"Invalid op value: {op}.")


def _set_value(values: Mapping, target_path: list[str], value: any) -> None:
    if len(target_path) >= 2:
        sub_values = values.setdefault(target_path[0], {})
        sub_path = target_path[1:]
        _set_value(sub_values, sub_path, value)
    else:
        values[target_path[0]] = value
