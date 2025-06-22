# 🚀 Streamlit Cloudデプロイ手順

## ファイル構成
```
streamlit_app/
├── app_api.py              # メインアプリ（Claude API版）
├── app_final.py            # 基本版（API不要）
├── requirements.txt        # 依存関係
├── .streamlit/
│   ├── config.toml        # Streamlit設定
│   └── secrets.toml       # シークレット設定例
├── .env                   # ローカル環境変数
└── DEPLOY.md             # このファイル
```

## Streamlit Cloudデプロイ手順

### 1. GitHubリポジトリ準備
```bash
# リポジトリをGitHubにプッシュ
git add .
git commit -m "Streamlit Cloud対応"
git push origin main
```

### 2. Streamlit Cloudアプリ作成
1. https://share.streamlit.io/ にアクセス
2. 「New app」をクリック
3. GitHubリポジトリを選択
4. 設定項目：
   - **Repository**: あなたのリポジトリ
   - **Branch**: main
   - **Main file path**: `streamlit_app/app_api.py`
   - **App URL**: 任意のURL

### 3. シークレット設定
Streamlit Cloudの管理画面で：
1. アプリ設定 → **Secrets** タブ
2. 以下を追加：
```toml
ANTHROPIC_API_KEY = "sk-ant-api03-your-actual-api-key-here"
```

### 4. デプロイ確認
- アプリURL: `https://your-app-name.streamlit.app`
- Claude API機能が正常動作することを確認

## 🔧 設定済み機能

### Streamlit Cloud対応済み
✅ **API設定**: `os.getenv()` + `st.secrets.get()`  
✅ **キャッシュ**: `@st.cache_resource`  
✅ **エラーハンドリング**: フォールバック機能  
✅ **UIテーマ**: カスタム設定済み  

### 2x2グリッド評価システム
✅ **詳細評価**: 構成・内容・論理性・表現  
✅ **深い分析**: 300+文字の具体的フィードバック  
✅ **改善提案**: AI生成の具体的アドバイス  

### 実データ対応
✅ **過去問**: 獨協大学・立教大学実データ  
✅ **2026年度**: 最新入試対応  
✅ **自動進行**: 単一選択肢の場合  

## 💰 運用コスト

### Claude-3-Haiku API
- **Input**: $0.25/1M tokens
- **Output**: $1.25/1M tokens  
- **1回あたり**: 約0.9-1.5円

### 推定月間コスト
- **100回利用**: 約90-150円
- **1000回利用**: 約900-1500円

## 🎯 デプロイ後の確認項目

1. **基本動作**: アプリが正常に起動
2. **API接続**: Claude APIが応答
3. **問題生成**: 大学別問題予想が動作
4. **評価機能**: 2x2グリッド表示
5. **模範解答**: 生成機能が動作

## 🔄 更新手順

コード更新後：
```bash
git add .
git commit -m "機能追加"
git push origin main
```
→ Streamlit Cloudが自動で再デプロイ

---

🎯 **準備完了！Streamlit Cloudでデプロイできます**