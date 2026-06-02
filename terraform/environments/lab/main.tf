# CloudStrike RedBlue Lab — Entorno de ataque y defensa
# Este archivo es el punto de entrada principal de Terraform

module "iam_attack" {
  source = "../../modules/iam-attack"
}

module "network" {
  source = "../../modules/network"
}

module "logging" {
  source = "../../modules/logging"
}