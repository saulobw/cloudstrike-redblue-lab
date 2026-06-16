# CloudStrike RedBlue Lab 🔴🔵

> Red Team + Blue Team en AWS — atacar, detectar y responder. Proyecto 2 de 3 del portafolio Cloud Security Engineering.

## ¿Qué es este proyecto?

CloudStrike RedBlue Lab es un laboratorio de seguridad ofensiva y defensiva sobre infraestructura AWS. Simula ataques reales contra una cuenta cloud mal configurada y luego implementa la detección y respuesta. Forma parte de un portafolio de tres proyectos de Cloud Security Engineering.

## El escenario

Una empresa tiene un desarrollador (`john.doe`) con permisos excesivos y un bucket S3 con credenciales expuestas. Un contratista externo (`contractor.temp`) con acceso limitado descubre estas vulnerabilidades y las explota.

## Fases del ataque y defensa

| Fase | Rol | Descripción |
|---|---|---|
| **Fase 1** | 🔴 Red Team | Reconocimiento — enumerar usuarios, permisos y archivos sensibles |
| **Fase 2** | 🔴 Red Team | Escalación de privilegios — crear usuario backdoor con acceso total |
| **Fase 3** | 🔴 Red Team | Exfiltración — robar credenciales del bucket S3 vulnerable |
| **Fase 4** | 🔵 Blue Team | Detección y respuesta — eliminar backdoor y asegurar la cuenta |

## Vulnerabilidades simuladas

| Vulnerabilidad | Descripción | MITRE ATT&CK |
|---|---|---|
| Permisos excesivos IAM | Usuario con `iam:*` sin restricciones | T1078 |
| Credenciales expuestas en S3 | Archivo con passwords en bucket sin cifrado | T1552.001 |
| Escalación de privilegios | Creación de usuario backdoor con admin total | T1098 |
| Exfiltración via S3 | Descarga de datos sensibles | T1530 |

## Stack técnico

- **IaC:** Terraform
- **Simulador:** LocalStack
- **Lenguaje:** Python 3 + boto3
- **Monitoreo:** AWS CloudWatch

## Estructura del proyecto
cloudstrike-redblue-lab/

├── terraform/

│   ├── environments/lab/     ← punto de entrada

│   └── modules/

│       ├── iam-attack/       ← usuarios vulnerables

│       ├── network/          ← VPC y bucket S3 vulnerable

│       └── logging/          ← CloudWatch y alarmas

├── scripts/

│   ├── recon/                ← reconocimiento

│   │   └── recon.py

│   ├── exploit/              ← escalación y exfiltración

│   │   ├── escalate.py

│   │   └── exfiltrate.py

│   └── defend/               ← detección y respuesta

│       └── defend.py

├── reports/                  ← reportes de seguridad

└── docs/                     ← arquitectura y decisiones

## Cómo ejecutar el laboratorio

``
# 1. Iniciar LocalStack
localstack start -d

# 2. Desplegar infraestructura vulnerable
cd terraform/environments/lab
terraform init && terraform apply

# 3. Red Team — Reconocimiento
python3 scripts/recon/recon.py

# 4. Red Team — Escalación de privilegios
python3 scripts/exploit/escalate.py

# 5. Red Team — Exfiltración
python3 scripts/exploit/exfiltrate.py

# 6. Blue Team — Detección y respuesta
python3 scripts/defend/defend.py
``

## Portafolio completo

| # | Proyecto | Descripción | Estado |
|---|---|---|---|
| 1 | **CloudGuard Foundation** | Infraestructura cloud segura | ✅ Completado |
| 2 | **CloudStrike RedBlue Lab** | Red Team + Blue Team en AWS | ✅ Completado |
| 3 | **CloudMind AI-SOC** | SOC con Inteligencia Artificial | 🔄 En progreso |

## Autor

**saulobw** — Cloud Security Engineering Portfolio  
[GitHub](https://github.com/saulobw) · [LinkedIn](#)

---
*Construido con fines educativos y de portafolio profesional*
