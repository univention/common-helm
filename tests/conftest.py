import os.path

import pytest


def pytest_addoption(parser):
    parser.addoption("--chart-path", help="Path of the Helm chart to test")


@pytest.fixture()
def chart_path(pytestconfig):
    """
    Path to the Helm chart which shall be tested.
    """
    chart_path = pytestconfig.option.chart_path
    if not chart_path:
        tests_path = os.path.dirname(os.path.abspath(__file__))
        chart_path = os.path.normpath(
            os.path.join(tests_path, "../helm/test-deployment")
        )
    return chart_path
