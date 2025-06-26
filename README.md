# Common Helm Support

This repository contains common Helm chart utilities which we saw being repeated
across our various Helm charts.

Helm charts:

- `nubus-common` is a library chart which provides shared utilities which are
  used across most charts for Nubus.

- `common` (deprecated) was the first attempt to create a common utility Helm
  chart. Use `nubus-common` instead.

- `test-*` - Charts starting with the prefix `test-` are used to test the
  library charts. They are not intended to be published or used outside of this
  repository.

Container images:

- `testrunner` provides an environment which has `pytest`, `pytest-helm` and the
  `helm-test-harness` installed. This image is intended to be used in CI
  pipelines to run the Helm chart unittests.

Python packages:

- `helm-test-harness` is a library of template classes. These classes can be
  used in test suites to define common expected behavior of a Helm chart.

  Usage documentation: [`./helm-test-harness/docs/usage.md`](./helm-test-harness/docs/usage.md)

- `pytest-helm` is a fork of the `pytest-helm` project from Github which seems
  to be unmaintained. We use this as a basis for our approach to test our Helm
  charts.

  Usage documentation: [`./pytest-helm/docs/usage.md`](./pytest-helm/docs/usage.md)

Test suites:

- `tests/common` are tests related to the Helm chart `common`.

- `tests/nubus-common` are tests related to the Helm chart `nubus-common`.

## History

The first iteration used a chart called `common` which did provide templates to
render manifest. Using the same prefix as the `common` chart out of the bitnami
repository. This approach did lead into a difficult to understand setup.

## Status - BETA

We did gain some confidence about the usage of `nubus-common` and use it across
our charts within the team.


## Contact

- Team Nubus Dev


## Structure

To be defined.


## Design notes


### Named template parameters

Named templates need various parameters to be available. Some parameters have
sane defaults and can be made optional.

The passing of parameters is modeled after the approach of "Named Parameters".
In Helm charts this translates into passing a `dict` as the context to the names
template, so that the keys in this `dict` are the named parameters. The
background is that named templates only allow a single parameter to be passed as
context.

Examples:

```yaml
# 1 - Applying local overrides
{{ include "common.ingress" (dict "top" . "ingress" .Values.ingress "overrides" "portal-server.ingress") }}
# 2 - Not applying any overrides
{{ include "common.ingress" (dict "top" . "ingress" .Values.ingress) }}

# 3 - Relying on the default of the parameter "ingress"
{{ include "common.ingress" (dict "top" .) }}


# The local overrides are defined also as a named template
{{- define "portal-server.ingress" -}}
data:
  myvalue: "local overrides applied"
{{- end -}}
```


#### Alternatives considered but not used

Other Helm charts which provide common functionality use the concept of
positional parameters and pass a `list` object as the context. This does result
into many calls to `index` with the respective number to fetch a parameter.

Compared to using named parameters the `include` call is less verbose. The
drawback is that the implementation is not as easy to understand anymore,
especially tracing a value through multiple named templates can be very
difficult.

Examples:

- <https://github.com/helm/charts/blob/master/incubator/common/templates/_util.tpl>



### Template customization options

Named templates which render a Manifest should support easy customization of the
result. Two aspects are important in this regard:

1. Tweaking some of the values by overriding them.
2. Passing in specific context values.


#### Overriding values

The named template should make use of a parameter called `overrides` which can
be optionally set to the name of a named template which shall be merged into the
result.

Note: The utility `common.utils.merge` already treats the parameter `overrides`
as optional.


#### Specific context values

The template for an Ingress is commonly using the values from the key
`.Values.ingress` to render itself. Still, a named template like
`common.ingress` should allow to explicitly pass in a different context. This
does allow to create multiple Ingress Manifests within one chart for special
cases, yet it sill allows to rely on the default for all simple charts.



## Common behavior


### `Deployment` resources


#### `global.configMapUcr`

The parameter `global.configMapUcr` can be used to refer to a `ConfigMap` which
contains the parameters for the Univention Configuration Registry (UCR).

If provided, then the key `base.conf` from this `ConfigMap` will be mounted into
the file `/etc/univention/base.conf`.

This is intended to make it easier to apply a stack wide UCR configuration.


#### `extraVolumes` and `extraVolumeMounts`

The resources of type `Deployment` do support the injection of extra volumes in
the following way:

```yaml
extraVolumeMounts:
  - name: "custom-entrypoints"
    mountPath: "/test"
    readOnly: true

extraVolumes:
  - name: "custom-entrypoints"
    configMap:
      name: "ums-umc-customization"
```

This mechanism is intended as a feature of last resort to plug customization in
when no cleaner way exists.



## Related external sources

### Former common chart from incubator project

A very good source of inspiration is the incubator/common chart, even though
it's archived and not maintained anymore.

It does show how a library of useful utility functions (comparable to Bitnami's
common chart) and also a library and utility for common templates can be
established.

Especially the second aspect goes beyond what we see in the Bitnami chart.

<https://github.com/helm/charts/tree/master/incubator/common>


### *Hahow's* fork of incubator/common

It's basically a maintained version.

<https://github.com/hahow/common-chart>


### *technosophos'* fork of incubator/common

This does seem to be a more modified fork of the common basis. Did not do an
in-depth inspection yet.

<https://github.com/technosophos/common-chart>


### Artifacthub overview

Searching for "common" does list quite a few examples of published common
charts and might yield more inspiration if needed.

<https://artifacthub.io/packages/search?ts_query_web=common&sort=relevance>


### Use a base chart via "Dependency-Alias" mechanism

If the charts of multiple services from the same team or group are identical,
then using a base chart as a dependency can be an option to further reduce
efforts.

An example of the approach is described within this post on Stackexchange:
<https://devops.stackexchange.com/questions/13379/use-one-helm-chart-for-all-microservices>

TODO: Update this section
# `pytest-helm` with adjustments

This repository contains a pytest plugin to help with testing Helm charts.

See [`README.upstream.rst`](./pytest-helm/README.upstream.rst) for the original README of
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

Tests are executed within the CI pipeline. Changes are only accepted if the
pipeline is passing.

If you depend on certain behavior, then make sure to cover this with respective
tests.
