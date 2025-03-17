import requests
import json
from typing import List, Dict, Any, Optional

class LLMChatClient:
    """
    シンプルなLLMチャットクライアント
    OpenAI API形式で指定されたエンドポイントにリクエストを送信するためのクラス
    """
    
    def __init__(self, endpoint_url: str = "http://127.0.0.1:8080", model: str = "gpt-3.5-turbo"):
        """
        初期化メソッド
        
        Args:
            endpoint_url: LLMサーバーのエンドポイントURL
            model: 使用するモデル名（デフォルトはgpt-3.5-turbo）
        """
        self.endpoint_url = endpoint_url
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
    
    def add_message(self, role: str, content: str) -> None:
        """
        会話履歴にメッセージを追加する
        
        Args:
            role: メッセージの送信者の役割 ("user", "assistant", または "system")
            content: メッセージの内容
        """
        self.conversation_history.append({"role": role, "content": content})
    
    def send_message(self, message: str, temperature: float = 0.7, max_tokens: int = 1000) -> Optional[str]:
        """
        メッセージを送信し、応答を受け取る（OpenAI API形式）
        
        Args:
            message: 送信するメッセージの内容
            temperature: 生成のランダム性を制御するパラメータ (0.0〜2.0)
            max_tokens: 生成する最大トークン数
            
        Returns:
            Optional[str]: LLMからの応答。エラーの場合はNone
        """
        # ユーザーメッセージを履歴に追加
        self.add_message("user", message)
        
        # OpenAI API形式のリクエストペイロードを作成
        payload = {
            "model": self.model,
            "messages": self.conversation_history,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            # POSTリクエストを送信
            response = requests.post(
                self.endpoint_url,
                headers=headers,
                data=json.dumps(payload)
            )
            
            # ステータスコードを確認
            response.raise_for_status()
            
            # レスポンスをJSONとしてパース
            response_data = response.json()
            
            # OpenAI API形式のレスポンスから回答を取得
            assistant_message = response_data["choices"][0]["message"]["content"]
            
            # アシスタントの回答を履歴に追加
            if assistant_message:
                self.add_message("assistant", assistant_message)
            
            return assistant_message
            
        except requests.exceptions.RequestException as e:
            print(f"エラー: リクエスト中にエラーが発生しました: {e}")
            return None
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            print(f"エラー: レスポンスの解析中にエラーが発生しました: {e}")
            return None

    def add_system_message(self, content: str) -> None:
        """
        システムメッセージを会話履歴に追加する
        
        Args:
            content: システムメッセージの内容
        """
        # システムメッセージは常に履歴の先頭に追加
        if self.conversation_history and self.conversation_history[0].get("role") == "system":
            self.conversation_history[0]["content"] = content
        else:
            self.conversation_history.insert(0, {"role": "system", "content": content})

    def clear_history(self) -> None:
        """会話履歴をクリアする"""
        self.conversation_history = []


# 使用例
if __name__ == "__main__":
    # クライアントを初期化
    client = LLMChatClient()
    
    # オプション: システムメッセージを設定
    client.add_system_message("あなたは役立つAIアシスタントです。")
    
    print("LLMチャットを開始します。終了するには 'exit' または 'quit' と入力してください。")
    
    while True:
        # ユーザー入力を取得
        user_input = input("\nあなた: ")
        
        # 終了コマンドをチェック
        if user_input.lower() in ["exit", "quit", "終了"]:
            print("チャットを終了します。")
            break
        
        # メッセージを送信し、応答を受け取る
        response = client.send_message(user_input)
        
        # 応答を表示
        if response:
            print(f"\nアシスタント: {response}")
        else:
            print("\nエラー: 応答を取得できませんでした。")
