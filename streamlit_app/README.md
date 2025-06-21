# 総合選抜型入試 小論文対策アプリ (Streamlit版)

大学の総合選抜型入試（AO入試）向けの小論文練習アプリケーションのStreamlit版です。過去問題データから次年度のテーマを予想し、本番さながらの環境で小論文練習ができます。

## 🌟 主要機能

### 📚 大学・学部検索
- 大学名での検索機能
- AO入試対応学部・学科のフィルタリング
- 過去問題データの表示

### 🎯 問題予想・出題
- 過去5年間のデータに基づく次年度テーマ予想
- 現代的なトレンドキーワードを組み込んだ問題生成
- 学部・学科に特化したコンテキスト反映

### ⏱️ 本番形式での練習
- リアルタイムタイマー機能
- 制限時間での自動提出
- 文字数カウント機能

### 🤖 AI採点システム
- **構成** (25点): 序論・本論・結論の構成評価
- **内容** (30点): 具体例・データ活用・多角的視点
- **論理性** (25点): 論理的接続・一貫性
- **表現** (20点): 文体・語彙・読みやすさ
- 総合100点満点での詳細フィードバック

### 📖 書き方ガイド
- **構成**: 小論文の基本構成・論理的文章構成
- **内容**: 説得力のある論拠・データ活用法
- **表現**: 適切な文体・効果的な表現技法
- **例文**: 高評価を得る小論文の実例

## 🚀 技術スタック

- **フレームワーク**: Streamlit
- **言語**: Python 3.8+
- **ライブラリ**: pandas, numpy
- **UI**: Streamlitの標準コンポーネント + カスタムCSS

## 🏗️ プロジェクト構造

```
streamlit_app/
├── app.py                    # メインアプリケーション
├── requirements.txt          # 依存関係
├── data/                     # データモジュール
│   ├── __init__.py
│   ├── models.py            # データクラス定義
│   ├── universities.py      # 大学・学部データ
│   └── writing_guides.py    # 書き方ガイドデータ
└── utils/                    # ユーティリティモジュール
    ├── __init__.py
    ├── question_predictor.py # 問題予想ロジック
    └── essay_scorer.py       # 採点システム
```

## 📦 セットアップ

### 前提条件
- Python 3.8以上
- pip

### インストール

```bash
# リポジトリのクローン
git clone https://github.com/Ume614/shoronbun.git
cd shoronbun/streamlit_app

# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# アプリケーションの起動
streamlit run app.py
```

アプリケーションは `http://localhost:8501` で起動します。

## 💡 使い方

1. **大学検索**: トップページで大学名を入力して検索
2. **学部・学科選択**: AO入試対応の学部・学科を選択
3. **問題確認**: 生成された予想問題を確認
4. **練習開始**: タイマーを開始して小論文を作成
5. **採点結果**: 提出後、詳細な採点結果とアドバイスを確認

## 🎨 UI/UX特徴

### レスポンシブデザイン
- デスクトップ・タブレット・モバイル対応
- Streamlitの標準レイアウトシステム活用

### インタラクティブ要素
- リアルタイムタイマー表示
- プログレスバーによる視覚的フィードバック
- 展開可能なセクション

### アクセシビリティ
- 明確な色分けとアイコン使用
- 読みやすいフォントサイズ
- 直感的なナビゲーション

## 📊 対応大学データ

現在、以下の大学の過去問題データを収録：
- 早稲田大学（政治経済学部、法学部）
- 慶應義塾大学（経済学部）
- 東京大学（教養学部）

※ データは継続的に拡充予定

## 🔧 カスタマイズ

### 大学データの追加
`data/universities.py`の`get_universities()`関数に新しい大学データを追加できます。

### 採点アルゴリズムの調整
`utils/essay_scorer.py`の`score_essay()`関数で採点基準を調整できます。

### 問題予想ロジックの変更
`utils/question_predictor.py`の`generate_predicted_question()`関数で予想アルゴリズムを変更できます。

## 🚀 デプロイ

### Streamlit Cloud
1. GitHubリポジトリをStreamlit Cloudに接続
2. `streamlit_app/app.py`をメインファイルに指定
3. `streamlit_app/requirements.txt`が自動で認識される

### Heroku
```bash
# Herokuアプリケーション作成
heroku create your-app-name

# Procfileの作成
echo "web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0" > Procfile

# デプロイ
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

## 🔮 今後の機能追加予定

- [ ] セッション状態の永続化
- [ ] CSVエクスポート機能
- [ ] より多くの大学データの追加
- [ ] 多言語対応
- [ ] ダークモード対応

## 🐛 トラブルシューティング

### よくある問題

**Q: アプリが起動しない**
A: Python 3.8以上がインストールされているか確認し、requirements.txtの全依存関係がインストールされているか確認してください。

**Q: タイマーが正しく動作しない**
A: ブラウザを更新して再度お試しください。Streamlitのセッション状態がリセットされます。

**Q: 文字化けが発生する**
A: ブラウザのエンコーディング設定をUTF-8に設定してください。

## 🤝 貢献

プルリクエストや課題報告を歓迎します。

## 📄 ライセンス

MIT License

## 📞 お問い合わせ

ご質問や提案がございましたら、GitHubのIssueからお気軽にお知らせください。

---

**開発者**: Ume614  
**リポジトリ**: https://github.com/Ume614/shoronbun