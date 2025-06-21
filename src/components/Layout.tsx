import React from 'react';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">
              小論文対策アプリ
            </h1>
            <nav className="flex space-x-6">
              <a href="#" className="text-gray-600 hover:text-primary-color transition-colors">
                練習問題
              </a>
              <a href="#" className="text-gray-600 hover:text-primary-color transition-colors">
                書き方ガイド
              </a>
              <a href="#" className="text-gray-600 hover:text-primary-color transition-colors">
                過去の結果
              </a>
            </nav>
          </div>
        </div>
      </header>
      
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
      
      <footer className="bg-gray-100 border-t border-gray-200 mt-16">
        <div className="container mx-auto px-4 py-6">
          <p className="text-center text-gray-600 text-sm">
            © 2024 小論文対策アプリ. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};