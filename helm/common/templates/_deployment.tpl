{{- /*
common.deployment will render a Deployment manifest and apply overrides if provided.

Arguments are passed as a dict with the following keys:

- top: The top level context

- overrides: (optional) Overrides to apply, this should set the values in "data".

*/}}

{{- define "common.deployment" -}}
{{- include "common.utils.merge" (set . "base" "common.deployment.tpl") }}
{{- end }}


{{- /*
common.deployment.tpl will render a Deployment manifest.

Arguments are passed as a dict with the following keys:

- top: The top level context

*/}}
{{- define "common.deployment.tpl" }}
apiVersion: {{ include "common.capabilities.deployment.apiVersion" .top }}
kind: Deployment
metadata:
  name: {{ include "common.names.fullname" .top }}
  labels:
    {{- include "common.labels.standard" .top | nindent 4 }}
spec:
  replicas: {{ .top.Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "common.labels.matchLabels" .top | nindent 6 }}
  template:
    metadata:
      {{- with .top.Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "common.labels.standard" .top | nindent 8 }}
    spec:
      {{- with .top.Values.affinity }}
      affinity:
        {{ toYaml . | nindent 8 | trim }}
      {{- end }}
      {{- with .top.Values.tolerations }}
      tolerations:
        {{ toYaml . | nindent 8 | trim }}
      {{- end }}
      {{- with .top.Values.nodeSelector }}
      nodeSelector:
        {{ toYaml . | nindent 8 | trim }}
      {{- end }}
      {{- with .top.Values.podSecurityContext }}
      securityContext:
        {{ toYaml . | nindent 8 | trim }}
      {{- end }}
      containers:
        - name: {{ include "common.names.name" .top }}
          securityContext:
            {{- toYaml .top.Values.securityContext | nindent 12 }}
          {{- with .top.Values.image }}
          image: "{{ .registry }}/{{ .repository }}{{ if .sha256 }}@sha256:{{ .sha256 }}{{ else }}:{{ .tag }}{{ end }}"
          imagePullPolicy: {{ .imagePullPolicy }}
          {{- end }}
          envFrom:
            - configMapRef:
                name: {{ include "common.names.fullname" .top }}
          ports:
            {{- range $key, $value := .top.Values.service.ports }}
            - name: {{ $key }}
              containerPort: {{ $value.containerPort }}
              protocol: {{ $value.protocol }}
            {{- end }}
          {{- if .top.Values.probes.liveness.enabled }}
          livenessProbe:
            tcpSocket:
              port: http
            initialDelaySeconds: {{ .top.Values.probes.liveness.initialDelaySeconds }}
            timeoutSeconds: {{ .top.Values.probes.liveness.timeoutSeconds }}
            periodSeconds: {{ .top.Values.probes.liveness.periodSeconds }}
            failureThreshold: {{ .top.Values.probes.liveness.failureThreshold }}
            successThreshold: {{ .top.Values.probes.liveness.successThreshold }}
          {{- end }}
          {{- if .top.Values.probes.readiness.enabled }}
          readinessProbe:
            tcpSocket:
              port: http
            initialDelaySeconds: {{ .top.Values.probes.readiness.initialDelaySeconds }}
            timeoutSeconds: {{ .top.Values.probes.readiness.timeoutSeconds }}
            periodSeconds: {{ .top.Values.probes.readiness.periodSeconds }}
            failureThreshold: {{ .top.Values.probes.readiness.failureThreshold }}
            successThreshold: {{ .top.Values.probes.readiness.successThreshold }}
          {{- end }}
          resources:
            {{- toYaml .top.Values.resources | nindent 12 }}
{{- end }}
