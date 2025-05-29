import textwrap
from io import StringIO

from pytest_helm._yaml import CustomYAML
from pytest_helm.models import YamlMapping, KubernetesResource
from ruamel.yaml import YAML


stub_stdout = """
---
# This is the first resource
apiVersion: stub.test/v1  # The presence of "apiVersion" indicates a KubernetesResource
kind: Stub  # The presence of "kind" indicates a KubernetesResource
metadata:
  name: first

---
# This is the second resource
apiVersion: stub.test/v1
kind: Stub
metadata:
  name: second
"""


def test_loads_custom_classes():
    yaml = CustomYAML()
    data = list(yaml.load_all(stub_stdout))
    first_resource = data[0]

    assert isinstance(first_resource, KubernetesResource)
    assert isinstance(first_resource["metadata"], YamlMapping)


def test_non_custom_yaml_does_not_return_custom_classes():
    yaml = YAML()
    data = list(yaml.load_all(stub_stdout))
    first_resource = data[0]

    assert not isinstance(first_resource, KubernetesResource)
    assert not isinstance(first_resource["metadata"], YamlMapping)


def test_dumps_custom_classes():
    yaml = CustomYAML()
    data = KubernetesResource()
    data["metadata"] = YamlMapping({"name": "stub-name"})

    output = _yaml_dump_as_string(yaml, data)

    expected_output = textwrap.dedent("""
      metadata:
        name: stub-name
    """).lstrip()

    assert output == expected_output


def test_preserves_comments():
    yaml = CustomYAML()
    data = list(yaml.load_all(stub_stdout))
    first_resource = data[0]
    output = _yaml_dump_as_string(yaml, first_resource)

    assert "# This is the first resource" in output
    assert '  # The presence of "apiVersion" indicates a KubernetesResource' in output


def _yaml_dump_as_string(yaml, data):
    out = StringIO()
    yaml.dump(data, out)
    output = out.getvalue()
    return output
