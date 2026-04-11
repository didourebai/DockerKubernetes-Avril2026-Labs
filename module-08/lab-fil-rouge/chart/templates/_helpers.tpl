{{/*
_helpers.tpl — Fonctions réutilisables dans les templates Helm
*/}}

{{/* Nom complet de la release */}}
{{- define "it-portal.fullname" -}}
{{- printf "%s" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/* Labels communs appliqués à toutes les ressources */}}
{{- define "it-portal.labels" -}}
app.kubernetes.io/name: it-portal
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Values.app.version | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}
