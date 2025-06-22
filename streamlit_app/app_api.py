import streamlit as st
import time
import random
import re
import os
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

# 拡張された大学データ
@st.cache_resource
def get_universities():
    return [
        University(
            id='waseda',
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
                                PastQuestion('waseda-sport-2023', 2023, 'スポーツが社会に果たす役割について、現代社会の課題と関連づけて論じなさい。', 90, '早稲田大学', 'スポーツ科学部', 'スポーツ科学科'),
                                PastQuestion('waseda-sport-2022', 2022, 'デジタル技術の発展がスポーツに与える影響と可能性について述べなさい。', 90, '早稲田大学', 'スポーツ科学部', 'スポーツ科学科'),
                                PastQuestion('waseda-sport-2021', 2021, 'コロナ禍におけるスポーツの価値と今後の在り方について論じなさい。', 90, '早稲田大学', 'スポーツ科学部', 'スポーツ科学科'),
                                PastQuestion('waseda-sport-2020', 2020, 'スポーツを通じた国際交流の意義と課題について論じなさい。', 90, '早稲田大学', 'スポーツ科学部', 'スポーツ科学科'),
                                PastQuestion('waseda-sport-2019', 2019, '高齢化社会におけるスポーツの役割について述べなさい。', 90, '早稲田大学', 'スポーツ科学部', 'スポーツ科学科')
                            ]
                        )
                    ]
                ),
            ]
        ),
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
                                PastQuestion('dokkyo-culture-2025', 2025, '【長文読解型】TikTokの影響力と情報発信について論じた文章を読み、「TikTokアプリを禁止すべき」との主張についてのあなたの考えを、本文の議論をふまえて述べなさい。（601字以上800字以内）', 90, '獨協大学', '外国語学部', '交流文化学科'),
                                PastQuestion('dokkyo-culture-2024', 2024, '【長文読解型】Twitter買収・デジタル時代の公共性について論じた文章を読み、「オンライン上の言論空間はどのようなものであるべきでしょうか」について、本文の議論をふまえたあなたの考えを述べなさい。（601字以上800字以内）', 90, '獨協大学', '外国語学部', '交流文化学科'),
                                PastQuestion('dokkyo-culture-2023', 2023, '【長文読解型】「利他」について論じた文章を読み、問1（短答式9字抜き出し）、問2「あなたは利他についてどのように考えますか」筆者の考えを参考にしてあなたの考えを述べなさい。（601字以上800字以内）', 90, '獨協大学', '外国語学部', '交流文化学科')
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
                                PastQuestion('showa-international-2023', 2023, '女性のグローバルリーダーシップについて、現代社会の課題と関連づけて論じなさい。', 90, '昭和女子大学', '国際学部', '国際教養学科'),
                                PastQuestion('showa-international-2022', 2022, '持続可能な国際協力の在り方について述べなさい。', 90, '昭和女子大学', '国際学部', '国際教養学科'),
                                PastQuestion('showa-international-2021', 2021, 'コロナ禍における国際教育の価値と課題について論じなさい。', 90, '昭和女子大学', '国際学部', '国際教養学科'),
                                PastQuestion('showa-international-2020', 2020, '文化の多様性と国際理解について述べなさい。', 90, '昭和女子大学', '国際学部', '国際教養学科'),
                                PastQuestion('showa-international-2019', 2019, 'AI時代における国際教養の意義について論じなさい。', 90, '昭和女子大学', '国際学部', '国際教養学科')
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
                                PastQuestion('jissen-international-2023', 2023, '実践的な国際協力の在り方について、具体的な事例を挙げて論じなさい。', 90, '実践女子大学', '国際学部', '国際学科'),
                                PastQuestion('jissen-international-2022', 2022, '女性の国際的な活躍と社会貢献について述べなさい。', 90, '実践女子大学', '国際学部', '国際学科'),
                                PastQuestion('jissen-international-2021', 2021, 'グローバル社会における実践的な学びの重要性について論じなさい。', 90, '実践女子大学', '国際学部', '国際学科'),
                                PastQuestion('jissen-international-2020', 2020, '国際社会での実践活動が個人に与える影響について述べなさい。', 90, '実践女子大学', '国際学部', '国際学科'),
                                PastQuestion('jissen-international-2019', 2019, '実践的な国際理解教育の在り方について論じなさい。', 90, '実践女子大学', '国際学部', '国際学科')
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
                    id='sport-wellness',
                    name='スポーツウェルネス学部',
                    has_ao=True,
                    departments=[
                        Department(
                            id='sport-wellness',
                            name='スポーツウェルネス学科',
                            has_ao=True,
                            past_questions=[
                                PastQuestion('rikkyo-wellness-2025', 2025, '【長文読解型】エスノメソドロジーについて論じた文章を読み、問1「エスノメソドロジー」について文章の論旨に沿ってまとめなさい（200字前後）、問2「エスノメソドロジー」の見方を異文化コミュニケーション研究でも適用できるかを考察し述べなさい（800字前後）', 90, '立教大学', 'スポーツウェルネス学部', 'スポーツウェルネス学科')
                            ]
                        )
                    ]
                )
            ]
        )
    ]

