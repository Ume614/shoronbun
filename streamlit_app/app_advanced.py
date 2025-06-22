import streamlit as st
import time
import random
import re
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional, Dict

# ページ設定
st.set_page_config(
    page_title="AI搭載 総合選抜型入試 小論文対策アプリ",
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

# 拡張された大学データ
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
                                PastQuestion('waseda-pol-2023', 2023, 'デジタル社会における民主主義の課題と可能性について、具体例を挙げて論じなさい。', 90, '早稲田大学', '政治経済学部', '政治学科'),
                                PastQuestion('waseda-pol-2022', 2022, 'グローバル化が進む現代において、国家の役割はどのように変化すべきか論じなさい。', 90, '早稲田大学', '政治経済学部', '政治学科'),
                                PastQuestion('waseda-pol-2021', 2021, 'コロナ禍を通じて見えた現代社会の課題と、その解決策について論じなさい。', 90, '早稲田大学', '政治経済学部', '政治学科'),
                                PastQuestion('waseda-pol-2020', 2020, '持続可能な社会の実現に向けて、政治が果たすべき役割について論じなさい。', 90, '早稲田大学', '政治経済学部', '政治学科'),
                                PastQuestion('waseda-pol-2019', 2019, '人工知能の発達が社会に与える影響と、それに対する政策の在り方について論じなさい。', 90, '早稲田大学', '政治経済学部', '政治学科')
                            ]
                        ),
                        Department(
                            id='economics',
                            name='経済学科',
                            has_ao=True,
                            past_questions=[
                                PastQuestion('waseda-econ-2023', 2023, '日本経済の持続的成長に向けた課題と解決策について論じなさい。', 90, '早稲田大学', '政治経済学部', '経済学科'),
                                PastQuestion('waseda-econ-2022', 2022, 'デジタル経済の発展が労働市場に与える影響について述べなさい。', 90, '早稲田大学', '政治経済学部', '経済学科'),
                                PastQuestion('waseda-econ-2021', 2021, 'ポストコロナ時代の経済政策について論じなさい。', 90, '早稲田大学', '政治経済学部', '経済学科'),
                                PastQuestion('waseda-econ-2020', 2020, '環境問題と経済発展の両立について論じなさい。', 90, '早稲田大学', '政治経済学部', '経済学科'),
                                PastQuestion('waseda-econ-2019', 2019, 'AI時代における雇用創出の在り方について述べなさい。', 90, '早稲田大学', '政治経済学部', '経済学科')
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
                                PastQuestion('waseda-law-2023', 2023, '法の支配と民主主義の関係について、現代社会の具体例を挙げて論じなさい。', 90, '早稲田大学', '法学部', '法学科'),
                                PastQuestion('waseda-law-2022', 2022, 'デジタル時代における個人情報保護と表現の自由の調和について論じなさい。', 90, '早稲田大学', '法学部', '法学科'),
                                PastQuestion('waseda-law-2021', 2021, 'コロナ禍における緊急事態宣言と憲法上の人権制約について述べなさい。', 90, '早稲田大学', '法学部', '法学科'),
                                PastQuestion('waseda-law-2020', 2020, '国際社会における法の役割と限界について論じなさい。', 90, '早稲田大学', '法学部', '法学科'),
                                PastQuestion('waseda-law-2019', 2019, 'AI判断システムの導入と司法制度の未来について述べなさい。', 90, '早稲田大学', '法学部', '法学科')
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
                                PastQuestion('keio-econ-2023', 2023, 'デジタル化が進む現代において、経済活動はどのように変化すべきか論じなさい。', 90, '慶應義塾大学', '経済学部', '経済学科'),
                                PastQuestion('keio-econ-2022', 2022, 'グローバル資本主義の課題と新しい経済システムの可能性について述べなさい。', 90, '慶應義塾大学', '経済学部', '経済学科'),
                                PastQuestion('keio-econ-2021', 2021, 'コロナ禍が明らかにした経済格差の問題と解決策について論じなさい。', 90, '慶應義塾大学', '経済学部', '経済学科'),
                                PastQuestion('keio-econ-2020', 2020, '持続可能な経済発展とイノベーションの関係について述べなさい。', 90, '慶應義塾大学', '経済学部', '経済学科'),
                                PastQuestion('keio-econ-2019', 2019, 'デジタル通貨の普及が金融システムに与える影響について論じなさい。', 90, '慶應義塾大学', '経済学部', '経済学科')
                            ]
                        )
                    ]
                ),
                Faculty(
                    id='business',
                    name='商学部',
                    has_ao=True,
                    departments=[
                        Department(
                            id='business',
                            name='商学科',
                            has_ao=True,
                            past_questions=[
                                PastQuestion('keio-bus-2023', 2023, 'ESG経営が企業価値に与える影響について論じなさい。', 90, '慶應義塾大学', '商学部', '商学科'),
                                PastQuestion('keio-bus-2022', 2022, 'デジタルマーケティングの進化と消費者行動の変化について述べなさい。', 90, '慶應義塾大学', '商学部', '商学科'),
                                PastQuestion('keio-bus-2021', 2021, 'ポストコロナ時代のビジネスモデル変革について論じなさい。', 90, '慶應義塾大学', '商学部', '商学科'),
                                PastQuestion('keio-bus-2020', 2020, 'スタートアップ企業の社会的価値創造について述べなさい。', 90, '慶應義塾大学', '商学部', '商学科'),
                                PastQuestion('keio-bus-2019', 2019, 'AIを活用したビジネス革新の可能性と課題について論じなさい。', 90, '慶應義塾大学', '商学部', '商学科')
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
                                PastQuestion('todai-liberal-2023', 2023, '多様性と包摂性が求められる現代社会において、教育の果たすべき役割について論じなさい。', 120, '東京大学', '教養学部', '教養学科'),
                                PastQuestion('todai-liberal-2022', 2022, '科学技術の発展と人間性の調和について、具体例を挙げて述べなさい。', 120, '東京大学', '教養学部', '教養学科'),
                                PastQuestion('todai-liberal-2021', 2021, 'グローバル化時代における文化的アイデンティティの意義について論じなさい。', 120, '東京大学', '教養学部', '教養学科'),
                                PastQuestion('todai-liberal-2020', 2020, '持続可能な社会の実現に向けた教養教育の役割について述べなさい。', 120, '東京大学', '教養学部', '教養学科'),
                                PastQuestion('todai-liberal-2019', 2019, 'AI時代における人間の知性と創造性の価値について論じなさい。', 120, '東京大学', '教養学部', '教養学科')
                            ]
                        )
                    ]
                )
            ]
        ),
        University(
            id='sophia',
            name='上智大学',
            faculties=[
                Faculty(
                    id='foreign-studies',
                    name='外国語学部',
                    has_ao=True,
                    departments=[
                        Department(
                            id='english',
                            name='英語学科',
                            has_ao=True,
                            past_questions=[
                                PastQuestion('sophia-eng-2023', 2023, '言語多様性の保護と国際コミュニケーションの促進の両立について論じなさい。', 90, '上智大学', '外国語学部', '英語学科'),
                                PastQuestion('sophia-eng-2022', 2022, 'デジタル時代における言語学習の変化と課題について述べなさい。', 90, '上智大学', '外国語学部', '英語学科'),
                                PastQuestion('sophia-eng-2021', 2021, '国際社会における英語の役割と他言語との共存について論じなさい。', 90, '上智大学', '外国語学部', '英語学科'),
                                PastQuestion('sophia-eng-2020', 2020, '異文化理解教育の重要性と実践方法について述べなさい。', 90, '上智大学', '外国語学部', '英語学科'),
                                PastQuestion('sophia-eng-2019', 2019, 'AI翻訳技術の発展が言語教育に与える影響について論じなさい。', 90, '上智大学', '外国語学部', '英語学科')
                            ]
                        )
                    ]
                )
            ]
        ),
        University(
            id='meiji',
            name='明治大学',
            faculties=[
                Faculty(
                    id='information',
                    name='情報コミュニケーション学部',
                    has_ao=True,
                    departments=[
                        Department(
                            id='information',
                            name='情報コミュニケーション学科',
                            has_ao=True,
                            past_questions=[
                                PastQuestion('meiji-info-2023', 2023, 'SNSが現代社会のコミュニケーションに与える影響について論じなさい。', 90, '明治大学', '情報コミュニケーション学部', '情報コミュニケーション学科'),
                                PastQuestion('meiji-info-2022', 2022, 'デジタルデバイドの解消に向けた取り組みについて述べなさい。', 90, '明治大学', '情報コミュニケーション学部', '情報コミュニケーション学科'),
                                PastQuestion('meiji-info-2021', 2021, 'メディアリテラシー教育の重要性と実践について論じなさい。', 90, '明治大学', '情報コミュニケーション学部', '情報コミュニケーション学科'),
                                PastQuestion('meiji-info-2020', 2020, '情報社会における個人のプライバシー保護について述べなさい。', 90, '明治大学', '情報コミュニケーション学部', '情報コミュニケーション学科'),
                                PastQuestion('meiji-info-2019', 2019, 'AI時代におけるヒューマンコミュニケーションの価値について論じなさい。', 90, '明治大学', '情報コミュニケーション学部', '情報コミュニケーション学科')
                            ]
                        )
                    ]
                )
            ]
        )
    ]

