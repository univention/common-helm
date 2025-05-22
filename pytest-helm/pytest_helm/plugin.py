# -*- coding: utf-8 -*-
import pytest

from .helm import Helm, HelmChart


def pytest_addoption(parser):
    group = parser.getgroup("helm")
    group.addoption("--chart-path", help="Path of the Helm chart to test")
    group.addoption(
        "--helm-debug",
        action="store_true",
        dest="helm_debug",
        default=False,
        help="Enable verbose output of the Helm checking, e.g. dump the template result.",
    )
    group.addoption(
        "--helm-path",
        action="store",
        dest="helm_path",
        default="helm",
        help="Path to the helm binary.",
    )
    group.addoption(
        "--values",
        action="append",
        help="Value files to use. Can be used multiple times.",
    )

    parser.addini("HELM_PATH", "Path to the helm binary")


def pytest_report_header(config):
    return [
        f"helm binary: {config.getoption('helm_path')}",
        f"values: {config.getoption('values')}",
    ]


@pytest.fixture
def helm_values(request):
    """
    Return a list of values files to add to helm calls.

    Override this fixture in your tests if you want certain default values to
    be included always.
    """
    return request.config.option.values


@pytest.fixture
def helm(request, helm_values):
    """
    Return a :class:`Helm` instance to help with `helm` interaction.
    """
    helm_path = request.config.option.helm_path
    debug = request.config.option.helm_debug
    return Helm(helm_path, helm_values, debug)


@pytest.fixture
def chart_default_path():
    """
    Override this fixture to provide a default path to the Helm chart under test.
    """
    return None


@pytest.fixture
def chart_path(pytestconfig, chart_default_path):
    """
    Path to the Helm chart which shall be tested.

    Override the fixture `chart_default_path` to provide a default for your
    test suite or a subset of your test suite. This way it is still possible to
    use the CLI parameter `--chart-path`.
    """
    chart_path = pytestconfig.option.chart_path
    return chart_path or chart_default_path


@pytest.fixture
def chart(helm, chart_path):
    """
    Return a :class:`HelmChart` instance

    Requires a fixture `chart_path` to be defined and return the path to the
    Helm chart under test.

    This is a fixture which represents one Helm chart under test. It knows for
    example the path to the chart and allows to just call `helm_template`
    without having to pass in the path in every test case. The main purpose it
    to simplify cases where a test suite is checking the behavior of one chart.
    """
    if not chart_path:
        raise RuntimeError('The fixture "chart_path" has to provide a value to use this fixture.')
    return HelmChart(chart_path, helm)
