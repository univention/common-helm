# -*- coding: utf-8 -*-
import io

import pytest

from ._yaml import CustomYAML
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
def helm_default_values():
    """
    Override this fixture to provide a list of default values.

    This fixture has to return a list of file paths.
    """
    return []


@pytest.fixture
def helm_values(request, helm_default_values):
    """
    Return a list of values files to add to helm calls.

    Override the fixture `helm_default_values` to provide a default for your
    test suite.
    """
    return request.config.option.values or helm_default_values


helm_fixture_key = pytest.StashKey[Helm]()


@pytest.fixture
def helm(request, helm_values):
    """
    Return a :class:`Helm` instance to help with `helm` interaction.
    """
    helm_path = request.config.option.helm_path
    debug = request.config.option.helm_debug
    fixture =  Helm(helm_path, helm_values, debug)
    request.node.stash[helm_fixture_key] = fixture
    return fixture


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


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield
    helm_fixture = item.stash.get(helm_fixture_key, None)
    if helm_fixture and call.when == "call":
        helm_template_results = helm_fixture._helm_template_results
        content = []
        for helm_template_result in helm_template_results:
            for resource in helm_template_result._accessed_resources:
                content.append(_resource_header(resource))
                content.append("\n---")

                out_stream = io.StringIO()
                with CustomYAML(output=out_stream) as myyaml:
                    myyaml.dump(resource)
                content.append(out_stream.getvalue())
        if content:
            report.sections.append(("Accessed Resources", "\n".join(content)))

        output = []
        helm_template_call_results = helm_fixture._helm_template_call_results
        for call_result in helm_template_call_results:
            if call_result.returncode != 0:
                output.append("Call:\n")
                output.append(" ".join(str(i) for i in call_result.args))
                if call_result.stdout:
                    output.append("\nStdout:\n")
                    output.append(call_result.stdout)
                if call_result.stderr:
                    output.append("\nStderr:\n")
                    output.append(call_result.stderr)
        if output:
            report.sections.append(("Failed helm template calls", "\n".join(output)))
    return report


def _resource_header(resource):
    return (
        f'Kubernetes resource: '
        f'kind={resource.findone("kind", default="<kind missing>")}, '
        f'name={resource.findone("metadata.name", default="<metadata.name missing>")}'
    )
