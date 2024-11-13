import React, { useEffect, useState } from 'react';
import { getDashboard, logout } from '../services/api';
import FilterForm from './FilterForm';
import ExperimentList from './ExperimentList';
import './Dashboard.css';
import { useNavigate } from 'react-router-dom';

function Dashboard({ user }) {
  const [experiments, setExperiments] = useState([]);
  const [filteredExperiments, setFilteredExperiments] = useState([]);
  const [filter, setFilter] = useState('');
  const [filterType, setFilterType] = useState('experiment.name');
  const navigate = useNavigate();
  const handleFilterChange = (e) => setFilter(e.target.value);
  const handleFilterTypeChange = (e) => setFilterType(e.target.value);

  const handleFilterSubmit = (e) => {
    e.preventDefault();
    handleFilter(filter, filterType); // Apply filter
  };

  const handleFilter = (filter, filterType) => {
    if (!filter) {
      setFilteredExperiments(experiments); // Reset if no filter
      return;
    }

    const filtered = experiments.filter((exp) => {
      const value = exp[filterType.split('.')[1]]; // Extract relevant field from experiment object
      return value && value.toString().toLowerCase().includes(filter.toLowerCase());
    });
    setFilteredExperiments(filtered);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log("user: ", user);
        const response = await getDashboard();
        setExperiments(response.data.data);
        setFilteredExperiments(response.data.data); // Initialize filtered experiments
      } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
      }
    };
    fetchData();
  }, []);

  const handleAddExperiment = () => {
    navigate('/add-experiment');
    // Logic to add a new experiment
  };

  return (
    <main>
      {user && (
        <button className="add-experiment" onClick={handleAddExperiment}>
          Add Experiment
        </button>
      )}

      <FilterForm
        filter={filter}
        filterType={filterType}
        onFilterChange={handleFilterChange}
        onFilterTypeChange={handleFilterTypeChange}
        onSubmit={handleFilterSubmit}
      />

      <ExperimentList experiments={filteredExperiments} user={user} />
    </main>
  );
}

export default Dashboard;
