import jsonpath

UNSET = object()


class YamlMapping(dict):
    """
    Represents a YAML map and provides the utility API for testing.
    """

    def findone(self, path, default=UNSET):
        """
        Finds the first matching object by `path`.

        - `path`: A JSON Path expression.
        - `default`: Optional. Will be returned if provided and the key is missing.

        Raises an `AttributeError` in case `path` does not find any object.

        Returns the first found object itself.
        """
        found = jsonpath.match(path, self)
        if not found:
            if default is not UNSET:
                return default
            raise KeyError(path)
        return found.obj

    def findall(self, path):
        """
        Finds all objects by `path`.

        - `path`: A JSON Path expression.

        Returns the found objects as a `list`. The list will be empty in case
        nothing is found.
        """
        return jsonpath.findall(path, self)


class KubernetesResource(YamlMapping):
    """
    Represents a single Kubernetes Resource rendered by Helm.

    This class allows to provide additional API methods only on the root map
    which represents a Kubernetes resource.
    """


class HelmTemplateResult(list):
    """
    The list of resources rendered by Helm via `Helm.helm_template`.
    """

    stdout: str = ""
    """
    Output of the call to "helm template".
    """

    stderr: str = ""
    """
    Error output of the call to "helm template".
    """

    def get_resources(self, *, api_version=None, kind=None, name=None, predicate=None):
        """
        Get the resources matching given criteria
        """
        resources = self
        docs = [doc for doc in resources if doc]
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

        This will raise `LookupError` if none or more than one resource is
        found.
        """
        resources = self.get_resources(*args, **kwargs)
        if len(resources) != 1:
            raise LookupError(
                "{} manifest found".format("No" if len(resources) == 0 else "More than one"),
            )
        return resources[0]
