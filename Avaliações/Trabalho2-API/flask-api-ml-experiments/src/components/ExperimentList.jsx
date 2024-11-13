import React from 'react';
import ExperimentCard from './ExperimentCard';

const ExperimentList = ({ experiments = [], user }) => (
  <div className="experiments-list">
    {experiments.length > 0 ? (
      experiments.map((experiment) => (
        <ExperimentCard key={experiment.id} experiment={experiment} user={user} />
      ))
    ) : (
      <p>No experiments available.</p>
    )}
  </div>
);

export default ExperimentList;
