# 🚗 Car Price Prediction System 

An intelligent AI-powered application that predicts used car prices in Indian Rupees using Machine Learning and Image Recognition.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green?style=flat-square)
![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🌟 Key Features

✨ **Dual Prediction Modes**
- 📝 **Form Input** - Enter car details manually
- 📸 **Image Upload** - Upload car photo for AI-powered prediction

🤖 **Smart ML Models**
- Random Forest, Gradient Boosting & XGBoost
- Automatic best model selection (R² > 0.85)
- ResNet50 deep learning for image analysis

💰 **INR Currency Support**
- All prices in Indian Rupees (₹)
- USD to INR conversion (1 USD = ₹83)

🎨 **Modern React Interface**
- Beautiful, responsive UI
- Real-time predictions
- Image preview and upload
- Backend connection monitoring

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
├── frontend/                       # React Frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js                 # Main component
│   │   ├── App.css                # Styles
│   │   ├── index.js               # Entry point
│   │   └── index.css              # Global styles
│   └── package.json               # Dependencies
├── model_training.py              # Train models
├── app.py                         # Flask API (Port 5000)
├── requirements.txt               # Python dependencies
├── run_backend.bat                # Start Flask (Windows)
└── run_react_frontend.bat         # Start React (Windows)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 16+ and npm
- Windows OS (or modify .bat files for Linux/Mac)

### 1️⃣ Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Train the Model
```bash
python model_training.py
```
This creates model files in `models/` folder.

### 3️⃣ Start Flask Backend
**Option A: Using Batch File (Windows)**
```bash
run_backend.bat
```

**Option B: Manual**
```bash
python app.py
```
Backend API runs on: `http://localhost:5000`

### 4️⃣ Start React Frontend (New Terminal)
**Option A: Using Batch File (Windows)**
```bash
run_react_frontend.bat
```

**Option B: Manual**
```bash
cd frontend
npm install
npm start
```
React app opens at: `http://localhost:3000`

---

## 💡 How to Use

### Method 1: Form Input 📝
1. Open `http://localhost:3000`
2. Ensure backend status shows **"✅ Connected to Backend"**
3. Click **"📝 Form Input"** tab
4. Fill in car details:
   - **Brand**: BMW, Toyota, Ford, etc.
   - **Model Year**: 1990-2025
   - **Mileage**: In miles
   - **Fuel Type**: Diesel, Gasoline, Hybrid, etc.
   - **Transmission**: Automatic, Manual
   - **Horsepower**: Engine power
   - **Engine Size**: In liters
   - **Accident History**: Yes/No
   - **Clean Title**: Yes/No
5. Click **"🔮 Predict Price"**
6. View predicted price in ₹ INR

### Method 2: Image Upload 📸
1. Click **"📸 Image Upload"** tab
2. Click upload area to select car image (JPG/PNG)
3. Image preview will appear
4. Fill in basic details:
   - Brand
   - Fuel Type
   - Transmission
5. Click **"🔮 Predict from Image"**
6. AI analyzes image and predicts price

---

## 🔧 API Endpoints

### 1. Health Check
```
GET http://localhost:5000/
Response: {"status": "API is running", "version": "1.0"}
```

### 2. Get Options
```
GET http://localhost:5000/get_options
Response: {
  "brands": ["BMW", "Toyota", ...],
  "fuel_types": ["Diesel", "Gasoline", ...],
  "transmissions": ["Automatic", "Manual"]
}
```

### 3. Predict Price (Form)
```
POST http://localhost:5000/predict
Body: {
  "brand": "BMW",
  "model_year": 2020,
  "mileage": 50000,
  "fuel_type": "Diesel",
  "transmission": "Automatic",
  "horsepower": 250,
  "engine_size": 3.0,
  "has_accident": 0,
  "is_clean_title": 1
}
Response: {
  "predicted_price": 2075000,
  "predicted_price_formatted": "₹20,75,000",
  "model_used": "Random Forest",
  "input_data": {...}
}
```

### 4. Predict Price (Image)
```
POST http://localhost:5000/predict_image
Form Data:
  - image: <file>
  - brand: "BMW"
  - fuel_type: "Diesel"
  - transmission: "Automatic"
  - has_accident: 0
  - is_clean_title: 1
Response: {
  "predicted_price": 2075000,
  "predicted_price_formatted": "₹20,75,000",
  ...
}
```

---

## 🎯 Machine Learning Pipeline

### Feature Engineering (10 Features)
1. **car_age** = Current Year - Model Year
2. **has_accident** = 1 if accident, else 0
3. **horsepower** = Extracted from engine field
4. **engine_size** = Liters from engine field
5. **is_clean_title** = 1 if clean, else 0
6. **is_automatic** = 1 if automatic transmission
7. **mileage_per_year** = mileage / car_age
8. **high_mileage** = 1 if > 100,000 miles
9. **luxury_brand** = 1 if premium brand
10. **fuel_economy** = Miles per gallon estimate

### Models Trained
- **Random Forest**: Ensemble of decision trees
- **Gradient Boosting**: Sequential tree building
- **XGBoost**: Optimized gradient boosting

### Image Prediction
- **ResNet50** (PyTorch): Pre-trained on ImageNet
- Extracts 2048 visual features
- Combined with car metadata
- Predicts price from appearance

---

## 📊 Model Performance

| Model | R² Score | MAE (₹) |
|-------|----------|---------|
| Random Forest | 0.872 | 1,24,500 |
| Gradient Boosting | 0.868 | 1,29,000 |
| XGBoost | 0.875 | 1,21,800 |

**Best Model**: XGBoost (R² = 0.875)

---

## 🐛 Troubleshooting

### Backend Not Running
**Error**: "🚨 Backend Not Running"

**Solution**:
1. Ensure Flask is running: `python app.py`
2. Check port 5000 is not in use
3. Verify models folder exists with .pkl files

### Module Not Found
**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
pip install -r requirements.txt
```

### React Won't Start
**Error**: Cannot find module 'react'

**Solution**:
```bash
cd frontend
npm install
```

### Model Files Missing
**Error**: "Model file not found"

**Solution**:
```bash
python model_training.py
```

### CORS Errors
**Error**: CORS policy blocked

**Solution**: Flask has CORS enabled. Ensure:
- Backend runs on port 5000
- React `package.json` has: `"proxy": "http://localhost:5000"`

---

## 📦 Dependencies

### Python (Backend)
- Flask 3.0.0
- flask-cors 4.0.0
- scikit-learn 1.5.1
- pandas 2.2.3
- numpy 1.26.4
- xgboost 2.1.0
- Pillow 10.4.0
- torch 2.4.0
- torchvision 0.19.0
- requests 2.32.3
- python-dotenv 1.0.1

### JavaScript (Frontend)
- react 18.2.0
- react-dom 18.2.0
- axios 1.6.0
- react-scripts 5.0.1

---

## 🎨 Technology Stack

### Backend
- **Framework**: Flask (Python)
- **ML Libraries**: scikit-learn, XGBoost
- **Deep Learning**: PyTorch, torchvision
- **Data Processing**: pandas, numpy
- **Image Processing**: Pillow

### Frontend
- **Framework**: React 18
- **HTTP Client**: Axios
- **Build Tool**: Create React App
- **Styling**: CSS3 with animations

---

## 📝 Files Overview

### `model_training.py`
Trains and saves ML models. Run this first!
- Loads `Dataset/used_cars.csv`
- Performs feature engineering
- Trains 3 models
- Saves best model as `models/best_model.pkl`
- Saves encoders and scalers

### `app.py`
Flask REST API backend.
- Loads trained models
- Provides 4 endpoints
- Handles predictions
- CORS enabled
- Error handling

### `frontend/src/App.js`
Main React component.
- Form input UI
- Image upload UI
- Backend connection check
- API calls with axios
- Result display

### `frontend/src/App.css`
Component styling.
- Purple gradient theme
- Responsive design
- Animations
- Mobile-friendly

---

## 🔐 Security Notes

- Never commit `.env` files
- Use environment variables for secrets
- Implement rate limiting for production
- Validate all user inputs
- Sanitize file uploads

---

## 🚀 Deployment

### Backend (Flask)
- Use Gunicorn: `gunicorn app:app`
- Deploy to: Heroku, AWS, Azure, Railway
- Set environment variables
- Use production WSGI server

### Frontend (React)
- Build: `npm run build`
- Deploy to: Vercel, Netlify, GitHub Pages
- Update API URL in production
- Enable HTTPS

---

## 📄 License

MIT License - Feel free to use this project!

---

## 👨‍💻 Author

**Car Price Prediction Team**

- Built with ❤️ using Python, React & Machine Learning
- © 2025 All Rights Reserved

---

## 🙏 Acknowledgments

- Dataset: Used Cars Dataset (1000+ records)
- PyTorch ResNet50: ImageNet pre-trained model
- scikit-learn: ML algorithms
- React: Modern UI framework
- Flask: Lightweight web framework

---

## 📞 Support

Having issues? Check:
1. ✅ Backend running on port 5000
2. ✅ React running on port 3000
3. ✅ Models folder exists with .pkl files
4. ✅ Dependencies installed (pip & npm)
5. ✅ Python 3.12+ and Node.js 16+ installed

**Happy Predicting! 🚗💰**
