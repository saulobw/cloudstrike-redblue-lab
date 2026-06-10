# ─────────────────────────────────────────
# VPC PRINCIPAL
# ─────────────────────────────────────────
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "cloudstrike-vpc"
    Environment = var.environment
    Project     = "cloudstrike-redblue-lab"
  }
}

# ─────────────────────────────────────────
# SUBREDES
# ─────────────────────────────────────────
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr
  map_public_ip_on_launch = true

  tags = {
    Name        = "cloudstrike-public-subnet"
    Environment = var.environment
  }
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = var.private_subnet_cidr

  tags = {
    Name        = "cloudstrike-private-subnet"
    Environment = var.environment
  }
}

# ─────────────────────────────────────────
# INTERNET GATEWAY
# ─────────────────────────────────────────
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name        = "cloudstrike-igw"
    Environment = var.environment
  }
}

# ─────────────────────────────────────────
# ROUTE TABLE PÚBLICA
# ─────────────────────────────────────────
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name        = "cloudstrike-public-rt"
    Environment = var.environment
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# ─────────────────────────────────────────
# BUCKET S3 VULNERABLE — SIN CIFRADO
# ─────────────────────────────────────────
resource "aws_s3_bucket" "vulnerable" {
  bucket        = "cloudstrike-vulnerable-data"
  force_destroy = true

  tags = {
    Name        = "cloudstrike-vulnerable-data"
    Environment = var.environment
    Risk        = "HIGH"
  }
}

resource "aws_s3_object" "sensitive_file" {
  bucket  = aws_s3_bucket.vulnerable.id
  key     = "sensitive/credentials.txt"
  content = "db_password=SuperSecret123!\napi_key=sk-prod-1234567890abcdef"
}