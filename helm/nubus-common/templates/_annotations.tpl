{{/*
Render the annotation entries for a resource.

Usage:

{{- include "nubus-common.annotations.entries" ( dict
  "values" .Values.additionalAnnotations
  "context" . )
  | nindent 4 }}

{{- include "nubus-common.annotations.entries" ( dict
  "values" ( list .Values.ingress.annotations .Values.additionalAnnotations )
  "context" . )
  | nindent 4 }}

Params:

- values - Dict | List[Dict] - Required. The annotation values to render. If
  a list is given, then the annotations will be merged.

  Precedence is from left to right, consistent with "common.tplvalues.merge".

  The values support templating.

- context - Dict - Required. The context for the template evaluation.

*/}}

{{- define "nubus-common.annotations.entries" }}

{{ $values := .values }}
{{- if kindIs "map" $values }}
  {{- $values = ( list $values ) }}
{{- end }}

{{- if .values }}
  {{- include "common.tplvalues.merge" ( dict "values" $values "context" .context ) }}
{{- end }}
{{- end }}
