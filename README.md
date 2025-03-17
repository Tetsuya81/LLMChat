# LLM Chat Client

OpenAI API形式のLLMサーバーと対話するためのシンプルなPythonクライアントライブラリです。

## 機能

- OpenAI API形式のエンドポイントとの通信
- 会話履歴の管理
- システムメッセージのサポート
- 温度（ランダム性）とトークン数の制御

## インストール

```bash
python -m venv .venv
source .venv/bin/activate  # Linuxの場合
# または
.venv\Scripts\activate  # Windowsの場合

pip install -r requirements.txt
```

## 使用方法

```python
from llm_chat_client import LLMChatClient

# クライアントの初期化
client = LLMChatClient(
    endpoint_url="http://127.0.0.1:8080",  # LLMサーバーのエンドポイント
    model="gpt-3.5-turbo"  # 使用するモデル
)

# システムメッセージの設定（オプション）
client.add_system_message("あなたは役立つAIアシスタントです。")

# メッセージの送信
response = client.send_message(
    "こんにちは！",
    temperature=0.7,  # 生成のランダム性（0.0〜2.0）
    max_tokens=1000  # 最大トークン数
)

print(response)
```

## 主なメソッド

- `send_message(message, temperature=0.7, max_tokens=1000)`: メッセージを送信し、応答を受け取ります
- `add_system_message(content)`: システムメッセージを設定します
- `clear_history()`: 会話履歴をクリアします

## 対話型モード

スクリプトを直接実行すると、対話型モードで起動します：

```bash
python llm-chat-client.py
```

## ライセンス

MIT
