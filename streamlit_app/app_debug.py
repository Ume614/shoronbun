import streamlit as st
import time
import random
import re
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

# ページ設定
st.set_page_config(
    page_title="小論文対策アプリ（デバッグ版）",
    page_icon="📝",
    layout="wide"
)

st.title("📝 小論文対策アプリ（デバッグ版）")

# 基本的なテスト
st.header("🔍 機能テスト")

# 1. 基本的なStreamlit機能テスト
st.subheader("1. 基本機能テスト")
test_input = st.text_input("テスト入力", "Hello World")
if test_input:
    st.success(f"入力されたテキスト: {test_input}")

# 2. データ構造テスト
st.subheader("2. データ構造テスト")

@dataclass
class TestData:
    name: str
    value: int

test_data = [
    TestData("早稲田大学", 1),
    TestData("慶應義塾大学", 2),
    TestData("東京大学", 3)
]

st.write("テストデータ:")
for data in test_data:
    st.write(f"- {data.name}: {data.value}")

# 3. 検索機能テスト
st.subheader("3. 検索機能テスト")
search_term = st.text_input("大学名を検索", placeholder="例: 早稲田")

if search_term:
    filtered_data = [d for d in test_data if search_term in d.name]
    st.write(f"検索結果: {len(filtered_data)}件")
    for data in filtered_data:
        st.write(f"✓ {data.name}")
else:
    st.write("全データ:")
    for data in test_data:
        st.write(f"• {data.name}")

# 4. セレクトボックステスト
st.subheader("4. セレクトボックステスト")
university_names = [d.name for d in test_data]
selected = st.selectbox("大学を選択", ["選択してください"] + university_names)

if selected != "選択してください":
    st.success(f"選択された大学: {selected}")

# 5. AI機能テスト（簡易版）
st.subheader("5. AI機能テスト")

def simple_ai_test(text):
    """簡単なAI機能のテスト"""
    word_count = len(text.replace(' ', ''))
    has_examples = '例えば' in text or '具体的に' in text
    
    score = 0
    feedback = []
    
    if word_count >= 100:
        score += 30
        feedback.append("十分な文字数です")
    else:
        feedback.append("文字数が不足しています")
    
    if has_examples:
        score += 20
        feedback.append("具体例が含まれています")
    else:
        feedback.append("具体例を追加してください")
    
    return {
        "score": score,
        "feedback": " / ".join(feedback),
        "word_count": word_count
    }

test_essay = st.text_area("テスト用小論文", 
                         placeholder="ここに文章を入力してください...",
                         height=200)

if st.button("AI採点テスト"):
    if test_essay.strip():
        result = simple_ai_test(test_essay)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("スコア", f"{result['score']}/50")
        with col2:
            st.metric("文字数", result['word_count'])
        
        st.info(f"フィードバック: {result['feedback']}")
    else:
        st.warning("文章を入力してください")

# 6. タイマーテスト
st.subheader("6. タイマーテスト")

if 'timer_start' not in st.session_state:
    st.session_state.timer_start = None

if st.button("タイマー開始"):
    st.session_state.timer_start = time.time()

if st.session_state.timer_start:
    elapsed = time.time() - st.session_state.timer_start
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    st.write(f"経過時間: {minutes}:{seconds:02d}")
    
    if st.button("タイマーリセット"):
        st.session_state.timer_start = None
        st.rerun()

# 7. 実際の大学データテスト
st.subheader("7. 実際の大学データテスト")

# 簡略化された大学データ
universities = [
    {
        "name": "早稲田大学",
        "faculties": [
            {
                "name": "政治経済学部",
                "departments": ["政治学科", "経済学科"]
            }
        ]
    },
    {
        "name": "慶應義塾大学", 
        "faculties": [
            {
                "name": "経済学部",
                "departments": ["経済学科"]
            }
        ]
    }
]

st.write("登録されている大学:")
for uni in universities:
    with st.expander(uni["name"]):
        for faculty in uni["faculties"]:
            st.write(f"**{faculty['name']}**")
            for dept in faculty["departments"]:
                st.write(f"- {dept}")

# 8. 環境情報
st.subheader("8. 環境情報")
import sys
import platform

st.write(f"Python バージョン: {sys.version}")
st.write(f"プラットフォーム: {platform.platform()}")
st.write(f"Streamlit バージョン: {st.__version__}")

# 9. エラーテスト
st.subheader("9. エラーハンドリングテスト")

if st.button("意図的エラーテスト"):
    try:
        # 意図的にエラーを発生
        result = 1 / 0
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.info("エラーハンドリングは正常に動作しています")

st.success("✅ デバッグ版の基本機能は正常に動作しています")

# 10. 実際のアプリの簡易版
st.subheader("10. 簡易版アプリテスト")

if st.button("簡易版アプリを試す"):
    st.session_state.show_simple_app = True

if 'show_simple_app' in st.session_state and st.session_state.show_simple_app:
    st.markdown("---")
    st.header("簡易版小論文アプリ")
    
    # 大学選択
    uni_choice = st.selectbox("大学選択", 
                              ["選択してください", "早稲田大学", "慶應義塾大学", "東京大学"])
    
    if uni_choice != "選択してください":
        st.success(f"選択: {uni_choice}")
        
        # 問題表示
        sample_questions = [
            "AIと人間の共存について論じなさい。",
            "持続可能な社会の実現について述べなさい。",
            "デジタル化が社会に与える影響について論じなさい。"
        ]
        
        question = random.choice(sample_questions)
        st.info(f"問題: {question}")
        
        # 簡易エディター
        essay = st.text_area("解答", height=300, key="simple_essay")
        
        if st.button("採点"):
            if essay.strip():
                # 簡易採点
                word_count = len(essay.replace(' ', ''))
                score = min(100, word_count // 5)  # 5文字で1点
                
                st.metric("スコア", f"{score}/100点")
                
                if score >= 80:
                    st.success("優秀!")
                elif score >= 60:
                    st.info("良好")
                else:
                    st.warning("要改善")
            else:
                st.error("文章を入力してください")
    
    if st.button("簡易版アプリを閉じる"):
        st.session_state.show_simple_app = False
        st.rerun()