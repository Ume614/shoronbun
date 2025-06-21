import { University } from '../types';

export const universities: University[] = [
  {
    id: 'waseda',
    name: '早稲田大学',
    faculties: [
      {
        id: 'political-science',
        name: '政治経済学部',
        hasAO: true,
        departments: [
          {
            id: 'politics',
            name: '政治学科',
            hasAO: true,
            pastQuestions: [
              {
                id: 'waseda-pol-2023',
                year: 2023,
                theme: 'デジタル社会における民主主義の課題と可能性について、具体例を挙げて論じなさい。',
                timeLimit: 90,
                university: '早稲田大学',
                faculty: '政治経済学部',
                department: '政治学科'
              },
              {
                id: 'waseda-pol-2022',
                year: 2022,
                theme: 'グローバル化が進む現代において、国家の役割はどのように変化すべきか論じなさい。',
                timeLimit: 90,
                university: '早稲田大学',
                faculty: '政治経済学部',
                department: '政治学科'
              },
              {
                id: 'waseda-pol-2021',
                year: 2021,
                theme: 'コロナ禍を通じて見えた現代社会の課題と、その解決策について論じなさい。',
                timeLimit: 90,
                university: '早稲田大学',
                faculty: '政治経済学部',
                department: '政治学科'
              },
              {
                id: 'waseda-pol-2020',
                year: 2020,
                theme: '持続可能な社会の実現に向けて、政治が果たすべき役割について論じなさい。',
                timeLimit: 90,
                university: '早稲田大学',
                faculty: '政治経済学部',
                department: '政治学科'
              },
              {
                id: 'waseda-pol-2019',
                year: 2019,
                theme: '人工知能の発達が社会に与える影響と、それに対する政策の在り方について論じなさい。',
                timeLimit: 90,
                university: '早稲田大学',
                faculty: '政治経済学部',
                department: '政治学科'
              }
            ]
          },
          {
            id: 'economics',
            name: '経済学科',
            hasAO: true,
            pastQuestions: [
              {
                id: 'waseda-econ-2023',
                year: 2023,
                theme: '日本経済の持続的成長に向けた課題と解決策について論じなさい。',
                timeLimit: 90,
                university: '早稲田大学',
                faculty: '政治経済学部',
                department: '経済学科'
              }
            ]
          }
        ]
      },
      {
        id: 'law',
        name: '法学部',
        hasAO: true,
        departments: [
          {
            id: 'law',
            name: '法学科',
            hasAO: true,
            pastQuestions: [
              {
                id: 'waseda-law-2023',
                year: 2023,
                theme: '法の支配と民主主義の関係について、現代社会の具体例を挙げて論じなさい。',
                timeLimit: 90,
                university: '早稲田大学',
                faculty: '法学部',
                department: '法学科'
              }
            ]
          }
        ]
      }
    ]
  },
  {
    id: 'keio',
    name: '慶應義塾大学',
    faculties: [
      {
        id: 'economics',
        name: '経済学部',
        hasAO: true,
        departments: [
          {
            id: 'economics',
            name: '経済学科',
            hasAO: true,
            pastQuestions: [
              {
                id: 'keio-econ-2023',
                year: 2023,
                theme: 'デジタル化が進む現代において、経済活動はどのように変化すべきか論じなさい。',
                timeLimit: 90,
                university: '慶應義塾大学',
                faculty: '経済学部',
                department: '経済学科'
              }
            ]
          }
        ]
      }
    ]
  },
  {
    id: 'todai',
    name: '東京大学',
    faculties: [
      {
        id: 'liberal-arts',
        name: '教養学部',
        hasAO: true,
        departments: [
          {
            id: 'liberal-arts',
            name: '教養学科',
            hasAO: true,
            pastQuestions: [
              {
                id: 'todai-liberal-2023',
                year: 2023,
                theme: '多様性と包摂性が求められる現代社会において、教育の果たすべき役割について論じなさい。',
                timeLimit: 120,
                university: '東京大学',
                faculty: '教養学部',
                department: '教養学科'
              }
            ]
          }
        ]
      }
    ]
  }
];