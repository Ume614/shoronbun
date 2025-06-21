export interface University {
  id: string;
  name: string;
  faculties: Faculty[];
}

export interface Faculty {
  id: string;
  name: string;
  departments: Department[];
  hasAO: boolean;
}

export interface Department {
  id: string;
  name: string;
  hasAO: boolean;
  pastQuestions: PastQuestion[];
}

export interface PastQuestion {
  id: string;
  year: number;
  theme: string;
  timeLimit: number; // minutes
  university: string;
  faculty: string;
  department: string;
}

export interface Essay {
  id: string;
  content: string;
  submittedAt: Date;
  timeSpent: number; // seconds
  question: PredictedQuestion;
}

export interface PredictedQuestion {
  id: string;
  theme: string;
  timeLimit: number;
  generatedAt: Date;
  basedOnQuestions: string[]; // past question IDs
  university: string;
  faculty: string;
  department: string;
}

export interface EssayScore {
  total: number;
  structure: number;
  content: number;
  logic: number;
  expression: number;
  feedback: string;
  suggestions: string[];
}

export interface WritingGuide {
  id: string;
  title: string;
  content: string;
  category: 'structure' | 'content' | 'expression' | 'examples';
}