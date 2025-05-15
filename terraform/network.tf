# VPC
resource "aws_vpc" "mcp_vpc" {
  cidr_block           = "10.101.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "mcp-server-iac-vpc"
  }
}

# パブリックサブネット
resource "aws_subnet" "public_subnet_1" {
  vpc_id                  = aws_vpc.mcp_vpc.id
  cidr_block              = "10.101.1.0/24"
  availability_zone       = "ap-northeast-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "mcp-server-iac-public-subnet-1"
  }
}

resource "aws_subnet" "public_subnet_2" {
  vpc_id                  = aws_vpc.mcp_vpc.id
  cidr_block              = "10.101.2.0/24"
  availability_zone       = "ap-northeast-1c"
  map_public_ip_on_launch = true

  tags = {
    Name = "mcp-server-iac-public-subnet-2"
  }
}

# インターネットゲートウェイ
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.mcp_vpc.id

  tags = {
    Name = "mcp-server-iac-igw"
  }
}

# ルートテーブル
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.mcp_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "mcp-server-iac-public-rt"
  }
}

# ルートテーブルの関連付け
resource "aws_route_table_association" "public_rta_1" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.public_route_table.id
}

resource "aws_route_table_association" "public_rta_2" {
  subnet_id      = aws_subnet.public_subnet_2.id
  route_table_id = aws_route_table.public_route_table.id
}

# セキュリティグループ
resource "aws_security_group" "ecs_sg" {
  name        = "mcp-server-iac-sg-ecs"
  description = "Security group for ECS"
  vpc_id      = aws_vpc.mcp_vpc.id

  # インバウンドルールは全てのトラフィックを許可
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # アウトバウンドルールも全てのトラフィックを許可
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "mcp-server-iac-sg-ecs"
  }
}

# S3のVPCエンドポイントを作成
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.mcp_vpc.id
  service_name = "com.amazonaws.ap-northeast-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids = [aws_route_table.public_route_table.id]

  tags = {
    Name = "mcp-server-iac-vpce-s3"
  }
}