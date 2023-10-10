{{- /*
common.configMap will render a ConfigMap manifest and apply overrides if provided.

Arguments are passed as a dict with the following keys:

- top: The top level context

- overrides: (optional) Overrides to apply, this should set the values in "data".

*/}}

{{- define "common.configMap" -}}
{{- include "common.utils.merge" (set . "base" "common.configMap.tpl") }}
{{- end }}


{{- /*
common.configMap.tpl will render a ConfigMap manifest.

Arguments are passed as a dict with the following keys:

- top: The top level context

*/}}
{{- define "common.configMap.tpl" }}
apiVersion: "v1"
kind: ConfigMap
metadata:
  name: '{{ include "common.names.fullname" .top }}'
  labels:
    {{- include "common.labels.standard" .top | nindent 4 }}
data: {}
{{- end }}
