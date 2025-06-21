import random
from datetime import datetime
from typing import List
from data.models import PastQuestion, PredictedQuestion

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