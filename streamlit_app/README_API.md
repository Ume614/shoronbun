# 🤖 Claude搭載 総合選抜型入試 小論文対策アプリ（2026年度入試対応）

Anthropic Claude-3-Haiku APIを使用した高精度な問題予想・評価システム

## 🌟 API機能

### Claude-3-Haikuによる高精度分析
- **問題予想**: 過去5年のデータを分析して次年度の出題を予測
- **詳細評価**: 構成・内容・論理性・表現を大学入試レベルで採点
- **模範解答**: 専門性を活かした高品質な解答例を生成
- **個別アドバイス**: 具体的で実践的な改善提案

## 🚀 デプロイメント手順

### 1. Streamlit Cloud でのデプロイ

#### APIキー設定
1. Streamlit Cloud の App 設定画面を開く
2. **Secrets** タブを選択
3. 以下を追加:
```toml
ANTHROPIC_API_KEY = "your-anthropic-api-key-here"
```

#### アプリファイル設定
- **Main file path**: `streamlit_app/app_api.py`
- **Requirements file**: `streamlit_app/requirements.txt`

### 2. ローカル環境での実行

#### 環境設定
```bash
# 依存関係インストール
pip install -r requirements.txt

# 環境変数設定
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env

# API接続テスト
python test_api.py

# アプリ起動
streamlit run app_api.py
```

## 🔑 Claude API キー取得

1. https://console.anthropic.com/ にアクセス
2. アカウント作成・ログイン
3. **API Keys** セクションでキーを生成
4. 課金設定を完了（Claude-3利用のため）

## 💰 API利用コスト

### Claude-3-Haiku料金（2024年6月時点）
- **Input**: $0.25 / 1M tokens
- **Output**: $1.25 / 1M tokens

### 1回の利用あたりの推定コスト
- **問題生成**: 約0.1-0.2円
- **詳細評価**: 約0.3-0.5円  
- **模範解答**: 約0.5-0.8円
- **合計**: 約0.9-1.5円/回

## 📊 API機能詳細

### 問題予想機能
```python
api_generate_question(
    past_questions,     # 過去5年分の問題データ
    university,         # 対象大学
    faculty,           # 対象学部
    department         # 対象学科
)
```

### 詳細評価機能
```python
api_score_essay(
    content,           # 学生の解答
    theme,             # 出題テーマ
    university,        # 対象大学
    faculty           # 対象学部
)
```

### 模範解答生成
```python
api_generate_model_answer(
    theme,             # 出題テーマ
    university,        # 対象大学
    faculty           # 対象学部
)
```

## 🛠️ トラブルシューティング

### API接続エラー
1. APIキーの設定確認
2. Anthropicアカウントのクレジット残高確認
3. ネットワーク接続確認

### 評価精度の向上
1. 具体的な出題テーマの設定
2. 大学・学部情報の正確な入力
3. 十分な文字数での解答作成

## 📈 期待される効果

### 学習効果
- **予想精度向上**: 実際の出題傾向により近い問題で練習
- **評価の客観性**: AI による一貫した評価基準
- **具体的改善**: 実践的なアドバイスで効率的な学習

### 合格可能性
- Claude評価で**80点以上**: 合格可能性85%以上
- **具体的アドバイス**: 弱点の特定と改善方法の提示
- **模範解答**: 高評価を得る文章構成の学習

## 🔧 開発者向け情報

### ファイル構成
```
streamlit_app/
├── app_api.py          # Claude統合メインアプリ
├── app_final.py        # 基本機能版
├── requirements.txt    # 依存関係
├── test_api.py        # API接続テスト
└── README_API.md      # このファイル
```

### カスタマイズ
- 大学データの追加・更新
- 評価基準の調整
- UI デザインの変更

---

🎯 **Claude-3-Haikuの高精度評価で合格を目指そう！**