{{/*

Render the full annotation structure for a resource.

The main purpose of this template is to make the annotations handling as
fool-proof as possible for the standard cases. It includes the key "annotations"
in its output and ensures that the key is only present if there are
annotations.

Cases which require additional entries should use the template
"nubus.annotations.entries" instead.

Common usage patterns:

{{- include "nubus-common.annotations.render" ( dict
  "values" .Values.additionalAnnotations
  "context" . )
  | nindent 2 }}

{{- include "nubus-common.annotations.render" ( dict
  "values" ( list .Values.ingress.annotations .Values.additionalAnnotations )
  "context" . )
  | nindent 2 }}

Params: See "nubus-common.annotations.entries".

*/}}

{{- define "nubus-common.annotations.render" }}
{{- $entries := include "nubus-common.annotations.entries" . }}
{{- if $entries -}}
annotations:
  {{- $entries | nindent 2 }}
{{- end }}
{{- end }}


{{/*

Render the annotation entries for a resource.

Common usage patterns:

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

{{- $values := .values }}
{{- if not ( kindIs "slice" $values ) }}
  {{- $values = ( list $values ) }}
{{- end }}
{{- if ( compact $values ) }}
  {{- include "common.tplvalues.merge" ( dict "values" $values "context" .context ) }}
{{- end }}
{{- end }}
