output "victim_user_name" {
  description = "Nombre del usuario víctima"
  value       = aws_iam_user.victim.name
}

output "victim_user_arn" {
  description = "ARN del usuario víctima"
  value       = aws_iam_user.victim.arn
}

output "attacker_user_name" {
  description = "Nombre del usuario atacante"
  value       = aws_iam_user.attacker.name
}

output "attacker_user_arn" {
  description = "ARN del usuario atacante"
  value       = aws_iam_user.attacker.arn
}

output "excessive_policy_arn" {
  description = "ARN de la política excesiva"
  value       = aws_iam_policy.excessive_policy.arn
}