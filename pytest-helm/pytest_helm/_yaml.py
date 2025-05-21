"""
Internal module which hooks up PyYAML so that the models are used.

Use `CustomSafeLoader` and `CustomSafeDumper` to parse or render YAML with the
custom models.
"""

from yaml import SafeDumper, SafeLoader

from .models import KubernetesResource, YamlMapping


def map_constructor(loader, node):
    value = loader.construct_mapping(node)
    if _is_kubernetes_resource(value):
        return KubernetesResource(value)
    return YamlMapping(value)


def _is_kubernetes_resource(value):
    # NOTE: There is no good way to find out if a given node is a root node in
    # PyYAML. This is why we check if well-known attributes are in "value".
    return "apiVersion" in value and "kind" in value


def map_representer(dumper, data):
    return dumper.represent_mapping("tag:yaml.org,2002:map", data)


class CustomSafeLoader(SafeLoader):
    """
    A custom loader class.

    It has its own registry of constructors. This ensures that the parsing of
    YAML `maps` into `YamlMappings` interferes with the regular `SafeLoader`.
    """


class CustomSafeDumper(SafeDumper):
    """
    A custom dumper class.

    It has its own registry of representers. This ensures that the
    representation of `YamlMapping` as a YAML `map` does not interfere with
    the regular `SafeDumper`.
    """


CustomSafeLoader.add_constructor("tag:yaml.org,2002:map", map_constructor)
CustomSafeDumper.add_representer(YamlMapping, map_representer)
