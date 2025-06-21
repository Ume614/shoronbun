import streamlit as st
import time
from datetime import datetime
from data.universities import get_universities
from data.writing_guides import get_writing_guides
from utils.question_predictor import generate_predicted_question
from utils.essay_scorer import score_essay
from data.models import Essay

# ページ設定
st.set_page_config(
    page_title="総合選抜型入試 小論文対策アプリ",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #4f46e5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton > button:hover {
        background-color: #3730a3;
    }
    .score-card {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin: 0.5rem 0;
    }
    .university-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .question-card {
        background-color: #f1f5f9;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #4f46e5;
        margin: 1rem 0;
    }
    .timer-display {
        font-size: 2rem;
        font-weight: bold;
        color: #dc2626;
        text-align: center;
        padding: 1rem;
        background-color: #fef2f2;
        border-radius: 8px;
        border: 2px solid #fecaca;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'current_state' not in st.session_state:
    st.session_state.current_state = 'selection'
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
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'time_limit' not in st.session_state:
    st.session_state.time_limit = 90
if 'essay_score' not in st.session_state:
    st.session_state.essay_score = None

def reset_state():
    """状態をリセットする"""
    st.session_state.current_state = 'selection'
    st.session_state.selected_university = None
    st.session_state.selected_faculty = None
    st.session_state.selected_department = None
    st.session_state.current_question = None
    st.session_state.essay_content = ""
    st.session_state.start_time = None
    st.session_state.essay_score = None

def main():
    st.title("📝 総合選抜型入試 小論文対策アプリ")
    
    # サイドバー
    with st.sidebar:
        st.header("ナビゲーション")
        
        if st.button("🏠 ホームに戻る"):
            reset_state()
            st.rerun()
        
        if st.button("📖 書き方ガイド"):
            show_writing_guide()
        
        st.markdown("---")
        st.markdown("### 現在の状態")
        
        if st.session_state.current_state == 'selection':
            st.info("🔍 大学・学部選択中")
        elif st.session_state.current_state == 'writing':
            st.info("✍️ 小論文作成中")
        elif st.session_state.current_state == 'result':
            st.info("📊 結果表示中")

    # メインコンテンツ
    if st.session_state.current_state == 'selection':
        show_university_selection()
    elif st.session_state.current_state == 'writing':
        show_essay_editor()
    elif st.session_state.current_state == 'result':
        show_results()

def show_university_selection():
    """大学選択画面"""
    st.header("🎯 大学・学部・学科を選択してください")
    
    universities = get_universities()
    
    # 大学検索
    search_term = st.text_input("🔍 大学名で検索", placeholder="例: 早稲田")
    
    if search_term:
        filtered_universities = [
            uni for uni in universities 
            if search_term.lower() in uni.name.lower()
        ]
    else:
        filtered_universities = universities
    
    if not filtered_universities:
        st.warning("該当する大学が見つかりませんでした。")
        return
    
    # 大学選択
    university_names = [uni.name for uni in filtered_universities]
    selected_uni_name = st.selectbox("📚 大学を選択", ["選択してください"] + university_names)
    
    if selected_uni_name != "選択してください":
        selected_university = next(uni for uni in filtered_universities if uni.name == selected_uni_name)
        st.session_state.selected_university = selected_university
        
        # AO対応学部のフィルタリング
        ao_faculties = [fac for fac in selected_university.faculties if fac.has_ao]
        
        if ao_faculties:
            st.markdown(f"### {selected_university.name} - AO入試対応学部")
            
            faculty_names = [fac.name for fac in ao_faculties]
            selected_fac_name = st.selectbox("🏛️ 学部を選択", ["選択してください"] + faculty_names)
            
            if selected_fac_name != "選択してください":
                selected_faculty = next(fac for fac in ao_faculties if fac.name == selected_fac_name)
                st.session_state.selected_faculty = selected_faculty
                
                # AO対応学科のフィルタリング
                ao_departments = [dept for dept in selected_faculty.departments if dept.has_ao]
                
                if ao_departments:
                    st.markdown(f"### {selected_faculty.name} - AO入試対応学科")
                    
                    dept_names = [dept.name for dept in ao_departments]
                    selected_dept_name = st.selectbox("🎓 学科を選択", ["選択してください"] + dept_names)
                    
                    if selected_dept_name != "選択してください":
                        selected_department = next(dept for dept in ao_departments if dept.name == selected_dept_name)
                        st.session_state.selected_department = selected_department
                        
                        # 過去問題情報表示
                        st.markdown("#### 📊 過去問題情報")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("過去問題数", len(selected_department.past_questions))
                        
                        with col2:
                            if selected_department.past_questions:
                                st.metric("制限時間", f"{selected_department.past_questions[0].time_limit}分")
                        
                        # 過去問題一覧
                        if selected_department.past_questions:
                            st.markdown("#### 📝 過去5年の出題テーマ")
                            for q in selected_department.past_questions:
                                with st.expander(f"{q.year}年度"):
                                    st.write(q.theme)
                        
                        # 練習開始ボタン
                        if st.button("🚀 予想問題で練習を開始", type="primary"):
                            question = generate_predicted_question(
                                selected_department.past_questions,
                                selected_university.name,
                                selected_faculty.name,
                                selected_department.name
                            )
                            st.session_state.current_question = question
                            st.session_state.current_state = 'writing'
                            st.rerun()

def show_essay_editor():
    """小論文エディター画面"""
    if not st.session_state.current_question:
        st.error("問題が設定されていません。")
        return
    
    question = st.session_state.current_question
    
    st.header("✍️ 小論文練習")
    
    # 問題表示
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.markdown("### 📋 出題テーマ")
    st.write(question.theme)
    st.markdown(f"**制限時間:** {question.time_limit}分 | **推奨文字数:** 800-1200字")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # タイマー開始
    if st.session_state.start_time is None:
        if st.button("⏰ タイマーを開始して練習を始める", type="primary"):
            st.session_state.start_time = time.time()
            st.session_state.time_limit = question.time_limit * 60  # 秒に変換
            st.rerun()
        
        st.info("準備ができたら上のボタンを押してタイマーを開始してください。")
        return
    
    # 経過時間とタイマー表示
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, st.session_state.time_limit - elapsed_time)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("経過時間", f"{int(elapsed_time // 60)}:{int(elapsed_time % 60):02d}")
    
    with col2:
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        if remaining_time > 0:
            st.markdown(f'<div class="timer-display">残り {minutes}:{seconds:02d}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="timer-display">時間切れ</div>', unsafe_allow_html=True)
    
    with col3:
        word_count = len(st.session_state.essay_content.replace(' ', '').replace('\n', ''))
        st.metric("文字数", word_count)
    
    # 小論文入力エリア
    if remaining_time > 0:
        essay_content = st.text_area(
            "📝 ここに小論文を書いてください",
            value=st.session_state.essay_content,
            height=400,
            placeholder="ここに小論文を入力してください...",
            key="essay_input"
        )
        st.session_state.essay_content = essay_content
        
        # 提出ボタン
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📤 提出する", type="primary", disabled=word_count < 100):
                submit_essay()
        
        with col2:
            if st.button("❌ 中断して戻る"):
                reset_state()
                st.rerun()
        
        if word_count < 100:
            st.warning(f"提出するには最低100文字必要です（現在: {word_count}文字）")
        
        # 書き方のヒント
        with st.expander("💡 書き方のヒント"):
            st.markdown("""
            - **序論**: 問題提起と自分の立場を明確に
            - **本論**: 根拠と具体例を用いて論証
            - **結論**: 主張をまとめ、今後の展望を示す
            - **反対意見**: にも言及し、多角的な視点を示す
            """)
    
    else:
        # 時間切れの場合は自動提出
        st.error("⏰ 制限時間が終了しました。自動的に提出されます。")
        if st.session_state.essay_content.strip():
            submit_essay()
        else:
            st.warning("内容が入力されていません。")

