# Quickstart

This is a guide for setting up the test harness for a Helm chart.


## Assumptions

- You have an existing repository.
- It has a Helm chart, we assume `helm/example-chart` as the location.
- You want to add unit tests or use the `helm-test-harness` for your chart.


## Integrate and configure the test suite

The easiest path is to use the
[Copier](https://copier.readthedocs.io/en/stable/) template from the repository
[`helm-chart-unittests`](https://git.knut.univention.de/univention/dev/tooling/copier-templates/helm-chart-unittests).

If your repository has multiple charts:

```shell
# TODO: Adjust the value of "chart_name".
chart_name=example-chart

copier copy -a .config/copier-answers.helm-chart-unittests-${chart_name}.yaml \
  https://git.knut.univention.de/univention/dev/tooling/copier-templates/helm-chart-unittests.git .
```

In case you are certain to have only one chart in your repository:

```shell
copier copy https://git.knut.univention.de/univention/dev/tooling/copier-templates/helm-chart-unittests.git .
```

Also add the answer file in the folder `.config` to your repository, it helps
with future updates when the template did evolve.

Verify the fresh setup by running `pytest`:

```shell
# TODO: Adjust paths as needed.
uv --project ../common-helm run pytest tests/chart
```

It should not fail, and it will not discover any tests yet.


## Add a test

Testing a chart is easiest done by using the fixture `chart`, just create a file
`test_example.py` inside of the folder with your chart tests:

```python
def test_example(chart):
    result = chart.helm_template()
    deployment = result.get_resource(kind="Deployment")
    name = deployment.findone("metadata.name")
    assert name == "example-deployment"
```

Details can be found in the usage documentation of `pytest-helm`.

The test will have to be adjusted depending on the names and kinds of the
Kubernetes objects which your chart deploys.


## Use the test harness

The test harness does provide template classes for re-use with multiple charts.
Verifying the correct handling of annotations can be done by creating a file
`common_behavior/test_annotations.py` in the folder with your chart tests:

```python
from univention.testing.helm.best_practice.annotations import Annotations


class TestAnnotations(Annotations):
    pass
```

This test template typically works out of the box. Many other templates will
require configuration by setting attribute on your subclass or by inheriting
from additional mixin classes.


## Running the tests locally

The intended way is to use the provided environment via `uv`. The following two
examples show how to run a shell with all needed Python dependencies:

```shell
uv --project ../common-helm run bash
uv --project ../common-helm run zsh
```

Inside you can just run regular `pytest` commands:

```shell
pytest tests/chart
pytest tests/chart -xvl -k annotation
```

Hint: The environment has both `pytest-helm` and `helm-test-harness` installed
for development so that it is possible to co-develop the test harness and your
chart at the same time.


## Further steps

See the [usage documentation](./usage.md) regarding the CI setup and further
explanations and details.
