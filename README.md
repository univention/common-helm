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

## Related external sources

### Former common chart from incubator project

A very good source of inspiration is the incubator/common chart, even though
it's archived and not maintained anymore.

It does show how a library of useful utility functions (comparable to Bitnami's
common chart) and also a library and utility for common templates can be
established.

Especially the second aspect goes beyond what we see in the Bitnami chart.

<https://github.com/helm/charts/tree/master/incubator/common>


### Hahow's fork of incubator/common

It's basically a maintained version.

<https://github.com/hahow/common-chart>


### technosophos' fork of incubator/common

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
