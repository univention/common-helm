import jsonpath


def findone(data, path):
    return jsonpath.match(path, data).obj


def findall(data, path):
    return jsonpath.findall(path, data)


def get_containers(manifest):
    try:
        init_containers = findall(manifest, "spec.template.spec.initContainers")
    except AttributeError:
        init_containers = []
    containers = findall(manifest, "spec.template.spec.containers")
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
