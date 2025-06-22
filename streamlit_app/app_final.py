import streamlit as st
import time
import random
import re
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

# ページ設定
st.set_page_config(
    page_title="総合選抜型入試 小論文対策アプリ",
    page_icon="📝",
    layout="wide"
)

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
@st.cache_data
def get_universities():
    return [
        University(
            id='waseda',
            name='早稲田大学',
            faculties=[
                Faculty(
                    id='political-science',
                    name='政治経済学部',
                    has_ao=True,
                    departments=[
                        Department(
                            id='politics',
                            name='政治学科',
                            has_ao=True,
                            past_questions=[
                                PastQuestion(
                                    id='waseda-pol-2023',
                                    year=2023,
                                    theme='デジタル社会における民主主義の課題と可能性について、具体例を挙げて論じなさい。',
                                    time_limit=90,
                                    university='早稲田大学',
                                    faculty='政治経済学部',
                                    department='政治学科'
                                ),
                                PastQuestion(
                                    id='waseda-pol-2022',
                                    year=2022,
                                    theme='グローバル化が進む現代において、国家の役割はどのように変化すべきか論じなさい。',
                                    time_limit=90,
                                    university='早稲田大学',
                                    faculty='政治経済学部',
                                    department='政治学科'
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        University(
            id='keio',
            name='慶應義塾大学',
            faculties=[
                Faculty(
                    id='economics',
                    name='経済学部',
                    has_ao=True,
                    departments=[
                        Department(
                            id='economics',
                            name='経済学科',
                            has_ao=True,
                            past_questions=[
                                PastQuestion(
                                    id='keio-econ-2023',
                                    year=2023,
                                    theme='デジタル化が進む現代において、経済活動はどのように変化すべきか論じなさい。',
                                    time_limit=90,
                                    university='慶應義塾大学',
                                    faculty='経済学部',
                                    department='経済学科'
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        University(
            id='todai',
            name='東京大学',
            faculties=[
                Faculty(
                    id='liberal-arts',
                    name='教養学部',
                    has_ao=True,
                    departments=[
                        Department(
                            id='liberal-arts',
                            name='教養学科',
                            has_ao=True,
                            past_questions=[
                                PastQuestion(
                                    id='todai-liberal-2023',
                                    year=2023,
                                    theme='多様性と包摂性が求められる現代社会において、教育の果たすべき役割について論じなさい。',
                                    time_limit=120,
                                    university='東京大学',
                                    faculty='教養学部',
                                    department='教養学科'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]

# 採点機能
def score_essay(content: str) -> dict:
    """採点機能"""
    if not content.strip():
        return {
            "total": 0,
            "structure": 0,
            "content": 0,
            "logic": 0,
            "expression": 0,
            "feedback": "文章が入力されていません。",
            "suggestions": ["文章を入力してください。"]
        }
    
    word_count = len(content.replace(' ', '').replace('\n', ''))
    paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
    
    structure_score = 0
    content_score = 0
    logic_score = 0
    expression_score = 0
    suggestions = []
    
    # 文字数評価
    if word_count >= 400:
        content_score += 15
    elif word_count >= 200:
        content_score += 10
    elif word_count >= 100:
        content_score += 5
    else:
        suggestions.append("文字数を増やしてください（400文字以上推奨）")
    
    # 段落構成評価
    if len(paragraphs) >= 3:
        structure_score += 15
    else:
        structure_score += 5
        suggestions.append("段落を増やして構成を明確にしてください")
    
    # キーワード評価
    if any(keyword in content for keyword in ['例えば', '具体的に', 'たとえば']):
        content_score += 10
    else:
        suggestions.append("具体例を追加してください")
    
    if any(keyword in content for keyword in ['しかし', '一方', 'ただし']):
        logic_score += 10
    else:
        suggestions.append("反対意見も考慮してください")
    
    if any(keyword in content for keyword in ['そのため', 'なぜなら', 'このように']):
        logic_score += 10
    else:
        suggestions.append("論理的接続詞を使用してください")
    
    # 表現評価
    if word_count >= 300:
        expression_score += 10
    
    # 合計スコア計算
    structure_score = min(structure_score, 25)
    content_score = min(content_score, 30)
    logic_score = min(logic_score, 25)
    expression_score = min(expression_score, 20)
    
    total = structure_score + content_score + logic_score + expression_score
    
    # フィードバック生成
    if total >= 80:
        feedback = "優秀な小論文です！"
    elif total >= 60:
        feedback = "良好な小論文です。"
    elif total >= 40:
        feedback = "基本的な要素はありますが、改善が必要です。"
    else:
        feedback = "大幅な改善が必要です。"
    
    return {
        "total": total,
        "structure": structure_score,
        "content": content_score,
        "logic": logic_score,
        "expression": expression_score,
        "feedback": feedback,
        "suggestions": suggestions
    }

# 問題予想機能
def generate_question(past_questions: List[PastQuestion], university: str, faculty: str, department: str) -> str:
    """問題生成"""
    trends = ['デジタル化', 'AI', '持続可能性', 'グローバル化', '多様性', '環境問題']
    contexts = ['社会', '経済', '政治', '教育', '技術', '文化']
    
    trend = random.choice(trends)
    context = random.choice(contexts)
    
    templates = [
        f"{trend}が進む現代において、{context}分野での課題と解決策について論じなさい。",
        f"{trend}の発展が{context}に与える影響について述べなさい。",
        f"{trend}と{context}の関係性について、あなたの考えを論じなさい。"
    ]
    
    return random.choice(templates)

# メイン関数
def main():
    st.title("📝 総合選抜型入試 小論文対策アプリ")
    
    # セッション状態の初期化
    if 'page' not in st.session_state:
        st.session_state.page = 'selection'
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
    if 'essay_score' not in st.session_state:
        st.session_state.essay_score = None
    if 'timer_started' not in st.session_state:
        st.session_state.timer_started = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    
    # サイドバー
    with st.sidebar:
        st.header("ナビゲーション")
        
        if st.button("🏠 ホームに戻る", key="home_btn"):
            reset_all_state()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 現在の状態")
        
        if st.session_state.page == 'selection':
            st.info("🔍 大学・学部選択中")
        elif st.session_state.page == 'writing':
            st.info("✍️ 小論文作成中")
        elif st.session_state.page == 'result':
            st.info("📊 結果表示中")
    
    # メインコンテンツ
    if st.session_state.page == 'selection':
        show_university_selection()
    elif st.session_state.page == 'writing':
        show_essay_editor()
    elif st.session_state.page == 'result':
        show_results()

def reset_all_state():
    """全セッション状態をリセット"""
    st.session_state.page = 'selection'
    st.session_state.selected_university = None
    st.session_state.selected_faculty = None
    st.session_state.selected_department = None
    st.session_state.current_question = None
    st.session_state.essay_content = ""
    st.session_state.essay_score = None
    st.session_state.timer_started = False
    st.session_state.start_time = None

def show_university_selection():
    """大学選択画面"""
    st.header("🎯 大学・学部・学科を選択してください")
    
    universities = get_universities()
    
    # 大学選択
    university_options = ["選択してください"] + [uni.name for uni in universities]
    selected_uni_name = st.selectbox("📚 大学を選択", university_options, key="uni_select")
    
    if selected_uni_name != "選択してください":
        selected_university = next(uni for uni in universities if uni.name == selected_uni_name)
        st.session_state.selected_university = selected_university
        
        # 学部選択
        ao_faculties = [fac for fac in selected_university.faculties if fac.has_ao]
        faculty_options = ["選択してください"] + [fac.name for fac in ao_faculties]
        selected_fac_name = st.selectbox("🏛️ 学部を選択", faculty_options, key="fac_select")
        
        if selected_fac_name != "選択してください":
            selected_faculty = next(fac for fac in ao_faculties if fac.name == selected_fac_name)
            st.session_state.selected_faculty = selected_faculty
            
            # 学科選択
            ao_departments = [dept for dept in selected_faculty.departments if dept.has_ao]
            dept_options = ["選択してください"] + [dept.name for dept in ao_departments]
            selected_dept_name = st.selectbox("🎓 学科を選択", dept_options, key="dept_select")
            
            if selected_dept_name != "選択してください":
                selected_department = next(dept for dept in ao_departments if dept.name == selected_dept_name)
                st.session_state.selected_department = selected_department
                
                # 過去問題情報
                st.markdown("#### 📊 過去問題情報")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("過去問題数", len(selected_department.past_questions))
                
                with col2:
                    if selected_department.past_questions:
                        st.metric("制限時間", f"{selected_department.past_questions[0].time_limit}分")
                
                # 過去問題一覧
                if selected_department.past_questions:
                    st.markdown("#### 📝 過去の出題テーマ")
                    for q in selected_department.past_questions:
                        with st.expander(f"{q.year}年度"):
                            st.write(q.theme)
                
                # 練習開始ボタン
                if st.button("🚀 予想問題で練習を開始", type="primary", key="start_btn"):
                    question = generate_question(
                        selected_department.past_questions,
                        selected_university.name,
                        selected_faculty.name,
                        selected_department.name
                    )
                    st.session_state.current_question = question
                    st.session_state.page = 'writing'
                    st.rerun()

def show_essay_editor():
    """小論文エディター画面"""
    if not st.session_state.current_question:
        st.error("問題が設定されていません。")
        return
    
    st.header("✍️ 小論文練習")
    
    # 問題表示
    st.markdown("### 📋 出題テーマ")
    st.info(st.session_state.current_question)
    st.markdown("**制限時間:** 90分 | **推奨文字数:** 400-800字")
    
    # タイマー管理（簡素化）
    if not st.session_state.timer_started:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏰ タイマーを開始", type="primary", key="timer_start_btn"):
                st.session_state.timer_started = True
                st.session_state.start_time = time.time()
                st.success("タイマーを開始しました！")
                st.rerun()
        
        with col2:
            if st.button("⏱️ タイマーなしで開始", key="no_timer_btn"):
                st.session_state.timer_started = True
                st.session_state.start_time = None
                st.info("タイマーなしで開始しました。")
                st.rerun()
        
        st.info("⚠️ Streamlit Cloudではタイマーが正確に動作しない場合があります。「タイマーなしで開始」を推奨します。")
        return
    
    # タイマー表示（手動更新）
    if st.session_state.start_time:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 時間を更新", key="update_timer"):
                st.rerun()
        
        with col2:
            elapsed_time = time.time() - st.session_state.start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            st.metric("経過時間", f"{minutes}:{seconds:02d}")
        
        with col3:
            remaining_time = max(0, 90 * 60 - elapsed_time)
            if remaining_time > 0:
                r_minutes = int(remaining_time // 60)
                r_seconds = int(remaining_time % 60)
                st.metric("残り時間", f"{r_minutes}:{r_seconds:02d}")
            else:
                st.metric("残り時間", "終了")
                st.warning("⏰ 制限時間が終了しました！")
    else:
        st.info("⏱️ タイマーなしモードで練習中")
    
    # 小論文入力
    essay_content = st.text_area(
        "📝 ここに小論文を書いてください",
        value=st.session_state.essay_content,
        height=400,
        placeholder="ここに小論文を入力してください...",
        key="essay_textarea"
    )
    
    # 文字数カウント（手動更新）
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 文字数を更新", key="update_count"):
            st.session_state.essay_content = essay_content
            st.rerun()
    
    with col2:
        current_content = essay_content if essay_content else st.session_state.essay_content
        word_count = len(current_content.replace(' ', '').replace('\n', ''))
        st.metric("文字数", word_count)
    
    # 内容を保存
    st.session_state.essay_content = essay_content
    
    # 提出条件の表示
    min_chars = 50
    can_submit = word_count >= min_chars
    
    if not can_submit:
        st.warning(f"⚠️ 提出するには最低{min_chars}文字必要です（現在: {word_count}文字）")
        st.info("「文字数を更新」ボタンを押して文字数を確認してください。")
    
    # ボタン
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤 提出する", type="primary", disabled=not can_submit, key="submit_btn"):
            st.session_state.essay_content = essay_content  # 最新の内容を保存
            st.session_state.page = 'result'
            st.rerun()
    
    with col2:
        if st.button("💾 下書き保存", key="save_btn"):
            st.session_state.essay_content = essay_content
            st.success("下書きを保存しました！")
    
    with col3:
        if st.button("❌ 中断して戻る", key="cancel_btn"):
            reset_all_state()
            st.rerun()
    
    # 書き方のヒント
    with st.expander("💡 書き方のヒント"):
        st.markdown("""
        - **序論**: 問題提起と自分の立場を明確に（全体の20%）
        - **本論**: 根拠と具体例を用いて論証（全体の60%）
        - **結論**: 主張をまとめ、今後の展望を示す（全体の20%）
        - **反対意見**: にも言及し、多角的な視点を示す
        - **具体例**: 「例えば」「具体的に」などを使用
        - **論理的接続**: 「そのため」「なぜなら」「このように」を活用
        """)

def show_results():
    """結果表示画面"""
    st.header("📊 採点結果")
    
    # 採点実行
    if st.session_state.essay_score is None:
        with st.spinner("採点中..."):
            st.session_state.essay_score = score_essay(st.session_state.essay_content)
    
    score = st.session_state.essay_score
    
    # 総合スコア表示
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 総合評価")
        st.metric("総合点数", f"{score['total']}/100点")
        st.progress(score['total'] / 100)
        
        # 評価グレード
        if score['total'] >= 80:
            grade, color = "A", "#22c55e"
        elif score['total'] >= 60:
            grade, color = "B", "#eab308"
        elif score['total'] >= 40:
            grade, color = "C", "#f97316"
        else:
            grade, color = "D", "#ef4444"
        
        st.markdown(f"<h2 style='color: {color}'>評価: {grade}</h2>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📈 詳細スコア")
        scores = [
            ("構成", score['structure'], 25),
            ("内容", score['content'], 30),
            ("論理性", score['logic'], 25),
            ("表現", score['expression'], 20)
        ]
        
        for name, value, max_val in scores:
            st.metric(name, f"{value}/{max_val}")
            if max_val > 0:
                st.progress(value / max_val)
    
    # フィードバック
    st.markdown("### 💬 評価コメント")
    st.info(score['feedback'])
    
    # 改善提案
    if score['suggestions']:
        st.markdown("### 💡 改善のアドバイス")
        for i, suggestion in enumerate(score['suggestions'], 1):
            st.markdown(f"{i}. {suggestion}")
    
    # 作成情報
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 作成情報")
        word_count = len(st.session_state.essay_content.replace(' ', '').replace('\n', ''))
        st.write(f"**文字数:** {word_count}文字")
        
        if st.session_state.start_time:
            elapsed_time = time.time() - st.session_state.start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            st.write(f"**所要時間:** {minutes}分{seconds}秒")
        else:
            st.write("**所要時間:** タイマー未使用")
    
    with col2:
        st.markdown("### 🏫 問題情報")
        if st.session_state.selected_university:
            st.write(f"**大学:** {st.session_state.selected_university.name}")
            st.write(f"**学部:** {st.session_state.selected_faculty.name}")
            st.write(f"**学科:** {st.session_state.selected_department.name}")
    
    # 解答表示
    with st.expander("📄 あなたの解答を確認"):
        st.markdown("#### 出題テーマ")
        st.write(st.session_state.current_question)
        st.markdown("#### 解答内容")
        st.write(st.session_state.essay_content)
    
    # アクションボタン
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 同じ問題をもう一度", key="retry_btn"):
            st.session_state.page = 'writing'
            st.session_state.essay_content = ""
            st.session_state.essay_score = None
            st.session_state.timer_started = False
            st.session_state.start_time = None
            st.rerun()
    
    with col2:
        if st.button("🆕 新しい問題に挑戦", type="primary", key="new_btn"):
            reset_all_state()
            st.rerun()

if __name__ == "__main__":
    main()