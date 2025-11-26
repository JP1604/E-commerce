import React from 'react';
import { Input } from '../ui/Input';

export const ProductFilters = ({
  searchTerm,
  onSearchChange,
  selectedCategory,
  onCategoryChange,
  categories,
}) => {
  return (
    <div className="flex flex-col md:flex-row gap-4 mb-8">
      <div className="flex-1">
        <Input
          type="text"
          placeholder="🔍 Buscar productos..."
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
        />
      </div>
      <select
        value={selectedCategory}
        onChange={(e) => onCategoryChange(e.target.value)}
        className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
      >
        <option value="">Todas las categorías</option>
        {categories.map((cat) => (
          <option key={cat} value={cat}>{cat}</option>
        ))}
      </select>
    </div>
  );
};
