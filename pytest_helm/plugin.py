# -*- coding: utf-8 -*-
import pytest
from .helm import Helm


def pytest_addoption(parser):
    group = parser.getgroup('helm')
    group.addoption(
        '--helm-path',
        action='store',
        dest='helm_path',
        default='helm',
        help='Path to the helm binary.',
    )
    group.addoption(
        "--values",
        action="append",
        help="Value files to use. Can be used multiple times.",
    )

    parser.addini('HELM_PATH', 'Path to the helm binary')


def pytest_report_header(config):
    return [
        f"helm binary: {config.getoption('helm_path')}",
        f"values: {config.getoption('values')}",
    ]


@pytest.fixture
def helm_values(request):
    """
    Return a list of values files to add to helm calls.
    """
    return request.config.option.values


@pytest.fixture
def helm(request, helm_values):
    """
    Return a :class:`Helm` instance to help with `helm` interaction.
    """
    helm_path = request.config.option.helm_path
    return Helm(helm_path, helm_values)
