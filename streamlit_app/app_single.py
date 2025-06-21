import streamlit as st
import time
import random
import re
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

# データクラス定義
@dataclass
class PastQuestion:
    id: str
    year: int
    theme: str
    time_limit: int  # minutes
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

@dataclass
class PredictedQuestion:
    id: str
    theme: str
    time_limit: int
    generated_at: datetime
    based_on_questions: List[str]  # past question IDs
    university: str
    faculty: str
    department: str

@dataclass
class Essay:
    id: str
    content: str
    submitted_at: datetime
    time_spent: int  # seconds
    question: PredictedQuestion

@dataclass
class EssayScore:
    total: int
    structure: int
    content: int
    logic: int
    expression: int
    feedback: str
    suggestions: List[str]

@dataclass
class WritingGuide:
    id: str
    title: str
    content: str
    category: str  # 'structure', 'content', 'expression', 'examples'

# 大学データ
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
                                ),
                                PastQuestion(
                                    id='waseda-pol-2021',
                                    year=2021,
                                    theme='コロナ禍を通じて見えた現代社会の課題と、その解決策について論じなさい。',
                                    time_limit=90,
                                    university='早稲田大学',
                                    faculty='政治経済学部',
                                    department='政治学科'
                                ),
                                PastQuestion(
                                    id='waseda-pol-2020',
                                    year=2020,
                                    theme='持続可能な社会の実現に向けて、政治が果たすべき役割について論じなさい。',
                                    time_limit=90,
                                    university='早稲田大学',
                                    faculty='政治経済学部',
                                    department='政治学科'
                                ),
                                PastQuestion(
                                    id='waseda-pol-2019',
                                    year=2019,
                                    theme='人工知能の発達が社会に与える影響と、それに対する政策の在り方について論じなさい。',
                                    time_limit=90,
                                    university='早稲田大学',
                                    faculty='政治経済学部',
                                    department='政治学科'
                                )
                            ]
                        ),
                        Department(
                            id='economics',
                            name='経済学科',
                            has_ao=True,
                            past_questions=[
                                PastQuestion(
                                    id='waseda-econ-2023',
                                    year=2023,
                                    theme='日本経済の持続的成長に向けた課題と解決策について論じなさい。',
                                    time_limit=90,
                                    university='早稲田大学',
                                    faculty='政治経済学部',
                                    department='経済学科'
                                )
                            ]
                        )
                    ]
                ),
                Faculty(
                    id='law',
                    name='法学部',
                    has_ao=True,
                    departments=[
                        Department(
                            id='law',
                            name='法学科',
                            has_ao=True,
                            past_questions=[
                                PastQuestion(
                                    id='waseda-law-2023',
                                    year=2023,
                                    theme='法の支配と民主主義の関係について、現代社会の具体例を挙げて論じなさい。',
                                    time_limit=90,
                                    university='早稲田大学',
                                    faculty='法学部',
                                    department='法学科'
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

# 問題予想機能
def generate_predicted_question(
    past_questions: List[PastQuestion],
    university: str,
    faculty: str,
    department: str
) -> PredictedQuestion:
    """過去問題データから次年度の予想問題を生成"""
    
    time_limit = past_questions[0].time_limit if past_questions else 90
    
    current_trends = [
        'デジタル化',
        'AI・人工知能',
        '持続可能性',
        'グローバル化',
        '多様性と包摂',
        '少子高齢化',
        '環境問題',
        '働き方改革',
        'コロナ後の社会',
        'イノベーション'
    ]

    subject_contexts = {
        '政治': ['民主主義', '政策', '国際関係', '社会制度', '公共政策'],
        '経済': ['経済成長', '市場', '金融', 'グローバル経済', '産業構造'],
        '法': ['法の支配', '人権', '司法制度', '国際法', '社会規範'],
        '文学': ['表現', '文化', 'コミュニケーション', '芸術', '言語'],
        '教育': ['学習', '人材育成', '教育制度', '知識社会', '生涯学習'],
        '医学': ['健康', '医療技術', '予防医学', '高齢化', '医療倫理'],
        '工学': ['技術革新', 'ものづくり', '環境技術', 'インフラ', 'デザイン'],
        '理学': ['科学技術', '研究', '発見', '自然科学', 'データサイエンス']
    }

    def get_relevant_contexts(faculty_name: str, department_name: str) -> List[str]:
        contexts = []
        
        for key, values in subject_contexts.items():
            if key in faculty_name or key in department_name:
                contexts.extend(values)
        
        return contexts if contexts else ['社会', '現代', '課題', '解決策', '将来']

    relevant_contexts = get_relevant_contexts(faculty, department)
    
    trend_keyword = random.choice(current_trends)
    context_keyword = random.choice(relevant_contexts)
    
    question_templates = [
        f"{trend_keyword}が進む現代において、{context_keyword}はどのような課題に直面し、どのような解決策が考えられるか、具体例を挙げて論じなさい。",
        f"{trend_keyword}の発展が{context_keyword}に与える影響について、メリットとデメリットを比較検討し、今後の在り方を論じなさい。",
        f"現代社会における{trend_keyword}の重要性を踏まえ、{context_keyword}の分野でどのような革新が必要か、あなたの考えを述べなさい。",
        f"{trend_keyword}を背景とした社会変化の中で、{context_keyword}が果たすべき役割と課題について論じなさい。",
        f"{trend_keyword}と{context_keyword}の関係性を分析し、持続可能な社会の実現に向けた提言を行いなさい。"
    ]

    selected_template = random.choice(question_templates)

    return PredictedQuestion(
        id=f"predicted-{int(datetime.now().timestamp())}",
        theme=selected_template,
        time_limit=time_limit,
        generated_at=datetime.now(),
        based_on_questions=[q.id for q in past_questions],
        university=university,
        faculty=faculty,
        department=department
    )

# 採点機能
def score_essay(content: str, theme: str) -> EssayScore:
    """小論文の採点を行う"""
    
    word_count = len(content.replace(' ', '').replace('\n', ''))
    paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
    
    structure_score = 0
    content_score = 0
    logic_score = 0
    expression_score = 0
    
    feedback = []
    suggestions = []

    # 文字数チェック
    if word_count < 100:
        feedback.append('文字数が不足しています。より詳細な論述が必要です。')
        suggestions.append('具体例や根拠を追加して、論述を充実させてください。')
    elif word_count > 1200:
        feedback.append('文字数が多すぎます。要点を絞って簡潔に論述してください。')
        suggestions.append('重要なポイントに焦点を当て、冗長な表現を削除してください。')

    # 構成評価
    if len(paragraphs) >= 3:
        structure_score += 15
        feedback.append('適切な段落構成が確認できます。')
    else:
        structure_score += 5
        feedback.append('段落構成を改善する必要があります。序論・本論・結論の構成を意識してください。')
        suggestions.append('序論で問題提起、本論で論証、結論でまとめという構成を心がけてください。')

    # 序論・結論の確認
    has_introduction = any(keyword in content for keyword in ['について', 'において', 'に関して'])
    has_conclusion = any(keyword in content for keyword in ['よって', '従って', '以上', 'このように'])
    
    if has_introduction:
        structure_score += 5
    else:
        suggestions.append('序論で明確な問題提起を行ってください。')
    
    if has_conclusion:
        structure_score += 5
    else:
        suggestions.append('結論部分で自分の主張を明確にまとめてください。')

    # 内容評価
    has_examples = any(keyword in content for keyword in ['例えば', '具体的に', 'たとえば'])
    has_data = bool(re.search(r'\d+%|\d+人|\d+件|\d+年', content))
    
    if has_examples:
        content_score += 10
        feedback.append('具体例が適切に使用されています。')
    else:
        suggestions.append('具体例を挙げて論証を強化してください。')
    
    if has_data:
        content_score += 10
        feedback.append('データや数値を用いた客観的な論証が見られます。')
    else:
        suggestions.append('可能であれば、統計データや数値を用いて論証を補強してください。')

    # 反対意見への言及
    has_counter_argument = any(keyword in content for keyword in ['一方', 'しかし', 'ただし', 'もっとも'])
    if has_counter_argument:
        content_score += 5
        logic_score += 10
        feedback.append('反対意見への言及が見られ、多角的な視点が示されています。')
    else:
        suggestions.append('反対意見にも触れ、より多角的な論述を心がけてください。')

    # 論理性評価
    logical_connectors = ['そのため', 'なぜなら', '理由は', 'その結果', 'このことから']
    connector_count = sum(content.count(connector) for connector in logical_connectors)
    
    if connector_count >= 2:
        logic_score += 15
        feedback.append('論理的な接続詞が適切に使用されています。')
    else:
        logic_score += 5
        suggestions.append('「そのため」「なぜなら」などの接続詞を使って論理的な流れを明確にしてください。')

    # 表現評価
    # 重複表現のチェック
    repetitive_patterns = re.findall(r'(.{10,})\1', content)
    if repetitive_patterns and len(repetitive_patterns) > 2:
        expression_score += 5
        feedback.append('表現に重複が見られます。より多様な表現を心がけてください。')
    else:
        expression_score += 15

    # 文章の長さ評価
    complex_sentences = re.findall(r'[。]{1}[^。]{50,}', content)
    if complex_sentences:
        expression_score += 10
        feedback.append('文章の長さが適切で読みやすい構成です。')
    else:
        suggestions.append('文章の長さを調整し、読みやすさを向上させてください。')

    # ボーナス点
    if 400 <= word_count <= 800:
        content_score += 5
    if len(paragraphs) >= 4:
        structure_score += 5
    if theme[:10] in content:
        content_score += 5

    # 上限設定
    structure_score = min(structure_score, 25)
    content_score = min(content_score, 30)
    logic_score = min(logic_score, 25)
    expression_score = min(expression_score, 20)

    total = structure_score + content_score + logic_score + expression_score

    # 総合評価
    if total >= 90:
        feedback.append('非常に優秀な小論文です。論理構成、内容、表現ともに高いレベルです。')
    elif total >= 75:
        feedback.append('良好な小論文です。いくつかの改善点はありますが、全体的に評価できます。')
    elif total >= 60:
        feedback.append('基本的な要素は満たしていますが、さらなる改善が必要です。')
    else:
        feedback.append('大幅な改善が必要です。構成と論証を見直してください。')

    return EssayScore(
        total=total,
        structure=structure_score,
        content=content_score,
        logic=logic_score,
        expression=expression_score,
        feedback=' '.join(feedback),
        suggestions=suggestions
    )

# 書き方ガイド
def get_writing_guides():
    return [
        WritingGuide(
            id='structure-1',
            title='小論文の基本構成',
            category='structure',
            content="""小論文の基本構成は以下の通りです：

1. **序論（導入部）**
   - 問題提起
   - 論点の明確化
   - 自分の立場の表明

2. **本論（展開部）**
   - 根拠の提示
   - 具体例・データの活用
   - 反対意見への言及と反駁

3. **結論（まとめ部）**
   - 論点の整理
   - 自分の主張の再確認
   - 今後の展望や提言

各部分の配分は、序論20%、本論60%、結論20%程度が理想的です。"""
        ),
        WritingGuide(
            id='structure-2',
            title='論理的な文章構成のコツ',
            category='structure',
            content="""論理的な文章を書くためのポイント：

1. **PREP法の活用**
   - Point（結論）
   - Reason（理由）
   - Example（具体例）
   - Point（結論の再確認）

2. **接続詞の効果的な使用**
   - 順接：そのため、従って、よって
   - 逆接：しかし、ところが、一方で
   - 添加：また、さらに、加えて

3. **段落の役割を明確に**
   - 一つの段落には一つの論点
   - 段落の冒頭で主張を明示
   - 段落間の関係性を意識"""
        ),
        WritingGuide(
            id='content-1',
            title='説得力のある論拠の作り方',
            category='content',
            content="""説得力のある論拠を構築するために：

1. **データ・統計の活用**
   - 信頼できるソースからの数値
   - 比較可能なデータの提示
   - トレンドや変化の明示

2. **具体例の選択**
   - 身近で理解しやすい事例
   - 複数の視点からの事例
   - 時事的な話題の活用

3. **専門家の意見**
   - 権威ある研究者の見解
   - 複数の専門分野からの観点
   - 最新の研究成果の反映"""
        ),
        WritingGuide(
            id='expression-1',
            title='適切な表現と文体',
            category='expression',
            content="""小論文に適した表現技法：

1. **文体の統一**
   - 敬語は使わず、丁寧語で統一
   - 「である調」で書く
   - 一人称は「私」を使用

2. **避けるべき表現**
   - 感情的な表現
   - 曖昧な表現（「〜と思う」「〜かもしれない」）
   - 極端な断定（「絶対に」「必ず」）

3. **効果的な表現技法**
   - 比喩や例え話の活用
   - 問いかけによる読者の関心喚起
   - 対比による論点の明確化"""
        )
    ]

# Streamlitアプリ
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
    """書き方ガイドをサイドバーに表示"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📖 小論文書き方ガイド")
    
    guides = get_writing_guides()
    categories = {
        'structure': '📋 構成',
        'content': '💡 内容',
        'expression': '✏️ 表現'
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