{{/*

Render the "imagePullSecrets" configuration based on the context.

Common usage patterns:

{{- include "nubus-common.images.renderPullSecrets" . | nindent 6 }}

Params:

- Requires the regular context.

*/}}

{{- define "nubus-common.images.renderPullSecrets" }}
{{- if or .Values.imagePullSecrets .Values.global.imagePullSecrets  }}
imagePullSecrets:
{{- range .Values.global.imagePullSecrets }}
  - name: "{{ tpl . $ }}"
{{- end }}
{{- range .Values.imagePullSecrets }}
  - name: "{{ tpl . $ }}"
{{- end }}
{{- end }}
{{- end }}
