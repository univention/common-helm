import os.path

import pytest


@pytest.fixture()
def chart_test_deployment():
    """Absolute path to the Helm chart `test-deployment`."""
    tests_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(tests_path, "../helm/test-deployment"))
