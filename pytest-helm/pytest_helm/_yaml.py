import jsonpath
from yaml import SafeDumper, SafeLoader


class HelmResource(dict):
    """
    Represents a single Kubernetes Resource rendered by Helm.
    """

    def findone(self, path):
        """
        Finds the first matching object by `path`.

        - `path`: A JSON Path expression.

        Raises an `AttributeError` in case `path` does not find any object.

        Returns the first found object itself.
        """
        return jsonpath.match(path, self).obj

    def findall(self, path):
        """
        Finds all objects by `path`.

        - `path`: A JSON Path expression.

        Returns the found objects as a `list`. The list will be empty in case
        nothing is found.
        """
        return jsonpath.findall(path, self)


def helm_resource_constructor(loader, node):
    value = loader.construct_mapping(node)
    return HelmResource(value)


def map_representer(dumper, data):
    return dumper.represent_mapping("tag:yaml.org,2002:map", data)


class CustomSafeLoader(SafeLoader):
    """
    A custom loader class.

    It has its own registry of constructors. This ensures that the parsing of
    YAML `maps` into `HelmResources` interferes with the regular `SafeLoader`.
    """


class CustomSafeDumper(SafeDumper):
    """
    A custom dumper class.

    It has its own registry of representers. This ensures that the
    representation of `HelmResource` as a YAML `map` does not interfere with
    the regular `SafeDumper`.
    """


CustomSafeLoader.add_constructor("tag:yaml.org,2002:map", helm_resource_constructor)
CustomSafeDumper.add_representer(HelmResource, map_representer)