# AI機能：詳細採点システム
def detailed_essay_scoring(content: str, theme: str) -> dict:
    """AI搭載の詳細採点システム"""
    if not content.strip():
        return {
            "total": 0,
            "structure": {"score": 0, "evaluation": "文章が入力されていません。"},
            "content": {"score": 0, "evaluation": "内容が確認できません。"},
            "logic": {"score": 0, "evaluation": "論理性を評価できません。"},
            "expression": {"score": 0, "evaluation": "表現を評価できません。"},
            "detailed_feedback": "文章を入力してください。",
            "specific_advice": ["文章を入力して再度提出してください。"],
            "model_answer": ""
        }
    
    word_count = len(content.replace(' ', '').replace('\n', ''))
    paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
    sentences = [s.strip() for s in re.split(r'[。！？]', content) if s.strip()]
    
    # 構成評価
    structure_score, structure_eval = evaluate_structure(content, paragraphs)
    
    # 内容評価
    content_score, content_eval = evaluate_content(content, theme, word_count)
    
    # 論理性評価
    logic_score, logic_eval = evaluate_logic(content, sentences)
    
    # 表現評価
    expression_score, expression_eval = evaluate_expression(content, sentences, word_count)
    
    total_score = structure_score + content_score + logic_score + expression_score
    
    # 詳細フィードバック生成
    detailed_feedback = generate_detailed_feedback(total_score, structure_score, content_score, logic_score, expression_score)
    
    # 具体的アドバイス生成
    specific_advice = generate_specific_advice(content, structure_score, content_score, logic_score, expression_score)
    
    # 模範解答生成
    model_answer = generate_model_answer(theme)
    
    return {
        "total": total_score,
        "structure": {"score": structure_score, "evaluation": structure_eval},
        "content": {"score": content_score, "evaluation": content_eval},
        "logic": {"score": logic_score, "evaluation": logic_eval},
        "expression": {"score": expression_score, "evaluation": expression_eval},
        "detailed_feedback": detailed_feedback,
        "specific_advice": specific_advice,
        "model_answer": model_answer
    }

def evaluate_structure(content: str, paragraphs: List[str]) -> tuple:
    """構成評価"""
    score = 0
    evaluation_parts = []
    
    # 段落数評価
    if len(paragraphs) >= 4:
        score += 8
        evaluation_parts.append("適切な段落数（序論・本論・結論）が確保されています。")
    elif len(paragraphs) >= 3:
        score += 6
        evaluation_parts.append("基本的な三段構成が確認できます。")
    else:
        score += 2
        evaluation_parts.append("段落数が不足しています。序論・本論・結論の構成を明確にしてください。")
    
    # 序論の評価
    first_paragraph = paragraphs[0] if paragraphs else ""
    if any(keyword in first_paragraph for keyword in ['について', 'において', 'に関して', 'とは']):
        score += 5
        evaluation_parts.append("序論で適切な問題提起が行われています。")
    else:
        evaluation_parts.append("序論での問題提起をより明確にしてください。")
    
    # 結論の評価
    last_paragraph = paragraphs[-1] if paragraphs else ""
    if any(keyword in last_paragraph for keyword in ['よって', '従って', '以上', 'このように', '結論として']):
        score += 7
        evaluation_parts.append("結論部分で適切なまとめが行われています。")
    else:
        evaluation_parts.append("結論での主張のまとめをより明確にしてください。")
    
    # 文章の流れ評価
    if len(paragraphs) >= 3:
        middle_paragraphs = paragraphs[1:-1]
        if any(any(keyword in p for keyword in ['まず', '次に', 'さらに', '最後に']) for p in middle_paragraphs):
            score += 5
            evaluation_parts.append("論理的な順序立てが確認できます。")
    
    score = min(score, 25)
    evaluation = " ".join(evaluation_parts)
    
    return score, evaluation

