# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

def pytest_addoption(parser):
    parser.addoption("--chart-path", help="Path of the Helm chart to test")
