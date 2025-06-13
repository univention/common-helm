# SPDX-FileCopyrightText: 2025 Univention GmbH
# SPDX-License-Identifier: AGPL-3.0-only

from pathlib import Path

import pytest


base_dir = (Path(__file__).parent / "../..").resolve()


@pytest.fixture
def helm_default_values():
    return []

@pytest.fixture
def chart_default_path():
    chart_path = base_dir / "helm/test-client-config"
    return chart_path
