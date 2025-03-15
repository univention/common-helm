# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from pytest_helm.utils import add_jsonpath_prefix


def test_add_jsonpath_prefix():
    values = add_jsonpath_prefix("config.logLevel", None)
    assert values == {"config": {"logLevel": None}}
