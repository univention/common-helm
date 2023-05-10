{{- define "common.ingress.tpl" -}}

apiVersion: {{ include "common.capabilities.ingress.apiVersion" . }}
kind: Ingress
metadata:
  name: {{ include "common.names.fullname" . }}
  labels:
    {{- include "common.labels.standard" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if .Values.ingress.ingressClassName }}
  ingressClassName: {{ .Values.ingress.ingressClassName }}
  {{- end }}
  {{- if .Values.ingress.tls.enabled }}
  tls:
    - hosts:
        - {{ .Values.ingress.host | quote }}
      secretName: "{{ .Values.ingress.tls.secretName }}"
  {{- end }}
  rules:
    - host: {{ required "The hostname has to be set in \"ingress.host\"." .Values.ingress.host | quote }}
      http:
        paths:
          {{- range .Values.ingress.paths }}
          - pathType: {{ .pathType }}
            path: {{ .path }}
            backend: {{- include "common.ingress.backend" (dict "serviceName" (include "common.names.fullname" $) "servicePort" "http" "context" $) | nindent 14 }}
          {{- end }}

{{- end -}}

{{- define "common.ingress" -}}
  {{- include "common.utils.merge" (append . "common.ingress.tpl") }}
{{- end }}
