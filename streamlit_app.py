import streamlit as st
import requests
import pandas as pd
from PIL import Image
import io
import time

# API Configuration
API_URL = "http://localhost:5000"

# Page config
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 15px;
        font-size: 18px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 20px 0;
    }
    .info-box {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: white;
    }
    .info-box strong {
        color: #FFD700;
        font-size: 16px;
        font-weight: bold;
    }
    .info-box br {
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None

# Fetch options from API
@st.cache_data
def get_options():
    try:
        response = requests.get(f"{API_URL}/get_options")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Title and description
st.title("🚗 Car Price Prediction System 🇮🇳")
st.markdown("### Predict the price of used cars in Indian Rupees (INR) using AI")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/200/car.png", width=150)
    st.header("About")
    st.info("""
    This application uses Machine Learning to predict car prices in Indian Rupees (₹) based on:
    - Car specifications (Form Input)
    - Car images (Image Upload)
    
    **Features:**
    - Multiple ML algorithms
    - Image-based prediction
    - Real-time analysis
    - INR currency support (1 USD = ₹83)
    """)
    
    st.header("Instructions")
    st.markdown("""
    1. Choose prediction method
    2. Fill in car details
    3. Click 'Predict Price'
    4. View estimated price!
    """)

# Get options from API
options = get_options()

if options is None:
    st.error("⚠️ Cannot connect to API. Please make sure the Flask backend is running on port 5000.")
    st.stop()

# Main content
tab1, tab2 = st.tabs(["📝 Form Input", "📸 Image Upload"])

# Tab 1: Form Input
with tab1:
    st.header("Enter Car Details")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        brand = st.selectbox("Brand", options=options['brands'], index=0)
        model_year = st.number_input("Model Year", min_value=1990, max_value=2025, value=2020, step=1)
        mileage = st.number_input("Mileage (miles)", min_value=0, max_value=500000, value=50000, step=1000)
    
    with col2:
        fuel_type = st.selectbox("Fuel Type", options=options['fuel_types'], index=0)
        transmission = st.selectbox("Transmission", options=options['transmissions'], index=0)
        horsepower = st.number_input("Horsepower", min_value=50, max_value=1000, value=250, step=10)
    
    with col3:
        engine_size = st.number_input("Engine Size (L)", min_value=1.0, max_value=8.0, value=3.0, step=0.1)
        has_accident = st.selectbox("Accident History", options=["No Accident", "Has Accident"], index=0)
        is_clean_title = st.selectbox("Clean Title", options=["Yes", "No"], index=0)
    
    # Convert selections to binary
    has_accident_val = 0 if has_accident == "No Accident" else 1
    is_clean_title_val = 1 if is_clean_title == "Yes" else 0
    
    st.markdown("---")
    
    if st.button("🔮 Predict Price", key="form_predict"):
        with st.spinner("Analyzing car details..."):
            try:
                payload = {
                    'brand': brand,
                    'model_year': model_year,
                    'mileage': mileage,
                    'fuel_type': fuel_type,
                    'transmission': transmission,
                    'has_accident': has_accident_val,
                    'is_clean_title': is_clean_title_val,
                    'horsepower': horsepower,
                    'engine_size': engine_size
                }
                
                response = requests.post(f"{API_URL}/predict", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.prediction_result = result
                    
                    # Display result
                    st.success("✅ Prediction Complete!")
                    
                    st.markdown(f"""
                    <div class="prediction-box">
                        💰 Estimated Price: {result['predicted_price_formatted']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display input summary
                    st.subheader("📋 Input Summary")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="info-box">
                        <strong>🚗 Brand:</strong> {brand}<br><br>
                        <strong>📅 Model Year:</strong> {model_year}<br><br>
                        <strong>🛣️ Mileage:</strong> {mileage:,} miles<br><br>
                        <strong>⛽ Fuel Type:</strong> {fuel_type}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="info-box">
                        <strong>⚙️ Transmission:</strong> {transmission}<br><br>
                        <strong>🏎️ Horsepower:</strong> {horsepower} HP<br><br>
                        <strong>🔧 Engine Size:</strong> {engine_size}L<br><br>
                        <strong>🚨 Accident:</strong> {has_accident}
                        </div>
                        """, unsafe_allow_html=True)
                    
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            
            except Exception as e:
                st.error(f"❌ Error connecting to API: {str(e)}")

# Tab 2: Image Upload
with tab2:
    st.header("Upload Car Image")
    st.info("📷 Upload a clear image of the car. The AI will analyze the image and estimate the price.")
    
    uploaded_file = st.file_uploader("Choose a car image...", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(image, caption='Uploaded Car Image', use_column_width=True)
        
        with col2:
            st.subheader("Additional Information (Optional)")
            st.markdown("*Provide more details for better accuracy*")
            
            img_brand = st.selectbox("Brand", options=options['brands'], index=0, key="img_brand")
            img_fuel = st.selectbox("Fuel Type", options=options['fuel_types'], index=0, key="img_fuel")
            img_transmission = st.selectbox("Transmission", options=options['transmissions'], index=0, key="img_trans")
            
            col_a, col_b = st.columns(2)
            with col_a:
                img_accident = st.selectbox("Accident", ["No", "Yes"], index=0, key="img_acc")
            with col_b:
                img_title = st.selectbox("Clean Title", ["Yes", "No"], index=0, key="img_title")
        
        st.markdown("---")
        
        if st.button("🔮 Predict from Image", key="image_predict"):
            with st.spinner("🤖 Analyzing image with AI..."):
                time.sleep(1)  # Simulate processing
                
                try:
                    # Prepare image for upload
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    img_byte_arr.seek(0)
                    
                    files = {'image': ('car.png', img_byte_arr, 'image/png')}
                    data = {
                        'brand': img_brand,
                        'fuel_type': img_fuel,
                        'transmission': img_transmission,
                        'has_accident': 1 if img_accident == "Yes" else 0,
                        'is_clean_title': 1 if img_title == "Yes" else 0
                    }
                    
                    response = requests.post(f"{API_URL}/predict_image", files=files, data=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success("✅ Image Analysis Complete!")
                        
                        st.markdown(f"""
                        <div class="prediction-box">
                            💰 Estimated Price: {result['predicted_price_formatted']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Show estimated features
                        if 'estimated_features' in result:
                            st.subheader("🔍 AI Detected Features")
                            est = result['estimated_features']
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Model Year", est['model_year'])
                            with col2:
                                st.metric("Mileage", f"{est['mileage']:,.0f} mi")
                            with col3:
                                st.metric("Horsepower", f"{est['horsepower']} HP")
                            
                            st.info(result.get('message', ''))
                    else:
                        st.error(f"Error: {response.json().get('error', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🚗 Car Price Prediction System | Powered by Machine Learning</p>
    <p>© 2025 - Built with Streamlit & Flask</p>
</div>
""", unsafe_allow_html=True)
