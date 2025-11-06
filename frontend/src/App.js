import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = 'http://localhost:5000';

function App() {
  const [backendStatus, setBackendStatus] = useState('checking');
  const [options, setOptions] = useState(null);
  const [activeTab, setActiveTab] = useState('form');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Form state
  const [formData, setFormData] = useState({
    brand: '',
    model_year: 2020,
    mileage: 53000,  // Median mileage from dataset (52,775)
    fuel_type: '',
    transmission: '',
    horsepower: 250,
    engine_size: 3.0,
    has_accident: 0,
    is_clean_title: 1
  });

  // Image state
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  // Check backend connection
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const response = await axios.get(`${API_URL}/`, { timeout: 3000 });
        if (response.status === 200) {
          setBackendStatus('connected');
          fetchOptions();
        }
      } catch (err) {
        setBackendStatus('disconnected');
      }
    };

    checkBackend();
  }, []);

  // Fetch dropdown options
  const fetchOptions = async () => {
    try {
      const response = await axios.get(`${API_URL}/get_options`);
      setOptions(response.data);
      setFormData(prev => ({
        ...prev,
        brand: response.data.brands[0],
        fuel_type: response.data.fuel_types[0],
        transmission: response.data.transmissions[0]
      }));
    } catch (err) {
      console.error('Failed to fetch options:', err);
    }
  };

  // Handle form input change
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Handle form submission
  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/predict`, formData, {
        timeout: 10000
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to predict price');
    } finally {
      setLoading(false);
    }
  };

  // Handle image selection
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'image/bmp'];
      if (!validTypes.includes(file.type)) {
        setError(`Invalid file type: ${file.type}. Please upload JPG, PNG, GIF, or WEBP image.`);
        return;
      }

      // Validate file size (max 10MB)
      const maxSize = 10 * 1024 * 1024; // 10MB
      if (file.size > maxSize) {
        setError('File too large. Maximum size is 10MB.');
        return;
      }

      console.log('✅ Image selected:', file.name, file.type, `${(file.size / 1024).toFixed(2)} KB`);
      setSelectedImage(file);
      setError(null);
      
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.onerror = () => {
        setError('Failed to read image file');
      };
      reader.readAsDataURL(file);
    }
  };

  // Handle image submission
  const handleImageSubmit = async (e) => {
    e.preventDefault();
    if (!selectedImage) {
      setError('Please select an image');
      return;
    }

    console.log('🚀 Submitting image prediction:', selectedImage.name, selectedImage.type);
    setLoading(true);
    setError(null);
    setResult(null);

    const imageFormData = new FormData();
    imageFormData.append('image', selectedImage, selectedImage.name);
    imageFormData.append('brand', formData.brand);
    imageFormData.append('fuel_type', formData.fuel_type);
    imageFormData.append('transmission', formData.transmission);
    imageFormData.append('has_accident', formData.has_accident);
    imageFormData.append('is_clean_title', formData.is_clean_title);

    console.log('📦 FormData prepared with image and metadata');

    try {
      const response = await axios.post(`${API_URL}/predict_image`, imageFormData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 15000
      });
      console.log('✅ Prediction successful:', response.data);
      setResult(response.data);
    } catch (err) {
      console.error('❌ Prediction failed:', err.response?.data || err.message);
      setError(err.response?.data?.error || 'Failed to predict from image');
    } finally {
      setLoading(false);
    }
  };

  if (backendStatus === 'checking') {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Connecting to backend...</p>
      </div>
    );
  }

  if (backendStatus === 'disconnected') {
    return (
      <div className="error-screen">
        <h1>🚨 Backend Not Running</h1>
        <p>Please start the Flask backend first:</p>
        <code>python app.py</code>
        <button onClick={() => window.location.reload()}>Retry Connection</button>
      </div>
    );
  }

  if (!options) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Loading options...</p>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>🚗 Car Price Predictor 💵</h1>
        <p>Predict used car prices in US Dollars ($) using AI</p>
        <div className="status-badge">✅ Connected to Backend</div>
      </header>

      <div className="container">
        {/* Tabs */}
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'form' ? 'active' : ''}`}
            onClick={() => setActiveTab('form')}
          >
            📝 Form Input
          </button>
          <button
            className={`tab ${activeTab === 'image' ? 'active' : ''}`}
            onClick={() => setActiveTab('image')}
          >
            📸 Image Upload
          </button>
        </div>

        {/* Form Tab */}
        {activeTab === 'form' && (
          <div className="tab-content">
            <form onSubmit={handleFormSubmit} className="prediction-form">
              <div className="form-grid">
                <div className="form-group">
                  <label>Brand</label>
                  <select name="brand" value={formData.brand} onChange={handleInputChange}>
                    {options.brands.map(brand => (
                      <option key={brand} value={brand}>{brand}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Model Year</label>
                  <input
                    type="number"
                    name="model_year"
                    value={formData.model_year}
                    onChange={handleInputChange}
                    min="1990"
                    max={new Date().getFullYear()}
                  />
                </div>

                <div className="form-group">
                  <label>Distance (km)</label>
                  <input
                    type="number"
                    name="mileage"
                    value={formData.mileage}
                    onChange={handleInputChange}
                    min="0"
                    max="410000"
                    step="1000"
                    placeholder="e.g., 53000"
                  />
                  <small className="field-hint">
                    {formData.mileage ? `${(formData.mileage).toLocaleString()} km` : 'Dataset range: 100 - 405,000 km'}
                  </small>
                </div>

                <div className="form-group">
                  <label>Fuel Type</label>
                  <select name="fuel_type" value={formData.fuel_type} onChange={handleInputChange}>
                    {options.fuel_types.map(fuel => (
                      <option key={fuel} value={fuel}>{fuel}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Transmission</label>
                  <select name="transmission" value={formData.transmission} onChange={handleInputChange}>
                    {options.transmissions.map(trans => (
                      <option key={trans} value={trans}>{trans}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Horsepower</label>
                  <input
                    type="number"
                    name="horsepower"
                    value={formData.horsepower}
                    onChange={handleInputChange}
                    min="50"
                    step="10"
                  />
                </div>

                <div className="form-group">
                  <label>Engine Size (L)</label>
                  <input
                    type="number"
                    name="engine_size"
                    value={formData.engine_size}
                    onChange={handleInputChange}
                    min="1.0"
                    max="8.0"
                    step="0.1"
                  />
                </div>

                <div className="form-group">
                  <label>Accident History</label>
                  <select name="has_accident" value={formData.has_accident} onChange={handleInputChange}>
                    <option value="0">No Accident</option>
                    <option value="1">Has Accident</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Clean Title</label>
                  <select name="is_clean_title" value={formData.is_clean_title} onChange={handleInputChange}>
                    <option value="1">Yes</option>
                    <option value="0">No</option>
                  </select>
                </div>
              </div>

              <button type="submit" className="submit-btn" disabled={loading}>
                {loading ? '⏳ Predicting...' : '🔮 Predict Price'}
              </button>
            </form>
          </div>
        )}

        {/* Image Tab */}
        {activeTab === 'image' && (
          <div className="tab-content">
            <form onSubmit={handleImageSubmit} className="prediction-form">
              <div className="image-upload-section">
                <label className="image-upload-label">
                  {imagePreview ? (
                    <img src={imagePreview} alt="Preview" className="image-preview" />
                  ) : (
                    <div className="upload-placeholder">
                      <span>📸</span>
                      <p>Click to upload car image</p>
                      <p className="small">JPG, PNG (Max 10MB)</p>
                    </div>
                  )}
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageChange}
                    style={{ display: 'none' }}
                  />
                </label>
              </div>

              <div className="form-grid">
                <div className="form-group">
                  <label>Brand</label>
                  <select name="brand" value={formData.brand} onChange={handleInputChange}>
                    {options.brands.map(brand => (
                      <option key={brand} value={brand}>{brand}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Fuel Type</label>
                  <select name="fuel_type" value={formData.fuel_type} onChange={handleInputChange}>
                    {options.fuel_types.map(fuel => (
                      <option key={fuel} value={fuel}>{fuel}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Transmission</label>
                  <select name="transmission" value={formData.transmission} onChange={handleInputChange}>
                    {options.transmissions.map(trans => (
                      <option key={trans} value={trans}>{trans}</option>
                    ))}
                  </select>
                </div>
              </div>

              <button type="submit" className="submit-btn" disabled={loading || !selectedImage}>
                {loading ? '⏳ Analyzing...' : '🔮 Predict from Image'}
              </button>
            </form>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="result-card">
            <h2>💰 Predicted Price</h2>
            <div className="price-display">
              {result.predicted_price_formatted}
            </div>
            {result.input_data && (
              <div className="input-summary">
                <h3>📋 Input Summary</h3>
                <div className="summary-grid">
                  <div><strong>Brand:</strong> {result.input_data.brand}</div>
                  <div><strong>Year:</strong> {result.input_data.model_year}</div>
                  <div><strong>Distance:</strong> {result.input_data.mileage ? result.input_data.mileage.toLocaleString() : result.input_data.distance?.toLocaleString()} km</div>
                  <div><strong>Fuel:</strong> {result.input_data.fuel_type}</div>
                  <div><strong>Transmission:</strong> {result.input_data.transmission}</div>
                  <div><strong>Horsepower:</strong> {result.input_data.horsepower} HP</div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="error-card">
            <h3>❌ Error</h3>
            <p>{error}</p>
          </div>
        )}
      </div>

      <footer className="app-footer">
        <p>🚗 Car Price Predictor | Built with React & Flask | © 2025</p>
      </footer>
    </div>
  );
}

export default App;
