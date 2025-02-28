# `pytest-helm` with adjustments

This repository contains a pytest plugin to help with testing Helm charts.

See [`README.upstream.rst`](./README.upstream.rst) for the original README of
the project.


## Usage

Pin the installation to a specific commit of this repository since there is no
versioning in place yet.

E.g. in your `Pipfile`:

```
pytest-helm = {ref = "main", git = "https://git.knut.univention.de/univention/customers/dataport/upx/tooling/pytest_helm.git"}
```

The generated `lock` file should then contain something like the following, e.g.
from `Pipfile.lock`:

```json
        "pytest-helm": {
            "git": "https://git.knut.univention.de/univention/customers/dataport/upx/tooling/pytest_helm.git",
            "ref": "e775b9afcfa545320ac1bcc840928ca51d0c2828"
        },
```


## Changes and testing

There is no automatic CI setup in place, please make sure that the tests are
passing before pushing up a change.

If you depend on certain behavior, make sure to add a test so that it will stay
intact over time.

The `pipenv` based environment allows to run the test suite:

```
pipenv run pytest
```
