# Using `pytest-helm`


## Repository integration

The container image `testrunner` provides all dependencies for using
`pytest-helm` it also includes the `helm-test-harness` package. It should be set
up in the Gitlab CI configuration and in the Docker Compose setup.


### Gitlab CI

The following example illustrates the configuration for the portal server:

```yaml
test-chart-portal-server:
  stage: test
  needs: []
  image: "gitregistry.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/testrunner:VERSION"
  script:
    - helm dep build helm/portal-server
    - pytest portal-server/tests/chart
```

Hints:

- `VERSION` has to be replaced with a specific version of the container image.


### Docker Compose

```yaml
  test-chart-portal-server:
    image:   gitregistry.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/testrunner:VERSION
    command: pytest portal-server/tests/chart
    profiles:
      - test
    volumes:
      - "../helm/portal-server/:/app/helm/portal-server"
      - "../portal-server/tests/chart:/app/portal-server/tests/chart"
```


## Test suite configuration

`pytest-helm` does need to know where the Helm chart is located. Optionally it
also allows to provide a set of default values which shall always be used. The
values should be provided by defining pytest fixtures.


### Path to the Helm chart

```python
from pathlib import Path

import pytest


base_dir = (Path(__file__).parent / "../../../").resolve()


@pytest.fixture()
def helm_default_values():
    """By default use "helm/portal-server/linter_values.yaml"."""
    default_values = [
        base_dir / "helm/portal-server/linter_values.yaml",
    ]
    return default_values


@pytest.fixture()
def chart_default_path():
    chart_path = base_dir / "helm/portal-server"
    return chart_path
```

Hints:

- `base_dir` should point to the base of your repository, so that the
  computation of other paths is easy to understand.

- `chart_default_path` is a required fixture which has to return the absolute
  path to the Helm chart under test.

- `helm_default_values` is optional, it is commonly used to inject the values
  from the file `linter_values.yaml` into the test setup.


## Example test

The following test is using the fixture `chart`:

- `chart.helm_template()` will render the chart's templates via a call to `helm
  template`.

- The `result` is an instance of the class `HelmTemplateResult`. Typically the
  method `get_resource` is used to inspect a resource, or `get_resources` to
  inspect multiple resources.

- The result from parsing the YAML data is wrapped into a class `YamlMapping`
  which provides extra methods to help locate nested elements. It is based on a
  regular `dict` so that dictionary access works as well.

```python
def test_example(chart):
    result = chart.helm_template()
    deployment = result.get_resource(kind="Deployment")
    name = deployment.findone("metadata.name")
    assert name == "example-deployment"
```


## Test templates

The package `helm-test-harness` does provide template classes as a testing
library. This library should be used to verify that a Helm chart is living up to
common expectations about its behavior.