def evaluate_content(content: str, theme: str, word_count: int) -> tuple:
    """内容評価"""
    score = 0
    evaluation_parts = []
    
    # 文字数評価
    if word_count >= 600:
        score += 8
        evaluation_parts.append("十分な文字数で詳細な論述が行われています。")
    elif word_count >= 400:
        score += 6
        evaluation_parts.append("適切な文字数で論述されています。")
    elif word_count >= 200:
        score += 4
        evaluation_parts.append("文字数は最低限ですが、もう少し詳細な論述が望ましいです。")
    else:
        evaluation_parts.append("文字数が不足しています。より詳細な論述を心がけてください。")
    
    # 具体例の評価
    example_keywords = ['例えば', '具体的に', 'たとえば', '実際に', '現実に']
    if any(keyword in content for keyword in example_keywords):
        score += 8
        evaluation_parts.append("具体例が適切に使用され、論証が強化されています。")
    else:
        evaluation_parts.append("具体例を追加して論証を強化してください。")
    
    # データ・数値の活用
    if re.search(r'\d+%|\d+人|\d+件|\d+年|\d+倍', content):
        score += 6
        evaluation_parts.append("数値やデータを用いた客観的な論証が見られます。")
    else:
        evaluation_parts.append("可能であれば統計データや数値を用いて論証を補強してください。")
    
    # テーマとの関連性
    theme_keywords = theme.split()[:3]  # テーマの最初の3語
    if any(keyword in content for keyword in theme_keywords):
        score += 8
        evaluation_parts.append("テーマに密接に関連した内容で論述されています。")
    else:
        evaluation_parts.append("テーマにより密接に関連した内容を心がけてください。")
    
    score = min(score, 30)
    evaluation = " ".join(evaluation_parts)
    
    return score, evaluation

def evaluate_logic(content: str, sentences: List[str]) -> tuple:
    """論理性評価"""
    score = 0
    evaluation_parts = []
    
    # 論理的接続詞の使用
    logical_connectors = ['そのため', 'なぜなら', '理由は', 'その結果', 'このことから', 'つまり', 'すなわち']
    connector_count = sum(content.count(connector) for connector in logical_connectors)
    
    if connector_count >= 3:
        score += 8
        evaluation_parts.append("豊富な論理的接続詞により、論理的な流れが明確です。")
    elif connector_count >= 2:
        score += 6
        evaluation_parts.append("論理的接続詞が適切に使用されています。")
    elif connector_count >= 1:
        score += 4
        evaluation_parts.append("論理的接続詞の使用が確認できますが、もう少し増やすとより効果的です。")
    else:
        evaluation_parts.append("論理的接続詞を使用して、文章の流れをより明確にしてください。")
    
    # 反対意見への言及
    counter_keywords = ['一方', 'しかし', 'ただし', 'もっとも', 'とはいえ', 'けれども']
    if any(keyword in content for keyword in counter_keywords):
        score += 8
        evaluation_parts.append("反対意見や異なる視点への言及があり、多角的な論述が行われています。")
    else:
        evaluation_parts.append("反対意見や異なる視点も考慮して、より多角的な論述を心がけてください。")
    
    # 因果関係の明確性
    causal_keywords = ['原因', '結果', '要因', '影響', '背景', '根拠']
    if sum(content.count(keyword) for keyword in causal_keywords) >= 2:
        score += 6
        evaluation_parts.append("因果関係が明確に示され、論理的な論証が行われています。")
    else:
        evaluation_parts.append("因果関係をより明確に示して、論証を強化してください。")
    
    # 論理の一貫性（重複や矛盾のチェック）
    if len(sentences) >= 5:
        score += 3
        evaluation_parts.append("適切な文数で論理的な展開が行われています。")
    
    score = min(score, 25)
    evaluation = " ".join(evaluation_parts)
    
    return score, evaluation

def evaluate_expression(content: str, sentences: List[str], word_count: int) -> tuple:
    """表現評価"""
    score = 0
    evaluation_parts = []
    
    # 文体の適切性
    if 'である' in content or 'だ。' in content:
        score += 5
        evaluation_parts.append("小論文に適した文体で書かれています。")
    else:
        evaluation_parts.append("小論文では「である調」の使用が推奨されます。")
    
    # 語彙の豊富さ
    unique_words = set(re.findall(r'[ぁ-んァ-ヶー一-龯]+', content))
    if len(unique_words) >= 100:
        score += 6
        evaluation_parts.append("豊富な語彙が使用され、表現力豊かな文章です。")
    elif len(unique_words) >= 70:
        score += 4
        evaluation_parts.append("適切な語彙が使用されています。")
    else:
        evaluation_parts.append("より多様な語彙を使用して表現力を向上させてください。")
    
    # 文の長さのバランス
    if sentences:
        avg_sentence_length = sum(len(s) for s in sentences) / len(sentences)
        if 30 <= avg_sentence_length <= 60:
            score += 4
            evaluation_parts.append("文の長さが適切で、読みやすい文章です。")
        else:
            evaluation_parts.append("文の長さを調整して、読みやすさを向上させてください。")
    
    # 重複表現のチェック
    repetitive_patterns = re.findall(r'(.{5,})\1', content)
    if not repetitive_patterns:
        score += 5
        evaluation_parts.append("重複表現がなく、簡潔で効果的な表現が使われています。")
    else:
        evaluation_parts.append("一部に重複表現が見られます。より多様な表現を心がけてください。")
    
    score = min(score, 20)
    evaluation = " ".join(evaluation_parts)
    
    return score, evaluation

def generate_detailed_feedback(total: int, structure: int, content: int, logic: int, expression: int) -> str:
    """詳細フィードバック生成"""
    if total >= 85:
        feedback = f"素晴らしい小論文です（{total}/100点）！全体的に高いレベルで論述されており、入試本番でも十分に通用する内容です。"
    elif total >= 70:
        feedback = f"良好な小論文です（{total}/100点）。基本的な要素は十分に満たされており、いくつかの改善点を修正することでさらに高い評価が期待できます。"
    elif total >= 55:
        feedback = f"標準的な小論文です（{total}/100点）。基本的な構成はできていますが、内容の深化と論理性の強化が必要です。"
    elif total >= 40:
        feedback = f"改善の余地があります（{total}/100点）。構成や論理展開を見直し、より具体的で説得力のある論述を心がけてください。"
    else:
        feedback = f"大幅な改善が必要です（{total}/100点）。小論文の基本的な書き方から見直し、構成・内容・論理性のすべての面で向上を図ってください。"
    
    # 各項目での強み・弱みを追加
    strengths = []
    weaknesses = []
    
    if structure >= 20: strengths.append("構成")
    elif structure < 15: weaknesses.append("構成")
    
    if content >= 24: strengths.append("内容")
    elif content < 18: weaknesses.append("内容")
    
    if logic >= 20: strengths.append("論理性")
    elif logic < 15: weaknesses.append("論理性")
    
    if expression >= 16: strengths.append("表現")
    elif expression < 12: weaknesses.append("表現")
    
    if strengths:
        feedback += f" 特に{'/'.join(strengths)}の面で優れています。"
    if weaknesses:
        feedback += f" {'/'.join(weaknesses)}の面での改善が重要です。"
    
    return feedback