# Claude API 関数群
def api_generate_question(past_questions: List[PastQuestion], university: str, faculty: str, department: str) -> str:
    """Claude APIを使用した問題予想"""
    try:
        client = get_claude_client()
        
        # 過去問題のテーマを抽出
        past_themes = [q.theme for q in past_questions]
        past_themes_text = "\n".join([f"- {theme}" for theme in past_themes])
        
        # 獨協大学・立教大学の場合は長文読解型問題を生成
        if university in ["獨協大学", "立教大学"]:
            prompt = f"""
あなたは大学入試の小論文問題作成の専門家です。{university}{faculty}の入試問題形式に従って、長文読解型の小論文問題を作成してください。

【過去問分析】
{past_themes_text}

【{university}の特徴】
- 長文読解型：600-1000字程度の文章提示
- 現代社会の課題：AI、SNS、デジタル社会、国際問題、哲学的・社会学的テーマ
- {faculty}適合性：{"国際性、文化論、言語と社会" if university == "獨協大学" else "スポーツ、健康、ウェルネス、社会学、人間関係論"}
- 設問形式：「本文の議論をふまえて〜について述べなさい」
- 文字数：{"601字以上800字以内" if university == "獨協大学" else "200字前後＋800字前後の複合問題"}

【作成要求】
以下の形式で問題を作成してください：

1. 「次の文章を読み、設問に答えなさい。」で開始
2. 600-1000字程度の現代的テーマの文章（著者名・出典付き）
3. 設問：{"「〜についてのあなたの考えを、本文の議論をふまえて述べなさい。（601字以上800字以内）」" if university == "獨協大学" else "問1（要約：200字前後）、問2（考察・応用：800字前後）の複合問題形式"}

2025年の最新時事問題で{faculty}に適した新しいテーマを選んでください（2026年度入試想定）。
"""
        else:
            prompt = f"""
あなたは大学入試の小論文問題作成の専門家です。以下の情報を基に、次年度の総合選抜型入試（AO入試）で出題される可能性の高い小論文問題を1つ生成してください。

【大学情報】
大学: {university}
学部: {faculty}
学科: {department}

【過去5年の出題テーマ】
{past_themes_text}

【要求事項】
1. 過去問題の傾向を分析し、出題パターンを踏襲する
2. 2025年の最新社会情勢や時事問題を反映する（2026年度入試対応）
3. {faculty}の専門性に関連したテーマを含める
4. 大学入試レベルの適切な難易度にする
5. 90分で論述可能な範囲に設定する
6. 問題文は「〜について論じなさい」で終わる

生成する問題文のみを出力してください。説明や解説は不要です。
"""
        
        # 獨協大学の長文読解型問題の場合はトークン数を増やす
        max_tokens = 1500 if university == "獨協大学" else 200
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=max_tokens,
            temperature=0.8,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text.strip()
    
    except Exception as e:
        st.error(f"AI問題生成エラー: {e}")
        # フォールバック（元のロジック）
        return fallback_generate_question(past_questions, university, faculty, department)

