# nubus-common

Common utilities and fragments for Helm charts in Nubus

- **Version**: 0.1.0
- **Type**: library
- **Homepage:** <https://git.knut.univention.de/univention/customers/dataport/upx/common-helm>

## Introduction

This chart bundles commonly used functionality to be used in our Helm charts for Nubus.

## OpenShift compatibility

The same Nubus charts and images run on vanilla Kubernetes and on OpenShift with the default
SecurityContextConstraint `restricted-v2`. Charts render security contexts and Ingress path types through these
helpers:

- `nubus-common.compatibility.renderSecurityContext` removes `runAsUser`, `runAsGroup`, `fsGroup` and an empty
  `seLinuxOptions` on OpenShift. OpenShift assigns user, fsGroup and SELinux level from the namespace's ranges and
  rejects other values. Containers then run with an arbitrary UID and GID 0.
- `nubus-common.compatibility.ingressPathType` renders `Exact` as `Prefix` on OpenShift, because the ingress-to-route
  controller creates no Route for `Exact` paths.

Both are controlled by values below `global.compatibility.openshift`:

| Value | Default | Meaning |
|---|---|---|
| `adaptSecurityContext` | `auto` | `auto`: adapt if the cluster serves the API `security.openshift.io/v1`; `force`: always adapt, for `helm template` without cluster access (GitOps); `disabled`: never adapt, e.g. with the SCC `anyuid` |
| `adaptIngress` | `auto` | the same for Ingress path types |

`adaptSecurityContext` is the value Bitnami charts use, so one setting covers Nubus and Bitnami-based subcharts. On
vanilla Kubernetes the rendered manifests are unchanged.

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://charts.bitnami.com/bitnami | common | ^2.x.x |

