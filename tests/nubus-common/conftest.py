
# SPDX-FileCopyrightText: 2025 Univention GmbH
# SPDX-License-Identifier: AGPL-3.0-only

import os.path

import pytest


@pytest.fixture()
def chart_path(pytestconfig):
    """
    Path to the Helm chart which shall be tested.
    """
    chart_path = pytestconfig.option.chart_path
    if not chart_path:
        tests_path = os.path.dirname(os.path.abspath(__file__))
        chart_path = os.path.normpath(
            os.path.join(tests_path, "../../helm/test-nubus-common"),
        )
    return chart_path
