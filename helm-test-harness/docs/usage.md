# Usage of the Helm Test Harness


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

Hints:

- `VERSION` has to be replaced with a specific version of the container image.

- The sources of the Helm chart and of the chart specific test suite should be
  bind-mounted into the container.


## Running tests via Docker manually

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


## Running tests in a local environment

The dependencies are managed via `uv`. Starting a shell which has the needed
Python dependencies available is possible in the following ways:

```shell
# Using bash
uv --project ~/work/common-helm run bash

# Using zsh
uv --project ~/work/common-helm run zsh
```

Inside of the shell you can run `pytest` directly as the following examples
based on the portal server show:

```shell
pytest portal-server/tests/chart -v
pytest portal-server/tests/chart -v --helm-debug
pytest portal-server/tests/chart -vsx --helm-debug
```

Hints:

- `~/work/common-helm` has to be replaced with the correct path to your local
  clone of `common-helm`.


## Chart specific tests

The same environment shall be used to provide and run chart specific tests, see
`pytest-helm` regarding further details. Examples are also provided in the tests
within the `common-helm` repository.
