# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.utils import apply_mapping


def test_apply_mapping_removes_the_source_value():
    prefix_mapping = {
        "a.b": "x",
    }
    values = {
        "x": {
            "sub": "structure",
        },
    }

    apply_mapping(values, prefix_mapping)

    assert values == {
        "a": {
            "b": {
                "sub": "structure",
            },
        },
    }


def test_apply_mapping_copies_the_value():
    prefix_mapping = {
        "a.b": "x",
    }
    values = {
        "x": {
            "sub": "structure",
        },
    }

    apply_mapping(values, prefix_mapping, copy=True)

    assert values == {
        "a": {
            "b": {
                "sub": "structure",
            },
        },
        "x": {
            "sub": "structure",
        },
    }
