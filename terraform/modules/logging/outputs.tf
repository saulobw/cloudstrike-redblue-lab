output "log_group_name" {
  description = "Nombre del log group de detección de ataques"
  value       = aws_cloudwatch_log_group.attack_detection.name
}

output "privilege_escalation_alarm" {
  description = "Nombre de la alarma de escalación de privilegios"
  value       = aws_cloudwatch_metric_alarm.privilege_escalation.alarm_name
}

output "sensitive_data_alarm" {
  description = "Nombre de la alarma de acceso a datos sensibles"
  value       = aws_cloudwatch_metric_alarm.sensitive_data_access.alarm_name
}