# プロバイダーの設定
terraform {
  # 必要なTerraformのバージョンを指定
  required_version = ">= 1.9.0"

  # 必要なプロバイダーを指定
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  # tfstateの管理にS3を使う場合は以下をコメントイン
  /*
  backend "s3" {
    bucket         = "your-terraform-state-bucket"
    key            = "terraform.tfstate"
    region         = "ap-northeast-1"
    dynamodb_table = "terraform-lock"
    encrypt        = true
  }
  */
}

# AWSプロバイダーの設定
provider "aws" {
  region = "ap-northeast-1"
}