def generate_specific_advice(content: str, structure: int, content_score: int, logic: int, expression: int) -> List[str]:
    """具体的アドバイス生成"""
    advice = []
    
    # 構成に関するアドバイス
    if structure < 20:
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
        if len(paragraphs) < 3:
            advice.append("【構成改善】序論・本論・結論の三段構成を明確にしてください。各段落の役割を意識して、序論で問題提起、本論で論証、結論でまとめを行いましょう。")
        
        first_paragraph = paragraphs[0] if paragraphs else ""
        if not any(keyword in first_paragraph for keyword in ['について', 'において', 'に関して']):
            advice.append("【序論改善】序論では「〜について」「〜において」などを使って、明確に問題提起を行ってください。例：『近年、デジタル化について様々な議論が行われている。』")
    
    # 内容に関するアドバイス
    if content_score < 24:
        if not any(keyword in content for keyword in ['例えば', '具体的に', 'たとえば']):
            advice.append("【内容強化】具体例を追加してください。『例えば、〜の場合、』『具体的には、』などを使って、実際の事例や体験を挙げると説得力が増します。")
        
        if not re.search(r'\d+%|\d+人|\d+件|\d+年', content):
            advice.append("【データ活用】可能な範囲で統計データや数値を含めてください。『約70%の企業が』『過去10年間で』などの表現により、客観性が向上します。")
    
    # 論理性に関するアドバイス
    if logic < 20:
        logical_connectors = ['そのため', 'なぜなら', 'その結果', 'このことから']
        if not any(connector in content for connector in logical_connectors):
            advice.append("【論理性向上】論理的接続詞を使用してください。『そのため』『なぜなら』『その結果』などにより、論理の流れを明確にしましょう。")
        
        if not any(keyword in content for keyword in ['一方', 'しかし', 'ただし']):
            advice.append("【多角的視点】反対意見にも触れてください。『一方で』『しかし』などを使って異なる立場の意見を紹介し、その上で自分の主張を展開すると説得力が高まります。")
    
    # 表現に関するアドバイス
    if expression < 16:
        if '思います' in content or '思う' in content:
            advice.append("【文体改善】小論文では『思う』ではなく『考える』『述べる』『論じる』などの表現を使用してください。また、『である調』で統一しましょう。")
        
        sentences = [s.strip() for s in re.split(r'[。！？]', content) if s.strip()]
        if sentences:
            avg_length = sum(len(s) for s in sentences) / len(sentences)
            if avg_length < 20:
                advice.append("【文章構成】文がやや短すぎます。修飾語や具体例を加えて、より詳細で豊かな表現を心がけてください。")
            elif avg_length > 80:
                advice.append("【文章構成】文が長すぎて読みにくくなっています。適切な箇所で文を分割し、読みやすさを向上させてください。")
    
    # 全体的なアドバイス
    word_count = len(content.replace(' ', '').replace('\n', ''))
    if word_count < 400:
        advice.append("【文字数】もう少し詳細な論述を心がけてください。根拠の説明や具体例の詳細化により、文字数と説得力の両方を向上させることができます。")
    
    return advice

def generate_model_answer(theme: str) -> str:
    """AIによる模範解答生成"""
    # テーマに基づいて模範解答を生成
    model_answers = {
        "デジタル": """【模範解答例】
現代社会におけるデジタル化の進展は、我々の生活様式を根本的に変革している。この変化について、その意義と課題を多角的に検討する必要がある。

まず、デジタル化の利点として、情報アクセスの平等化が挙げられる。例えば、オンライン教育プラットフォームにより、地理的制約を超えた学習機会が提供されている。実際に、コロナ禍において多くの教育機関がオンライン授業を導入し、教育の継続性を保つことができた。

一方で、デジタルデバイドという課題も存在する。高齢者や低所得世帯において、デジタル技術へのアクセスが制限される場合がある。この問題に対しては、政府や自治体による支援策の充実が不可欠である。

さらに、プライバシー保護とイノベーションのバランスも重要な論点である。企業がデータを活用してサービスを向上させる一方で、個人情報の適切な管理が求められる。

このように、デジタル化は多大な恩恵をもたらす一方で、社会的課題も生み出している。重要なことは、技術の発展と人間中心の価値観を両立させる社会システムの構築である。""",
        
        "AI": """【模範解答例】
人工知能（AI）の急速な発達は、21世紀最大の技術革新として社会のあらゆる分野に影響を与えている。この変革について、その可能性と課題を総合的に検討したい。

AIの最大の利点は、人間の能力を拡張し、効率性を向上させることである。医療分野では、AI診断システムにより早期発見率が向上し、多くの生命が救われている。また、自動運転技術の発展により、交通事故の大幅な減少が期待されている。

しかし、雇用への影響という深刻な課題も存在する。単純作業の自動化により、一部の職種が失われる可能性がある。この問題に対しては、リスキリング（再教育）プログラムの充実や、新たな価値創造分野での雇用創出が重要である。

さらに、AI判断の透明性と責任の所在も重要な論点である。金融や司法などの重要な判断にAIが関与する場合、その決定プロセスの説明可能性が求められる。

結論として、AIと人間の共存には、技術的進歩と倫理的配慮の両立が不可欠である。AIを脅威として捉えるのではなく、人間性を尊重しながら技術を活用する社会の実現を目指すべきである。""",
        
        "持続可能": """【模範解答例】
持続可能な社会の実現は、現代社会が直面する最重要課題の一つである。環境保護と経済発展の両立について、多面的な検討を行いたい。

持続可能性の核心は、将来世代のニーズを損なうことなく、現在のニーズを満たすことである。この観点から、まず環境負荷の削減が不可欠である。例えば、再生可能エネルギーの普及により、CO2排出量の大幅な削減が可能となる。実際に、太陽光発電コストの低下により、多くの国で導入が進んでいる。

一方で、急激な環境政策の実施は経済活動に負の影響を与える可能性がある。このため、段階的な移行計画と企業への支援制度が重要である。例えば、炭素税の導入と同時に、グリーン技術への投資支援を行う政策が効果的である。

また、消費者の意識変革も欠かせない要素である。持続可能な商品の選択や、循環型消費行動の定着により、市場メカニズムを通じた変化が促進される。

このように、持続可能な社会の実現には、政府・企業・市民の協働が不可欠である。短期的な利益にとらわれず、長期的視点に立った社会設計を進めることが、我々に求められている責務である。"""
    }
    
    # テーマに最も関連する模範解答を選択
    for key, answer in model_answers.items():
        if key in theme:
            return answer
    
    # デフォルトの模範解答
    return """【模範解答例】
現代社会は急速な変化の中にあり、多様な課題と可能性が併存している。本テーマについて、その意義と課題を多角的に検討したい。

まず、この問題の重要性について述べる。社会の変化は、我々の生活様式や価値観に大きな影響を与えている。例えば、技術の発展により新たな機会が生まれる一方で、従来の制度や慣習との間に摩擦が生じている。

一方で、この変化には課題も伴う。急激な変化は社会の一部に負の影響をもたらし、格差の拡大や不安の増大を招く可能性がある。このため、変化のメリットを最大化しつつ、負の影響を最小限に抑制する政策的配慮が重要である。

さらに、持続可能な発展の観点から、長期的視点に立った取り組みが必要である。短期的な利益にとらわれることなく、将来世代への責任を考慮した意思決定が求められる。

結論として、現代社会の課題解決には、多様な立場の人々が協働し、バランスの取れた議論を通じて最適解を見出すことが重要である。変化を恐れるのではなく、積極的に向き合い、より良い社会の実現を目指すべきである。"""

