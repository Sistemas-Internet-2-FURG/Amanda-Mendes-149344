import React from 'react';

const FilterForm = ({ filter, filterType, onFilterChange, onFilterTypeChange, onSubmit }) => (
  <form className="filter-form" onSubmit={onSubmit}>
    <input
      className="filter-component"
      type="text"
      name="filter"
      value={filter}
      onChange={onFilterChange}
      placeholder="Filter experiments"
    />
    <select className="filter-component" name="filter_type" value={filterType} onChange={onFilterTypeChange}>
      <option value="experiment.name">Name</option>
      <option value="experiment.optimizer">Optimizer</option>
      {/* Add more options as needed */}
    </select>
    <button type="submit" className="filter-component submit">
      Filter
    </button>
  </form>
);

export default FilterForm;
