{{/*
SPDX-License-Identifier: AGPL-3.0-only
SPDX-FileCopyrightText: 2026 Univention GmbH
*/}}

{{/*

Render a pod or container "securityContext", adapted to the target platform.

The key "enabled" is always removed. On OpenShift, the keys "runAsUser",
"runAsGroup" and "fsGroup" are removed as well. The default
SecurityContextConstraint "restricted-v2" assigns the user and fsGroup from
the namespace's range and rejects pods which request IDs outside of it. The
container then runs with an arbitrary UID and GID 0. An empty "seLinuxOptions"
is removed too: the SCC only fills in the namespace's SELinux level when the
key is absent, and rejects the empty level otherwise.

Adaptation is controlled by "global.compatibility.openshift.adaptSecurityContext".
This is the same value the Bitnami common chart uses, so one setting covers
Nubus charts and Bitnami-based subcharts:

- "auto" (default): adapt if the cluster serves the API "security.openshift.io/v1"
- "force": always adapt, e.g. for "helm template" without cluster access
- "disabled": never adapt, e.g. when the workloads use the SCC "anyuid"

Common usage patterns:

{{- if .Values.podSecurityContext.enabled }}
securityContext:
  {{- include "nubus-common.compatibility.renderSecurityContext" (dict
    "secContext" .Values.podSecurityContext
    "context" .) | nindent 2 }}
{{- end }}

Params:

- secContext: The securityContext values, may contain the key "enabled".
- context: The regular context.

*/}}

{{- define "nubus-common.compatibility.renderSecurityContext" -}}
{{- $adapted := omit (.secContext | default dict) "enabled" -}}
{{- if include "nubus-common.compatibility.shouldAdaptSecurityContext" .context -}}
{{- $adapted = omit $adapted "runAsUser" "runAsGroup" "fsGroup" -}}
{{- range $key, $value := $adapted -}}
{{- if and (eq $key "seLinuxOptions") (empty $value) -}}
{{- $adapted = omit $adapted "seLinuxOptions" -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- toYaml $adapted -}}
{{- end -}}

{{/*

Returns "true" if the securityContext has to be adapted for OpenShift, otherwise
an empty string. See "nubus-common.compatibility.renderSecurityContext".

Params:

- Requires the regular context.

*/}}

{{- define "nubus-common.compatibility.shouldAdaptSecurityContext" -}}
{{- include "nubus-common.compatibility.shouldAdapt" (dict "key" "adaptSecurityContext" "context" .) -}}
{{- end -}}

{{/*

Render the "pathType" of an Ingress path, adapted to the target platform.

On OpenShift, Ingress objects are turned into Routes by the ingress-to-route
controller, which ignores paths with the pathType "Exact": these paths get no
Route at all. On OpenShift "Exact" is therefore rendered as "Prefix". Nubus
uses "Exact" for single files like "/univention/portal/portal.json", where a
prefix match is equivalent; more specific paths still take precedence.

Adaptation is controlled by "global.compatibility.openshift.adaptIngress" with
the same values as "adaptSecurityContext": "auto" (default), "force", "disabled".

Usage:

- pathType: {{ include "nubus-common.compatibility.ingressPathType" (dict
    "pathType" .pathType
    "context" $) }}

Params:

- pathType: The pathType as configured, e.g. "Exact" or "Prefix".
- context: The regular context.

*/}}

{{- define "nubus-common.compatibility.ingressPathType" -}}
{{- if and (eq .pathType "Exact") (include "nubus-common.compatibility.shouldAdapt" (dict "key" "adaptIngress" "context" .context)) -}}
Prefix
{{- else -}}
{{- .pathType -}}
{{- end -}}
{{- end -}}

{{/*

Returns "true" if an OpenShift adaptation is active, otherwise an empty string.

Params:

- key: The name of the setting below "global.compatibility.openshift".
- context: The regular context.

*/}}

{{- define "nubus-common.compatibility.shouldAdapt" -}}
{{- $mode := dig "compatibility" "openshift" .key "auto" (get .context.Values "global" | default dict) -}}
{{- if not (has $mode (list "auto" "force" "disabled")) -}}
{{- fail (printf "global.compatibility.openshift.%s must be one of auto, force, disabled; got %q" .key $mode) -}}
{{- end -}}
{{- if or (eq $mode "force") (and (eq $mode "auto") (include "nubus-common.compatibility.isOpenShift" .context)) -}}
true
{{- end -}}
{{- end -}}

{{/*

Returns "true" if the target cluster is OpenShift, otherwise an empty string.

Params:

- Requires the regular context.

*/}}

{{- define "nubus-common.compatibility.isOpenShift" -}}
{{- if .Capabilities.APIVersions.Has "security.openshift.io/v1" -}}
true
{{- end -}}
{{- end -}}
