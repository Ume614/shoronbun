#!/usr/bin/env python3
"""
Claude API接続テスト
"""
import os
from dotenv import load_dotenv
import anthropic

def test_claude_connection():
    """Claude API接続テスト"""
    print("🤖 Claude API接続テストを開始...")
    
    # 環境変数読み込み
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ ANTHROPIC_API_KEY が設定されていません")
        print("📝 設定方法:")
        print("1. .env ファイルを作成")
        print("2. ANTHROPIC_API_KEY=your-api-key-here を記述")
        return False
    
    try:
        # Claude クライアント作成
        client = anthropic.Anthropic(api_key=api_key)
        
        # 簡単なテスト
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=50,
            messages=[
                {"role": "user", "content": "こんにちは。API接続テストです。"}
            ]
        )
        
        print("✅ Claude API接続成功!")
        print(f"📨 レスポンス: {response.content[0].text}")
        return True
        
    except Exception as e:
        print(f"❌ API接続エラー: {e}")
        print("📝 確認項目:")
        print("1. APIキーが正しく設定されているか")
        print("2. Anthropicアカウントに十分なクレジットがあるか")
        print("3. ネットワーク接続が正常か")
        return False

if __name__ == "__main__":
    test_claude_connection()