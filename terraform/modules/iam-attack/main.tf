# ─────────────────────────────────────────
# USUARIO VÍCTIMA — MAL CONFIGURADO
# ─────────────────────────────────────────
resource "aws_iam_user" "victim" {
  name = "john.doe"

  tags = {
    Name        = "john-doe-victim"
    Environment = var.environment
    Role        = "developer"
    Risk        = "HIGH"
  }
}

resource "aws_iam_user_login_profile" "victim" {
  user                    = aws_iam_user.victim.name
  password_reset_required = false
}

# ─────────────────────────────────────────
# POLÍTICA EXCESIVA — DEMASIADOS PERMISOS
# ─────────────────────────────────────────
resource "aws_iam_policy" "excessive_policy" {
  name        = "ExcessiveDeveloperPolicy"
  description = "Política con permisos excesivos — vulnerable a propósito"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "iam:*",
          "s3:*",
          "ec2:*",
          "secretsmanager:*",
          "kms:*"
        ]
        Resource = "*"
      }
    ]
  })
}

# ─────────────────────────────────────────
# ADJUNTAR POLÍTICA AL USUARIO VÍCTIMA
# ─────────────────────────────────────────
resource "aws_iam_user_policy_attachment" "victim_policy" {
  user       = aws_iam_user.victim.name
  policy_arn = aws_iam_policy.excessive_policy.arn
}

# ─────────────────────────────────────────
# USUARIO ATACANTE — ACCESO INICIAL LIMITADO
# ─────────────────────────────────────────
resource "aws_iam_user" "attacker" {
  name = "contractor.temp"

  tags = {
    Name        = "contractor-temp-attacker"
    Environment = var.environment
    Role        = "contractor"
    Risk        = "SIMULATED-ATTACKER"
  }
}

resource "aws_iam_policy" "limited_policy" {
  name        = "LimitedContractorPolicy"
  description = "Acceso inicial limitado del atacante"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "iam:List*",
          "iam:Get*",
          "s3:ListBucket",
          "s3:GetObject"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_user_policy_attachment" "attacker_policy" {
  user       = aws_iam_user.attacker.name
  policy_arn = aws_iam_policy.limited_policy.arn
}