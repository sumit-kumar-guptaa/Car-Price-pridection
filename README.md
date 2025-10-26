# 🚗 Car Price Prediction System 

An intelligent AI-powered application that predicts used car prices in Indian Rupees using Machine Learning and uploading Photos.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39.0-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🌟 Key Features

✨ **Dual Prediction Modes**
- 📝 **Form Input** - Enter car details manually
- 📸 **Image Upload** - Upload car photo for AI-powered prediction

🤖 **Smart ML Models**
- Random Forest, Gradient Boosting & XGBoost
- Automatic best model selection (R² > 0.85)
- ResNet50 for image analysis

💰 **INR Currency Support**
- All prices in Indian Rupees (₹)
- USD to INR conversion (1 USD = ₹83)

🎨 **Modern Web Interface**
- Interactive Streamlit UI
- Color-coded input display
- Real-time predictions

---

## 📁 Project Structure

```
Car Price Pridection/
├── Dataset/
│   └── used_cars.csv              # Training data (1000+ cars)
├── Pridection/
│   └── data.ipynb                 # EDA & Model Development
├── models/                         # Saved models (auto-generated)
│   ├── best_model.pkl
│   ├── scaler.pkl
│   ├── label_encoders.pkl
│   └── mappings.pkl
├── model_training.py              # Train models
├── app.py                         # Flask API (Port 5000)
├── streamlit_app.py               # Web UI (Port 8501)
└── requirements.txt               # Dependencies
```

---

## 🚀 Quick Start

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Train the Model
```bash
python model_training.py
```

### 3️⃣ Start Backend API
```bash
python app.py
```
API runs on: `http://localhost:5000`

### 4️⃣ Start Frontend (New Terminal)
```bash
streamlit run streamlit_app.py
```
App opens at: `http://localhost:8501`

---

## 💡 How to Use

### Method 1: Form Input
1. Open `http://localhost:8501`
2. Select **"🔧 Form Input"** tab
3. Fill in details:
   - Brand (BMW, Toyota, etc.)
   - Model Year (2019)
   - Mileage (50,000 miles)
   - Fuel Type (Diesel, Gasoline)
   - Transmission (Automatic, Manual)
   - Engine specs
   - Accident history
   - Clean title status
4. Click **"🔮 Predict Price"**
5. See predicted price in ₹

### Method 2: Image Upload
1. Select **"📸 Image Upload"** tab
2. Upload car image (JPG/PNG)
3. Add basic details (brand, fuel type, etc.)
4. Click **"🔮 Predict Price from Image"**
5. AI analyzes image and predicts price

---

## 🔌 API Endpoints

### Get Options
```http
GET /get_options
```
Returns available brands, fuel types, and transmissions.

### Predict from Form
```http
POST /predict
Content-Type: application/json

{
  "brand": "BMW",
  "model_year": 2019,
  "mileage": 50000,
  "fuel_type": "Diesel",
  "engine": "3.0L Twin Turbo I6 250hp",
  "transmission": "10-Speed A/T",
  "accident": "None reported",
  "clean_title": "Yes"
}
```

### Predict from Image
```http
POST /predict_image
Content-Type: multipart/form-data

- image: File
- brand: String
- fuel_type: String
- transmission: String
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Backend** | Flask 3.0.0, Flask-CORS |
| **ML/AI** | scikit-learn, XGBoost, PyTorch, ResNet50 |
| **Data** | pandas, numpy |
| **Frontend** | Streamlit 1.39.0 |
| **Visualization** | matplotlib, seaborn |

---

## 📊 Model Details

### Features Used (10 total)
1. Brand (encoded)
2. Model Year
3. Mileage
4. Fuel Type (encoded)
5. Transmission (encoded)
6. Car Age (calculated)
7. Accident History (binary)
8. Clean Title (binary)
9. Horsepower (extracted)
10. Engine Size (extracted)

### Training Process
```
Load Data → Clean Data → Extract Features → 
Train 3 Models → Compare Performance → 
Save Best Model (R² > 0.85)
```

### Performance Metrics
- **R² Score**: > 0.85 (85%+ accuracy)
- **MAE**: < ₹1,50,000
- **RMSE**: < ₹2,00,000

---

## ⚙️ Configuration

### Change Currency Rate
Edit `model_training.py`:
```python
USD_TO_INR = 83  # Update exchange rate
```
Then retrain: `python model_training.py`

### Change Ports
**Backend** (`app.py`):
```python
app.run(debug=True, port=5000)  # Change port
```

**Frontend** (`streamlit_app.py`):
```python
API_URL = "http://localhost:5000"  # Match backend port
```

---

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| **Model files not found** | Run `python model_training.py` |
| **API connection error** | Check Flask is running on port 5000 |
| **Image upload fails** | Use JPG/PNG format, max 10MB |
| **Wrong predictions** | Retrain model, check input data |
| **Port already in use** | Change port in app.py |

---

## 📚 Dataset

**File**: `Dataset/used_cars.csv`
- **Records**: 1000+ cars
- **Features**: 12 columns (brand, model, year, mileage, fuel, engine, transmission, colors, accident, title, price)
- **Target**: Price (converted from USD to INR)

---

## 🎯 Future Enhancements

- [ ] Add more ML models (Neural Networks)
- [ ] Multi-language support (Hindi, Tamil)
- [ ] Price trend analysis & charts
- [ ] User authentication & history
- [ ] Mobile app version
- [ ] Real-time market data
- [ ] Car comparison feature
- [ ] Deploy to cloud (AWS/Azure)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/NewFeature`
3. Commit changes: `git commit -m "Add NewFeature"`
4. Push to branch: `git push origin feature/NewFeature`
5. Open Pull Request

---

## 📝 License

MIT License - Free to use and modify

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- Kaggle for dataset
- PyTorch team for ResNet50
- scikit-learn & Streamlit communities
- Open-source contributors

---

<div align="center">

### ⭐ Star this repo if you find it helpful! ⭐

**Made with ❤️ and Python**

![Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python)
![ML](https://img.shields.io/badge/Machine-Learning-FF6F00?style=for-the-badge)

</div>

---

**Version**: 1.0.0  
**Last Updated**: October 26, 2025  
**Status**: ✅ Production Ready
