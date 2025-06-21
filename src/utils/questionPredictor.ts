import { PastQuestion, PredictedQuestion } from '../types';

export const generatePredictedQuestion = (
  pastQuestions: PastQuestion[],
  university: string,
  faculty: string,
  department: string
): PredictedQuestion => {
  const themes = pastQuestions.map(q => q.theme);
  const timeLimit = pastQuestions[0]?.timeLimit || 90;
  
  const currentTrends = [
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
  ];

  const subjectContexts = {
    '政治': ['民主主義', '政策', '国際関係', '社会制度', '公共政策'],
    '経済': ['経済成長', '市場', '金融', 'グローバル経済', '産業構造'],
    '法': ['法の支配', '人権', '司法制度', '国際法', '社会規範'],
    '文学': ['表現', '文化', 'コミュニケーション', '芸術', '言語'],
    '教育': ['学習', '人材育成', '教育制度', '知識社会', '生涯学習'],
    '医学': ['健康', '医療技術', '予防医学', '高齢化', '医療倫理'],
    '工学': ['技術革新', 'ものづくり', '環境技術', 'インフラ', 'デザイン'],
    '理学': ['科学技術', '研究', '発見', '自然科学', 'データサイエンス']
  };

  const getRelevantContexts = (facultyName: string, departmentName: string): string[] => {
    const contexts: string[] = [];
    
    Object.entries(subjectContexts).forEach(([key, values]) => {
      if (facultyName.includes(key) || departmentName.includes(key)) {
        contexts.push(...values);
      }
    });
    
    return contexts.length > 0 ? contexts : ['社会', '現代', '課題', '解決策', '将来'];
  };

  const relevantContexts = getRelevantContexts(faculty, department);
  
  const trendKeyword = currentTrends[Math.floor(Math.random() * currentTrends.length)];
  const contextKeyword = relevantContexts[Math.floor(Math.random() * relevantContexts.length)];
  
  const questionTemplates = [
    `${trendKeyword}が進む現代において、${contextKeyword}はどのような課題に直面し、どのような解決策が考えられるか、具体例を挙げて論じなさい。`,
    `${trendKeyword}の発展が${contextKeyword}に与える影響について、メリットとデメリットを比較検討し、今後の在り方を論じなさい。`,
    `現代社会における${trendKeyword}の重要性を踏まえ、${contextKeyword}の分野でどのような革新が必要か、あなたの考えを述べなさい。`,
    `${trendKeyword}を背景とした社会変化の中で、${contextKeyword}が果たすべき役割と課題について論じなさい。`,
    `${trendKeyword}と${contextKeyword}の関係性を分析し、持続可能な社会の実現に向けた提言を行いなさい。`
  ];

  const selectedTemplate = questionTemplates[Math.floor(Math.random() * questionTemplates.length)];

  return {
    id: `predicted-${Date.now()}`,
    theme: selectedTemplate,
    timeLimit,
    generatedAt: new Date(),
    basedOnQuestions: pastQuestions.map(q => q.id),
    university,
    faculty,
    department
  };
};