def submit_essay():
    """小論文を提出して採点"""
    if not st.session_state.essay_content.strip():
        st.error("小論文が入力されていません。")
        return
    
    # 採点実行
    score = score_essay(st.session_state.essay_content, st.session_state.current_question.theme)
    st.session_state.essay_score = score
    
    # 結果画面に移行
    st.session_state.current_state = 'result'
    st.rerun()

def show_results():
    """結果表示画面"""
    if not st.session_state.essay_score:
        st.error("採点結果がありません。")
        return
    
    score = st.session_state.essay_score
    question = st.session_state.current_question
    
    st.header("📊 採点結果")
    
    # 総合スコア表示
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 総合評価")
        
        # スコアバー
        score_percentage = score.total / 100
        st.metric("総合点数", f"{score.total}/100点")
        st.progress(score_percentage)
        
        # 評価グレード
        if score.total >= 90:
            grade = "A"
            grade_color = "#22c55e"
        elif score.total >= 80:
            grade = "B"
            grade_color = "#eab308"
        elif score.total >= 70:
            grade = "C"
            grade_color = "#f97316"
        elif score.total >= 60:
            grade = "D"
            grade_color = "#ef4444"
        else:
            grade = "F"
            grade_color = "#dc2626"
        
        st.markdown(f"<h2 style='color: {grade_color}'>評価: {grade}</h2>", unsafe_allow_html=True)
    
    with col2:
        # 各項目の詳細スコア
        st.markdown("### 📈 詳細スコア")
        
        scores = [
            ("構成", score.structure, 25),
            ("内容", score.content, 30),
            ("論理性", score.logic, 25),
            ("表現", score.expression, 20)
        ]
        
        for name, score_value, max_score in scores:
            percentage = score_value / max_score
            st.metric(name, f"{score_value}/{max_score}")
            st.progress(percentage)
    
    # フィードバック
    st.markdown("### 💬 評価コメント")
    st.info(score.feedback)
    
    # 改善提案
    if score.suggestions:
        st.markdown("### 💡 改善のアドバイス")
        for i, suggestion in enumerate(score.suggestions, 1):
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
    
    with col2:
        st.markdown("### 🏫 問題情報")
        st.write(f"**大学:** {question.university}")
        st.write(f"**学部:** {question.faculty}")
        st.write(f"**学科:** {question.department}")
    
    # 解答内容表示
    with st.expander("📄 あなたの解答を確認"):
        st.markdown("#### 出題テーマ")
        st.write(question.theme)
        st.markdown("#### 解答内容")
        st.write(st.session_state.essay_content)
    
    # アクションボタン
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 同じ問題をもう一度", type="secondary"):
            st.session_state.current_state = 'writing'
            st.session_state.essay_content = ""
            st.session_state.start_time = None
            st.session_state.essay_score = None
            st.rerun()
    
    with col2:
        if st.button("🆕 新しい問題に挑戦", type="primary"):
            reset_state()
            st.rerun()

def show_writing_guide():
    """書き方ガイドをモーダル風に表示"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📖 小論文書き方ガイド")
    
    guides = get_writing_guides()
    categories = {
        'structure': '📋 構成',
        'content': '💡 内容',
        'expression': '✏️ 表現',
        'examples': '📝 例文'
    }
    
    selected_category = st.sidebar.selectbox(
        "カテゴリを選択",
        list(categories.keys()),
        format_func=lambda x: categories[x]
    )
    
    # 選択されたカテゴリのガイドを表示
    category_guides = [g for g in guides if g.category == selected_category]
    
    for guide in category_guides:
        with st.sidebar.expander(guide.title):
            st.markdown(guide.content)

if __name__ == "__main__":
    main()