# AI問題予想機能
def ai_generate_question(past_questions: List[PastQuestion], university: str, faculty: str, department: str) -> str:
    """AIによる問題予想"""
    
    # 過去問題からキーワードを抽出
    themes = [q.theme for q in past_questions]
    all_themes_text = " ".join(themes)
    
    # トレンドキーワードの定義
    current_trends = [
        'デジタル変革', 'AI・機械学習', '持続可能性', 'カーボンニュートラル',
        'ダイバーシティ', 'インクルージョン', '働き方改革', 'ウェルビーイング',
        'グローバル化', 'ローカライゼーション', 'イノベーション', 'スタートアップ',
        'サーキュラーエコノミー', 'SDGs', 'ESG経営', 'リスキリング',
        'メンタルヘルス', 'デジタルデバイド', 'サイバーセキュリティ', '量子コンピュータ'
    ]
    
    # 学部・学科別のコンテキスト
    domain_contexts = {
        '政治': ['民主主義', '政策立案', '国際関係', '公共政策', '行政改革', '地方創生'],
        '経済': ['市場経済', '金融政策', '産業構造', '労働市場', '国際貿易', '経済格差'],
        '法': ['法制度', '人権保護', '司法制度', '国際法', '企業法務', '憲法改正'],
        '商': ['企業経営', 'マーケティング', 'ビジネスモデル', '起業', 'イノベーション', 'ESG'],
        '外国語': ['国際コミュニケーション', '多言語社会', '異文化理解', '言語教育', '翻訳技術'],
        '情報': ['情報社会', 'デジタル技術', 'メディア', 'コミュニケーション', 'プライバシー'],
        '教養': ['人文学', '学際研究', '批判的思考', '文化研究', '社会科学', '総合知']
    }
    
    # 学部・学科に関連するコンテキストを特定
    relevant_contexts = []
    for key, contexts in domain_contexts.items():
        if key in faculty or key in department:
            relevant_contexts.extend(contexts)
    
    if not relevant_contexts:
        relevant_contexts = ['社会', '現代', '課題', '解決策', '将来展望']
    
    # トレンドとコンテキストを組み合わせて問題を生成
    selected_trend = random.choice(current_trends)
    selected_context = random.choice(relevant_contexts)
    
    # 過去問題のスタイルを分析
    question_styles = [
        f"{selected_trend}が{selected_context}分野に与える影響について、具体例を挙げながら論じなさい。また、今後の課題と解決策についてもあなたの考えを述べなさい。",
        f"現代社会における{selected_trend}の意義を踏まえ、{selected_context}の観点から将来のあるべき姿について論じなさい。",
        f"{selected_trend}の進展により{selected_context}分野で生じている変化について分析し、それに対する適切な対応策を提言しなさい。",
        f"{selected_trend}と{selected_context}の関係性について考察し、持続可能な社会の実現に向けた方策を論じなさい。",
        f"グローバル化が進む中で{selected_trend}が{selected_context}に与える影響について、メリットとデメリットを比較検討し、今後の方向性を述べなさい。"
    ]
    
    return random.choice(question_styles)

# 大学検索機能
def search_universities(query: str, universities: List[University]) -> List[University]:
    """大学検索機能"""
    if not query:
        return universities
    
    query_lower = query.lower()
    filtered = []
    
    for uni in universities:
        # 大学名での検索
        if query_lower in uni.name.lower():
            filtered.append(uni)
            continue
        
        # 学部名での検索
        for faculty in uni.faculties:
            if query_lower in faculty.name.lower():
                filtered.append(uni)
                break
        
        # 学科名での検索
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
    st.title("🤖 AI搭載 総合選抜型入試 小論文対策アプリ")
    st.markdown("### 最新AI技術による詳細評価・具体的アドバイス・模範解答生成")
    
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
    
    # サイドバー
    with st.sidebar:
        st.header("🧭 ナビゲーション")
        
        if st.button("🏠 ホームに戻る", key="home_btn"):
            reset_all_state()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 現在の状態")
        
        if st.session_state.page == 'selection':
            st.info("🔍 大学・学部選択中")
        elif st.session_state.page == 'writing':
            st.info("✍️ AI小論文練習中")
        elif st.session_state.page == 'result':
            st.info("📈 AI詳細評価表示中")
        
        # 検索履歴の表示
        if st.session_state.search_history:
            st.markdown("### 🕒 検索履歴")
            for i, search_term in enumerate(reversed(st.session_state.search_history[-5:])):
                if st.button(f"📚 {search_term}", key=f"history_{i}"):
                    st.session_state.quick_search = search_term
                    st.rerun()
    
    # メインコンテンツ
    if st.session_state.page == 'selection':
        show_advanced_university_selection()
    elif st.session_state.page == 'writing':
        show_ai_essay_editor()
    elif st.session_state.page == 'result':
        show_detailed_results()

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

