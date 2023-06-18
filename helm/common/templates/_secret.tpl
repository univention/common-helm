{{- /*
common.secret will render a Secret manifest and apply overrides if provided.

Arguments are passed as a dict with the following keys:

- top: The top level context

- overrides: (optional) Overrides to apply, this should set the values in "data".

*/}}

{{- define "common.secret" -}}
{{- include "common.utils.merge" (set . "base" "common.secret.tpl") }}
{{- end }}


{{- /*
common.secret.tpl will render a Secret manifest.

Arguments are passed as a dict with the following keys:

- top: The top level context

*/}}
{{- define "common.secret.tpl" }}
apiVersion: v1
kind: Secret
type: Opaque
metadata:
  name: '{{ include "common.names.fullname" .top }}'
  labels:
    {{- include "common.labels.standard" .top | nindent 4 }}
data: {}
{{- end }}
