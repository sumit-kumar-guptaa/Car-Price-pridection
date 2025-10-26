from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
from PIL import Image
import io
import base64
import torch
import torchvision.models as models
import torchvision.transforms as transforms

app = Flask(__name__)
CORS(app)

# Load the trained model and encoders
print("Loading models...")
with open('models/best_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('models/label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)

with open('models/mappings.pkl', 'rb') as f:
    mappings = pickle.load(f)

print("Models loaded successfully!")

# Load pretrained ResNet model for image feature extraction
print("Loading image model...")
image_model = models.resnet50(pretrained=True)
image_model.eval()

# Image preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def extract_features_from_image(image):
    """Extract features from car image using ResNet"""
    try:
        image_tensor = preprocess(image).unsqueeze(0)
        with torch.no_grad():
            features = image_model(image_tensor)
        return features.numpy().flatten()
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None

def estimate_car_features_from_image(image_features):
    """
    Estimate car features from image features
    This is a simplified approach - in production, you'd train a specialized model
    """
    # Use image features to estimate some properties
    # This is a placeholder - you would train a proper model for this
    feature_sum = np.sum(image_features[:100])
    
    # Simple heuristic estimates (these should be replaced with a trained model)
    estimated_year = int(2015 + (feature_sum % 10))  # Estimate year between 2015-2024
    estimated_mileage = abs(int(50000 + (feature_sum * 1000) % 100000))  # 50k-150k miles
    estimated_horsepower = abs(int(200 + (feature_sum * 10) % 300))  # 200-500 HP
    
    return {
        'model_year': estimated_year,
        'milage_clean': estimated_mileage,
        'horsepower': estimated_horsepower
    }

@app.route('/')
def home():
    return jsonify({
        'message': 'Car Price Prediction API',
        'status': 'running',
        'endpoints': {
            '/predict': 'POST - Predict car price with form data',
            '/predict_image': 'POST - Predict car price from image',
            '/get_options': 'GET - Get available options for dropdowns'
        }
    })

@app.route('/get_options', methods=['GET'])
def get_options():
    """Return available options for frontend dropdowns"""
    return jsonify({
        'brands': sorted(mappings['brands']),
        'fuel_types': sorted(mappings['fuel_types']),
        'transmissions': sorted(mappings['transmissions'])
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict car price based on form inputs"""
    try:
        data = request.get_json()
        
        # Extract features from request
        brand = data.get('brand')
        model_year = int(data.get('model_year'))
        mileage = float(data.get('mileage'))
        fuel_type = data.get('fuel_type')
        transmission = data.get('transmission')
        has_accident = int(data.get('has_accident', 0))
        is_clean_title = int(data.get('is_clean_title', 1))
        horsepower = float(data.get('horsepower', 250))
        engine_size = float(data.get('engine_size', 3.0))
        
        # Calculate car age
        car_age = 2025 - model_year
        
        # Encode categorical variables
        try:
            brand_encoded = label_encoders['brand'].transform([brand])[0]
        except:
            brand_encoded = 0  # Default if brand not found
            
        try:
            fuel_encoded = label_encoders['fuel_type'].transform([fuel_type])[0]
        except:
            fuel_encoded = 0
            
        try:
            trans_encoded = label_encoders['transmission'].transform([transmission])[0]
        except:
            trans_encoded = 0
        
        # Prepare features array
        features = np.array([[
            brand_encoded,
            model_year,
            mileage,
            fuel_encoded,
            trans_encoded,
            car_age,
            has_accident,
            is_clean_title,
            horsepower,
            engine_size
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        return jsonify({
            'success': True,
            'predicted_price': round(float(prediction), 2),
            'predicted_price_formatted': f"₹{prediction:,.2f}",
            'input_data': {
                'brand': brand,
                'model_year': model_year,
                'mileage': mileage,
                'fuel_type': fuel_type,
                'transmission': transmission,
                'car_age': car_age,
                'has_accident': has_accident,
                'horsepower': horsepower
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/predict_image', methods=['POST'])
def predict_from_image():
    """Predict car price from uploaded image"""
    try:
        # Get image from request
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        file = request.files['image']
        image = Image.open(io.BytesIO(file.read())).convert('RGB')
        
        # Extract features from image
        image_features = extract_features_from_image(image)
        
        if image_features is None:
            return jsonify({'success': False, 'error': 'Failed to process image'}), 400
        
        # Get additional form data
        brand = request.form.get('brand', 'Toyota')
        fuel_type = request.form.get('fuel_type', 'Gasoline')
        transmission = request.form.get('transmission', 'Automatic')
        has_accident = int(request.form.get('has_accident', 0))
        is_clean_title = int(request.form.get('is_clean_title', 1))
        
        # Estimate features from image
        estimated = estimate_car_features_from_image(image_features)
        
        # Use provided values or estimates
        model_year = int(request.form.get('model_year', estimated['model_year']))
        mileage = float(request.form.get('mileage', estimated['milage_clean']))
        horsepower = float(request.form.get('horsepower', estimated['horsepower']))
        engine_size = float(request.form.get('engine_size', 3.0))
        
        car_age = 2025 - model_year
        
        # Encode categorical variables
        try:
            brand_encoded = label_encoders['brand'].transform([brand])[0]
        except:
            brand_encoded = 0
            
        try:
            fuel_encoded = label_encoders['fuel_type'].transform([fuel_type])[0]
        except:
            fuel_encoded = 0
            
        try:
            trans_encoded = label_encoders['transmission'].transform([transmission])[0]
        except:
            trans_encoded = 0
        
        # Prepare features
        features = np.array([[
            brand_encoded,
            model_year,
            mileage,
            fuel_encoded,
            trans_encoded,
            car_age,
            has_accident,
            is_clean_title,
            horsepower,
            engine_size
        ]])
        
        # Scale and predict
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        
        return jsonify({
            'success': True,
            'predicted_price': round(float(prediction), 2),
            'predicted_price_formatted': f"₹{prediction:,.2f}",
            'estimated_features': {
                'model_year': model_year,
                'mileage': mileage,
                'horsepower': horsepower
            },
            'message': 'Prediction based on image analysis and provided data'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Car Price Prediction API Starting...")
    print("="*50)
    print("Available endpoints:")
    print("  - GET  /")
    print("  - GET  /get_options")
    print("  - POST /predict")
    print("  - POST /predict_image")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
