{{- /*
common.service will render a Service manifest and apply overrides if provided.

Arguments are passed as a dict with the following keys:

- top: The top level context

- service: (optional) The service values, defaults to .Values.service from .top.

- overrides: (optional) Overrides to apply, this should set the values in "data".

*/}}

{{- define "common.service" }}
  {{- $_ := set . "service" (default .top.Values.service .service) -}}
  {{- if .service.enabled }}
    {{- include "common.utils.merge" (set . "base" "common.service.tpl") }}
  {{- end }}
{{- end }}


{{- /*
common.service.tpl will render a Service manifest.

Arguments are passed as a dict with the following keys:

- top: The top level context

- service: The service values, typically .Values.service

*/}}
{{- define "common.service.tpl" }}
apiVersion: v1
kind: Service
metadata:
  name: {{ include "common.names.fullname" .top }}
  labels:
    {{- include "common.labels.standard" .top | nindent 4 }}
spec:
  type: {{ .service.type }}
  {{- if .service.sessionAffinity.enabled }}
  sessionAffinity: "ClientIP"
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: {{ .service.sessionAffinity.timeoutSeconds }}
  {{- end }}
  ports:
    {{- range $key, $value := .service.ports }}
    - port: {{ $value.port }}
      targetPort: {{ default $key $value.containerPort }}
      protocol: {{ $value.protocol }}
      name: {{ $key }}
      {{- if and (eq $.service.type "NodePort") $value.nodePort }}
      nodePort: {{ $value.nodePort }}
      {{- end }}
    {{- end }}
  selector:
    {{- include "common.labels.matchLabels" .top | nindent 4 }}
{{- end }}
