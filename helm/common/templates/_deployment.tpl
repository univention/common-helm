{{- /*
common.deployment will render a Deployment manifest and apply overrides if provided.

Arguments are passed as a dict with the following keys:

- top: The top level context

- overrides: (optional) Overrides to apply.

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
      # TODO: Consolidate this to only support "global.imagePullSecrets"
      {{- with (coalesce .top.Values.global.imagePullSecrets .top.Values.image.pullSecrets .top.Values.imagePullSecrets) }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .top.Values.podSecurityContext }}
      securityContext:
        {{ toYaml . | nindent 8 | trim }}
      {{- end }}
      containers:
        - name: {{ include "common.names.name" .top }}
          securityContext:
            {{- toYaml .top.Values.securityContext | nindent 12 }}
          {{- $registry := .top.Values.image.registry | default .top.Values.global.imageRegistry }}
          {{- with .top.Values.image }}
          image: "{{ if $registry }}{{ $registry }}/{{ end }}{{ .repository }}{{ if .tag }}:{{ .tag }}{{ end }}{{ if .digest }}@{{ .digest }}{{ end }}"
          imagePullPolicy: {{ .pullPolicy }}
          {{- end }}
          envFrom:
            - configMapRef:
                name: {{ include "common.names.fullname" .top }}
          volumeMounts:
            {{- if .top.Values.extraVolumeMounts }}
            {{ toYaml .top.Values.extraVolumeMounts | nindent 12 }}
            {{- end }}
            {{- if .top.Values.mountUcr }}
            - name: "config-map-ucr-defaults"
              mountPath: "/etc/univention/base-defaults.conf"
              subPath: "base.conf"
            {{- end }}
            {{- if (and .top.Values.mountUcr .top.Values.global .top.Values.global.configMapUcr) }}
            - name: "config-map-ucr"
              mountPath: "/etc/univention/base.conf"
              subPath: "base.conf"
            {{- end }}
            {{- if (and .top.Values.mountUcr .top.Values.global .top.Values.global.configMapUcrForced) }}
            - name: "config-map-ucr-forced"
              mountPath: "/etc/univention/base-forced.conf"
              subPath: "base.conf"
            {{- end }}
            {{- if .top.Values.mountSecrets }}
            - name: "secrets"
              # TODO: conflict with /run/secrets, should use a namespace
              mountPath: "/var/secrets"
            {{- end }}
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
      volumes:
        {{- if .top.Values.extraVolumes }}
        {{ toYaml .top.Values.extraVolumes | nindent 8 }}
        {{- end }}
        {{- if .top.Values.mountUcr }}
        - name: "config-map-ucr-defaults"
          configMap:
            name: {{ required "Please provide the name of the UCR ConfigMap in .Values.global.configMapUcrDefaults!" .top.Values.global.configMapUcrDefaults | quote }}
        {{- end }}
        {{- if (and .top.Values.mountUcr .top.Values.global .top.Values.global.configMapUcr) }}
        - name: "config-map-ucr"
          configMap:
            name: "{{ .top.Values.global.configMapUcr }}"
        {{- end }}
        {{- if (and .top.Values.mountUcr .top.Values.global .top.Values.global.configMapUcrForced) }}
        - name: "config-map-ucr-forced"
          configMap:
            name: "{{ .top.Values.global.configMapUcrForced }}"
        {{- end }}
        {{- if .top.Values.mountSecrets }}
        - name: "secrets"
          secret:
            secretName: {{ include "common.names.fullname" .top | quote }}
        {{- end }}
{{- end }}
