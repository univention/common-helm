from ._warnings import deprecated
from ._yaml import CustomYAML, YamlMapping


@deprecated("Use the attribute findone on the parsed YamlMapping instead.")
def findone(data, path):
    """
    Finds the first matching object by `path` in `data`.

    - `data`: The data to look into.
    - `path`: A JSON Path expression.

    Raises an `AttributeError` in case `path` does not find any object.

    Returns the first found object itself.
    """
    return YamlMapping.findone(data, path)


@deprecated("Use the attribute findall on the parsed YamlMapping instead.")
def findall(data, path):
    """
    Finds all objects by `path` in `data`.

    - `data`: The data to look into.
    - `path`: A JSON Path expression.

    Returns the found objects as a `list`. The list will be empty in case
    nothing is found.
    """
    return YamlMapping.findall(data, path)


def load_yaml(source: str):
    """
    Utility function to conveniently load YAML sources.
    """
    return CustomYAML().load(source)


def get_containers(resource: YamlMapping) -> list:
    """
    Return all containers of a Workload Resource.

    Includes both init containers and regular containers.
    """
    init_containers = resource.findone("..spec.template.spec.initContainers", default=[])
    containers = resource.findone("..spec.template.spec.containers")
    return init_containers + containers


def add_jsonpath_prefix(prefix_jsonpath: str, localpart) -> dict:
    keys = prefix_jsonpath.split('.')
    result = {}
    current = result
    for key in keys[:-1]:
        current[key] = {}
        current = current[key]
    # Set the final key to the provided value
    current[keys[-1]] = localpart
    return result