def api_score_essay(content: str, theme: str, university: str, faculty: str) -> dict:
    """Claude APIを使用した詳細採点"""
    try:
        client = get_claude_client()
        
        prompt = f"""
あなたは厳格な大学入試の小論文採点官です。{university}{faculty}の入試基準で以下の小論文を厳しく評価してください。

【出題テーマ】
{theme}

【受験生の解答】
{content}

【厳格な採点基準（大学入試レベル）】
1. 構成（25点満点）: 
   - 序論での問題提起と立場表明の明確性
   - 本論での論点の整理と段落構成
   - 結論での主張の再確認と提案
   - 全体的な論理的流れ

2. 内容（30点満点）:
   - テーマに対する理解度の深さ
   - 具体例・データ・事例の適切性と効果性
   - {faculty}の専門性を活かした視点
   - 独創性と洞察力
   - 現実性のある提案

3. 論理性（25点満点）:
   - 論理的一貫性と因果関係の明確性
   - 反対意見への言及と反駁
   - 根拠と主張の適切な関係性
   - 論点の飛躍や矛盾の有無

4. 表現（20点満点）:
   - 文体統一と表現の適切性
   - 語彙の豊富さと専門用語の使用
   - 文の長さと読みやすさ
   - 誤字脱字や文法の正確性

【厳しい評価要求】
- 平均的な受験生なら50-60点が標準
- 80点以上は上位10%レベル
- 90点以上は最優秀レベル
- 具体的な改善点を「〜である」を「〜に変更すべきである」の形で指摘
- 実際の文章例を引用して問題点を指摘
- {university}{faculty}の入試レベルに特化した評価
- 文章の具体的な箇所を特定して改善指導

【出力形式】
以下のJSON形式で厳格に出力してください：
{{
  "structure_score": 数値(0-25),
  "content_score": 数値(0-30),
  "logic_score": 数値(0-25),
  "expression_score": 数値(0-20),
  "structure_evaluation": "構成の具体的問題点と改善策。序論・本論・結論の各段落を個別に分析し、段落内の論理展開、段落間の接続、全体的な流れを300字以上で詳述。",
  "content_evaluation": "内容の深度、具体例の適切性、{faculty}の専門性との関連、独創性、現実性を具体的に分析。不足している具体例、データ、専門的視点を明示し、どのような内容を追加すべきかを300字以上で詳述。",
  "logic_evaluation": "論理的一貫性、因果関係の妥当性、反対意見への配慮、根拠と主張の関係性を詳細分析。論理の飛躍箇所、矛盾点、論証の弱い部分を具体的に指摘し、改善方法を300字以上で詳述。",
  "expression_evaluation": "文体の統一性、語彙の豊富さ、文章の読みやすさ、専門用語の使用、誤字脱字を詳細チェック。文章レベル向上のための具体的修正案を300字以上で詳述。",
  "detailed_feedback": "{university}{faculty}の入試基準での総合評価。現在のレベル、合格可能性、重点改善項目、学習計画を含む総合的な指導を400字以上で詳述。",
  "specific_advice": [
    "序論の構成について：「[実際の文章の具体的箇所]」を「[具体的な改善文例]」に変更し、問題提起をより明確にすべきである",
    "本論の論証について：「[論理的に弱い箇所]」に「[具体的なデータや事例]」を追加して説得力を強化すべきである",
    "結論の提案について：「[抽象的な表現]」を「[具体的で実現可能な提案]」に変更して実践性を高めるべきである",
    "全体の表現について：「[不適切な表現例]」を「[より適切な学術的表現]」に統一すべきである",
    "{faculty}の専門性について：「[専門性が不足している箇所]」に「[具体的な専門的視点や知識]」を加えて学部適合性を高めるべきである",
    "文字数と構成について：現在[実際の文字数]字だが、[具体的な増減指示]して全体のバランスを改善すべきである"
  ]
}}
"""
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2500,
            temperature=0.2,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        import json
        result = json.loads(response.content[0].text)
        
        # 総合点数を計算
        total_score = result["structure_score"] + result["content_score"] + result["logic_score"] + result["expression_score"]
        
        return {
            "total": total_score,
            "structure": {"score": result["structure_score"], "evaluation": result["structure_evaluation"]},
            "content": {"score": result["content_score"], "evaluation": result["content_evaluation"]},
            "logic": {"score": result["logic_score"], "evaluation": result["logic_evaluation"]},
            "expression": {"score": result["expression_score"], "evaluation": result["expression_evaluation"]},
            "detailed_feedback": result["detailed_feedback"],
            "specific_advice": result["specific_advice"]
        }
    
    except Exception as e:
        st.error(f"AI採点エラー: {e}")
        # フォールバック（元のロジック）
        return fallback_score_essay(content, theme)

def api_generate_model_answer(theme: str, university: str, faculty: str) -> str:
    """Claude APIを使用した模範解答生成"""
    try:
        client = get_claude_client()
        
        prompt = f"""
あなたは{university}{faculty}の入試対策専門講師です。以下の小論文テーマに対する模範解答を作成してください。

【テーマ】
{theme}

【要求事項】
1. {faculty}の専門性を活かした内容
2. 大学入試で高評価を得るレベル
3. 800-1000文字程度
4. 序論・本論・結論の明確な構成
5. 具体例やデータの適切な活用
6. 論理的で説得力のある論述
7. 反対意見への配慮も含める

【注意点】
- 「である調」で統一
- 専門用語は適切に使用
- 現実的で実現可能な提案を含める
- 読み手を意識した表現

模範解答のみを出力してください。解説は不要です。
"""
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1500,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text.strip()
    
    except Exception as e:
        st.error(f"模範解答生成エラー: {e}")
        return "申し訳ありません。模範解答の生成に失敗しました。APIの設定を確認してください。"

