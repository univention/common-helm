import logging
import os
import subprocess
import tempfile

import yaml

from ._warnings import deprecated
from ._yaml import CustomSafeDumper, CustomSafeLoader
from .models import HelmTemplateResult

log = logging.getLogger(__name__)


class Helm:

    def __init__(self, helm_cmd="helm", values=None, debug=False):
        self.helm_cmd = helm_cmd
        self.debug = debug
        self.values = values or tuple()

    def helm_template(
        self,
        chart,
        values=None,
        template_file: str | None = None,
        helm_args: list[str] | None = None,
        release_name: str = "",
    ):
        """
        Generates helm templates from a chart.

        `values` can be passed to override the default chart values.

        The returned value is an instance of `HelmTemplateResult`. It provides
        a useful API to inspect the generated YAML data and also to access the
        output of the call to Helm.
        """
        values = values or {}
        fd, path = tempfile.mkstemp()
        try:
            values_yaml = yaml.dump(values, Dumper=CustomSafeDumper)
            with os.fdopen(fd, "w") as tmp:
                tmp.write(values_yaml)

            if self.debug:
                print("Dumped Helm values:\n")
                print(values_yaml)

            args = [self.helm_cmd, "template"]

            if release_name:
                args.append(release_name)
            args.append(chart)

            for item in self.values:
                args.extend(("--values", item))
            args.extend(("--values", path))

            if template_file:
                args.extend(("--show-only", template_file))

            run_result = self._run_command(*args, *helm_args or [])
        finally:
            os.remove(path)

        result = HelmTemplateResult(
            doc for doc in yaml.load_all(run_result.stdout, Loader=CustomSafeLoader) if doc)
        result.stdout = run_result.stdout
        result.stderr = run_result.stderr
        return result

    @deprecated("Use the method 'HelmTemplateResult.get_resources' instead.")
    def get_resources(self, resources, *, api_version=None, kind=None, name=None, predicate=None):
        """
        Get the resources matching given criteria
        """
        return HelmTemplateResult.get_resources(
            resources,
            api_version=api_version,
            kind=kind,
            name=name,
            predicate=predicate,
        )

    @deprecated("Use the method 'HelmTemplateResult.get_resource' instead.")
    def get_resource(self, *args, **kwargs):
        """
        Get one manifest.
        This will raise LookupError if none or more than one manifest is found
        """
        resources = HelmTemplateResult.get_resources(*args, **kwargs)
        if len(resources) != 1:
            raise LookupError(
                "{} manifest found".format("No" if len(resources) == 0 else "More than one"),
            )
        return resources[0]


    def _run_command(self, *args) -> subprocess.CompletedProcess:
        """
        Utility to run a command and capture its output.

        Runs a command via `subprocess.run` and returns the `CompletedProcess`
        instance.

        Will raise `subprocess.CalledProcessError` in case of a non-zero exit
        status.
        """
        log.debug("Running helm: %s", args)
        result = subprocess.run(args, capture_output=True, text=True)

        if self.debug:
            print("Helm output:\n")
            print(result.stdout)
            print("Helm output stderr:\n")
            print(result.stderr)

        result.check_returncode()
        return result


class HelmChart:
    """
    Represents one Helm chart under test.

    Its main feature is to add knowledge about the chart's path around the
    fixture `Helm`.
    """

    def __init__(self, chart_path: str, helm: Helm):
        self.chart_path = chart_path
        self._helm = helm

    def helm_template(self, *args, **kwargs):
        """
        Templates the chart based on `Helm.helm_template`.

        See `Helm.helm_template` regarding the supported arguments.
        """
        return self._helm.helm_template(self.chart_path, *args, **kwargs)
