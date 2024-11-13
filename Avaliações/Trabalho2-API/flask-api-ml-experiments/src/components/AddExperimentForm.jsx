import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './AddExperimentForm.css';
import { getDatasets, addExperiment } from '../services/api';

const AddExperimentForm = ({ user }) => {
  const navigate = useNavigate();
  const [datasets, setDatasets] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    train_accuracy: '',
    validation_accuracy: '',
    test_accuracy: '',
    optimizer: '',
    epochs: '',
    learning_rate: '',
    patience: '',
    dataset_id: ''
  });

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

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Add the appropriate logic to send form data to the server
    // Example:
    console.log("adding experiment");
    await addExperiment({ ...formData, sessionId: user?.sessionId });
    console.log("experiment added");
    // Optionally handle errors and success notifications
    navigate('/'); // Redirect back to Dashboard on successful submission
  };

  return (
    <main>
      <a className="add-experiment-cancel" href="/dashboard">
        ⬅️ Back to Dashboard
      </a>

      <h2 className="add-experiment-title">Add a New Experiment!</h2>

      <form className="add-experiment-form" onSubmit={handleSubmit}>
        <input
          className="add-experiment-component"
          type="text"
          name="name"
          placeholder="Enter the experiment name"
          required
          value={formData.name}
          onChange={handleChange}
        />
        <input
          className="add-experiment-component"
          type="number"
          step="0.01"
          name="train_accuracy"
          placeholder="Enter the train accuracy"
          required
          value={formData.train_accuracy}
          onChange={handleChange}
        />
        <input
          className="add-experiment-component"
          type="number"
          step="0.01"
          name="validation_accuracy"
          placeholder="Enter the validation accuracy"
          required
          value={formData.validation_accuracy}
          onChange={handleChange}
        />
        <input
          className="add-experiment-component"
          type="number"
          step="0.01"
          name="test_accuracy"
          placeholder="Enter the test accuracy"
          required
          value={formData.test_accuracy}
          onChange={handleChange}
        />
        <input
          className="add-experiment-component"
          type="text"
          name="optimizer"
          placeholder="Enter the optimizer used"
          required
          value={formData.optimizer}
          onChange={handleChange}
        />
        <input
          className="add-experiment-component"
          type="number"
          name="epochs"
          placeholder="Enter the number of epochs"
          required
          value={formData.epochs}
          onChange={handleChange}
        />
        <input
          className="add-experiment-component"
          type="number"
          step="0.0001"
          name="learning_rate"
          placeholder="Enter the learning rate"
          required
          value={formData.learning_rate}
          onChange={handleChange}
        />
        <input
          className="add-experiment-component"
          type="number"
          name="patience"
          placeholder="Enter the patience value"
          required
          value={formData.patience}
          onChange={handleChange}
        />
        <select
          className="add-experiment-component"
          name="dataset_id"
          required
          value={formData.dataset_id}
          onChange={handleChange}
        >
          <option value="" hidden style={{color: 'black'}}>Select the dataset used</option>
          {datasets.map((dataset) => (
            <option key={dataset.id} value={dataset.id} style={{color: 'black'}}>
              {dataset.name}
            </option>
          ))}
        </select>
        <input
          className="add-experiment-component submit"
          type="submit"
          value="Register"
        />
      </form>
    </main>
  );
};

export default AddExperimentForm;
