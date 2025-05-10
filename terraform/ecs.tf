# ECSクラスター
resource "aws_ecs_cluster" "app_cluster" {
  name = "mcp-server-iac-ecs-cluster"

  tags = {
    Name = "mcp-server-iac-ecs-cluster"
  }
}

# ECSタスク定義
resource "aws_ecs_task_definition" "app_task" {
  family                   = "mcp-server-iac-ecs-task"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  
  container_definitions = jsonencode([
    {
      name       = "mcp-server-iac"
      image      = "${aws_ecr_repository.app_repo.repository_url}:latest"
      essenntial = "true",
        "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
            "awslogs-group": "/ecs/mcp-server-iac-ecs",
            "awslogs-region": "ap-northeast-1",
            "awslogs-stream-prefix": "ecs"
        }
      },
      "portMappings": [
            {
                "name": "8000",
                "containerPort": 8000,
                "hostPort": 8000,
                "protocol": "tcp",
                "appProtocol": "http"
            }
        ]
    }
  ])

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "ARM64"
  }

  lifecycle { ignore_changes = [container_definitions]}

  tags = {
    Name = "mcp-server-iac-ecs-task"
  }

  depends_on = [aws_cloudwatch_log_group.ecs_logs]
}

# ECSサービス
resource "aws_ecs_service" "app_service" {
  name            = "mcp-server-iac-ecs-service"
  cluster         = aws_ecs_cluster.app_cluster.id
  task_definition = aws_ecs_task_definition.app_task.arn
  launch_type     = "FARGATE"
  desired_count   = 1
  
  # ネットワーク設定
  network_configuration {
    subnets          = [aws_subnet.public_subnet_1.id, aws_subnet.public_subnet_2.id]
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }
  
  # ヘルスチェックの猶予期間
  health_check_grace_period_seconds = 60

  tags = {
    Name = "mcp-server-iac-ecs-service"
  }

  # 循環参照を避けるためにIAMロールの変更を無視
  depends_on = [aws_iam_role_policy_attachment.ecs_task_execution_role_policy]
}

# CloudWatch Logsのロググループ
resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/ecs/mcp-server-iac-ecs"
  retention_in_days = 30

  tags = {
    Name        = "mcp-server-iac-ecs-logs"
  }
}