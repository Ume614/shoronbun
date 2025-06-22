import streamlit as st
import time
import random
import re
import os
import json
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional, Dict
import anthropic
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="🤖 Claude API搭載 総合選抜型入試 小論文対策アプリ（2026年度入試対応）",
    page_icon="📝",
    layout="wide"
)

# Claude API 設定
@st.cache_resource
def get_claude_client():
    """Claude クライアントを取得"""
    api_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ Claude API キーが設定されていません。環境変数 ANTHROPIC_API_KEY を設定してください。")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)

# データクラス定義
@dataclass
class PastQuestion:
    id: str
    year: int
    theme: str
    time_limit: int
    university: str
    faculty: str
    department: str

@dataclass
class Department:
    id: str
    name: str
    has_ao: bool
    past_questions: List[PastQuestion]

@dataclass
class Faculty:
    id: str
    name: str
    departments: List[Department]
    has_ao: bool

@dataclass
class University:
    id: str
    name: str
    faculties: List[Faculty]

# 大学データ
@st.cache_resource
def get_universities():
    return [
        University(
            id='dokkyo',
            name='獨協大学',
            faculties=[
                Faculty(
                    id='foreign-languages',
                    name='外国語学部',
                    has_ao=True,
                    departments=[
                        Department(
                            id='exchange-culture',
                            name='交流文化学科',
                            has_ao=True,
                            past_questions=[
                                PastQuestion(
                                    id='dokkyo-culture-2025',
                                    year=2025,
                                    theme='【長文読解型】TikTokの影響力と情報発信について論じた文章を読み、「TikTokアプリを禁止すべき」との主張についてのあなたの考えを、本文の議論をふまえて述べなさい。（601字以上800字以内）',
                                    time_limit=90,
                                    university='獨協大学',
                                    faculty='外国語学部',
                                    department='交流文化学科'
                                ),
                                PastQuestion(
                                    id='dokkyo-culture-2024',
                                    year=2024,
                                    theme='【長文読解型】Twitter買収・デジタル時代の公共性について論じた文章を読み、「オンライン上の言論空間はどのようなものであるべきでしょうか」について、本文の議論をふまえたあなたの考えを述べなさい。（601字以上800字以内）',
                                    time_limit=90,
                                    university='獨協大学',
                                    faculty='外国語学部',
                                    department='交流文化学科'
                                ),
                                PastQuestion(
                                    id='dokkyo-culture-2023',
                                    year=2023,
                                    theme='【長文読解型】「利他」について論じた文章を読み、問1（短答式9字抜き出し）、問2「あなたは利他についてどのように考えますか」筆者の考えを参考にしてあなたの考えを述べなさい。（601字以上800字以内）',
                                    time_limit=90,
                                    university='獨協大学',
                                    faculty='外国語学部',
                                    department='交流文化学科'
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        University(
            id='rikkyo',
            name='立教大学',
            faculties=[
                Faculty(
                    id='sports-wellness',
                    name='スポーツウェルネス学部',
                    has_ao=True,
                    departments=[
                        Department(
                            id='sports-wellness',
                            name='スポーツウェルネス学科',
                            has_ao=True,
                            past_questions=[
                                PastQuestion(
                                    id='rikkyo-sports-2025',
                                    year=2025,
                                    theme='スポーツ活動における優秀な実績を持つあなたが、大学でどのような学びを深めたいか、具体的な目標と計画を述べなさい。（800字以内）',
                                    time_limit=60,
                                    university='立教大学',
                                    faculty='スポーツウェルネス学部',
                                    department='スポーツウェルネス学科'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]

# Claude API関数
def api_generate_question(past_questions: List[PastQuestion], university: str, faculty: str, department: str) -> str:
    """Claude APIを使用した問題予想"""
    try:
        client = get_claude_client()
        
        past_themes = [q.theme for q in past_questions[-3:]]
        past_themes_text = "\n".join([f"- {theme}" for theme in past_themes])
        
        prompt = f"""あなたは{university}{faculty}{department}の総合選抜型入試問題作成の専門家です。

過去3年の出題傾向：
{past_themes_text}

2026年度入試の出題予想を1問作成してください。

【要求事項】
1. 過去問の傾向を分析し、2026年に出題されそうなテーマを選定
2. 現代社会の課題や最新トピックを反映
3. {university}の特色や{faculty}の専門性を考慮
4. 文字数制限と制限時間を明記
5. 学生の思考力と表現力を問う内容

出力形式：
問題文のみを出力してください。"""

        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text.strip()
        
    except Exception as e:
        st.error(f"API エラー: {str(e)}")
        return fallback_generate_question(past_questions, university, faculty, department)

def api_score_essay(content: str, theme: str, university: str, faculty: str) -> dict:
    """Claude APIを使用した詳細採点"""
    try:
        client = get_claude_client()
        
        prompt = f"""あなたは{university}{faculty}の入試評価の専門家です。以下の小論文を詳細に評価してください。

【出題テーマ】
{theme}

【学生の解答】
{content}

【評価基準】
以下の4項目を100点満点で評価し、詳細なフィードバックを提供してください：

1. 構成・組織化 (25点満点)
2. 内容・論点 (25点満点)  
3. 論理性・一貫性 (25点満点)
4. 表現・文章力 (25点満点)

各項目について300文字以上の具体的な評価と改善提案を含めてください。

以下のJSON形式で回答してください：
{
  "総合得点": 数値,
  "構成": {"得点": 数値, "評価": "詳細評価文", "改善点": "具体的改善提案"},
  "内容": {"得点": 数値, "評価": "詳細評価文", "改善点": "具体的改善提案"},
  "論理性": {"得点": 数値, "評価": "詳細評価文", "改善点": "具体的改善提案"},
  "表現": {"得点": 数値, "評価": "詳細評価文", "改善点": "具体的改善提案"},
  "総合評価": "全体的な評価コメント",
  "具体的アドバイス": ["改善提案1", "改善提案2", "改善提案3", "改善提案4", "改善提案5", "改善提案6"]
}"""

        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        
        # JSON部分を抽出
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start != -1 and json_end != -1:
            json_text = response_text[json_start:json_end]
            return json.loads(json_text)
        else:
            raise ValueError("JSON形式の応答が見つかりません")
            
    except Exception as e:
        st.error(f"API エラー: {str(e)}")
        return fallback_score_essay(content, theme, university, faculty)

def api_generate_model_answer(theme: str, university: str, faculty: str) -> str:
    """Claude APIを使用した模範解答生成"""
    try:
        client = get_claude_client()
        
        prompt = f"""あなたは{university}{faculty}の入試対策専門家です。以下のテーマで模範解答を作成してください。

【出題テーマ】
{theme}

【要求事項】
1. {university}{faculty}の求める学生像に適した内容
2. 論理的で説得力のある構成
3. 具体例や根拠を含む
4. 適切な文字数（600-800字程度）
5. 合格レベルの文章力

模範解答のみを出力してください。"""

        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text.strip()
        
    except Exception as e:
        st.error(f"API エラー: {str(e)}")
        return f"模範解答の生成でエラーが発生しました: {str(e)}"

# フォールバック関数
def fallback_generate_question(past_questions: List[PastQuestion], university: str, faculty: str, department: str) -> str:
    themes = [
        "デジタル社会における情報リテラシーの重要性について論じなさい。",
        "持続可能な社会の実現に向けて、私たちができることを具体的に述べなさい。",
        "多様性を尊重する社会づくりについてあなたの考えを述べなさい。"
    ]
    return f"{random.choice(themes)}（800字以内、90分）"

def fallback_score_essay(content: str, theme: str, university: str, faculty: str) -> dict:
    base_score = min(85, max(60, len(content) // 10 + random.randint(50, 75)))
    return {
        "総合得点": base_score,
        "構成": {"得点": base_score-5, "評価": "構成は概ね適切です。", "改善点": "より明確な段落構成を意識してください。"},
        "内容": {"得点": base_score-3, "評価": "内容は適切です。", "改善点": "より具体的な例を含めてください。"},
        "論理性": {"得点": base_score-2, "評価": "論理展開は妥当です。", "改善点": "論理的つながりを強化してください。"},
        "表現": {"得点": base_score-1, "評価": "表現は適切です。", "改善点": "より多様な表現を使用してください。"},
        "総合評価": "全体的に良い文章です。",
        "具体的アドバイス": ["構成を明確にする", "具体例を追加", "論理的つながりを強化", "表現を多様化"]
    }

# メイン関数
def main():
    st.title("🤖 Claude API搭載 総合選抜型入試 小論文対策アプリ（2026年度入試対応）")
    st.markdown("---")
    
    # 初期化
    if 'step' not in st.session_state:
        st.session_state.step = 'select'
    if 'selected_university' not in st.session_state:
        st.session_state.selected_university = None
    if 'selected_faculty' not in st.session_state:
        st.session_state.selected_faculty = None
    if 'selected_department' not in st.session_state:
        st.session_state.selected_department = None
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'essay_content' not in st.session_state:
        st.session_state.essay_content = ""
    if 'essay_result' not in st.session_state:
        st.session_state.essay_result = None
    
    universities = get_universities()
    
    # ステップ1: 大学選択
    if st.session_state.step == 'select':
        st.header("🎯 大学・学部・学科選択")
        
        university_names = [u.name for u in universities]
        selected_uni_name = st.selectbox("大学を選択してください", university_names)
        
        if selected_uni_name:
            selected_university = next(u for u in universities if u.name == selected_uni_name)
            st.session_state.selected_university = selected_university
            
            faculty_names = [f.name for f in selected_university.faculties if f.has_ao]
            selected_fac_name = st.selectbox("学部を選択してください", faculty_names)
            
            if selected_fac_name:
                selected_faculty = next(f for f in selected_university.faculties if f.name == selected_fac_name)
                st.session_state.selected_faculty = selected_faculty
                
                dept_names = [d.name for d in selected_faculty.departments if d.has_ao]
                selected_dept_name = st.selectbox("学科を選択してください", dept_names)
                
                if selected_dept_name:
                    selected_department = next(d for d in selected_faculty.departments if d.name == selected_dept_name)
                    st.session_state.selected_department = selected_department
                    
                    if st.button("問題生成へ進む", type="primary"):
                        st.session_state.step = 'question'
                        st.rerun()
    
    # ステップ2: 問題生成
    elif st.session_state.step == 'question':
        st.header("🎲 問題生成")
        
        with st.spinner("Claude AIが問題を生成中..."):
            past_questions = st.session_state.selected_department.past_questions
            question = api_generate_question(
                past_questions,
                st.session_state.selected_university.name,
                st.session_state.selected_faculty.name,
                st.session_state.selected_department.name
            )
            st.session_state.current_question = question
        
        st.success("✅ 問題生成完了！")
        st.markdown("### 📝 出題")
        st.write(question)
        
        if st.button("小論文入力へ進む", type="primary"):
            st.session_state.step = 'essay'
            st.rerun()
    
    # ステップ3: 小論文入力
    elif st.session_state.step == 'essay':
        st.header("✍️ 小論文入力")
        
        # タイマー機能
        if 'start_time' not in st.session_state:
            st.session_state.start_time = None
        if 'timer_started' not in st.session_state:
            st.session_state.timer_started = False
        
        # タイマーコントロール
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 📝 出題")
            st.write(st.session_state.current_question)
        
        with col2:
            if not st.session_state.timer_started:
                if st.button("⏰ タイマー開始", type="secondary"):
                    st.session_state.start_time = time.time()
                    st.session_state.timer_started = True
                    st.rerun()
            else:
                if st.session_state.start_time:
                    elapsed = time.time() - st.session_state.start_time
                    remaining = max(0, 90*60 - elapsed)  # 90分
                    mins = int(remaining // 60)
                    secs = int(remaining % 60)
                    
                    if remaining > 0:
                        st.metric("⏰ 残り時間", f"{mins:02d}:{secs:02d}")
                    else:
                        st.error("⏰ 時間終了！")
                        st.markdown("制限時間が終了しました。提出してください。")
        
        essay_content = st.text_area(
            "小論文を入力してください",
            value=st.session_state.essay_content,
            height=300,
            placeholder="ここに小論文を入力してください..."
        )
        st.session_state.essay_content = essay_content
        
        char_count = len(essay_content)
        st.write(f"文字数: {char_count}文字")
        
        # 提出バリデーション
        min_chars = 100
        can_submit = char_count >= min_chars
        
        if not can_submit:
            st.warning(f"⚠️ 提出には最低{min_chars}文字必要です（現在: {char_count}文字）")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🤖 Claude詳細評価で提出", type="primary", disabled=not can_submit):
                st.session_state.essay_content = essay_content
                st.session_state.step = 'result'
                st.rerun()
        
        with col2:
            if st.button("💾 下書き保存"):
                st.session_state.essay_content = essay_content
                st.success("✅ 下書きを保存しました")
        
        with col3:
            if st.button("🔄 リセット"):
                st.session_state.essay_content = ""
                st.rerun()
        
        with col4:
            if st.button("❌ 中断"):
                st.session_state.step = 'select'
                st.rerun()
    
    # ステップ4: 結果表示
    elif st.session_state.step == 'result':
        st.header("📊 評価結果")
        
        if st.session_state.essay_result is None:
            with st.spinner("Claude AIが評価中..."):
                result = api_score_essay(
                    st.session_state.essay_content,
                    st.session_state.current_question,
                    st.session_state.selected_university.name,
                    st.session_state.selected_faculty.name
                )
                st.session_state.essay_result = result
        
        result = st.session_state.essay_result
        
        # 総合評価
        st.markdown("### 🎯 総合評価")
        score = result.get("総合得点", 0)
        st.metric("総合得点", f"{score}/100点")
        
        # 詳細評価（2x2グリッド）
        st.markdown("### 📈 詳細評価")
        
        categories = [
            ("構成・組織化", "構成", "🏗️"),
            ("内容・論点", "内容", "💡"),
            ("論理性・一貫性", "論理性", "🔗"),
            ("表現・文章力", "表現", "✨")
        ]
        
        # 2×2のグリッド配置
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        columns = [row1_col1, row1_col2, row2_col1, row2_col2]
        
        for i, (category_name, key, emoji) in enumerate(categories):
            with columns[i]:
                category_data = result.get(key, {})
                score_val = category_data.get("得点", 0)
                evaluation = category_data.get("評価", "評価なし")
                improvement = category_data.get("改善点", "改善点なし")
                
                st.metric(f"{emoji} {category_name}", f"{score_val}/25点")
                
                with st.expander(f"詳細を見る"):
                    st.markdown("**評価:**")
                    st.write(evaluation)
                    st.markdown("**改善点:**")
                    st.write(improvement)
        
        # 総合コメント
        st.markdown("### 💬 総合コメント")
        st.write(result.get("総合評価", "評価を生成できませんでした。"))
        
        # 具体的アドバイス
        st.markdown("### 🎯 具体的改善アドバイス")
        advice_list = result.get("具体的アドバイス", [])
        for i, advice in enumerate(advice_list, 1):
            st.write(f"{i}. {advice}")
        
        # 模範解答
        if st.button("模範解答を確認"):
            with st.spinner("模範解答を生成中..."):
                model_answer = api_generate_model_answer(
                    st.session_state.current_question,
                    st.session_state.selected_university.name,
                    st.session_state.selected_faculty.name
                )
                
                st.markdown("### 📚 模範解答")
                st.write(model_answer)
        
        # リセットボタン
        if st.button("最初からやり直す"):
            for key in ['step', 'selected_university', 'selected_faculty', 'selected_department', 
                       'current_question', 'essay_content', 'essay_result']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()