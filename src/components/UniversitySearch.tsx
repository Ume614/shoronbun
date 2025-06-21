import React, { useState, useMemo } from 'react';
import { University, Faculty, Department } from '../types';

interface UniversitySearchProps {
  universities: University[];
  onSelect: (university: University, faculty: Faculty, department: Department) => void;
}

export const UniversitySearch: React.FC<UniversitySearchProps> = ({
  universities,
  onSelect
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedUniversity, setSelectedUniversity] = useState<University | null>(null);
  const [selectedFaculty, setSelectedFaculty] = useState<Faculty | null>(null);

  const filteredUniversities = useMemo(() => {
    if (!searchTerm) return universities;
    return universities.filter(uni =>
      uni.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [universities, searchTerm]);

  const aoFaculties = useMemo(() => {
    if (!selectedUniversity) return [];
    return selectedUniversity.faculties.filter(faculty => faculty.hasAO);
  }, [selectedUniversity]);

  const aoDepartments = useMemo(() => {
    if (!selectedFaculty) return [];
    return selectedFaculty.departments.filter(dept => dept.hasAO);
  }, [selectedFaculty]);

  const handleUniversitySelect = (university: University) => {
    setSelectedUniversity(university);
    setSelectedFaculty(null);
  };

  const handleFacultySelect = (faculty: Faculty) => {
    setSelectedFaculty(faculty);
  };

  const handleDepartmentSelect = (department: Department) => {
    if (selectedUniversity && selectedFaculty) {
      onSelect(selectedUniversity, selectedFaculty, department);
    }
  };

  return (
    <div className="space-y-6">
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">大学を検索</h2>
        <input
          type="text"
          placeholder="大学名を入力してください"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full"
        />
        
        {searchTerm && (
          <div className="mt-4 space-y-2 max-h-48 overflow-y-auto">
            {filteredUniversities.map(university => (
              <button
                key={university.id}
                onClick={() => handleUniversitySelect(university)}
                className={`w-full text-left p-3 rounded-lg border transition-colors ${
                  selectedUniversity?.id === university.id
                    ? 'bg-primary-color text-white border-primary-color'
                    : 'bg-white border-gray-300 hover:border-primary-color'
                }`}
              >
                {university.name}
                <span className="badge ml-2">
                  AO対応学部: {university.faculties.filter(f => f.hasAO).length}
                </span>
              </button>
            ))}
          </div>
        )}
      </div>

      {selectedUniversity && aoFaculties.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">
            {selectedUniversity.name} - 学部を選択
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {aoFaculties.map(faculty => (
              <button
                key={faculty.id}
                onClick={() => handleFacultySelect(faculty)}
                className={`text-left p-3 rounded-lg border transition-colors ${
                  selectedFaculty?.id === faculty.id
                    ? 'bg-primary-color text-white border-primary-color'
                    : 'bg-white border-gray-300 hover:border-primary-color'
                }`}
              >
                {faculty.name}
                <div className="text-sm mt-1 opacity-75">
                  AO対応学科: {faculty.departments.filter(d => d.hasAO).length}
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {selectedFaculty && aoDepartments.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">
            {selectedFaculty.name} - 学科を選択
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {aoDepartments.map(department => (
              <button
                key={department.id}
                onClick={() => handleDepartmentSelect(department)}
                className="text-left p-3 rounded-lg border border-gray-300 bg-white hover:border-primary-color hover:bg-primary-50 transition-colors"
              >
                {department.name}
                <div className="text-sm text-gray-600 mt-1">
                  過去問: {department.pastQuestions.length}件
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};