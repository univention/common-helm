{{- /*
common.virtualservice will render an VirtualService manifest and apply
overrides if provided.

Arguments are passed as a dict with the following keys:

- top: The top level context

- istio: (optional) The istio related values, defaults to .Values.istio from .top.

- overrides: (optional) Overrides to apply.

Only renders output if ".istio.enabled" and ".istio.virtualService" evaluate to "true".
*/}}

{{- define "common.virtualService" -}}
  {{- $_ := set . "istio" (default .top.Values.istio .istio) -}}
  {{- if and .istio.enabled .istio.virtualService.enabled }}
    {{- include "common.utils.merge" (set . "base" "common.virtualService.tpl") }}
  {{- end }}
{{- end }}


{{- /*
common.virtualService.tpl will render an VirtualService manifest.

Arguments are passed as a dict with the following keys:

- top: The top level context

- istio: The istio related values, typically .Values.istio

*/}}
{{- define "common.virtualService.tpl" }}

apiVersion: "networking.istio.io/v1beta1"
kind: "VirtualService"
metadata:
  name: {{ include "common.names.fullname" .top | quote }}
  labels:
    {{- include "common.labels.standard" .top | nindent 4 }}
  {{- with .istio.virtualService.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  hosts:
    - {{ required "The hostname has to be set in \"istio.host\"." .istio.host | quote }}
  gateways:
    - {{ .istio.gateway.externalGatewayName | default (printf "%s-%s" (include "common.names.fullname" .top) "-gateway") }}
  http:
    {{- $parent := . -}}
    {{- /* TODO: Refactor to avoid duplication with the range call below */}}
    {{- range .istio.virtualService.pathOverrides }}
    - match:
        - uri:
            {{ .match }}: {{ .path | quote }}
      {{- if .rewrite }}
      rewrite:
        uri: {{ .rewrite | quote }}
      {{- end }}
      route:
        {{ toYaml .route | nindent 6 }}
      headers:
        request:
          set:
            x-forwarded-host: "{{ $parent.istio.host }}"
    {{- end }}
    {{- range .istio.virtualService.paths }}
    - match:
        - uri:
            {{ .match }}: {{ .path | quote }}
      {{- if .rewrite }}
      rewrite:
        uri: {{ .rewrite | quote }}
      {{- end }}
      route:
        - destination:
            port:
              number: {{ $parent.top.Values.service.ports.http.port }}
            host: {{ include "common.names.fullname" $parent.top | quote }}
      headers:
        request:
          set:
            x-forwarded-host: "{{ $parent.istio.host }}"
    {{- end }}
{{- end }}
