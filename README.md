# Common Helm Support - EXPERIMENTAL

This repository contains common Helm chart utilities which we saw being repeated
across our various Helm charts.

## Status

Please consider this repository experimental and don't depend on it.

We've seen in the team SouvAP Dev repeating fragments and patterns in our Helm
charts and explore if a collection of common baseline charts can help us to
reduce our efforts to maintain those.

Once we have a conclusion within our team we will decide if we keep this
repository and remove the experimental status or if we opt for a different
approach.


## Contact

- Team SouvAP Dev

  - <johannes.bornhold.extern@univention.de>


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
