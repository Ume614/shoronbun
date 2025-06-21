import React, { useState, useEffect, useRef } from 'react';
import { PredictedQuestion } from '../types';

interface EssayEditorProps {
  question: PredictedQuestion;
  onSubmit: (content: string, timeSpent: number) => void;
  onCancel: () => void;
}

export const EssayEditor: React.FC<EssayEditorProps> = ({
  question,
  onSubmit,
  onCancel
}) => {
  const [content, setContent] = useState('');
  const [timeRemaining, setTimeRemaining] = useState(question.timeLimit * 60);
  const [isActive, setIsActive] = useState(false);
  const [timeSpent, setTimeSpent] = useState(0);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;
    
    if (isActive && timeRemaining > 0) {
      interval = setInterval(() => {
        setTimeRemaining(time => {
          const newTime = time - 1;
          setTimeSpent(question.timeLimit * 60 - newTime);
          
          if (newTime <= 0) {
            handleSubmit();
            return 0;
          }
          return newTime;
        });
      }, 1000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isActive, timeRemaining, question.timeLimit]);

  const formatTime = (seconds: number): string => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const getTimeColor = (): string => {
    const percentage = (timeRemaining / (question.timeLimit * 60)) * 100;
    if (percentage <= 10) return 'text-red-600';
    if (percentage <= 25) return 'text-orange-600';
    return 'text-gray-900';
  };

  const startTimer = () => {
    setIsActive(true);
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  };

  const handleSubmit = () => {
    setIsActive(false);
    onSubmit(content, timeSpent);
  };

  const wordCount = content.replace(/\s/g, '').length;

  return (
    <div className="max-w-4xl mx-auto">
      <div className="card mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">小論文練習</h2>
          <div className="flex items-center space-x-4">
            <div className="text-sm text-gray-600">
              文字数: <span className="font-medium">{wordCount}</span>
            </div>
            <div className={`text-lg font-mono font-bold ${getTimeColor()}`}>
              残り時間: {formatTime(timeRemaining)}
            </div>
          </div>
        </div>

        <div className="bg-gray-50 p-4 rounded-lg mb-6">
          <h3 className="font-medium text-gray-900 mb-2">出題テーマ</h3>
          <p className="text-gray-800 leading-relaxed">{question.theme}</p>
          <div className="mt-3 flex items-center space-x-4 text-sm text-gray-600">
            <span>制限時間: {question.timeLimit}分</span>
            <span>推奨文字数: 800-1200字</span>
          </div>
        </div>

        {!isActive ? (
          <div className="text-center py-8">
            <p className="text-gray-600 mb-6">
              準備ができたら「開始」ボタンを押してください。<br />
              タイマーが開始され、制限時間内で小論文を書いてください。
            </p>
            <div className="space-x-4">
              <button
                onClick={startTimer}
                className="bg-primary-color text-white px-8 py-3 rounded-lg font-medium hover:bg-primary-dark transition-colors"
              >
                開始する
              </button>
              <button
                onClick={onCancel}
                className="secondary"
              >
                戻る
              </button>
            </div>
          </div>
        ) : (
          <>
            <textarea
              ref={textareaRef}
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="ここに小論文を書いてください..."
              className="w-full h-96 resize-none"
              style={{ fontSize: '16px', lineHeight: '1.6' }}
            />
            
            <div className="flex justify-between items-center mt-6">
              <div className="text-sm text-gray-600">
                進捗: {Math.round((timeSpent / (question.timeLimit * 60)) * 100)}%
              </div>
              <div className="space-x-4">
                <button
                  onClick={handleSubmit}
                  disabled={content.trim().length < 100}
                  className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                    content.trim().length >= 100
                      ? 'bg-primary-color text-white hover:bg-primary-dark'
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  提出する
                </button>
                <button
                  onClick={onCancel}
                  className="secondary"
                >
                  中断
                </button>
              </div>
            </div>
            
            {content.trim().length < 100 && (
              <p className="text-sm text-orange-600 mt-2">
                提出するには最低100文字必要です（現在: {content.trim().length}文字）
              </p>
            )}
          </>
        )}
      </div>

      {isActive && (
        <div className="card">
          <h3 className="font-medium mb-3">書き方のヒント</h3>
          <ul className="text-sm text-gray-600 space-y-1">
            <li>• 序論：問題提起と自分の立場を明確に</li>
            <li>• 本論：根拠と具体例を用いて論証</li>
            <li>• 結論：主張をまとめ、今後の展望を示す</li>
            <li>• 反対意見にも言及し、多角的な視点を示す</li>
          </ul>
        </div>
      )}
    </div>
  );
};