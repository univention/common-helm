{{/*

Return the image name based on the image configuration and the global defaults.

The function interface is compatible with the one defined in Bitnami's "common"
chart.

Use like in the following example:

{{ include "common.images.image" ( dict "imageRoot" .Values.path.to.the.image "global" .Values.global ) }}

*/}}

{{- define "common.images.image" }}
  {{- $registry := .imageRoot.registry | default .global.imageRegistry }}
  {{- if $registry }}{{ $registry }}/{{ end }}
  {{- .imageRoot.repository }}
  {{- if .imageRoot.tag }}:{{ .imageRoot.tag }}{{ end }}
  {{- if .imageRoot.digest }}@{{ .imageRoot.digest }}{{ end }}
{{- end }}
