import React, { useState } from 'react';
import { WritingGuide } from '../types';

interface WritingGuideModalProps {
  guides: WritingGuide[];
  isOpen: boolean;
  onClose: () => void;
}

export const WritingGuideModal: React.FC<WritingGuideModalProps> = ({
  guides,
  isOpen,
  onClose
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('structure');

  if (!isOpen) return null;

  const categories = [
    { id: 'structure', name: '構成' },
    { id: 'content', name: '内容' },
    { id: 'expression', name: '表現' },
    { id: 'examples', name: '例文' }
  ];

  const filteredGuides = guides.filter(guide => guide.category === selectedCategory);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-4xl max-h-[90vh] w-full flex flex-col">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold">小論文書き方ガイド</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl"
          >
            ×
          </button>
        </div>

        <div className="flex flex-1 overflow-hidden">
          <div className="w-48 bg-gray-50 p-4 border-r border-gray-200">
            <nav className="space-y-2">
              {categories.map(category => (
                <button
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`w-full text-left px-3 py-2 rounded-lg transition-colors ${
                    selectedCategory === category.id
                      ? 'bg-primary-color text-white'
                      : 'text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {category.name}
                </button>
              ))}
            </nav>
          </div>

          <div className="flex-1 p-6 overflow-y-auto">
            <div className="space-y-6">
              {filteredGuides.map(guide => (
                <div key={guide.id} className="border-b border-gray-200 pb-6 last:border-b-0">
                  <h3 className="text-lg font-medium mb-3">{guide.title}</h3>
                  <div className="prose prose-sm max-w-none">
                    <div className="whitespace-pre-line text-gray-700 leading-relaxed">
                      {guide.content}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="flex justify-end p-6 border-t border-gray-200">
          <button
            onClick={onClose}
            className="secondary"
          >
            閉じる
          </button>
        </div>
      </div>
    </div>
  );
};