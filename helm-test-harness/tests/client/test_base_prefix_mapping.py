# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.client import base

def test_apply_mapping_removes_the_source_value():
    prefix_mapping = {
        "a.b": "x",
    }
    values = {
        "x": {
            "sub": "structure",
        },
    }

    base.apply_mapping(values, prefix_mapping)

    assert values == {
        "a": {
            "b": {
                "sub": "structure",
            },
        },
    }