# フォールバック関数（API失敗時用）
def fallback_generate_question(past_questions: List[PastQuestion], university: str, faculty: str, department: str) -> str:
    """API失敗時のフォールバック問題生成"""
    trends = ['デジタル変革', 'AI技術', '持続可能性', 'グローバル化', '多様性']
    contexts = ['社会', '経済', '政治', '教育', '文化']
    
    trend = random.choice(trends)
    context = random.choice(contexts)
    
    return f"{trend}が進む現代において、{context}分野での課題と解決策について、{faculty}の観点から論じなさい。"

def fallback_score_essay(content: str, theme: str) -> dict:
    """API失敗時のフォールバック採点"""
    word_count = len(content.replace(' ', '').replace('\n', ''))
    
    # 簡易採点
    structure_score = min(20, word_count // 30)
    content_score = min(25, word_count // 25)
    logic_score = min(20, word_count // 35)
    expression_score = min(15, word_count // 40)
    
    total = structure_score + content_score + logic_score + expression_score
    
    return {
        "total": total,
        "structure": {"score": structure_score, "evaluation": "APIが利用できないため簡易評価を実施"},
        "content": {"score": content_score, "evaluation": "APIが利用できないため簡易評価を実施"},
        "logic": {"score": logic_score, "evaluation": "APIが利用できないため簡易評価を実施"},
        "expression": {"score": expression_score, "evaluation": "APIが利用できないため簡易評価を実施"},
        "detailed_feedback": "APIが利用できないため、詳細評価は行えませんでした。",
        "specific_advice": ["Claude APIキーを設定してください", "より詳細な評価を受けるにはAPI機能を有効にしてください"]
    }

# 小論文書き方ガイド関数
def show_essay_writing_guide():
    """総合型選抜入試での小論文の書き方ガイド"""
    st.markdown("## 📝 総合型選抜入試 小論文の書き方ガイド")
    
    # タブで分類
    tab1, tab2, tab3, tab4 = st.tabs(["📋 基本構成", "✍️ 書き方のコツ", "⚠️ 注意点", "🎯 合格のポイント"])
    
    with tab1:
        st.markdown("### 📋 小論文の基本構成")
        st.markdown("""
        #### **1. 序論（全体の20%）**
        - **問題提起**: テーマに対する明確な問題意識を示す
        - **立場表明**: 自分の考えや立場を簡潔に述べる
        - **論文の方向性**: どのような観点から論じるかを予告
        
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

# 大学検索機能
def search_universities(query: str, universities: List[University]) -> List[University]:
    """大学検索機能"""
    if not query:
        return universities
    
    query_lower = query.lower()
    filtered = []
    
    for uni in universities:
        if query_lower in uni.name.lower():
            filtered.append(uni)
            continue
        
        for faculty in uni.faculties:
            if query_lower in faculty.name.lower():
                filtered.append(uni)
                break
        
        for faculty in uni.faculties:
            for dept in faculty.departments:
                if query_lower in dept.name.lower():
                    filtered.append(uni)
                    break
            if uni in filtered:
                break
    
    return filtered

# メイン関数
def main():
    st.title("🤖 Claude API搭載 総合選抜型入試 小論文対策アプリ")
    st.markdown("### 2026年度入試対応 - Claude-3-Haikuによる高精度問題予想・詳細評価・模範解答生成")
    
    # API状態確認
    try:
        client = get_claude_client()
        st.success("✅ Claude API接続完了 - Claude-3-Haikuによる高精度分析が利用可能です")
    except:
        st.warning("⚠️ Claude API未設定 - 基本機能のみ利用可能です")
        with st.expander("📝 API設定方法"):
            st.markdown("""
            **Streamlit Cloud での設定方法:**
            1. Streamlit Cloud の App 設定画面を開く
            2. "Secrets" タブを選択
            3. 以下の形式で追加:
            ```
            ANTHROPIC_API_KEY = "your-api-key-here"
            ```
            
            **ローカル環境での設定方法:**
            1. `.env` ファイルを作成
            2. `ANTHROPIC_API_KEY=your-api-key-here` を記述
            
            **APIキーの取得:**
            1. https://console.anthropic.com/ にアクセス
            2. アカウント作成後、API Keys セクションでキーを生成
            """)
    
    # セッション状態の初期化
    if 'page' not in st.session_state:
        st.session_state.page = 'selection'
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
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
    if 'model_answer' not in st.session_state:
        st.session_state.model_answer = None
    if 'show_writing_guide' not in st.session_state:
        st.session_state.show_writing_guide = False
    
    # サイドバー
    with st.sidebar:
        st.header("🧭 ナビゲーション")
        
        if st.button("🏠 ホームに戻る", key="home_btn"):
            reset_all_state()
            st.rerun()
        
        # 小論文書き方ガイド
        st.markdown("### 📝 学習サポート")
        if st.button("📖 小論文の書き方ガイド", key="writing_guide_btn"):
            st.session_state.show_writing_guide = not st.session_state.show_writing_guide
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🤖 AI機能状態")
        
        try:
            get_claude_client()
            st.success("Claude-3-Haiku 利用可能")
            st.info("高精度分析実行中")
        except:
            st.error("API未設定")
            st.warning("基本機能のみ")
        
        st.markdown("### 📊 現在の状態")
        
        if st.session_state.page == 'selection':
            st.info("🔍 大学・学部選択中")
        elif st.session_state.page == 'writing':
            st.info("✍️ Claude小論文練習中")
        elif st.session_state.page == 'result':
            st.info("📈 Claude詳細評価表示中")
        
        # 検索履歴の表示
        if st.session_state.search_history:
            st.markdown("### 🕒 検索履歴")
            for i, search_term in enumerate(reversed(st.session_state.search_history[-5:])):
                if st.button(f"📚 {search_term}", key=f"history_{i}"):
                    st.session_state.quick_search = search_term
                    st.rerun()
    
    # メインコンテンツ
    if st.session_state.show_writing_guide:
        show_essay_writing_guide()
    elif st.session_state.page == 'selection':
        show_api_university_selection()
    elif st.session_state.page == 'writing':
        show_api_essay_editor()
    elif st.session_state.page == 'result':
        show_api_results()

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
    st.session_state.model_answer = None

def show_api_university_selection():
    """API対応大学選択画面"""
    st.header("🎯 Claude大学・学部・学科選択システム")
    
    universities = get_universities()
    
    # シンプルな大学選択
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
                    
                    # 過去5年分のテーマ表示
                    if selected_department.past_questions:
                        st.markdown("#### 📝 過去5年の出題テーマ")
                        sorted_questions = sorted(selected_department.past_questions, key=lambda x: x.year, reverse=True)
                        
                        for i, q in enumerate(sorted_questions):
                            with st.expander(f"📅 {q.year}年度 ({q.time_limit}分)", expanded=(i < 2)):
                                st.write(q.theme)
                    
                    # Claude AI練習開始
                    st.markdown("---")
                    st.markdown("#### 🤖 Claude AI練習")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("🤖 AI分析", "Claude-3-Haiku")
                    
                    with col2:
                        st.metric("📊 分析データ", f"過去{len(selected_department.past_questions)}年分")
                    
                    # 学部・学科が自動選択された場合は自動的に練習開始
                    auto_selected = (len(ao_faculties) == 1 and len(ao_departments) == 1)
                    
                    if auto_selected:
                        st.info("🚀 選択肢が1つのため、自動的にClaude予想問題を生成します...")
                        if st.button("📝 小論文練習を開始", type="primary", key="auto_start_btn"):
                            with st.spinner("🧠 Claudeが過去問題を分析して予想問題を生成中..."):
                                ai_question = api_generate_question(
                                    selected_department.past_questions,
                                    selected_university.name,
                                    selected_faculty.name,
                                    selected_department.name
                                )
                                st.session_state.current_question = ai_question
                                st.session_state.page = 'writing'
                                st.success("✨ Claude予想問題を生成しました！")
                                time.sleep(1)
                                st.rerun()
                    else:
                        if st.button("🚀 Claude予想問題で練習開始", type="primary", key="claude_start_btn"):
                            with st.spinner("🧠 Claudeが過去問題を分析して予想問題を生成中..."):
                                ai_question = api_generate_question(
                                    selected_department.past_questions,
                                    selected_university.name,
                                    selected_faculty.name,
                                    selected_department.name
                                )
                                st.session_state.current_question = ai_question
                                st.session_state.page = 'writing'
                                st.success("✨ Claude予想問題を生成しました！")
                                time.sleep(1)
                                st.rerun()
        else:
            st.warning(f"⚠️ {selected_university.name}にはAO入試対応学部がありません")
    
    # 利用可能な大学一覧
    with st.expander("📋 利用可能な大学・学部・学科一覧", expanded=False):
        for uni in universities:
            ao_faculty_count = len([f for f in uni.faculties if f.has_ao])
            st.markdown(f"**{uni.name}** (AO対応: {ao_faculty_count}学部)")
            for faculty in uni.faculties:
                if faculty.has_ao:
                    ao_dept_count = len([d for d in faculty.departments if d.has_ao])
                    st.markdown(f"　🏛️ {faculty.name} ({ao_dept_count}学科)")
                    for dept in faculty.departments:
                        if dept.has_ao:
                            st.markdown(f"　　🎓 {dept.name} - 過去問題{len(dept.past_questions)}件")

def show_api_essay_editor():
    """Claude対応小論文エディター"""
    if not st.session_state.current_question:
        st.error("問題が設定されていません。")
        return
    
    st.header("🤖 Claude小論文練習システム")
    
    # Claude生成問題の表示
    st.markdown("### 🧠 Claude予想問題")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.info(st.session_state.current_question)
    
    with col2:
        if st.button("🔄 新しいClaude予想問題", key="new_claude_question"):
            with st.spinner("🤖 Claudeが新しい予想問題を生成中..."):
                new_question = api_generate_question(
                    st.session_state.selected_department.past_questions,
                    st.session_state.selected_university.name,
                    st.session_state.selected_faculty.name,
                    st.session_state.selected_department.name
                )
                st.session_state.current_question = new_question
                st.rerun()
    
    # 出題条件表示
    if st.session_state.selected_department and st.session_state.selected_department.past_questions:
        time_limit = st.session_state.selected_department.past_questions[0].time_limit
    else:
        time_limit = 90
        
    st.markdown(f"**📋 出題条件:** 制限時間 {time_limit}分 | 推奨文字数 600-1000字 | Claude詳細評価対象")
    
    # タイマー管理
    if not st.session_state.timer_started:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⏰ タイマー開始", type="primary", key="timer_start_btn"):
                st.session_state.timer_started = True
                st.session_state.start_time = time.time()
                st.success("⏰ タイマーを開始しました！")
                st.rerun()
        
        with col2:
            if st.button("⏱️ タイマーなしで開始", key="no_timer_btn"):
                st.session_state.timer_started = True
                st.session_state.start_time = None
                st.info("⏱️ タイマーなしで開始しました")
                st.rerun()
        
        with col3:
            if st.button("📖 Claudeガイド", key="claude_guide_btn"):
                with st.expander("🤖 Claudeからのアドバイス", expanded=True):
                    st.markdown("""
                    **🎯 高評価のポイント:**
                    - 序論で明確な問題提起と立場表明
                    - 本論で具体例とデータの効果的活用
                    - 反対意見への言及で多角的視点を示す
                    - 結論で独自の提言や展望を示す
                    
                    **📊 Claude評価基準:**
                    - 論理的一貫性と構成の明確性
                    - 専門性と独創性のバランス
                    - 社会的関心と実現可能性
                    """)
        
        st.info("💡 準備ができたら上のボタンで練習を開始してください")
        return
    
    # タイマー表示
    if st.session_state.start_time:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 時間更新", key="update_timer"):
                st.rerun()
        
        with col2:
            elapsed_time = time.time() - st.session_state.start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            st.metric("⏱️ 経過時間", f"{minutes}:{seconds:02d}")
        
        with col3:
            remaining_time = max(0, time_limit * 60 - elapsed_time)
            if remaining_time > 0:
                r_minutes = int(remaining_time // 60)
                r_seconds = int(remaining_time % 60)
                st.metric("⏰ 残り時間", f"{r_minutes}:{r_seconds:02d}")
            else:
                st.metric("⏰ 残り時間", "終了")
                st.error("⏰ 制限時間終了！Claude評価で提出してください")
        
        with col4:
            progress = min(elapsed_time / (time_limit * 60), 1.0)
            st.metric("📊 進行度", f"{int(progress * 100)}%")
    else:
        st.info("⏱️ タイマーなしモードで練習中")
    
    # Claude小論文エディター
    st.markdown("### ✍️ Claude小論文エディター")
    
    essay_content = st.text_area(
        "📝 ここに小論文を書いてください（Claudeが高精度で分析・評価）",
        value=st.session_state.essay_content,
        height=400,
        placeholder="小論文をここに入力してください...\n\n💡 Claudeからのヒント:\n- 明確な問題提起で始める\n- 具体例とデータで論証を強化\n- 多角的視点で説得力を向上",
        key="claude_essay_textarea"
    )
    
    # リアルタイム文字数カウント
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 文字数・構成チェック", key="check_count"):
            st.session_state.essay_content = essay_content
            st.rerun()
    
    with col2:
        current_content = essay_content if essay_content else st.session_state.essay_content
        word_count = len(current_content.replace(' ', '').replace('\n', ''))
        st.metric("📝 文字数", word_count)
        
        if word_count < 200:
            st.error("文字数不足")
        elif word_count < 400:
            st.warning("やや不足")
        elif word_count < 800:
            st.success("適切")
        else:
            st.info("十分")
    
    with col3:
        paragraphs = len([p for p in current_content.split('\n') if p.strip()])
        st.metric("📑 段落数", paragraphs)
        
        if paragraphs < 3:
            st.warning("構成要改善")
        else:
            st.success("構成良好")
    
    # 内容を保存
    st.session_state.essay_content = essay_content
    
    # 提出ボタン
    min_chars = 100
    can_submit = word_count >= min_chars
    
    if not can_submit:
        st.warning(f"⚠️ 提出には最低{min_chars}文字必要です（現在: {word_count}文字）")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🤖 Claude詳細評価で提出", type="primary", disabled=not can_submit, key="claude_submit_btn"):
            st.session_state.essay_content = essay_content
            st.session_state.page = 'result'
            st.rerun()
    
    with col2:
        if st.button("💾 下書き保存", key="save_draft"):
            st.session_state.essay_content = essay_content
            st.success("💾 下書きを保存しました！")
    
    with col3:
        if st.button("🔄 リセット", key="reset_essay"):
            st.session_state.essay_content = ""
            st.rerun()
    
    with col4:
        if st.button("❌ 中断", key="cancel_writing"):
            reset_all_state()
            st.rerun()

def show_api_results():
    """Claude評価結果画面"""
    st.header("🤖 Claude詳細評価結果")
    
    # Claude採点実行
    if st.session_state.essay_score is None:
        with st.spinner("🧠 Claudeが詳細分析中... 大学入試レベルの厳正な評価を実施しています"):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.03)
                progress_bar.progress(i + 1)
            
            st.session_state.essay_score = api_score_essay(
                st.session_state.essay_content, 
                st.session_state.current_question,
                st.session_state.selected_university.name,
                st.session_state.selected_faculty.name
            )
            progress_bar.empty()
    
    score = st.session_state.essay_score
    
    # 総合評価ヘッダー
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("### 🎯 Claude総合評価")
        st.metric("📊 総合点数", f"{score['total']}/100点")
        
        # 評価グレード
        if score['total'] >= 90:
            grade, color, comment = "S", "#9d4edd", "最優秀"
        elif score['total'] >= 80:
            grade, color, comment = "A", "#22c55e", "優秀"
        elif score['total'] >= 70:
            grade, color, comment = "B", "#eab308", "良好"
        elif score['total'] >= 60:
            grade, color, comment = "C", "#f97316", "普通"
        else:
            grade, color, comment = "D", "#ef4444", "要改善"
        
        st.markdown(f"<h1 style='color: {color}'>評価: {grade}（{comment}）</h1>", unsafe_allow_html=True)
    
    with col2:
        # 推定偏差値
        estimated_rank = min(80, max(20, score['total'] - 20))
        st.metric("📈 推定偏差値", f"{estimated_rank}")
        
        # 合格可能性
        if score['total'] >= 85:
            pass_rate = "95%以上"
        elif score['total'] >= 75:
            pass_rate = "85-90%"
        elif score['total'] >= 65:
            pass_rate = "70-80%"
        else:
            pass_rate = "60%以下"
        
        st.metric("🎯 合格可能性", pass_rate)
    
    with col3:
        st.metric("🤖 評価AI", "Claude")
        st.metric("🏛️ 対象大学", st.session_state.selected_university.name[:4] + "...")
    
    # AI詳細スコア分析（2×2配置）
    st.markdown("### 📊 Claude AI詳細分析")
    
    score_data = [
        ("📋 構成", score['structure']['score'], 25, score['structure']['evaluation']),
        ("💡 内容", score['content']['score'], 30, score['content']['evaluation']),
        ("🔗 論理性", score['logic']['score'], 25, score['logic']['evaluation']),
        ("✏️ 表現", score['expression']['score'], 20, score['expression']['evaluation'])
    ]
    
    # 2×2のグリッド配置
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    columns = [row1_col1, row1_col2, row2_col1, row2_col2]
    
    for i, (emoji_name, score_val, max_val, evaluation) in enumerate(score_data):
        with columns[i]:
            # スコア表示
            percentage = score_val / max_val if max_val > 0 else 0
            st.metric(emoji_name, f"{score_val}/{max_val}")
            st.progress(percentage)
            
            # パフォーマンス評価
            if percentage >= 0.8:
                perf_color, perf_text = "#22c55e", "優秀"
            elif percentage >= 0.6:
                perf_color, perf_text = "#eab308", "良好"
            elif percentage >= 0.4:
                perf_color, perf_text = "#f97316", "普通"
            else:
                perf_color, perf_text = "#ef4444", "要改善"
            
            st.markdown(f"<span style='color: {perf_color}'>**{perf_text}**</span>", unsafe_allow_html=True)
            
            # 詳細評価（展開可能）
            with st.expander(f"{emoji_name} 詳細分析", expanded=False):
                st.write(evaluation)
    
    # Claude詳細フィードバック
    st.markdown("### 🤖 Claude詳細フィードバック")
    st.info(score['detailed_feedback'])
    
    # 具体的改善アドバイス
    if score['specific_advice']:
        st.markdown("### 💡 Claude具体的改善アドバイス")
        for i, advice in enumerate(score['specific_advice'], 1):
            st.markdown(f"**{i}.** {advice}")
    
    # Claude模範解答生成
    if st.session_state.model_answer is None:
        if st.button("📖 Claude模範解答を生成", key="generate_model"):
            with st.spinner("🤖 Claudeが模範解答を生成中..."):
                model_answer = api_generate_model_answer(
                    st.session_state.current_question,
                    st.session_state.selected_university.name,
                    st.session_state.selected_faculty.name
                )
                st.session_state.model_answer = model_answer
                st.rerun()
    else:
        with st.expander("📖 Claude生成模範解答", expanded=False):
            st.markdown("**💡 このテーマに対するClaude模範解答:**")
            st.markdown(st.session_state.model_answer)
            st.warning("⚠️ これはClaudeが生成した参考例です。実際の入試では自分の言葉で表現することが重要です。")
    
    # あなたの解答表示
    with st.expander("📄 あなたの解答を確認", expanded=False):
        st.markdown("#### 🎯 出題テーマ")
        st.write(st.session_state.current_question)
        st.markdown("#### ✍️ あなたの解答内容")
        st.text_area("あなたの解答", value=st.session_state.essay_content, height=200, disabled=True, label_visibility="collapsed")
    
    # アクションボタン
    st.markdown("### 🎯 次のアクション")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 同じ問題で再挑戦", key="retry_same"):
            st.session_state.page = 'writing'
            st.session_state.essay_content = ""
            st.session_state.essay_score = None
            st.session_state.model_answer = None
            st.session_state.timer_started = False
            st.session_state.start_time = None
            st.rerun()
    
    with col2:
        if st.button("🤖 新しいClaude予想問題", key="new_claude_question_result"):
            with st.spinner("🧠 新しい予想問題を生成中..."):
                new_question = api_generate_question(
                    st.session_state.selected_department.past_questions,
                    st.session_state.selected_university.name,
                    st.session_state.selected_faculty.name,
                    st.session_state.selected_department.name
                )
                st.session_state.current_question = new_question
                st.session_state.page = 'writing'
                st.session_state.essay_content = ""
                st.session_state.essay_score = None
                st.session_state.model_answer = None
                st.session_state.timer_started = False
                st.session_state.start_time = None
                st.rerun()
    
    with col3:
        if st.button("🏛️ 別の大学で練習", key="change_university"):
            reset_all_state()
            st.rerun()
    
    with col4:
        if st.button("📊 Claude評価結果DL", key="download_claude_result"):
            result_text = f"""
Claude小論文評価結果

【基本情報】
大学: {st.session_state.selected_university.name}
学部: {st.session_state.selected_faculty.name}  
学科: {st.session_state.selected_department.name}
評価AI: Claude
実施日: {datetime.now().strftime('%Y年%m月%d日')}

【Claude評価結果】
総合点数: {score['total']}/100点
- 構成: {score['structure']['score']}/25点
- 内容: {score['content']['score']}/30点  
- 論理性: {score['logic']['score']}/25点
- 表現: {score['expression']['score']}/20点

【Claude詳細評価】
{score['detailed_feedback']}

【Claude改善アドバイス】
{chr(10).join([f"{i+1}. {advice}" for i, advice in enumerate(score['specific_advice'])])}

【出題テーマ】
{st.session_state.current_question}

【解答内容】
{st.session_state.essay_content}

【Claude模範解答】
{st.session_state.model_answer if st.session_state.model_answer else '未生成'}
            """
            
            st.download_button(
                label="📄 Claude評価結果をダウンロード",
                data=result_text,
                file_name=f"claude_essay_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()