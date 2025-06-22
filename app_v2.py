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

# Claude API 設定（キャッシュなし）
def get_claude_client():
    """Claude クライアントを取得（評価の度に新しいクライアント）"""
    api_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ Claude API キーが設定されていません。環境変数 ANTHROPIC_API_KEY を設定してください。")
        st.stop()
    # 毎回新しいクライアントを作成（キャッシュ回避）
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
                                PastQuestion('waseda-sport-2021', 2021, 'コロナ禍におけるスポーツの価値と今後の在り方について論じなさい。', 90, '早稲田大学', 'スポーツ科学部', 'スポーツ科学科')
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
                                PastQuestion('showa-intl-2023', 2023, '国際社会における多様性の重要性について、具体例を挙げて論じなさい。', 90, '昭和女子大学', '国際学部', '国際教養学科'),
                                PastQuestion('showa-intl-2022', 2022, 'グローバル化が教育に与える影響について述べなさい。', 90, '昭和女子大学', '国際学部', '国際教養学科')
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
                                PastQuestion('jissen-intl-2023', 2023, '持続可能な国際協力のあり方について、あなたの考えを述べなさい。', 90, '実践女子大学', '国際学部', '国際学科'),
                                PastQuestion('jissen-intl-2022', 2022, '文化交流が社会に与える意義について論じなさい。', 90, '実践女子大学', '国際学部', '国際学科')
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
        
        # 過去問データの存在確認
        if not past_questions:
            st.warning("⚠️ 過去問データが見つかりません。汎用的な問題を生成します。")
            return fallback_generate_question(past_questions, university, faculty, department)
        
        # 過去問の詳細分析
        past_questions_detail = []
        for q in past_questions[-3:]:
            past_questions_detail.append(f"【{q.year}年】{q.theme}")
        
        past_questions_text = "\n".join(past_questions_detail)
        
        st.info(f"📚 {len(past_questions)}件の過去問データを分析して問題を生成中...")
        
        # 過去問の特徴分析
        keywords = []
        for q in past_questions:
            if 'デジタル' in q.theme or 'SNS' in q.theme or 'AI' in q.theme or 'TikTok' in q.theme or 'Twitter' in q.theme:
                keywords.append('デジタル・テクノロジー')
            if '社会' in q.theme or '公共' in q.theme:
                keywords.append('社会問題')
            if '国際' in q.theme or 'グローバル' in q.theme:
                keywords.append('国際・グローバル')
            if 'スポーツ' in q.theme:
                keywords.append('スポーツ・健康')
            if '利他' in q.theme or '多様性' in q.theme:
                keywords.append('価値観・倫理')
        
        trend_keywords = list(set(keywords))
        
        prompt = f"""あなたは{university}{faculty}{department}の総合選抜型入試問題作成の専門家です。

【過去3年間の実際の出題】
{past_questions_text}

【出題傾向分析】
頻出キーワード: {', '.join(trend_keywords) if trend_keywords else '社会問題、現代課題'}

【2026年度予想問題作成指示】
上記の過去問を詳細に分析し、以下の条件で2026年度の出題を予想してください：

1. 過去問の出題パターン・形式を踏襲する
2. 過去のテーマの発展・応用版として構成
3. 2026年の社会情勢を反映した最新性
4. {university}{faculty}の求める人材像に適合
5. 過去問と同様の文字数制限・時間設定
6. 学部の専門性を活かした視点を含む

【重要】過去問の傾向を必ず反映し、継続性のある出題としてください。

出力形式：
問題文のみを簡潔に出力してください。"""

        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=800,
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
        
        # 評価用の一意性確保
        import hashlib
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # プロンプトに一意性を追加（キャッシュ回避）
        import random
        random_seed = random.randint(10000, 99999)
        
        prompt = f"""【緊急評価指令 - ID: {content_hash}-{current_time}-{random_seed}】
あなたは{university}{faculty}の厳格な入試評価委員です。以下の小論文を完全に新規として評価してください。

🚨 重要指示:
1. この評価は独立した新しい評価です
2. 文章の長さ、構成、内容、表現を詳細に分析してください
3. 前回とは異なる視点で厳格に採点してください
4. 必ず具体的な改善点を文章から引用して指摘してください
5. 評価スコアは文章の実際の質に基づいて変動させてください

【評価対象文章の特徴】
- 文字数: {len(content)}文字
- 文章ハッシュ: {content_hash}
- 評価時刻: {current_time}

【出題テーマ】
{theme}

【学生の解答】
{content}

【厳格評価基準】
以下の4項目を100点満点で厳しく評価してください。文章の質に応じて点数を大きく変動させてください：

1. 構成・組織化 (25点満点): 序論・本論・結論の明確性、段落構成、全体の論理的流れ
2. 内容・論点 (25点満点): 論点の深度、根拠の妥当性、具体例の適切性、独創性
3. 論理性・一貫性 (25点満点): 論理展開の正確性、矛盾の有無、因果関係の明確性
4. 表現・文章力 (25点満点): 語彙力、文章の正確性、読みやすさ、誤字脱字

【詳細要求事項】
- 各項目の評価文は400文字以上で、この文章特有の問題点と改善方法を詳述
- 改善点は実際の文章から具体的な部分を引用して指摘
- 総合評価は200文字以上で、この文章の特徴を踏まえた厳格な判定
- 具体的アドバイスは8つ以上の、この文章に特化した詳細な改善提案
- 文字数や内容の変化に応じて評価を大きく変動させてください

【SABCD評価・偏差値・合格可能性も算出】
- 文章の質に応じて評価を大幅に変動させる
- 同じ文章でも角度を変えて厳格に再評価する

以下のJSON形式で回答してください：
{{
  "総合得点": 65,
  "SABCD評価": "C",
  "偏差値": 48,
  "合格可能性": "35%",
  "構成": {{"得点": 15, "評価": "400文字以上の詳細評価", "改善点": "具体的な文章引用と改善方法"}},
  "内容": {{"得点": 17, "評価": "400文字以上の詳細評価", "改善点": "具体的な文章引用と改善方法"}},
  "論理性": {{"得点": 16, "評価": "400文字以上の詳細評価", "改善点": "具体的な文章引用と改善方法"}},
  "表現": {{"得点": 17, "評価": "400文字以上の詳細評価", "改善点": "具体的な文章引用と改善方法"}},
  "総合評価": "200文字以上の厳格な総合判定コメント",
  "具体的アドバイス": ["詳細改善提案1", "詳細改善提案2", "詳細改善提案3", "詳細改善提案4", "詳細改善提案5", "詳細改善提案6", "詳細改善提案7", "詳細改善提案8"]
}}"""

        # temperatureを追加して応答にバリエーションを持たせる
        temperature = 0.7 + (random.randint(0, 30) / 100)  # 0.7-1.0の範囲
        
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=4000,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        
        # JSON部分を抽出
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start != -1 and json_end != -1:
            json_text = response_text[json_start:json_end]
            parsed_result = json.loads(json_text)
            return parsed_result
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
    # 厳しい採点基準
    base_score = min(75, max(45, len(content) // 15 + random.randint(35, 60)))
    
    # SABCD評価
    if base_score >= 85: sabcd = "S"
    elif base_score >= 75: sabcd = "A" 
    elif base_score >= 65: sabcd = "B"
    elif base_score >= 55: sabcd = "C"
    else: sabcd = "D"
    
    # 偏差値計算
    deviation = max(35, min(65, base_score * 0.8 + random.randint(-5, 5)))
    
    # 合格可能性
    if base_score >= 80: possibility = f"{random.randint(85, 95)}%"
    elif base_score >= 70: possibility = f"{random.randint(65, 80)}%"
    elif base_score >= 60: possibility = f"{random.randint(35, 60)}%"
    else: possibility = f"{random.randint(10, 30)}%"
    
    return {
        "総合得点": base_score,
        "SABCD評価": sabcd,
        "偏差値": deviation,
        "合格可能性": possibility,
        "構成": {
            "得点": base_score//4-2, 
            "評価": "序論・本論・結論の構成は見られるものの、段落間の論理的つながりが不明確な部分があります。各段落の役割をより明確にし、論理的な流れを意識した構成にする必要があります。特に序論での問題提起と結論での解決策提示の対応関係を強化してください。", 
            "改善点": "段落の冒頭に接続語を使用し、前の段落との関係を明示する。各段落が全体の論証にどう貢献するかを明確にする。"
        },
        "内容": {
            "得点": base_score//4-1, 
            "評価": "基本的な論点は押さえているが、根拠の深度と具体性に課題があります。抽象的な議論にとどまり、具体的なデータや事例による論証が不足しています。また、多角的な視点からの検討が不十分で、反対意見への配慮も欠けています。", 
            "改善点": "統計データや具体的事例を3つ以上引用する。反対意見を明示し、それに対する反駁を論理的に展開する。"
        },
        "論理性": {
            "得点": base_score//4, 
            "評価": "論理展開に一定の筋道は見られますが、論証の飛躍や因果関係の不明確な部分が散見されます。前提と結論の関係が曖昧で、読み手にとって説得力に欠ける構造となっています。論理的な推論過程をより丁寧に説明する必要があります。", 
            "改善点": "「なぜならば」「したがって」などの論理接続詞を適切に使用し、因果関係を明確化する。主張と根拠の対応関係を一つずつ確認する。"
        },
        "表現": {
            "得点": base_score//4+1, 
            "評価": "基本的な文章力は備わっているものの、語彙の多様性や表現の工夫に改善の余地があります。同じ表現の反復が目立ち、読み手の関心を引きつける工夫が不足しています。また、文体の統一性にも注意が必要です。", 
            "改善点": "同義語や類義語を積極的に使用し表現を多様化する。文末表現のバリエーションを増やし、読みやすさを向上させる。"
        },
        "総合評価": f"現在の文章は基本的な要素は満たしているものの、{university}{faculty}の入試レベルとしては改善が必要です。特に論証の深度と具体性の向上が急務です。論理的思考力と表現力のさらなる向上により、合格レベルに到達することは十分可能です。",
        "具体的アドバイス": [
            "序論で問題の背景をより詳細に説明し、なぜその問題が重要なのかを明確にする",
            "本論では主張を支える根拠を3つ以上提示し、それぞれに具体例やデータを付加する", 
            "反対意見を想定し、それに対する反駁を論理的に展開する",
            "段落間の接続を強化し、論理的な流れを明確にする",
            "結論では単なるまとめではなく、社会への提案や将来への展望を含める",
            "文章表現を多様化し、読み手の関心を維持する工夫を凝らす",
            "誤字脱字のチェックを徹底し、文体の統一を図る",
            "制限時間内で見直しの時間を確保し、論理的整合性を最終確認する"
        ]
    }

def show_writing_guide():
    """小論文の書き方ガイド"""
    with st.container():
        st.markdown("#### 📚 総合選抜型入試 小論文の書き方")
        
        st.markdown("""
        **📝 基本構成（800字の場合）**
        1. **序論（100-150字）**: 問題提起・立場表明
        2. **本論（500-550字）**: 根拠・論証・具体例
        3. **結論（100-150字）**: まとめ・提案
        
        **🎯 高評価のポイント**
        - **明確な論理構成**: 序論→本論→結論の流れ
        - **具体的な根拠**: データ・事例・体験談
        - **批判的思考**: 多角的な視点・反対意見への配慮
        - **独自性**: 自分なりの考察・提案
        
        **⚠️ 注意事項**
        - 文字数制限の厳守（±50字以内）
        - 適切な敬語・文体の統一
        - 誤字脱字の回避
        - 時間配分（構想20%・執筆70%・見直し10%）
        """)
        
        with st.expander("🔍 詳細な書き方テクニック"):
            st.markdown("""
            **序論の書き方**
            - 問題の背景を簡潔に述べる
            - 自分の立場を明確に表明
            - 本論での論証の方向性を示す
            
            **本論の書き方**
            - 主張を支える根拠を3つ程度提示
            - 具体例・データ・体験を交える
            - 反対意見にも言及し、反駁する
            
            **結論の書き方**
            - 主張を簡潔に再確認
            - 社会への提案・将来への展望
            - 印象的な締めくくり
            """)
        
        st.info("💡 この画面は入力中も参照できます。サイドバーから随時確認してください。")

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
    
    # サイドバー
    with st.sidebar:
        st.header("🧭 ナビゲーション")
        
        if st.button("🏠 ホームに戻る"):
            st.session_state.step = 'select'
            st.session_state.selected_university = None
            st.session_state.selected_faculty = None
            st.session_state.selected_department = None
            st.session_state.current_question = None
            st.session_state.essay_content = ""
            st.session_state.essay_result = None
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📝 学習サポート")
        
        # 小論文の書き方ガイド
        if st.button("📖 小論文の書き方ガイド"):
            st.session_state.show_guide = not st.session_state.get('show_guide', False)
            st.rerun()
        
        if st.session_state.get('show_guide', False):
            show_writing_guide()
        
        st.markdown("---")
        st.markdown("### 🤖 AI機能状態")
        
        try:
            get_claude_client()
            st.success("✅ Claude-3-Haiku 利用可能")
            st.info("🔬 厳格評価システム稼働中")
        except:
            st.error("❌ API未設定")
            st.warning("⚠️ 基本機能のみ")
    
    # ステップ1: 大学選択→問題生成→入力
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
                    
                    st.info(f"📋 選択内容: {selected_university.name} {selected_faculty.name} {selected_department.name}")
                    
                    if st.button("🚀 問題生成して練習開始", type="primary"):
                        # 問題生成
                        with st.spinner("🤖 Claude AIが過去問を分析して問題を生成中..."):
                            past_questions = selected_department.past_questions
                            question = api_generate_question(
                                past_questions,
                                selected_university.name,
                                selected_faculty.name,
                                selected_department.name
                            )
                            st.session_state.current_question = question
                        
                        st.success("✅ 問題生成完了！小論文入力画面に移動します")
                        st.session_state.step = 'essay'
                        st.rerun()
    
    # ステップ2: 小論文入力
    elif st.session_state.step == 'essay':
        st.header("✍️ 小論文練習")
        
        # 選択した大学情報を表示
        if st.session_state.selected_university:
            st.success(f"🎯 {st.session_state.selected_university.name} {st.session_state.selected_faculty.name} {st.session_state.selected_department.name}")
        
        # 問題表示（常に表示）
        st.markdown("### 📝 出題テーマ")
        if st.session_state.current_question:
            st.info(st.session_state.current_question)
        else:
            st.error("問題が生成されていません。最初からやり直してください。")
            return
        
        # タイマー機能
        if 'start_time' not in st.session_state:
            st.session_state.start_time = None
        if 'timer_started' not in st.session_state:
            st.session_state.timer_started = False
        
        # タイマーコントロール
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### ✍️ 解答入力")
        
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
            height=350,
            placeholder="ここに小論文を入力してください...",
            key="essay_input"
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
                # 評価結果をリセット（新しい評価のため）
                st.session_state.essay_result = None
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
            if st.button("❌ 最初から"):
                for key in ['step', 'selected_university', 'selected_faculty', 'selected_department', 
                           'current_question', 'essay_content', 'essay_result', 'start_time', 'timer_started']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
    
    # ステップ3: 結果表示・修正・再評価
    elif st.session_state.step == 'result':
        st.header("📊 評価結果")
        
        # 問題を常に表示
        st.markdown("### 📝 出題テーマ")
        st.info(st.session_state.current_question)
        
        # 評価実行
        if st.session_state.essay_result is None:
            evaluation_time = datetime.now().strftime("%H:%M:%S")
            
            with st.spinner("🤖 Claude AIが厳格に評価中..."):
                try:
                    
                    result = api_score_essay(
                        st.session_state.essay_content,
                        st.session_state.current_question,
                        st.session_state.selected_university.name,
                        st.session_state.selected_faculty.name
                    )
                    
                    # 評価時刻を記録
                    result["評価時刻"] = evaluation_time
                    result["文字数"] = len(st.session_state.essay_content)
                    result["AI使用"] = "Claude-3-Haiku"
                    result["評価ID"] = f"Claude-{evaluation_time}"
                    result["評価内容"] = f"新規評価 - 文字数{len(st.session_state.essay_content)}"
                    
                    st.session_state.essay_result = result
                    
                except Exception as e:
                    st.error(f"❌ Claude API エラー: {str(e)}")
                    st.warning("🔄 フォールバック評価を使用します")
                    
                    result = fallback_score_essay(
                        st.session_state.essay_content,
                        st.session_state.current_question,
                        st.session_state.selected_university.name,
                        st.session_state.selected_faculty.name
                    )
                    result["評価時刻"] = evaluation_time
                    result["文字数"] = len(st.session_state.essay_content)
                    result["AI使用"] = "フォールバック"
                    
                    st.session_state.essay_result = result
        
        result = st.session_state.essay_result
        
        # 評価情報表示
        st.markdown("### 📊 評価情報")
        eval_col1, eval_col2, eval_col3 = st.columns(3)
        with eval_col1:
            st.metric("評価時刻", result.get("評価時刻", "不明"))
        with eval_col2:
            st.metric("文字数", f"{result.get('文字数', 0)}文字")
        with eval_col3:
            ai_used = result.get("AI使用", "不明")
            color = "🤖" if "Claude" in ai_used else "⚠️"
            st.metric("AI評価", f"{color} {ai_used}")
        
        # 総合評価
        st.markdown("### 🎯 総合評価")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            score = result.get("総合得点", 0)
            st.metric("総合得点", f"{score}/100点")
        
        with col2:
            sabcd = result.get("SABCD評価", "C")
            st.metric("SABCD評価", sabcd)
        
        with col3:
            deviation = result.get("偏差値", 50)
            st.metric("偏差値", deviation)
        
        with col4:
            possibility = result.get("合格可能性", "50%")
            st.metric("合格可能性", possibility)
        
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
        
        # あなたの解答表示と修正機能
        st.markdown("---")
        st.markdown("### ✏️ あなたの解答を修正して再評価")
        
        # 現在の解答を表示
        st.markdown("#### 📄 現在の解答内容")
        
        # 現在の文章を読み取り専用で表示
        st.text_area(
            "現在の解答（読み取り専用）",
            value=st.session_state.essay_content,
            height=200,
            disabled=True,
            key="current_essay_display"
        )
        
        # 新しい文章入力フィールド
        st.markdown("#### ✏️ 修正版を入力してください")
        
        # セッション状態に新しい文章用のキーを作成
        if 'new_essay_content' not in st.session_state:
            st.session_state.new_essay_content = st.session_state.essay_content
        
        new_essay = st.text_area(
            "修正した文章を入力",
            value=st.session_state.new_essay_content,
            height=300,
            help="評価コメントを参考に文章を修正してください",
            key="new_essay_input"
        )
        
        # リアルタイムで新しい文章を更新
        st.session_state.new_essay_content = new_essay
        
        char_count_new = len(new_essay)
        st.write(f"文字数: {char_count_new}文字")
        
        # 変更検出
        has_changed = new_essay != st.session_state.essay_content
        if has_changed:
            st.info("🔄 文章が変更されています")
        else:
            st.warning("⚠️ 文章に変更がありません")
        
        # 修正・再評価ボタン
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 修正版で再評価", type="primary", disabled=char_count_new < 100 or not has_changed):
                # セッション状態を確実に更新
                st.session_state.essay_content = new_essay
                st.session_state.essay_result = None
                
                # 追加のクリア処理
                for key in ['essay_result']:
                    if key in st.session_state:
                        del st.session_state[key]
                
                st.success("✅ 新しい文章で評価を開始します...")
                time.sleep(1)
                st.rerun()
        
        with col2:
            if st.button("📚 模範解答を確認"):
                with st.spinner("模範解答を生成中..."):
                    model_answer = api_generate_model_answer(
                        st.session_state.current_question,
                        st.session_state.selected_university.name,
                        st.session_state.selected_faculty.name
                    )
                    st.session_state.model_answer = model_answer
                
        with col3:
            if st.button("✍️ 入力画面に戻る"):
                st.session_state.step = 'essay'
                st.rerun()
        
        with col4:
            if st.button("🆕 新しい問題で練習"):
                # 同じ大学・学部で新しい問題を生成
                st.session_state.essay_content = ""
                st.session_state.essay_result = None
                st.session_state.current_question = None
                st.session_state.start_time = None
                st.session_state.timer_started = False
                st.session_state.step = 'select'
                st.rerun()
        
        # 模範解答表示
        if 'model_answer' in st.session_state and st.session_state.model_answer:
            st.markdown("---")
            st.markdown("### 📚 模範解答")
            st.write(st.session_state.model_answer)
            st.info("💡 模範解答は参考例です。実際の入試では自分の言葉で表現することが重要です。")
        
        # 完全リセットボタン
        st.markdown("---")
        if st.button("🏠 最初からやり直す", help="全てリセットして大学選択から始める"):
            for key in ['step', 'selected_university', 'selected_faculty', 'selected_department', 
                       'current_question', 'essay_content', 'essay_result', 'model_answer',
                       'start_time', 'timer_started']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()