def show_advanced_university_selection():
    """高度な大学選択画面"""
    st.header("🎯 AI大学検索・学部学科選択システム")
    
    universities = get_universities()
    
    # 大学検索
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # クイック検索があるかチェック
        default_search = ""
        if 'quick_search' in st.session_state:
            default_search = st.session_state.quick_search
            del st.session_state.quick_search
        
        search_query = st.text_input(
            "🔍 大学名・学部名・学科名で検索", 
            value=default_search,
            placeholder="例: 早稲田、政治経済、情報コミュニケーション",
            key="search_input"
        )
    
    with col2:
        if st.button("🔍 検索実行", key="search_btn"):
            if search_query and search_query not in st.session_state.search_history:
                st.session_state.search_history.append(search_query)
            st.rerun()
    
    # 検索結果の表示
    if search_query:
        filtered_universities = search_universities(search_query, universities)
        
        if filtered_universities:
            st.success(f"🎯 検索結果: {len(filtered_universities)}件の大学が見つかりました")
            
            # 大学選択
            uni_options = ["選択してください"] + [uni.name for uni in filtered_universities]
            selected_uni_name = st.selectbox("📚 大学を選択", uni_options, key="uni_select")
            
            if selected_uni_name != "選択してください":
                selected_university = next(uni for uni in filtered_universities if uni.name == selected_uni_name)
                st.session_state.selected_university = selected_university
                
                # 選択された大学の詳細情報
                with st.expander(f"📖 {selected_university.name} の詳細情報", expanded=True):
                    st.markdown(f"**AO入試対応学部数:** {len([f for f in selected_university.faculties if f.has_ao])}学部")
                    
                    for faculty in selected_university.faculties:
                        if faculty.has_ao:
                            st.markdown(f"• **{faculty.name}**")
                            ao_depts = [d for d in faculty.departments if d.has_ao]
                            for dept in ao_depts:
                                st.markdown(f"  - {dept.name} (過去問題: {len(dept.past_questions)}件)")
                
                # 学部選択
                ao_faculties = [fac for fac in selected_university.faculties if fac.has_ao]
                if ao_faculties:
                    st.markdown(f"### 🏛️ {selected_university.name} - AO入試対応学部")
                    
                    fac_options = ["選択してください"] + [fac.name for fac in ao_faculties]
                    selected_fac_name = st.selectbox("学部を選択", fac_options, key="fac_select")
                    
                    if selected_fac_name != "選択してください":
                        selected_faculty = next(fac for fac in ao_faculties if fac.name == selected_fac_name)
                        st.session_state.selected_faculty = selected_faculty
                        
                        # 学科選択
                        ao_departments = [dept for dept in selected_faculty.departments if dept.has_ao]
                        if ao_departments:
                            st.markdown(f"### 🎓 {selected_faculty.name} - AO入試対応学科")
                            
                            dept_options = ["選択してください"] + [dept.name for dept in ao_departments]
                            selected_dept_name = st.selectbox("学科を選択", dept_options, key="dept_select")
                            
                            if selected_dept_name != "選択してください":
                                selected_department = next(dept for dept in ao_departments if dept.name == selected_dept_name)
                                st.session_state.selected_department = selected_department
                                
                                # 過去5年分のテーマ表示
                                st.markdown(f"#### 📝 {selected_department.name} - 過去5年の出題テーマ")
                                
                                if selected_department.past_questions:
                                    # 年度順に並び替え
                                    sorted_questions = sorted(selected_department.past_questions, key=lambda x: x.year, reverse=True)
                                    
                                    for i, q in enumerate(sorted_questions):
                                        with st.expander(f"📅 {q.year}年度 ({q.time_limit}分)", expanded=(i < 2)):
                                            st.write(q.theme)
                                            if i < 2:  # 最新2件は詳細表示
                                                st.info(f"💡 この問題の特徴: テーマ '{q.theme[:15]}...' は{q.year}年の社会情勢を反映した出題です。")
                                
                                # AI問題予想・練習開始
                                st.markdown("---")
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.metric("📊 分析データ", f"過去{len(selected_department.past_questions)}年分")
                                
                                with col2:
                                    st.metric("⏱️ 想定時間", f"{selected_department.past_questions[0].time_limit}分" if selected_department.past_questions else "90分")
                                
                                if st.button("🤖 AI予想問題で練習開始", type="primary", key="ai_start_btn"):
                                    with st.spinner("🧠 AI が過去5年のデータを分析して予想問題を生成中..."):
                                        time.sleep(2)  # AI処理をシミュレート
                                        ai_question = ai_generate_question(
                                            selected_department.past_questions,
                                            selected_university.name,
                                            selected_faculty.name,
                                            selected_department.name
                                        )
                                        st.session_state.current_question = ai_question
                                        st.session_state.page = 'writing'
                                        st.success("✨ AI予想問題を生成しました！")
                                        time.sleep(1)
                                        st.rerun()
                else:
                    st.warning("この大学にはAO入試対応学部がありません。")
        else:
            st.warning("🚫 該当する大学が見つかりませんでした。検索条件を変更してお試しください。")
    else:
        # 検索前の全大学表示
        st.info("💡 上記の検索ボックスで大学名・学部名・学科名を検索できます")
        
        st.markdown("### 📚 利用可能な大学一覧")
        for uni in universities:
            ao_faculty_count = len([f for f in uni.faculties if f.has_ao])
            with st.expander(f"{uni.name} (AO対応: {ao_faculty_count}学部)", expanded=False):
                for faculty in uni.faculties:
                    if faculty.has_ao:
                        ao_dept_count = len([d for d in faculty.departments if d.has_ao])
                        st.markdown(f"**{faculty.name}** ({ao_dept_count}学科)")
                        for dept in faculty.departments:
                            if dept.has_ao:
                                st.markdown(f"  • {dept.name} - 過去問題{len(dept.past_questions)}件")

