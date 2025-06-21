import React from 'react';
import { EssayScore, Essay } from '../types';

interface ScoreResultProps {
  essay: Essay;
  score: EssayScore;
  onRetry: () => void;
  onNewQuestion: () => void;
}

export const ScoreResult: React.FC<ScoreResultProps> = ({
  essay,
  score,
  onRetry,
  onNewQuestion
}) => {
  const getScoreColor = (scoreValue: number, maxScore: number): string => {
    const percentage = (scoreValue / maxScore) * 100;
    if (percentage >= 80) return 'text-green-600';
    if (percentage >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getGrade = (totalScore: number): string => {
    if (totalScore >= 90) return 'A';
    if (totalScore >= 80) return 'B';
    if (totalScore >= 70) return 'C';
    if (totalScore >= 60) return 'D';
    return 'F';
  };

  const formatTime = (seconds: number): string => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}分${remainingSeconds}秒`;
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold">採点結果</h2>
          <div className="text-right">
            <div className="text-3xl font-bold text-primary-color">
              {score.total}点
            </div>
            <div className="text-lg font-medium text-gray-600">
              評価: {getGrade(score.total)}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-sm text-gray-600 mb-1">構成</div>
            <div className={`text-xl font-bold ${getScoreColor(score.structure, 25)}`}>
              {score.structure}/25
            </div>
          </div>
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-sm text-gray-600 mb-1">内容</div>
            <div className={`text-xl font-bold ${getScoreColor(score.content, 30)}`}>
              {score.content}/30
            </div>
          </div>
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-sm text-gray-600 mb-1">論理性</div>
            <div className={`text-xl font-bold ${getScoreColor(score.logic, 25)}`}>
              {score.logic}/25
            </div>
          </div>
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-sm text-gray-600 mb-1">表現</div>
            <div className={`text-xl font-bold ${getScoreColor(score.expression, 20)}`}>
              {score.expression}/20
            </div>
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <h3 className="font-medium text-blue-900 mb-2">総合評価</h3>
          <p className="text-blue-800">{score.feedback}</p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-medium mb-3">作成情報</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">文字数:</span>
                <span>{essay.content.replace(/\s/g, '').length}文字</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">所要時間:</span>
                <span>{formatTime(essay.timeSpent)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">提出日時:</span>
                <span>{new Date(essay.submittedAt).toLocaleString('ja-JP')}</span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="font-medium mb-3">問題情報</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">大学:</span>
                <span>{essay.question.university}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">学部:</span>
                <span>{essay.question.faculty}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">学科:</span>
                <span>{essay.question.department}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {score.suggestions.length > 0 && (
        <div className="card">
          <h3 className="font-medium mb-4">改善のアドバイス</h3>
          <ul className="space-y-2">
            {score.suggestions.map((suggestion, index) => (
              <li key={index} className="flex items-start">
                <span className="text-primary-color mr-2">•</span>
                <span className="text-gray-700">{suggestion}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="card">
        <h3 className="font-medium mb-4">あなたの解答</h3>
        <div className="bg-gray-50 p-4 rounded-lg">
          <div className="text-sm text-gray-600 mb-2">テーマ: {essay.question.theme}</div>
          <div className="whitespace-pre-wrap text-gray-800 leading-relaxed">
            {essay.content}
          </div>
        </div>
      </div>

      <div className="flex justify-center space-x-4">
        <button
          onClick={onRetry}
          className="secondary px-6 py-3"
        >
          同じ問題をもう一度
        </button>
        <button
          onClick={onNewQuestion}
          className="bg-primary-color text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-dark transition-colors"
        >
          新しい問題に挑戦
        </button>
      </div>
    </div>
  );
};