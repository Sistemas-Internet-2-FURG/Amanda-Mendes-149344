import React, { useState, useEffect } from 'react';
import { deleteExperiment, getDataset } from '../services/api';
import { useNavigate } from 'react-router-dom';

const ExperimentCard = ({ experiment, user }) => {
  const navigate = useNavigate();
  const [dataset, setDataset] = useState(null);

  const handleDelete = async (id) => {
    await deleteExperiment(id);
    window.location.reload();
  };

  const handleDatasetClick = async (id) => {
    console.log("getting dataset: ", id)
    const datasetInfo = (await getDataset(id)).data.data;
    console.log("dataset: ", datasetInfo);
    setDataset(datasetInfo);
  };

  return (
    <div className="experiment-card">
      <section className="experiment-info-container">
        <div className="experiment-info">
          <span className="experiment-name">{experiment.name}</span>
          <span className="experiment-id">ID: {experiment.id}</span>
          <span className="experiment-id">User: {experiment.user_name}</span>
          <span>Optimizer: {experiment.optimizer}</span>
          <span>Epochs: {experiment.epochs}</span>
          <span>Learning Rate: {experiment.learning_rate}</span>
          <span>Patience: {experiment.patience}</span>
          <a href={`/dataset/${experiment.id}`} className="dataset-link" onClick={(event) => { event.preventDefault(); handleDatasetClick(experiment.id); }}>
            Dataset: {experiment.dataset_id}
          </a>
          {dataset && (
            <div className="dataset-info">
              <span>Dataset Name: {dataset.name}</span>
              <span>Dataset Size: {dataset.size}</span>
              <span>Dataset Classes: {dataset.n_classes}</span>
              <span>Train Split: {dataset.train_split}</span>
              <span>Validation Split: {dataset.val_split}</span>
              <span>Test Split: {dataset.test_split}</span>
              <span>Imbalance Ratio: {dataset.imbalance_ratio}</span>
            </div>
          )}
          <span>Train Accuracy: {experiment.train_accuracy}</span>
          <span>Validation Accuracy: {experiment.validation_accuracy}</span>
          <span>Test Accuracy: {experiment.test_accuracy}</span>
        </div>

        {user?.id === experiment.user_id && (
          <div className="experiment-actions">
            {console.log("editing experiment: ", experiment.id)}
            <button className="experiment-button edit" onClick={() => navigate(`/edit-experiment/${experiment.id}`)}>Edit</button>
            <button className="experiment-button" onClick={() => handleDelete(experiment.id)}>Delete</button>
          </div>
        )}
      </section>
    </div>
  );
};

export default ExperimentCard;
