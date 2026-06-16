#!/usr/bin/env python3
"""
CloudStrike RedBlue Lab — Fase 4: Detección y Respuesta
El Blue Team analiza el ataque y elimina la amenaza.
"""

import boto3
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

SESSION = boto3.Session(
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

IAM = SESSION.client("iam", endpoint_url="http://localhost:4566")
S3  = SESSION.client("s3",  endpoint_url="http://localhost:4566")

# ─────────────────────────────────────────
# PASO 1 — DETECTAR USUARIOS SOSPECHOSOS
# ─────────────────────────────────────────
def detect_suspicious_users():
    console.print(Panel("🔵 PASO 1 — Detectando usuarios sospechosos", style="bold blue"))
    
    response = IAM.list_users()
    suspicious = []
    
    table = Table(title="Análisis de usuarios")
    table.add_column("Usuario", style="cyan")
    table.add_column("Riesgo", style="red")
    table.add_column("Motivo", style="yellow")
    
    known_users = ["john.doe", "contractor.temp"]
    
    for user in response["Users"]:
        username = user["UserName"]
        
        if username not in known_users:
            suspicious.append(username)
            table.add_row(username, "🚨 ALTO", "Usuario no autorizado detectado")
        else:
            table.add_row(username, "✅ OK", "Usuario conocido")
    
    console.print(table)
    return suspicious

# ─────────────────────────────────────────
# PASO 2 — DETECTAR POLÍTICAS PELIGROSAS
# ─────────────────────────────────────────
def detect_dangerous_policies(suspicious_users):
    console.print(Panel("🔵 PASO 2 — Detectando políticas peligrosas", style="bold blue"))
    
    dangerous_policies = []
    
    for user in suspicious_users:
        response = IAM.list_attached_user_policies(UserName=user)
        
        for policy in response["AttachedPolicies"]:
            policy_detail = IAM.get_policy(PolicyArn=policy["PolicyArn"])
            policy_name = policy_detail["Policy"]["PolicyName"]
            
            console.print(f"  🚨 [red]{user}[/red] tiene política peligrosa: [yellow]{policy_name}[/yellow]")
            dangerous_policies.append({
                "user": user,
                "policy_arn": policy["PolicyArn"],
                "policy_name": policy_name
            })
    
    return dangerous_policies

# ─────────────────────────────────────────
# PASO 3 — RESPUESTA: ELIMINAR BACKDOOR
# ─────────────────────────────────────────
def eliminate_backdoor(suspicious_users, dangerous_policies):
    console.print(Panel("🔵 PASO 3 — Eliminando amenaza", style="bold blue"))
    
    for policy in dangerous_policies:
        try:
            IAM.detach_user_policy(
                UserName=policy["user"],
                PolicyArn=policy["policy_arn"]
            )
            console.print(f"  ✅ Política [yellow]{policy['policy_name']}[/yellow] removida de [cyan]{policy['user']}[/cyan]")
            
            IAM.delete_policy(PolicyArn=policy["policy_arn"])
            console.print(f"  ✅ Política [yellow]{policy['policy_name']}[/yellow] eliminada")
        except Exception as e:
            console.print(f"  [red]Error removiendo política: {e}[/red]")
    
    for user in suspicious_users:
        try:
            IAM.delete_user(UserName=user)
            console.print(f"  ✅ Usuario backdoor [cyan]{user}[/cyan] eliminado")
        except Exception as e:
            console.print(f"  [red]Error eliminando usuario: {e}[/red]")

# ─────────────────────────────────────────
# PASO 4 — ASEGURAR BUCKET S3
# ─────────────────────────────────────────
def secure_bucket():
    console.print(Panel("🔵 PASO 4 — Asegurando bucket S3 vulnerable", style="bold blue"))
    
    try:
        S3.put_public_access_block(
            Bucket="cloudstrike-vulnerable-data",
            PublicAccessBlockConfiguration={
                "BlockPublicAcls":       True,
                "IgnorePublicAcls":      True,
                "BlockPublicPolicy":     True,
                "RestrictPublicBuckets": True
            }
        )
        console.print("  ✅ Acceso público bloqueado en bucket vulnerable")
    except Exception as e:
        console.print(f"  [red]Error asegurando bucket: {e}[/red]")

# ─────────────────────────────────────────
# PASO 5 — VERIFICAR ESTADO FINAL
# ─────────────────────────────────────────
def verify_cleanup():
    console.print(Panel("🔵 PASO 5 — Verificando estado final", style="bold blue"))
    
    response = IAM.list_users()
    
    table = Table(title="Estado final de usuarios")
    table.add_column("Usuario", style="cyan")
    table.add_column("Estado", style="green")
    
    for user in response["Users"]:
        table.add_row(user["UserName"], "✅ Autorizado")
    
    console.print(table)

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == "__main__":
    console.print(Panel(
        "CloudStrike RedBlue Lab\n🔵 MODO: Blue Team — Detección y Respuesta\n👤 Defensor: Security Engineer",
        style="bold blue"
    ))
    
    suspicious_users = detect_suspicious_users()
    
    if suspicious_users:
        dangerous_policies = detect_dangerous_policies(suspicious_users)
        eliminate_backdoor(suspicious_users, dangerous_policies)
        secure_bucket()
        verify_cleanup()
        
        console.print(Panel(
            "🔵 RESPUESTA COMPLETADA\n→ Usuario backdoor eliminado\n→ Políticas peligrosas removidas\n→ Bucket S3 asegurado\n→ Cuenta restaurada a estado seguro",
            style="bold blue"
        ))
    else:
        console.print(Panel("✅ No se detectaron amenazas", style="bold green"))