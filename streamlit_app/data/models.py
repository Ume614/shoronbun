from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class PastQuestion:
    id: str
    year: int
    theme: str
    time_limit: int  # minutes
    university: str
    faculty: str
    department: str

@dataclass
class Department:
    id: str
    name: str
    has_ao: bool
    past_questions: List[PastQuestion]

@dataclass
class Faculty:
    id: str
    name: str
    departments: List[Department]
    has_ao: bool

@dataclass
class University:
    id: str
    name: str
    faculties: List[Faculty]

@dataclass
class PredictedQuestion:
    id: str
    theme: str
    time_limit: int
    generated_at: datetime
    based_on_questions: List[str]  # past question IDs
    university: str
    faculty: str
    department: str

@dataclass
class Essay:
    id: str
    content: str
    submitted_at: datetime
    time_spent: int  # seconds
    question: PredictedQuestion

@dataclass
class EssayScore:
    total: int
    structure: int
    content: int
    logic: int
    expression: int
    feedback: str
    suggestions: List[str]

@dataclass
class WritingGuide:
    id: str
    title: str
    content: str
    category: str  # 'structure', 'content', 'expression', 'examples'