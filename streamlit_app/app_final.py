import streamlit as st
import time
import random
import re
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

# ページ設定
st.set_page_config(
    page_title="総合選抜型入試 小論文対策アプリ（2026年度入試対応）",
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
            id='showa-women',
            name='昭和女子大学',
            faculties=[
                Faculty(
                    id='international',
                    name='国際学部',
                    has_ao=True,
                    departments=[
                        Department(
                            id='international-studies',
                            name='国際教養学科',
                            has_ao=True,
                            past_questions=[
                                PastQuestion(
                                    id='showa-international-2023',
                                    year=2023,
                                    theme='女性のグローバルリーダーシップについて、現代社会の課題と関連づけて論じなさい。',
                                    time_limit=90,
                                    university='昭和女子大学',
                                    faculty='国際学部',
                                    department='国際教養学科'
                                ),
                                PastQuestion(
                                    id='showa-international-2022',
                                    year=2022,
                                    theme='持続可能な国際協力の在り方について述べなさい。',
                                    time_limit=90,
                                    university='昭和女子大学',
                                    faculty='国際学部',
                                    department='国際教養学科'
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        University(
            id='jissen-women',
            name='実践女子大学',
            faculties=[
                Faculty(
                    id='international',
                    name='国際学部',
                    has_ao=True,
                    departments=[
                        Department(
                            id='international-studies',
                            name='国際学科',
                            has_ao=True,
                            past_questions=[
                                PastQuestion(
                                    id='jissen-international-2023',
                                    year=2023,
                                    theme='実践的な国際協力の在り方について、具体的な事例を挙げて論じなさい。',
                                    time_limit=90,
                                    university='実践女子大学',
                                    faculty='国際学部',
                                    department='国際学科'
                                ),
                                PastQuestion(
                                    id='jissen-international-2022',
                                    year=2022,
                                    theme='女性の国際的な活躍と社会貢献について述べなさい。',
                                    time_limit=90,
                                    university='実践女子大学',
                                    faculty='国際学部',
                                    department='国際学科'
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        University(
            id='waseda-new',
            name='早稲田大学',
            faculties=[
                Faculty(
                    id='sport-science',
                    name='スポーツ科学部',
                    has_ao=True,
                    departments=[
                        Department(
                            id='sport-science',
                            name='スポーツ科学科',
                            has_ao=True,
                            past_questions=[
                                PastQuestion(
                                    id='waseda-sport-2023',
                                    year=2023,
                                    theme='スポーツが社会に果たす役割について、現代社会の課題と関連づけて論じなさい。',
                                    time_limit=90,
                                    university='早稲田大学',
                                    faculty='スポーツ科学部',
                                    department='スポーツ科学科'
                                ),
                                PastQuestion(
                                    id='waseda-sport-2022',
                                    year=2022,
                                    theme='デジタル技術の発展がスポーツに与える影響と可能性について述べなさい。',
                                    time_limit=90,
                                    university='早稲田大学',
                                    faculty='スポーツ科学部',
                                    department='スポーツ科学科'
                                )
                            ]
                        )
                    ]
                ),
            ]
        ),
        University(
            id='rikkyo',
            name='立教大学',
            faculties=[
                Faculty(
                    id='sport-wellness',
                    name='スポーツウェルネス学部',
                    has_ao=True,
                    departments=[
                        Department(
                            id='sport-wellness',
                            name='スポーツウェルネス学科',
                            has_ao=True,
                            past_questions=[
                                PastQuestion(
                                    id='rikkyo-wellness-2025',
                                    year=2025,
                                    theme='【長文読解型】エスノメソドロジーについて論じた文章を読み、問1「エスノメソドロジー」について文章の論旨に沿ってまとめなさい（200字前後）、問2「エスノメソドロジー」の見方を異文化コミュニケーション研究でも適用できるかを考察し述べなさい（800字前後）',
                                    time_limit=90,
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

# AI評価シミュレーション（基本版）
def simulate_ai_evaluation(content: str, theme: str, university: str, faculty: str) -> dict:
    """AI風の詳細評価を生成（基本版）"""
    import random
    
    word_count = len(content.replace(' ', '').replace('\n', ''))
    paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
    
    # AIらしい詳細分析
    structure_patterns = [
        f"序論で「{content[:20]}...」として問題提起していますが、より具体的な社会的背景を示すと効果的です。",
        f"段落構成は{len(paragraphs)}段落となっていますが、論点ごとの整理をより明確にすべきです。",
        f"結論部分の「{content[-30:]}...」は主張の再確認ができていますが、将来への展望も加えるべきです。"
    ]
    
    content_patterns = [
        f"{faculty}の専門性を活かした視点として、国際的な比較事例を追加することを推奨します。",
        f"「{random.choice(['AI', 'デジタル化', 'グローバル化'])}」について言及していますが、具体的なデータや統計を引用すると説得力が増します。",
        f"現在の記述は一般論に留まっているため、{university}の理念と関連付けた独自の視点を加えるべきです。"
    ]
    
    logic_patterns = [
        f"論理的接続として「{'、'.join(random.sample(['なぜなら', 'そのため', 'しかし', 'このように'], 2))}」などの接続詞をより効果的に使用すべきです。",
        f"反対意見への配慮が不足しています。「一方で〜という見方もある」という記述を追加してください。",
        f"因果関係の説明において、より段階的な論証プロセスを構築する必要があります。"
    ]
    
    expression_patterns = [
        f"現在{word_count}字ですが、{faculty}の論文として600-800字程度に拡充することを推奨します。",
        f"「である調」と「です・ます調」が混在しています。論文調に統一してください。",
        f"同じ表現の繰り返しが見られます。類義語を用いて表現の多様性を高めるべきです。"
    ]
    
    # スコア算出（より厳格）
    structure_score = max(5, min(25, len(paragraphs) * 6 + random.randint(-3, 3)))
    content_score = max(8, min(30, word_count // 30 + random.randint(-5, 5)))
    logic_score = max(6, min(25, (word_count // 40) + len([w for w in ['なぜなら', 'そのため', 'しかし'] if w in content]) * 4))
    expression_score = max(5, min(20, word_count // 50 + (5 if 'である' in content else 0)))
    
    return {
        "total": structure_score + content_score + logic_score + expression_score,
        "structure": {"score": structure_score, "evaluation": random.choice(structure_patterns)},
        "content": {"score": content_score, "evaluation": random.choice(content_patterns)},
        "logic": {"score": logic_score, "evaluation": random.choice(logic_patterns)},
        "expression": {"score": expression_score, "evaluation": random.choice(expression_patterns)},
        "detailed_feedback": f"総合的な分析として、{university}{faculty}の入試基準では現在のレベルは{'合格圏内' if structure_score + content_score + logic_score + expression_score >= 70 else '改善が必要'}です。特に{random.choice(['構成の明確化', '具体例の充実', '論理的説得力', '表現力の向上'])}に重点を置いた練習が効果的でしょう。",
        "specific_advice": [
            f"序論の「{content[:15] if content else '問題提起'}...」の部分を「より具体的な社会的背景を示した問題提起」に変更すべきである",
            f"本論において「{random.choice(['具体例', 'データ', '国際比較', '専門的視点'])}」を追加して論証を強化すべきである",
            f"結論の表現を「実現可能な具体的提案を含めた将来展望」として充実させるべきである"
        ]
    }

# 採点機能（基本版 - AI評価連携）
def score_essay(content: str, theme: str = "", university: str = "", faculty: str = "") -> dict:
    """AI連携採点機能（基本版）"""
    if not content.strip():
        return {
            "total": 0,
            "structure": {"score": 0, "evaluation": "文章が入力されていません。"},
            "content": {"score": 0, "evaluation": "内容がありません。"},
            "logic": {"score": 0, "evaluation": "論理構成が確認できません。"},
            "expression": {"score": 0, "evaluation": "表現が確認できません。"},
            "detailed_feedback": "文章を入力してください。",
            "specific_advice": ["文章を入力してから採点を実行してください。"]
        }
    
    # AI評価シミュレーションを使用
    return simulate_ai_evaluation(content, theme, university, faculty)

# 問題予想機能
def generate_question(past_questions: List[PastQuestion], university: str, faculty: str, department: str) -> str:
    """問題生成"""
    # 獨協大学・立教大学の場合は長文読解型問題を生成
    if university in ["獨協大学", "立教大学"]:
        sample_texts = [
            {
                "text": """近年、人工知能（AI）技術の急速な発展により、翻訳アプリや言語学習アプリが普及している。これらの技術は言語の壁を下げ、国際コミュニケーションを促進する一方で、「外国語を学ぶ必要がなくなるのではないか」という議論も生まれている。しかし、言語学習は単に情報を伝達する手段を習得することではない。言語を学ぶ過程で、その言語が使われる文化や思考様式、価値観に触れることができる。また、自分とは異なる言語的背景を持つ人々の視点を理解することで、より豊かな人間関係を築くことが可能になる。AI技術と人間の言語学習能力は、対立するものではなく、補完し合う関係にあると考えるべきだろう。""",
                "question": "AI技術の発展が外国語学習に与える影響について、あなたの考えを本文の議論をふまえて述べなさい。（601字以上800字以内）"
            },
            {
                "text": """SNSの普及により、世界中の人々が瞬時に情報を共有できるようになった。この変化は国際理解を深める機会を提供する一方で、文化的な誤解や偏見を生み出すリスクも抱えている。短時間で大量の情報が流れるSNSでは、複雑な文化的背景や歴史的文脈が省略されがちである。その結果、表面的な情報のみに基づいて他国や他文化を判断してしまう傾向が強まっている。真の国際理解を促進するためには、SNSという新しいツールの特性を理解しつつ、深い文化的探究心を持って情報に接することが重要である。""",
                "question": "SNSが国際理解に与える影響について、あなたの考えを本文の議論をふまえて述べなさい。（601字以上800字以内）"
            },
            {
                "text": """グローバル化の進展により、英語が「国際共通語」としての地位を確立している。しかし、この現象は言語の多様性にとって脅威となる可能性も指摘されている。世界には約7000の言語が存在するが、そのうち多くが消滅の危機に瀕している。言語の消失は、その言語に込められた独特の世界観や文化的価値の喪失を意味する。一方で、共通語の存在は国際協力や平和構築に不可欠な要素でもある。我々は言語の多様性を保護しながら、同時に効果的な国際コミュニケーションを実現する方法を模索する必要がある。""",
                "question": "言語の多様性と国際共通語の関係について、あなたの考えを本文の議論をふまえて述べなさい。（601字以上800字以内）"
            },
            {
                "text": """エスノメソドロジーとは、人々が日常生活において、他者との相互行為を通じて社会的現実を構築する「方法」を研究する社会学のアプローチである。例えば、講師が学生に講義をする際、学生たちの微細な表情やしぐさを読み取りながら話を進める。これは一方的な情報伝達ではなく、相互行為による「方法」の実践である。現代のスポーツ指導においても、同様の相互行為が重要な役割を果たしている。指導者は選手の反応を読み取り、選手は指導者の意図を理解しようとする相互的なコミュニケーションが、効果的な指導を可能にする。このような人々の「方法」を理解することは、より良い人間関係やコミュニケーションの構築に役立つだろう。""",
                "question": "問1．エスノメソドロジーについて、この文章の論旨に沿ってまとめなさい。（200字前後）　問2．エスノメソドロジーの見方をスポーツ指導やウェルネス活動に適用する意義について述べなさい。（800字前後）"
            }
        ]
        
        # 大学別に適切なサンプル問題を選択
        if university == "立教大学" and faculty == "スポーツウェルネス学部":
            # 立教大学の場合はエスノメソドロジー問題を優先
            selected = sample_texts[3]  # エスノメソドロジー問題
        else:
            # 獨協大学の場合は言語・文化系問題を優先
            selected = random.choice(sample_texts[:3])
        
        return f"次の文章を読み、設問に答えなさい。\n\n{selected['text']}\n\n（架空の文章・出典省略）\n\n設問\n{selected['question']}"
    
    # その他の大学の場合は従来通り
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

# 小論文書き方ガイド
def show_essay_writing_guide():
    """総合型選抜入試での小論文の書き方ガイド"""
    st.markdown("## 📝 総合型選抜入試 小論文の書き方ガイド")
    
    # タブで分類
    tab1, tab2, tab3, tab4 = st.tabs(["📋 基本構成", "✍️ 書き方のコツ", "⚠️ 注意点", "🎯 合格のポイント"])
    
    with tab1:
        st.markdown("### 📋 小論文の基本構成")
        st.markdown("""
        #### **1. 序論（全体の20%）**
        - **問題提起**: テーマに関する現状や課題を明確に示す
        - **立場表明**: 自分の基本的な考えや主張を述べる
        - **論文の方向性**: これから論じる内容の概要を示す
        
        **例文:**
        > 現代社会において〇〇は重要な課題となっている。この問題に対して、私は△△の観点から□□であると考える。以下、××の視点から論じていく。
        
        #### **2. 本論（全体の60%）**
        - **根拠の提示**: データ、事例、理論的背景を示す
        - **具体例**: 身近な例や社会現象を引用
        - **反対意見への言及**: 多角的な視点を示す
        - **論理的展開**: 筋道立てて議論を進める
        
        #### **3. 結論（全体の20%）**
        - **主張の再確認**: 序論で述べた立場を再度明確に
        - **提案・展望**: 具体的な解決策や今後の方向性
        - **印象的な締めくくり**: 読み手に強い印象を残す
        """)
    
    with tab2:
        st.markdown("### ✍️ 効果的な書き方のコツ")
        st.markdown("""
        #### **論理的な文章構成**
        - **PREP法**: Point（結論）→ Reason（理由）→ Example（例）→ Point（結論）
        - **起承転結**: 起（問題提起）→ 承（現状分析）→ 転（解決策）→ 結（まとめ）
        
        #### **説得力を高める表現**
        - **具体例の活用**: 「例えば」「具体的には」「〜の場合」
        - **論理的接続**: 「そのため」「なぜなら」「このように」「一方で」
        - **データの引用**: 「調査によると」「統計では」「研究結果から」
        
        #### **読みやすい文章**
        - **適切な段落分け**: 一つの段落に一つの論点
        - **文の長さ**: 一文は50字以内を目安
        - **である調**: 論文調で統一
        - **専門用語**: 適切に使用し、必要に応じて説明
        """)
    
    with tab3:
        st.markdown("### ⚠️ よくある注意点")
        st.markdown("""
        #### **避けるべき表現**
        - ❌ 「〜と思います」「〜だと思う」（断定的に書く）
        - ❌ 「みんな」「絶対」（極端な表現を避ける）
        - ❌ 「〜など」の多用（具体性に欠ける）
        - ❌ 感情的な表現（客観的な論調を保つ）
        
        #### **構成上の注意**
        - ❌ 序論が長すぎる（全体の20%以内に）
        - ❌ 結論で新しい論点を出す（まとめに徹する）
        - ❌ 根拠のない主張（必ず理由や例を示す）
        - ❌ 論点のずれ（テーマから外れない）
        
        #### **時間管理**
        - ⏰ 構想・アウトライン作成: 10分
        - ⏰ 本文執筆: 70分
        - ⏰ 見直し・修正: 10分
        """)
    
    with tab4:
        st.markdown("### 🎯 総合型選抜で高評価を得るポイント")
        st.markdown("""
        #### **独創性・個性を示す**
        - 自分なりの視点や経験を含める
        - 志望学部の専門性と関連づける
        - 将来の目標や関心と結び付ける
        
        #### **社会性・時事性**
        - 現代社会の課題への理解を示す
        - 最新の動向や事例を取り入れる
        - グローバルな視点を持つ
        
        #### **実現可能性**
        - 現実的で具体的な提案をする
        - 実際に取り組める解決策を示す
        - 自分の行動計画を含める
        
        #### **文章力・表現力**
        - 正確な日本語を使用する
        - 豊かな語彙を活用する
        - 読み手を意識した表現にする
        
        #### **志望校・学部への理解**
        - 大学の理念や特色を理解している
        - 学部の専門性を活かした論述
        - 入学後の学習計画との関連性
        """)

# メイン関数
def main():
    st.title("📝 総合選抜型入試 小論文対策アプリ")
    st.markdown("### 2026年度入試対応 - 基本機能版")
    
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
    if 'show_writing_guide' not in st.session_state:
        st.session_state.show_writing_guide = False
    
    # サイドバー
    with st.sidebar:
        st.header("ナビゲーション")
        
        if st.button("🏠 ホームに戻る", key="home_btn"):
            reset_all_state()
            st.rerun()
        
        # 小論文書き方ガイド
        st.markdown("### 📝 学習サポート")
        if st.button("📖 小論文の書き方ガイド", key="writing_guide_btn"):
            st.session_state.show_writing_guide = not st.session_state.show_writing_guide
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
    if st.session_state.show_writing_guide:
        show_essay_writing_guide()
    elif st.session_state.page == 'selection':
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
    st.markdown("### 📚 大学を選択してください")
    university_options = ["選択してください"] + [uni.name for uni in universities]
    selected_uni_name = st.selectbox("大学名", university_options, key="uni_select")
    
    if selected_uni_name != "選択してください":
        selected_university = next(uni for uni in universities if uni.name == selected_uni_name)
        st.session_state.selected_university = selected_university
        
        # 学部選択（自動進行対応）
        ao_faculties = [fac for fac in selected_university.faculties if fac.has_ao]
        if ao_faculties:
            # 学部が1つしかない場合は自動選択
            if len(ao_faculties) == 1:
                selected_faculty = ao_faculties[0]
                st.session_state.selected_faculty = selected_faculty
                st.info(f"✅ 自動選択: {selected_faculty.name}")
            else:
                st.markdown(f"### 🏛️ {selected_university.name} - 学部を選択")
                faculty_options = ["選択してください"] + [fac.name for fac in ao_faculties]
                selected_fac_name = st.selectbox("学部名", faculty_options, key="fac_select")
                
                if selected_fac_name != "選択してください":
                    selected_faculty = next(fac for fac in ao_faculties if fac.name == selected_fac_name)
                    st.session_state.selected_faculty = selected_faculty
                else:
                    selected_faculty = None
            
            # 学部が選択された場合の学科選択
            if st.session_state.selected_faculty:
                selected_faculty = st.session_state.selected_faculty
                ao_departments = [dept for dept in selected_faculty.departments if dept.has_ao]
                
                if ao_departments:
                    # 学科が1つしかない場合は自動選択
                    if len(ao_departments) == 1:
                        selected_department = ao_departments[0]
                        st.session_state.selected_department = selected_department
                        st.info(f"✅ 自動選択: {selected_department.name}")
                    else:
                        st.markdown(f"### 🎓 {selected_faculty.name} - 学科を選択")
                        dept_options = ["選択してください"] + [dept.name for dept in ao_departments]
                        selected_dept_name = st.selectbox("学科名", dept_options, key="dept_select")
                        
                        if selected_dept_name != "選択してください":
                            selected_department = next(dept for dept in ao_departments if dept.name == selected_dept_name)
                            st.session_state.selected_department = selected_department
                
                # 学科が選択された場合（自動 or 手動）
                if st.session_state.selected_department:
                    selected_department = st.session_state.selected_department
                    
                    # 選択完了表示
                    st.success(f"✅ 選択完了: {selected_university.name} {selected_faculty.name} {selected_department.name}")
                    
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
                    
                    # 練習開始ボタン（自動進行対応）
                    st.markdown("---")
                    auto_selected = (len(ao_faculties) == 1 and len(ao_departments) == 1)
                    
                    if auto_selected:
                        st.info("🚀 選択肢が1つのため、自動的に予想問題を生成します...")
                        if st.button("📝 小論文練習を開始", type="primary", key="auto_start_btn"):
                            question = generate_question(
                                selected_department.past_questions,
                                selected_university.name,
                                selected_faculty.name,
                                selected_department.name
                            )
                            st.session_state.current_question = question
                            st.session_state.page = 'writing'
                            st.rerun()
                    else:
                        if st.button("🚀 2026年度予想問題で練習開始", type="primary", key="start_btn"):
                            question = generate_question(
                                selected_department.past_questions,
                                selected_university.name,
                                selected_faculty.name,
                                selected_department.name
                            )
                            st.session_state.current_question = question
                            st.session_state.page = 'writing'
                            st.rerun()
        else:
            st.warning(f"⚠️ {selected_university.name}にはAO入試対応学部がありません")

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
    
    # AI採点実行
    if st.session_state.essay_score is None:
        with st.spinner("🤖 AI分析中... 詳細な評価とアドバイスを生成しています"):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
            
            st.session_state.essay_score = score_essay(
                st.session_state.essay_content,
                st.session_state.current_question,
                st.session_state.selected_university.name if st.session_state.selected_university else "",
                st.session_state.selected_faculty.name if st.session_state.selected_faculty else ""
            )
            progress_bar.empty()
    
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
        st.markdown("### 📈 AI詳細スコア")
        score_data = [
            ("📋 構成", score['structure']['score'], 25, score['structure']['evaluation']),
            ("💡 内容", score['content']['score'], 30, score['content']['evaluation']),
            ("🔗 論理性", score['logic']['score'], 25, score['logic']['evaluation']),
            ("✏️ 表現", score['expression']['score'], 20, score['expression']['evaluation'])
        ]
        
        for emoji_name, score_val, max_val, evaluation in score_data:
            col_a, col_b = st.columns([1, 2])
            
            with col_a:
                st.metric(emoji_name, f"{score_val}/{max_val}")
                if max_val > 0:
                    percentage = score_val / max_val
                    st.progress(percentage)
                    
                    if percentage >= 0.8:
                        perf_color, perf_text = "#22c55e", "優秀"
                    elif percentage >= 0.6:
                        perf_color, perf_text = "#eab308", "良好"
                    elif percentage >= 0.4:
                        perf_color, perf_text = "#f97316", "普通"
                    else:
                        perf_color, perf_text = "#ef4444", "要改善"
                    
                    st.markdown(f"<span style='color: {perf_color}'>**{perf_text}**</span>", unsafe_allow_html=True)
            
            with col_b:
                st.markdown(f"**AI評価:** {evaluation}")
    
    # AI詳細フィードバック
    st.markdown("### 🤖 AI詳細フィードバック")
    st.info(score['detailed_feedback'])
    
    # AI具体的改善アドバイス
    if score['specific_advice']:
        st.markdown("### 💡 AI具体的改善アドバイス")
        for i, advice in enumerate(score['specific_advice'], 1):
            st.markdown(f"**{i}.** {advice}")
    
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