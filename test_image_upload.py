"""
Test script to verify image upload works correctly
"""
import requests
from PIL import Image
import io

# Create a simple test image
print("📸 Creating test image...")
test_image = Image.new('RGB', (640, 480), color='red')
img_byte_arr = io.BytesIO()
test_image.save(img_byte_arr, format='JPEG')
img_byte_arr.seek(0)

# Prepare the request
files = {'image': ('test_car.jpg', img_byte_arr, 'image/jpeg')}
data = {
    'brand': 'BMW',
    'fuel_type': 'Gasoline',
    'transmission': 'Automatic',
    'has_accident': 0,
    'is_clean_title': 1
}

print("🚀 Sending request to backend...")
try:
    response = requests.post('http://localhost:5000/predict_image', files=files, data=data, timeout=10)
    print(f"\n✅ Status Code: {response.status_code}")
    print(f"📋 Response: {response.json()}")
except Exception as e:
    print(f"\n❌ Error: {e}")
