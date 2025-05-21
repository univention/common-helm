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

    def run_command(self, *args) -> bytes:
        """
        Runs a command and returns stdout
        """
        result = subprocess.run(args, stdout=subprocess.PIPE)
        log.debug("Running helm: %s", args)
        if result.returncode != 0:
            raise RuntimeError(f"Error running command {' '.join(args)}")
        return result.stdout

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

            output = self.run_command(self.helm_cmd, "template", chart, *helm_args)
        finally:
            os.remove(path)

        if self.debug:
            print("Helm output:\n")
            print(output.decode())

        result = HelmTemplateResult(yaml.load_all(output, Loader=CustomSafeLoader))
        return result

    @deprecated("Use the method 'HelmTemplateResult.get_resources' instead.")
    def get_resources(self, manifests, *, api_version=None, kind=None, name=None, predicate=None):
        """
        Get the manifests matching given criteria
        """
        return HelmTemplateResult.get_resources(
            manifests,
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
        manifests = HelmTemplateResult.get_resources(*args, **kwargs)
        if len(manifests) != 1:
            raise LookupError(
                "{} manifest found".format("No" if len(manifests) == 0 else "More than one"),
            )
        return manifests[0]
