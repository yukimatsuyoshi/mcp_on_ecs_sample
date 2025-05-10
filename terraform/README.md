# Terraform のサンプルコード

MCPサーバーをECSで起動するためのインフラリソースを管理するサンプルコードになります

## リソースのデプロイ手順
1. AWS CLIの認証設定に関して、東京リージョンのプロファイルであることを確認してください（そうでない場合は切り替える）
2. terraformディレクトリに移動し、```terraform init```を実行
3. 先にECRリポジトリのみデプロイしたいので、ECRのリソースにターゲットを絞って```terraform plan```を実行
    - ```terraform plan -target aws_ecr_repository.app_repo```
4. plan結果に問題がなければ、ECRのリソースにターゲットを絞って```terraform apply```を実行
    - ```terraform apply -target aws_ecr_repository.app_repo```
5. ECRのプライベートリポジトリが作成されたら、mcp_serverディレクトリに移動し、dockerイメージをプッシュ（mcp_serverディレクトリの
READMEを参照）
6. 残りのリソースをデプロイするために、ターゲットを絞らず```terraform plan```を実行
7. plan結果に問題がなければ、```terraform apply```を実行
8. ECSのコンソールでタスクが正常起動することを確認したら、Claude for Desktop や Cline で動作確認