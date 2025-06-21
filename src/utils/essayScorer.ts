import { EssayScore } from '../types';

export const scoreEssay = async (content: string, theme: string): Promise<EssayScore> => {
  const wordCount = content.replace(/\s/g, '').length;
  const paragraphs = content.split('\n').filter(p => p.trim().length > 0);
  
  let structureScore = 0;
  let contentScore = 0;
  let logicScore = 0;
  let expressionScore = 0;
  
  const feedback: string[] = [];
  const suggestions: string[] = [];

  if (wordCount < 100) {
    feedback.push('文字数が不足しています。より詳細な論述が必要です。');
    suggestions.push('具体例や根拠を追加して、論述を充実させてください。');
  } else if (wordCount > 1200) {
    feedback.push('文字数が多すぎます。要点を絞って簡潔に論述してください。');
    suggestions.push('重要なポイントに焦点を当て、冗長な表現を削除してください。');
  }

  if (paragraphs.length >= 3) {
    structureScore += 15;
    feedback.push('適切な段落構成が確認できます。');
  } else {
    structureScore += 5;
    feedback.push('段落構成を改善する必要があります。序論・本論・結論の構成を意識してください。');
    suggestions.push('序論で問題提起、本論で論証、結論でまとめという構成を心がけてください。');
  }

  const hasIntroduction = content.includes('について') || content.includes('において') || content.includes('に関して');
  const hasConclusion = content.includes('よって') || content.includes('従って') || content.includes('以上') || content.includes('このように');
  
  if (hasIntroduction) {
    structureScore += 5;
  } else {
    suggestions.push('序論で明確な問題提起を行ってください。');
  }
  
  if (hasConclusion) {
    structureScore += 5;
  } else {
    suggestions.push('結論部分で自分の主張を明確にまとめてください。');
  }

  const hasExamples = content.includes('例えば') || content.includes('具体的に') || content.includes('たとえば');
  const hasData = /\d+%|\d+人|\d+件|\d+年/.test(content);
  
  if (hasExamples) {
    contentScore += 10;
    feedback.push('具体例が適切に使用されています。');
  } else {
    suggestions.push('具体例を挙げて論証を強化してください。');
  }
  
  if (hasData) {
    contentScore += 10;
    feedback.push('データや数値を用いた客観的な論証が見られます。');
  } else {
    suggestions.push('可能であれば、統計データや数値を用いて論証を補強してください。');
  }

  const hasCounterArgument = content.includes('一方') || content.includes('しかし') || content.includes('ただし') || content.includes('もっとも');
  if (hasCounterArgument) {
    contentScore += 5;
    logicScore += 10;
    feedback.push('反対意見への言及が見られ、多角的な視点が示されています。');
  } else {
    suggestions.push('反対意見にも触れ、より多角的な論述を心がけてください。');
  }

  const logicalConnectors = ['そのため', 'なぜなら', '理由は', 'その結果', 'このことから'];
  const connectorCount = logicalConnectors.reduce((count, connector) => {
    return count + (content.match(new RegExp(connector, 'g')) || []).length;
  }, 0);
  
  if (connectorCount >= 2) {
    logicScore += 15;
    feedback.push('論理的な接続詞が適切に使用されています。');
  } else {
    logicScore += 5;
    suggestions.push('「そのため」「なぜなら」などの接続詞を使って論理的な流れを明確にしてください。');
  }

  const repetitivePatterns = content.match(/(.{10,})\1/g);
  if (repetitivePatterns && repetitivePatterns.length > 2) {
    expressionScore += 5;
    feedback.push('表現に重複が見られます。より多様な表現を心がけてください。');
  } else {
    expressionScore += 15;
  }

  const complexSentences = content.match(/[。]{1}[^。]{50,}/g);
  if (complexSentences && complexSentences.length > 0) {
    expressionScore += 10;
    feedback.push('文章の長さが適切で読みやすい構成です。');
  } else {
    suggestions.push('文章の長さを調整し、読みやすさを向上させてください。');
  }

  if (wordCount >= 400 && wordCount <= 800) {
    contentScore += 5;
  }
  if (paragraphs.length >= 4) {
    structureScore += 5;
  }
  if (content.includes(theme.substring(0, 10))) {
    contentScore += 5;
  }

  structureScore = Math.min(structureScore, 25);
  contentScore = Math.min(contentScore, 30);
  logicScore = Math.min(logicScore, 25);
  expressionScore = Math.min(expressionScore, 20);

  const total = structureScore + contentScore + logicScore + expressionScore;

  if (total >= 90) {
    feedback.push('非常に優秀な小論文です。論理構成、内容、表現ともに高いレベルです。');
  } else if (total >= 75) {
    feedback.push('良好な小論文です。いくつかの改善点はありますが、全体的に評価できます。');
  } else if (total >= 60) {
    feedback.push('基本的な要素は満たしていますが、さらなる改善が必要です。');
  } else {
    feedback.push('大幅な改善が必要です。構成と論証を見直してください。');
  }

  return {
    total,
    structure: structureScore,
    content: contentScore,
    logic: logicScore,
    expression: expressionScore,
    feedback: feedback.join(' '),
    suggestions
  };
};