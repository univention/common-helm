"""
Internal module which hooks up PyYAML and ruamel.yaml so that the models are used.

The extension mechanism is in both implementations based on a class based
attribute, so that this module does create subclasses to avoid interference
with usage of the YAML libraries in other places.

Use `CustomSafeLoader` and `CustomSafeDumper` to parse or render YAML with the
custom models.
"""

import ruamel.yaml
from yaml import SafeDumper, SafeLoader

from .models import KubernetesResource, YamlMapping

GENERIC_MAPPING_TAG = "tag:yaml.org,2002:map"


def pyyaml_map_constructor(loader, node):
    value = loader.construct_mapping(node)
    if _is_kubernetes_resource(node):
        return KubernetesResource(value)
    return YamlMapping(value)


def map_constructor(constructor, node):
    cls = YamlMapping
    if _is_kubernetes_resource(node):
        cls = KubernetesResource

    # See: `RoundTripConstructor.construct_yaml_map`
    data = cls()
    data._yaml_set_line_col(node.start_mark.line, node.start_mark.column)
    yield data
    constructor.construct_mapping(node, data, deep=True)
    constructor.set_collection_style(data, node)


def _is_kubernetes_resource(node):
    # NOTE: There is no good way to find out if a given node is a root node in
    # PyYAML. This is why we check if well-known attributes are in "value".
    keys = {key_node.value for key_node, value_node in node.value}
    return keys.issuperset({"apiVersion", "kind"})



def map_representer(dumper, data):
    return dumper.represent_mapping(GENERIC_MAPPING_TAG, data)


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


CustomSafeLoader.add_constructor(GENERIC_MAPPING_TAG, pyyaml_map_constructor)
CustomSafeDumper.add_representer(YamlMapping, map_representer)
CustomSafeDumper.add_representer(KubernetesResource, map_representer)


# Ruamel integration


class CustomYAML(ruamel.yaml.YAML):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.Constructor = CustomRoundTripConstructor
        self.Representer = CustomRoundTripRepresenter


class CustomRoundTripConstructor(ruamel.yaml.RoundTripConstructor):
    """
    A custom subclass to keep the class attributes separate.
    """


class CustomRoundTripRepresenter(ruamel.yaml.RoundTripRepresenter):
    """
    A custom subclass to keep the class attributes separate.
    """


CustomRoundTripConstructor.add_constructor(GENERIC_MAPPING_TAG, map_constructor)
CustomRoundTripRepresenter.add_representer(YamlMapping, map_representer)
CustomRoundTripRepresenter.add_representer(KubernetesResource, map_representer)
