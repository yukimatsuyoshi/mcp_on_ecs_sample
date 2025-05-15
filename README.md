# MCPサーバーサンプルコード

[Qiitaの記事:「」]()のサンプルコードになります。記事を読み進める際に参考にしていただければと思います。

## ディレクトリ構成

### mcp_client
- MCPサーバー構築後にプログラムから利用できることを確認するためのコード群です
- cliから動作確認するためのmain.pyと、streamlitを利用して実装したGUIのコードであるmain_gui.pyがあります
- それぞれの実行方法に関してはmcp_clientディレクトリ下のREADMEに詳しく記載しています

### mcp_server
- サンプルのMCPサーバーのコード群になります。以下のMCPのドキュメントのQuickStartを愚直に行なったものになります
    - https://modelcontextprotocol.io/quickstart/server
- dockerで起動するためのDockerfileも配置しています。イメージの作成や実行方法等はmcp_server下のREADMEに詳しく記載しています

### terraform
- MCPサーバーをECSで起動するためのインフラリソースを管理するサンプルコードになります
- デプロイ方法についてはterraformディレクトリ下のREADMEに詳しく記載しています


## セットアップ

### 前提条件

- Python 3.10以上
- terraform 1.9以上
    - tfenvでのバージョン管理がおすすめです
- プロジェクト管理に**uv**を利用しているので、事前にインストールしておいてください
    - こちらも上記の[QuickStart](https://modelcontextprotocol.io/quickstart/server)を参考にしてください
- AWS CLIの認証設定
    - mcp_client のプログラムからの実行を試す場合は、東京リージョン(ap-northeast-1)だけではなく、バージニア北部(us-east-1)のプロファイルも用意して切り替えるか、環境変数のAWS_REGIONをus-east-1に変更してください

### mcp_server / mcp_client ディレクトリ共通のセットアップ

1. 仮想環境を作成して有効化します：

```bash
uv venv
source .venv/bin/activate  # Linuxの場合
# または
.venv\Scripts\activate  # Windowsの場合
```

2. uv syncを実行して必要なパッケージをインストールします:

```bash
uv sync
```