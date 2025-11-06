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
from datetime import datetime
import traceback

app = Flask(__name__)
CORS(app)

# Current year for dynamic calculation
CURRENT_YEAR = datetime.now().year

# Load the trained model and encoders
print("🔄 Loading models...")
try:
    with open('models/best_model.pkl', 'rb') as f:
        model = pickle.load(f)

    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    with open('models/label_encoders.pkl', 'rb') as f:
        label_encoders = pickle.load(f)

    with open('models/mappings.pkl', 'rb') as f:
        mappings = pickle.load(f)

    print("✅ Models loaded successfully!")
except FileNotFoundError as e:
    print(f"❌ Model files not found! Please run 'python model_training.py' first.")
    exit(1)
except Exception as e:
    print(f"❌ Error loading models: {e}")
    exit(1)

# Load pretrained ResNet model for image feature extraction
print("🔄 Loading image model...")
image_model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
image_model.eval()
print("✅ Image model loaded!")

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
    estimated_mileage = abs(int(20000 + (feature_sum * 1000) % 380000))  # 20k-400k miles (dataset range)
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
        
        # Validate required fields
        required_fields = ['brand', 'model_year', 'mileage', 'fuel_type', 'transmission']
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({
                'success': False,
                'error': f'Missing fields: {", ".join(missing)}'
            }), 400
        
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
        
        # Calculate car age dynamically
        car_age = CURRENT_YEAR - model_year
        
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
        
        # Make prediction (model predicts in USD)
        prediction_usd = model.predict(features_scaled)[0]
        
        return jsonify({
            'success': True,
            'predicted_price': round(float(prediction_usd), 2),
            'predicted_price_formatted': f"${prediction_usd:,.2f}",
            'input_data': {
                'brand': brand,
                'model_year': model_year,
                'mileage': round(mileage, 0),
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
    print("\n🔍 Starting image prediction...")
    try:
        # Debug: Print all form data
        print(f"📋 Form keys: {list(request.form.keys())}")
        print(f"📋 Files keys: {list(request.files.keys())}")
        
        # Get image from request
        if 'image' not in request.files:
            print("❌ No 'image' key in request.files")
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        file = request.files['image']
        print(f"📎 File received: {file.filename}, Content-Type: {file.content_type}")
        
        # Validate file
        if not file or file.filename == '':
            print("❌ File is empty or has no filename")
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Read image bytes
        try:
            # Reset file pointer to beginning
            file.seek(0)
            image_bytes = file.read()
            print(f"📊 Image bytes read: {len(image_bytes)} bytes")
            
            if len(image_bytes) == 0:
                return jsonify({'success': False, 'error': 'Empty file received'}), 400
            
            # Try to open image with PIL
            print("🖼️ Attempting to open image with PIL...")
            image_stream = io.BytesIO(image_bytes)
            image = Image.open(image_stream)
            
            print(f"✅ Image opened: Format={image.format}, Size={image.size}, Mode={image.mode}")
            
            # Convert to RGB
            if image.mode != 'RGB':
                print(f"🔄 Converting from {image.mode} to RGB")
                image = image.convert('RGB')
            
            print(f"✅ Image ready: {image.size[0]}x{image.size[1]} RGB")
            
        except Exception as img_error:
            print(f"❌ Image error: {type(img_error).__name__}: {str(img_error)}")
            print(f"❌ Full traceback:\n{traceback.format_exc()}")
            return jsonify({
                'success': False, 
                'error': f'Cannot process image: {str(img_error)}. Please upload a valid JPG or PNG image.'
            }), 400
        
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
        
        car_age = CURRENT_YEAR - model_year
        
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
        prediction_usd = model.predict(features_scaled)[0]
        
        return jsonify({
            'success': True,
            'predicted_price': round(float(prediction_usd), 2),
            'predicted_price_formatted': f"${prediction_usd:,.2f}",
            'estimated_features': {
                'model_year': model_year,
                'mileage': round(mileage, 0),
                'horsepower': horsepower
            },
            'message': 'Prediction based on image analysis and provided data'
        })
        
    except Exception as e:
        print(f"❌ Error in predict_image: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Prediction error: {str(e)}'
        }), 400

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 CAR PRICE PREDICTION API - USD ($)")
    print("="*60)
    print("📡 Backend URL: http://localhost:5000")
    print("📡 Network URL: http://0.0.0.0:5000")
    print("\n📋 Available Endpoints:")
    print("  ✅ GET  /              - API status")
    print("  ✅ GET  /get_options   - Get dropdown options")
    print("  ✅ POST /predict       - Predict from form data")
    print("  ✅ POST /predict_image - Predict from image")
    print("="*60)
    print("💡 Tip: Keep this terminal running!")
    print("💡 Open React frontend in another terminal")
    print("="*60 + "\n")
    
    # Run Flask - Windows compatible (no signal issues)
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
