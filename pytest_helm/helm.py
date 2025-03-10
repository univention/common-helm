import tempfile
import subprocess
import yaml
import os


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
        if result.returncode != 0:
            raise RuntimeError(f"Error running command {' '.join(args)}")
        return result.stdout

    def helm_template(self, chart, values={}, template_file: str | None = None, helm_args: list[str] | None = None):
        """
        Generates helm templates from a chart
        `values` can be passed to override the default chart values
        """
        fd, path = tempfile.mkstemp()
        output = ""
        try:
            with os.fdopen(fd, "w") as tmp:
                tmp.write(yaml.dump(values))

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
            print(output.decode())

        result = list(yaml.safe_load_all(output))
        return result

    def helm_template_file(self, chart, values: dict, template_file: str, helm_args: list[str] | None = None) -> dict:
        assert template_file
        result = [ i for i in self.helm_template(chart, values, template_file, helm_args) if i is not None ]
        assert len(result) <= 1
        if len(result) == 0:
            return {}
        return result[0]

    def get_resources(
        self, manifests, *, api_version=None, kind=None, name=None, predicate=None
    ):
        """
        Get the manifests matching given criteria
        """
        docs = [doc for doc in manifests if doc]
        if predicate:
            docs = [doc for doc in docs if predicate(doc)]
        if api_version:
            docs = [doc for doc in docs if api_version == doc.get("apiVersion")]
        if kind:
            docs = [doc for doc in docs if kind == doc.get("kind")]
        if name:
            docs = [doc for doc in docs if name == doc.get("metadata", {}).get("name")]
        return docs

    def get_resource(self, *args, **kwargs):
        """
        Get one manifest.
        This will raise LookupError if none or more than one manifest is found
        """
        manifests = self.get_resources(*args, **kwargs)
        if len(manifests) != 1:
            raise LookupError(
                "{} manifest found".format(
                    "No" if len(manifests) == 0 else "More than one"
                )
            )
        return manifests[0]
