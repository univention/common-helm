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
    ):
        """
        Generates helm templates from a chart.

        `values` can be passed to override the default chart values.
        """
        values = values or {}
        fd, path = tempfile.mkstemp()
        output = ""
        try:
            values_yaml = yaml.dump(values, Dumper=CustomSafeDumper)
            with os.fdopen(fd, "w") as tmp:
                tmp.write(values_yaml)

            if self.debug:
                print("Dumped Helm values:\n")
                print(values_yaml)

            helm_args = helm_args or []
            for item in self.values:
                helm_args.extend(("--values", item))
            helm_args.extend(("--values", path))

            if template_file:
                helm_args.extend(("--show-only", template_file))

            run_result = _run_command(self.helm_cmd, "template", chart, *helm_args)
            output = run_result.stdout
        finally:
            os.remove(path)

        if self.debug:
            print("Helm output:\n")
            print(output)

        result = HelmTemplateResult(yaml.load_all(output, Loader=CustomSafeLoader))
        result.stdout = output
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


def _run_command(*args) -> subprocess.CompletedProcess:
    """
    Utility to run a command and capture its output.

    Runs a command via `subprocess.run` and returns the `CompletedProcess`
    instance.

    Will raise `subprocess.CalledProcessError` in case of a non-zero exit
    status.
    """
    log.debug("Running helm: %s", args)
    result = subprocess.run(args, capture_output=True, check=True, text=True)
    return result
