# Usage of the Helm Test Harness

## Running tests locally and development

The intended way to work locally with the test harness is to use `uv`. Both
`pytest-helm` and `helm-test-harness` will be available as a development
installation, so that it is easy to co-develop your chart and the test harness.


### One off run of the tests

Using `uv run` it is possible to directly run `pytest`:

```shell
uv --project ../common-helm run pytest tests/chart
```


### Development shell

The following commands will run a shell which has all Python dependencies
available:

```shell
# Using bash
uv --project ../common-helm run bash

# Using zsh
uv --project ../common-helm run zsh
```

Inside of the shell you can run `pytest` directly as the following examples
based on the portal server show:

```shell
pytest portal-server/tests/chart -v
pytest portal-server/tests/chart -v --helm-debug
pytest portal-server/tests/chart -vsx --helm-debug
```

Hints:

- `../common-helm` has to be replaced with the correct path to your local
  clone of `common-helm`.


## Test a Helm chart

The container image `testrunner` provides all dependencies for using the test
harness, it also does include the `helm-test-harness` package itself. It should
be set up in the Gitlab CI configuration and in the Docker Compose setup.


### Gitlab CI integration

The following example illustrates the configuration for the portal server:

```yaml
test-chart-portal-server:
  stage: test
  needs: []
  image: "gitregistry.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/testrunner:VERSION"
  script:
    - helm dep build helm/portal-server
    - pytest -W error portal-server/tests/chart
```

Hints:

- `VERSION` has to be replaced with a specific version of the container image.

- `-W error` shall be used within the CI pipline to ensure that we catch up with
  _DeprecationWarnings_ when upgrading to a new version of the test harness.


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

Hints:

- `VERSION` has to be replaced with a specific version of the container image.

- The sources of the Helm chart and of the chart specific test suite should be
  bind-mounted into the container.


## Running tests via in the testrunner container

The following example is based on the portal server which has the configuration
for Docker Compose in the subdirectory `docker`.

```shell
# Only needed if your docker-compose.yaml is in the subdirectory "docker"
cd docker

# Run the test suite
docker compose run -it --rm test-chart-portal-server

# Deal with trouble via pdb
docker compose run -it --rm test-chart-portal-server pytest portal-server/tests/chart --pdb

# Have a shell
docker compose run -it --rm test-chart-portal-server bash
pytest portal-server/tests/chart
```


## Chart specific tests

The same environment shall be used to provide and run chart specific tests, see
`pytest-helm` regarding further details. Examples are also provided in the tests
within the `common-helm` repository.
