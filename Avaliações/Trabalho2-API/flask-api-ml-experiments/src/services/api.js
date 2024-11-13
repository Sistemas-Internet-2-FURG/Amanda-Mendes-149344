import axios from 'axios';

const API_BASE_URL = "/api";

export const login = (email, name) => axios.post(`${API_BASE_URL}/login`, { email, name });
export const logout = () => axios.post(`${API_BASE_URL}/logout`);
export const getDashboard = () => axios.get(`${API_BASE_URL}/dashboard`, { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } });
export const getDataset = (experimentId) => axios.get(`${API_BASE_URL}/dataset/${experimentId}`, { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } });
export const addExperiment = (experimentData) => axios.post(`${API_BASE_URL}/add_experiment`, experimentData, { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } });
export const putExperiment = (experimentData) => axios.post(`${API_BASE_URL}/put_experiment`, experimentData, { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } });
export const deleteExperiment = (experimentId) => axios.post(`${API_BASE_URL}/delete_experiment`, { experiment_id: experimentId }, { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } });
export const filterExperiments = (filterData) => axios.post(`${API_BASE_URL}/filter_experiments`, filterData, { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } });
export const getDatasets = () => axios.get(`${API_BASE_URL}/datasets`, { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } });
export const getExperiment = (experimentId) => axios.get(`${API_BASE_URL}/experiment/${experimentId}`, { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } });
