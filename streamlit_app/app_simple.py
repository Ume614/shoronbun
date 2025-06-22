import streamlit as st
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="🤖 Claude API搭載 総合選抜型入試 小論文対策アプリ（2026年度入試対応）",
    page_icon="📝",
    layout="wide"
)

st.title("🤖 Claude API搭載 総合選抜型入試 小論文対策アプリ（2026年度入試対応）")

# API キー確認
api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    st.success("✅ Claude API キーが設定されています")
    st.write(f"キー長: {len(api_key)} 文字")
else:
    st.error("⚠️ Claude API キーが設定されていません")

# 基本的な入力フォーム
st.header("📝 小論文練習")

university = st.selectbox("大学を選択", ["獨協大学", "立教大学", "昭和女子大学"])
essay_text = st.text_area("小論文を入力してください", height=200)

if st.button("評価開始"):
    if essay_text:
        st.success("✅ 入力を受け付けました")
        st.write(f"選択大学: {university}")
        st.write(f"文字数: {len(essay_text)}文字")
    else:
        st.error("小論文を入力してください")