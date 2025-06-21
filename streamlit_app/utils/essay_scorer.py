import re
from typing import List
from data.models import EssayScore

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