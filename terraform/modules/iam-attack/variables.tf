variable "environment" {
  description = "Nombre del entorno"
  type        = string
  default     = "lab"
}

variable "weak_password" {
  description = "Contraseña débil intencional para el usuario víctima"
  type        = string
  default     = "Password123!"
}
