# MCPサーバー

https://modelcontextprotocol.io/introduction の Quickstart（For Server Developers）を実施したものになります。
どのようなツールが実装されているかは上記Quickstartドキュメントをご確認ください

## 前提

- リポジトリ直下のREADMEに従って環境のセットアップが完了していること

## MCP Inspectorでの確認方法

1. ```npx -y @modelcontextprotocol/inspector```を実行
2. 起動されたInspectorのURLが表示されるのでアクセス
3. ブラウザで開くことを確認したら、左メニューでTransportType等の設定を選択
  - STDIOの場合：CommandとArgumentを入力する（ローカルでの起動とdockerでの起動では異なるため注意）
  - 
4. 

## ローカルでの動作確認方法

1. mcp_serverディレクトリに移動
2. weather.pyの L103 ```mcp.run(transport="stdio")``` をコメントインし、L104 ```mcp.run(transport="streamable-http", host="0.0.0.0", port=8000, log_level="debug")```をコメントアウトする
3. (Claude for Desktopで確認する場合の例) ```code ~/Library/Application\ Support/Claude/claude_desktop_config.json``` で Claude for Desktop の設定ファイルを開く
4. 以下を記載し、保存する
    ``` 
    {
        "mcpServers": {
            "weather": {
                "command": "uv", // macの場合はフルパスを指定する必要があります
                "args": [
                    "--directory",
                    "/ABSOLUTE/PATH/TO/PARENT/FOLDER/mcp_server",
                    "run",
                    "weather.py"
                ]
            }
        }
    }
    ```
5. Claud for Desktopを開き、ツールが使えるようになっているかどうか確認する

## Dockerでの動作確認方法
1. mcp_serverディレクトリに移動
2. weather.pyの L103 ```mcp.run(transport="stdio")``` をコメントインし、L104 ```mcp.run(transport="streamable-http", host="0.0.0.0", port=8000, log_level="debug")```をコメントアウトする
3. ```docker build -t mcp-server . ```を実行してdockerイメージをビルドする
4. (Claude for Desktopで確認する場合の例) ```code ~/Library/Application\ Support/Claude/claude_desktop_config.json``` で Claude for Desktop の設定ファイルを開く
5. 以下を記載し、保存する
    ``` 
    {
        "mcpServers": {
          "weather": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "mcp-server"
            ],
          }
        }
    }
    ```
6. Claud for Desktopを開き、ツールが使えるようになっているかどうか確認する


## ECS上でMCPサーバーを起動する場合と動作確認方法
1. ECRリポジトリを作成する
  - 手動で作成 or Terraformで作成
2. ECRにログイン
    ```bash
    aws ecr get-login-password --region <リージョン> | docker login --username AWS --password-stdin <アカウントID>.dkr.ecr.<リージョン>.amazonaws.com
    ```
3. イメージのビルド
    ```bash
    docker build -t mcp-server .
    ```
4. イメージにタグ付け
    ```bash
    docker tag mcp-server:latest <アカウントID>.dkr.ecr.<リージョン>.amazonaws.com/mcp-server:latest
    ```
5. イメージのプッシュ
    ```bash
    docker push <アカウントID>.dkr.ecr.<リージョン>.amazonaws.com/mcp-server:latest
    ```
6. 記事を参考にしてECS周りを手動で作成 or Terraformで作成
7. ```npm install -g mcp-remote```で mcp-remote をインストール
8. (Claude for Desktopで確認する場合の例) ```code ~/Library/Application\ Support/Claude/claude_desktop_config.json``` で Claude for Desktop の設定ファイルを開く
9. 以下を記載し、保存する
    ``` 
    {
        "mcpServers": {
            "weather-ecs": {
                "command": "mcp-remote", // macの場合はフルパスを指定する必要があります
                "args": [
                    "http://52.195.167.65:8000/mcp/",
                    "--allow-http"
                ]
            }
        }
    }
    ```
10. Claud for Desktopを開き、ツールが使えるようになっているかどうか確認する