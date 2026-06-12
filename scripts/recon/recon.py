#!/usr/bin/env python3
"""
CloudStrike RedBlue Lab — Fase 1: Reconocimiento
Simula las acciones de un atacante con acceso inicial limitado.
El atacante es: contractor.temp
"""

import boto3
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# ─────────────────────────────────────────
# CONFIGURACIÓN — ATACANTE
# ─────────────────────────────────────────
SESSION = boto3.Session(
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

IAM = SESSION.client("iam", endpoint_url="http://localhost:4566")
S3  = SESSION.client("s3",  endpoint_url="http://localhost:4566")

# ─────────────────────────────────────────
# FUNCIÓN 1 — ENUMERAR USUARIOS
# ─────────────────────────────────────────
def enumerate_users():
    console.print(Panel("🔍 FASE 1 — Enumerando usuarios IAM", style="bold red"))
    
    response = IAM.list_users()
    
    table = Table(title="Usuarios encontrados")
    table.add_column("Usuario", style="cyan")
    table.add_column("ARN", style="yellow")
    table.add_column("Creado", style="green")
    
    for user in response["Users"]:
        table.add_row(
            user["UserName"],
            user["Arn"],
            str(user["CreateDate"])
        )
    
    console.print(table)
    return [u["UserName"] for u in response["Users"]]

# ─────────────────────────────────────────
# FUNCIÓN 2 — ENUMERAR POLÍTICAS DE USUARIO
# ─────────────────────────────────────────
def enumerate_user_policies(users):
    console.print(Panel("🔍 FASE 2 — Analizando permisos de cada usuario", style="bold red"))
    
    for user in users:
        response = IAM.list_attached_user_policies(UserName=user)
        policies = response["AttachedPolicies"]
        
        if policies:
            console.print(f"\n[cyan]{user}[/cyan] tiene estas políticas:")
            for policy in policies:
                console.print(f"  → [yellow]{policy['PolicyName']}[/yellow]")
                
                if "Excessive" in policy["PolicyName"]:
                    console.print(f"  ⚠️  [bold red]ALERTA: política con permisos excesivos detectada[/bold red]")

# ─────────────────────────────────────────
# FUNCIÓN 3 — ENUMERAR BUCKETS S3
# ─────────────────────────────────────────
def enumerate_buckets():
    console.print(Panel("🔍 FASE 3 — Enumerando buckets S3", style="bold red"))
    
    response = S3.list_buckets()
    
    table = Table(title="Buckets S3 encontrados")
    table.add_column("Bucket", style="cyan")
    table.add_column("Creado", style="green")
    
    for bucket in response["Buckets"]:
        table.add_row(
            bucket["Name"],
            str(bucket["CreationDate"])
        )
    
    console.print(table)
    return [b["Name"] for b in response["Buckets"]]

# ─────────────────────────────────────────
# FUNCIÓN 4 — BUSCAR ARCHIVOS SENSIBLES
# ─────────────────────────────────────────
def find_sensitive_files(buckets):
    console.print(Panel("🔍 FASE 4 — Buscando archivos sensibles", style="bold red"))
    
    sensitive_keywords = ["credential", "password", "secret", "key", "token"]
    
    for bucket in buckets:
        try:
            response = S3.list_objects_v2(Bucket=bucket)
            
            if "Contents" in response:
                for obj in response["Contents"]:
                    key = obj["Key"].lower()
                    for keyword in sensitive_keywords:
                        if keyword in key:
                            console.print(f"  🎯 [bold red]ARCHIVO SENSIBLE:[/bold red] s3://{bucket}/{obj['Key']}")
        except Exception as e:
            console.print(f"  [red]Sin acceso a {bucket}: {e}[/red]")

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == "__main__":
    console.print(Panel(
        "CloudStrike RedBlue Lab\n🔴 MODO: Red Team — Reconocimiento\n👤 Atacante: contractor.temp",
        style="bold red"
    ))
    
    users = enumerate_users()
    enumerate_user_policies(users)
    buckets = enumerate_buckets()
    find_sensitive_files(buckets)
    
    console.print(Panel(
        "✅ Reconocimiento completado\n→ Usuario vulnerable encontrado: john.doe\n→ Archivo sensible encontrado: s3://cloudstrike-vulnerable-data/sensitive/credentials.txt",
        style="bold yellow"
    ))