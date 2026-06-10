# ─────────────────────────────────────────
# CLOUDWATCH LOG GROUP — DETECTIVE
# ─────────────────────────────────────────
resource "aws_cloudwatch_log_group" "attack_detection" {
  name              = "/cloudstrike/attack-detection"
  retention_in_days = var.log_retention_days

  tags = {
    Name        = "cloudstrike-attack-detection"
    Environment = var.environment
    Team        = "blue-team"
  }
}

# ─────────────────────────────────────────
# ALARMA — ESCALACIÓN DE PRIVILEGIOS
# ─────────────────────────────────────────
resource "aws_cloudwatch_metric_alarm" "privilege_escalation" {
  alarm_name          = "cloudstrike-privilege-escalation"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "PrivilegeEscalation"
  namespace           = "CloudStrikeSecurity"
  period              = 300
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "Alerta: posible escalación de privilegios detectada"

  tags = {
    Name        = "cloudstrike-priv-esc-alarm"
    Environment = var.environment
    Team        = "blue-team"
  }
}

# ─────────────────────────────────────────
# ALARMA — ACCESO A DATOS SENSIBLES
# ─────────────────────────────────────────
resource "aws_cloudwatch_metric_alarm" "sensitive_data_access" {
  alarm_name          = "cloudstrike-sensitive-data-access"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "SensitiveDataAccess"
  namespace           = "CloudStrikeSecurity"
  period              = 300
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "Alerta: acceso a datos sensibles detectado"

  tags = {
    Name        = "cloudstrike-data-access-alarm"
    Environment = var.environment
    Team        = "blue-team"
  }
}