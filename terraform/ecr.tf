# ECRプライベートリポジトリの作成
resource "aws_ecr_repository" "app_repo" {
  name                 = "mcp-server-iac-ecr"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "mcp-server-iac-ecr"
  }
}