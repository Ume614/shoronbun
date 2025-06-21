import React, { useState } from 'react';
import { Layout } from './components/Layout';
import { UniversitySearch } from './components/UniversitySearch';
import { EssayEditor } from './components/EssayEditor';
import { ScoreResult } from './components/ScoreResult';
import { WritingGuideModal } from './components/WritingGuideModal';
import { universities } from './data/universities';
import { writingGuides } from './data/writingGuides';
import { generatePredictedQuestion } from './utils/questionPredictor';
import { scoreEssay } from './utils/essayScorer';
import { University, Faculty, Department, PredictedQuestion, Essay, EssayScore } from './types';

type AppState = 'selection' | 'writing' | 'result';

function App() {
  const [currentState, setCurrentState] = useState<AppState>('selection');
  const [selectedUniversity, setSelectedUniversity] = useState<University | null>(null);
  const [selectedFaculty, setSelectedFaculty] = useState<Faculty | null>(null);
  const [selectedDepartment, setSelectedDepartment] = useState<Department | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<PredictedQuestion | null>(null);
  const [currentEssay, setCurrentEssay] = useState<Essay | null>(null);
  const [currentScore, setCurrentScore] = useState<EssayScore | null>(null);
  const [isGuideOpen, setIsGuideOpen] = useState(false);

  const handleUniversitySelect = (university: University, faculty: Faculty, department: Department) => {
    setSelectedUniversity(university);
    setSelectedFaculty(faculty);
    setSelectedDepartment(department);
    
    const question = generatePredictedQuestion(
      department.pastQuestions,
      university.name,
      faculty.name,
      department.name
    );
    setCurrentQuestion(question);
    setCurrentState('writing');
  };

  const handleEssaySubmit = async (content: string, timeSpent: number) => {
    if (!currentQuestion) return;

    const essay: Essay = {
      id: `essay-${Date.now()}`,
      content,
      submittedAt: new Date(),
      timeSpent,
      question: currentQuestion
    };

    setCurrentEssay(essay);

    const score = await scoreEssay(content, currentQuestion.theme);
    setCurrentScore(score);
    setCurrentState('result');
  };

  const handleRetry = () => {
    setCurrentState('writing');
  };

  const handleNewQuestion = () => {
    setCurrentState('selection');
    setSelectedUniversity(null);
    setSelectedFaculty(null);
    setSelectedDepartment(null);
    setCurrentQuestion(null);
    setCurrentEssay(null);
    setCurrentScore(null);
  };

  const handleCancel = () => {
    setCurrentState('selection');
    setCurrentQuestion(null);
  };

  return (
    <Layout>
      <div className="min-h-screen">
        {currentState === 'selection' && (
          <div>
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                総合選抜型入試 小論文対策
              </h1>
              <p className="text-lg text-gray-600 mb-6">
                大学・学部・学科を選択して、予想問題に挑戦しましょう
              </p>
              <button
                onClick={() => setIsGuideOpen(true)}
                className="secondary"
              >
                📖 書き方ガイドを見る
              </button>
            </div>
            
            <UniversitySearch
              universities={universities}
              onSelect={handleUniversitySelect}
            />
          </div>
        )}

        {currentState === 'writing' && currentQuestion && (
          <EssayEditor
            question={currentQuestion}
            onSubmit={handleEssaySubmit}
            onCancel={handleCancel}
          />
        )}

        {currentState === 'result' && currentEssay && currentScore && (
          <ScoreResult
            essay={currentEssay}
            score={currentScore}
            onRetry={handleRetry}
            onNewQuestion={handleNewQuestion}
          />
        )}

        <WritingGuideModal
          guides={writingGuides}
          isOpen={isGuideOpen}
          onClose={() => setIsGuideOpen(false)}
        />
      </div>
    </Layout>
  );
}

export default App;
