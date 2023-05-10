{{- /*
common.ingress.tpl will render an Ingress manifest.

Arguments are passed as a dict with the following keys:

- top: The top level context

# TODO: Can ingress be set by default to .Values.ingress if not provided?
- ingress: The ingress values, typically .Values.ingress

*/}}
{{- define "common.ingress.tpl" -}}

apiVersion: {{ include "common.capabilities.ingress.apiVersion" .top }}
kind: Ingress
metadata:
  name: {{ include "common.names.fullname" .top }}
  labels:
    {{- include "common.labels.standard" .top | nindent 4 }}
  {{- with .ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if .ingress.ingressClassName }}
  ingressClassName: {{ .ingress.ingressClassName }}
  {{- end }}
  {{- if .ingress.tls.enabled }}
  tls:
    - hosts:
        - {{ .ingress.host | quote }}
      secretName: "{{ .ingress.tls.secretName }}"
  {{- end }}
  rules:
    {{- /* TODO: Validation should be done in a different way.
           Might be that this should be part of the using chart and not in this library. */}}
    - host: {{ required "The hostname has to be set in \"ingress.host\"." .ingress.host | quote }}
      http:
        paths:
          {{- range .ingress.paths }}
          - pathType: {{ .pathType }}
            path: {{ .path }}
            backend: {{- include "common.ingress.backend" (dict "serviceName" (include "common.names.fullname" $.top) "servicePort" "http" "context" $.top) | nindent 14 }}
          {{- end }}

{{- end -}}

{{- define "common.ingress" -}}
  {{- include "common.utils.merge" (set . "base" "common.ingress.tpl") }}
{{- end }}
