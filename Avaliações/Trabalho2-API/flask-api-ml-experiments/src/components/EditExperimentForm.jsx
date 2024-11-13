import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './EditExperimentForm.css';
import { getDatasets, getExperiment, putExperiment } from '../services/api';

function EditExperimentForm() {
  const {experiment} = useParams();
  const [formData, setFormData] = useState({
    name: '',
    train_accuracy: '',
    validation_accuracy: '',
    test_accuracy: '',
    optimizer: '',
    epochs: '',
    learning_rate: '',
    patience: '',
    dataset_id: '',
  });
  const [datasets, setDatasets] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getDatasets();
        console.log("datasets: ", response);
        setDatasets(response.data.data);
      } catch (error) {
        console.error("Failed to fetch datasets:", error);
      }
    };
    fetchData();
  }, []);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchExperimentData = async () => {
      console.log("experiment: ", experiment);
      if (experiment) {
        try {
          const response = await getExperiment(experiment); // Fetch experiment data
          const experimentData = response.data.data; // Assuming the data is in response.data
          console.log("exp data: ", experimentData);
          setFormData({
            name: experimentData.name || '',
            train_accuracy: experimentData.train_accuracy ? parseFloat(experimentData.train_accuracy) / 100 : '',
            validation_accuracy: experimentData.validation_accuracy ? parseFloat(experimentData.validation_accuracy) / 100 : '',
            test_accuracy: experimentData.test_accuracy ? parseFloat(experimentData.test_accuracy) / 100 : '',
            optimizer: experimentData.optimizer || '',
            epochs: experimentData.epochs || '',
            learning_rate: experimentData.learning_rate || '',
            patience: experimentData.patience || '',
            dataset_id: experimentData.dataset_id || '',
          });
        } catch (error) {
          console.error("Failed to fetch experiment data:", error);
        }
      }
    };
    fetchExperimentData();
  }, [experiment]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    putExperiment({ ...formData, experiment_id: experiment });
    navigate('/dashboard');
    //onSave(formData);  // Trigger save action with form data
  };

  return (
    <main className="edit-experiment-container">
      <a className="put-experiment-cancel" onClick={() => navigate('/dashboard')}>
        ⬅️ Back to Dashboard
      </a>
      
      <h2 className="put-experiment-title">Edit Your Experiment!</h2>
      <form className="put-experiment-form" onSubmit={handleSubmit}>
        <input
          className="put-experiment-component"
          type="text"
          name="name"
          placeholder={experiment?.name || "Enter experiment name"}
          value={formData.name}
          onChange={handleChange}
          required
        />
        <input
          className="put-experiment-component"
          type="number"
          step="0.01"
          name="train_accuracy"
          placeholder={experiment?.train_accuracy || "Train accuracy"}
          value={formData.train_accuracy}
          onChange={handleChange}
          required
        />
        <input
          className="put-experiment-component"
          type="number"
          step="0.01"
          name="validation_accuracy"
          placeholder={experiment?.validation_accuracy || "Validation accuracy"}
          value={formData.validation_accuracy}
          onChange={handleChange}
          required
        />
        <input
          className="put-experiment-component"
          type="number"
          step="0.01"
          name="test_accuracy"
          placeholder={experiment?.test_accuracy || "Test accuracy"}
          value={formData.test_accuracy}
          onChange={handleChange}
          required
        />
        <input
          className="put-experiment-component"
          type="text"
          name="optimizer"
          placeholder={experiment?.optimizer || "Optimizer"}
          value={formData.optimizer}
          onChange={handleChange}
          required
        />
        <input
          className="put-experiment-component"
          type="number"
          name="epochs"
          placeholder={experiment?.epochs || "Epochs"}
          value={formData.epochs}
          onChange={handleChange}
          required
        />
        <input
          className="put-experiment-component"
          type="number"
          step="0.0001"
          name="learning_rate"
          placeholder={experiment?.learning_rate || "Learning rate"}
          value={formData.learning_rate}
          onChange={handleChange}
          required
        />
        <input
          className="put-experiment-component"
          type="number"
          name="patience"
          placeholder={experiment?.patience || "Patience"}
          value={formData.patience}
          onChange={handleChange}
          required
        />
        <select
          className="put-experiment-component"
          name="dataset_id"
          value={formData.dataset_id}
          onChange={handleChange}
          required
        >
          <option value="" hidden style={{color: 'black'}}>Select the dataset used</option>
          {datasets.map((dataset) => (
            <option key={dataset.id} value={dataset.id}>
              {dataset.name}
            </option>
          ))}
        </select>
        <input
          className="put-experiment-component submit"
          type="submit"
          value="Save"
        />
      </form>
    </main>
  );
}

export default EditExperimentForm;
