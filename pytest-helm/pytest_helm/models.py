import jsonpath


class YamlMapping(dict):
    """
    Represents a YAML map and provides the utility API for testing.
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


class KubernetesResource(YamlMapping):
    """
    Represents a single Kubernetes Resource rendered by Helm.

    This class allows to provide additional API methods only on the root map
    which represents a Kubernetes resource.
    """