def show_ai_essay_editor():
    """AI小論文エディター画面"""
    if not st.session_state.current_question:
        st.error("問題が設定されていません。")
        return
    
    st.header("🤖 AI小論文練習システム")
    
    # AI生成問題の表示
    st.markdown("### 🧠 AI予想問題")
    
    # 問題生成の説明
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.info(st.session_state.current_question)
    
    with col2:
        if st.button("🔄 新しい予想問題", key="new_question_btn"):
            with st.spinner("🤖 新しい予想問題を生成中..."):
                time.sleep(1)
                new_question = ai_generate_question(
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
        
    st.markdown(f"**📋 出題条件:** 制限時間 {time_limit}分 | 推奨文字数 600-1000字 | AI詳細評価対象")
    
    # AI分析情報
    with st.expander("🔍 この予想問題のAI分析", expanded=False):
        st.markdown(f"""
        **🎯 分析結果:**
        - 過去5年の出題傾向から生成された最新予想問題
        - 現在のトレンドキーワードを組み込み済み
        - {st.session_state.selected_faculty.name}の専門性を考慮
        - 入試本番レベルの難易度に調整
        """)
    
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
            if st.button("📖 書き方ガイド", key="guide_btn"):
                show_writing_guide_modal()
        
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
                if remaining_time <= 300:  # 5分以下
                    st.warning("⚠️ 残り時間わずかです！")
            else:
                st.metric("⏰ 残り時間", "終了")
                st.error("⏰ 制限時間終了！提出してください")
        
        with col4:
            progress = min(elapsed_time / (time_limit * 60), 1.0)
            st.metric("📊 進行度", f"{int(progress * 100)}%")
    else:
        st.info("⏱️ タイマーなしモードで練習中")
    
    # AI小論文エディター
    st.markdown("### ✍️ AI小論文エディター")
    
    essay_content = st.text_area(
        "📝 ここに小論文を書いてください（AIが文体・構成・論理性をリアルタイム分析）",
        value=st.session_state.essay_content,
        height=400,
        placeholder="小論文をここに入力してください...\n\n💡 AIからのヒント:\n- 序論で明確な問題提起を行う\n- 本論で具体例と論拠を示す\n- 結論で主張をまとめる",
        key="ai_essay_textarea"
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
        
        # 進捗インジケーター
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
    
    # AI簡易分析（プレビュー）
    if word_count >= 100:
        with st.expander("🤖 AI簡易分析プレビュー", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                has_examples = any(kw in current_content for kw in ['例えば', '具体的に', 'たとえば'])
                st.metric("具体例", "✓" if has_examples else "✗")
            
            with col2:
                has_logic = any(kw in current_content for kw in ['そのため', 'なぜなら', 'このため'])
                st.metric("論理接続", "✓" if has_logic else "✗")
            
            with col3:
                has_counter = any(kw in current_content for kw in ['一方', 'しかし', 'ただし'])
                st.metric("多角的視点", "✓" if has_counter else "✗")
    
    # 提出ボタン
    min_chars = 100
    can_submit = word_count >= min_chars
    
    if not can_submit:
        st.warning(f"⚠️ 提出には最低{min_chars}文字必要です（現在: {word_count}文字）")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🤖 AI詳細評価で提出", type="primary", disabled=not can_submit, key="ai_submit_btn"):
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

def show_writing_guide_modal():
    """書き方ガイドモーダル"""
    st.markdown("### 📖 小論文書き方ガイド")
    
    guide_tabs = st.tabs(["📋 構成", "💡 内容", "✏️ 表現", "📝 例文"])
    
    with guide_tabs[0]:
        st.markdown("""
        #### 小論文の基本構成
        
        **1. 序論（全体の20%）**
        - 問題提起：「〜について」「〜において」
        - 論点の明確化
        - 自分の立場の表明
        
        **2. 本論（全体の60%）**
        - 根拠の提示：「なぜなら」「理由は」
        - 具体例・データの活用：「例えば」「実際に」
        - 反対意見への言及：「一方で」「しかし」
        
        **3. 結論（全体の20%）**
        - 論点の整理：「以上のように」
        - 主張の再確認：「このように」
        - 今後の展望：「今後は」
        """)
    
    with guide_tabs[1]:
        st.markdown("""
        #### 説得力のある内容の作り方
        
        **具体例の活用**
        - 身近で理解しやすい事例
        - 時事的な話題の引用
        - 複数の視点からの事例
        
        **データの活用**
        - 「約70%の」「過去10年で」
        - 信頼できるソースの引用
        - 比較可能なデータの提示
        
        **専門性の表現**
        - 学部・学科に関連した専門用語
        - 学術的な視点からの分析
        - 最新の研究動向への言及
        """)
    
    with guide_tabs[2]:
        st.markdown("""
        #### 適切な表現技法
        
        **文体の統一**
        - 「である調」で統一
        - 敬語は使わない
        - 一人称は「私」を使用
        
        **避けるべき表現**
        - 「〜と思う」→「〜と考える」
        - 「〜かもしれない」→「〜と推測される」
        - 「絶対に」「必ず」→断定を避ける
        
        **効果的な表現**
        - 比喩や例え話の活用
        - 問いかけによる関心喚起
        - 対比による論点の明確化
        """)
    
    with guide_tabs[3]:
        st.markdown("""
        #### 高評価を得る文章例
        
        **序論の例**
        ```
        現代社会におけるデジタル化の進展は、我々の生活様式を
        根本的に変革している。この変化について、その意義と
        課題を多角的に検討する必要がある。
        ```
        
        **本論の例**
        ```
        まず、デジタル化の利点として、情報アクセスの平等化が
        挙げられる。例えば、オンライン教育により地理的制約を
        超えた学習機会が提供されている。一方で、デジタル
        デバイドという課題も存在する。
        ```
        
        **結論の例**
        ```
        このように、デジタル化は多大な恩恵をもたらす一方で、
        社会的課題も生み出している。重要なことは、技術の発展と
        人間中心の価値観を両立させることである。
        ```
        """)

def show_detailed_results():
    """AI詳細評価結果画面"""
    st.header("🤖 AI詳細評価結果")
    
    # AI採点実行
    if st.session_state.essay_score is None:
        with st.spinner("🧠 AI が詳細分析中... 構成・内容・論理性・表現を多角的に評価しています"):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
            
            st.session_state.essay_score = detailed_essay_scoring(
                st.session_state.essay_content, 
                st.session_state.current_question
            )
            progress_bar.empty()
    
    score = st.session_state.essay_score
    
    # 総合評価ヘッダー
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("### 🎯 AI総合評価")
        st.metric("📊 総合点数", f"{score['total']}/100点", 
                 delta=f"{score['total'] - 60}/60点 (平均比)" if score['total'] >= 60 else None)
        
        # 評価グレード
        if score['total'] >= 90:
            grade, color, comment = "S", "#9d4edd", "最優秀"
        elif score['total'] >= 80:
            grade, color, comment = "A", "#22c55e", "優秀"
        elif score['total'] >= 70:
            grade, color, comment = "B", "#eab308", "良好"
        elif score['total'] >= 60:
            grade, color, comment = "C", "#f97316", "普通"
        elif score['total'] >= 50:
            grade, color, comment = "D", "#ef4444", "要改善"
        else:
            grade, color, comment = "F", "#dc2626", "不合格"
        
        st.markdown(f"<h1 style='color: {color}'>評価: {grade}（{comment}）</h1>", unsafe_allow_html=True)
    
    with col2:
        # 偏差値風表示
        estimated_rank = min(80, max(20, score['total'] - 20))
        st.metric("📈 推定偏差値", f"{estimated_rank}")
        
        # 合格可能性
        if score['total'] >= 80:
            pass_rate = "95%以上"
            pass_color = "green"
        elif score['total'] >= 70:
            pass_rate = "80-90%"
            pass_color = "green"
        elif score['total'] >= 60:
            pass_rate = "60-70%"
            pass_color = "orange"
        else:
            pass_rate = "40%以下"
            pass_color = "red"
        
        st.metric("🎯 合格可能性", pass_rate)
    
    with col3:
        # 所要時間・効率性
        if st.session_state.start_time:
            elapsed = time.time() - st.session_state.start_time
            efficiency = score['total'] / max(elapsed / 60, 1)  # 点数/分
            st.metric("⚡ 効率性", f"{efficiency:.1f}点/分")
        
        word_count = len(st.session_state.essay_content.replace(' ', '').replace('\n', ''))
        st.metric("📝 文字効率", f"{score['total'] / max(word_count, 1) * 100:.1f}点/100字")
    
    # 詳細スコア分析
    st.markdown("### 📊 AI詳細スコア分析")
    
    score_data = [
        ("📋 構成", score['structure']['score'], 25, score['structure']['evaluation']),
        ("💡 内容", score['content']['score'], 30, score['content']['evaluation']),
        ("🔗 論理性", score['logic']['score'], 25, score['logic']['evaluation']),
        ("✏️ 表現", score['expression']['score'], 20, score['expression']['evaluation'])
    ]
    
    for emoji_name, score_val, max_val, evaluation in score_data:
        col1, col2 = st.columns([1, 2])
        
        with col1:
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
        
        with col2:
            st.markdown(f"**AI評価:** {evaluation}")
    
    # AI詳細フィードバック
    st.markdown("### 🤖 AI詳細フィードバック")
    st.info(score['detailed_feedback'])
    
    # 具体的改善アドバイス
    if score['specific_advice']:
        st.markdown("### 💡 AI具体的改善アドバイス")
        for i, advice in enumerate(score['specific_advice'], 1):
            st.markdown(f"**{i}.** {advice}")
    
    # AI模範解答
    if score['model_answer']:
        with st.expander("📖 AI生成模範解答", expanded=False):
            st.markdown("**💡 このテーマに対するAI模範解答例:**")
            st.markdown(score['model_answer'])
            st.warning("⚠️ これはAIが生成した参考例です。実際の入試では自分の言葉で表現することが重要です。")
    
    # 作成情報・統計
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 作成統計情報")
        word_count = len(st.session_state.essay_content.replace(' ', '').replace('\n', ''))
        st.write(f"**📝 総文字数:** {word_count}文字")
        
        paragraphs = len([p for p in st.session_state.essay_content.split('\n') if p.strip()])
        st.write(f"**📑 段落数:** {paragraphs}段落")
        
        sentences = len([s for s in re.split(r'[。！？]', st.session_state.essay_content) if s.strip()])
        st.write(f"**📄 文数:** {sentences}文")
        
        if st.session_state.start_time:
            elapsed_time = time.time() - st.session_state.start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            st.write(f"**⏱️ 所要時間:** {minutes}分{seconds}秒")
        else:
            st.write("**⏱️ 所要時間:** タイマー未使用")
    
    with col2:
        st.markdown("### 🏫 出題情報")
        if st.session_state.selected_university:
            st.write(f"**🏛️ 大学:** {st.session_state.selected_university.name}")
            st.write(f"**📚 学部:** {st.session_state.selected_faculty.name}")
            st.write(f"**🎓 学科:** {st.session_state.selected_department.name}")
        
        st.write("**🤖 問題生成:** AI予想問題")
        st.write("**📊 評価方式:** AI詳細分析")
        st.write(f"**📅 実施日:** {datetime.now().strftime('%Y年%m月%d日')}")
    
    # あなたの解答表示
    with st.expander("📄 あなたの解答を確認", expanded=False):
        st.markdown("#### 🎯 出題テーマ")
        st.write(st.session_state.current_question)
        st.markdown("#### ✍️ あなたの解答内容")
        st.text_area("", value=st.session_state.essay_content, height=200, disabled=True)
    
    # アクションボタン
    st.markdown("### 🎯 次のアクション")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 同じ問題で再挑戦", key="retry_same"):
            st.session_state.page = 'writing'
            st.session_state.essay_content = ""
            st.session_state.essay_score = None
            st.session_state.timer_started = False
            st.session_state.start_time = None
            st.rerun()
    
    with col2:
        if st.button("🤖 新しいAI予想問題", key="new_ai_question"):
            with st.spinner("🧠 新しい予想問題を生成中..."):
                time.sleep(1)
                new_question = ai_generate_question(
                    st.session_state.selected_department.past_questions,
                    st.session_state.selected_university.name,
                    st.session_state.selected_faculty.name,
                    st.session_state.selected_department.name
                )
                st.session_state.current_question = new_question
                st.session_state.page = 'writing'
                st.session_state.essay_content = ""
                st.session_state.essay_score = None
                st.session_state.timer_started = False
                st.session_state.start_time = None
                st.rerun()
    
    with col3:
        if st.button("🏛️ 別の大学で練習", key="change_university"):
            reset_all_state()
            st.rerun()
    
    with col4:
        if st.button("📊 結果をダウンロード", key="download_result"):
            # 結果をテキスト形式で生成
            result_text = f"""
AI小論文評価結果

【基本情報】
大学: {st.session_state.selected_university.name if st.session_state.selected_university else 'N/A'}
学部: {st.session_state.selected_faculty.name if st.session_state.selected_faculty else 'N/A'}  
学科: {st.session_state.selected_department.name if st.session_state.selected_department else 'N/A'}
実施日: {datetime.now().strftime('%Y年%m月%d日')}

【評価結果】
総合点数: {score['total']}/100点
- 構成: {score['structure']['score']}/25点
- 内容: {score['content']['score']}/30点  
- 論理性: {score['logic']['score']}/25点
- 表現: {score['expression']['score']}/20点

【AI評価】
{score['detailed_feedback']}

【出題テーマ】
{st.session_state.current_question}

【解答内容】
{st.session_state.essay_content}
            """
            
            st.download_button(
                label="📄 評価結果をダウンロード",
                data=result_text,
                file_name=f"essay_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()