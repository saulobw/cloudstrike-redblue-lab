variable "environment" {
  description = "Nombre del entorno"
  type        = string
  default     = "lab"
}

variable "log_retention_days" {
  description = "Días de retención de logs"
  type        = number
  default     = 90
}