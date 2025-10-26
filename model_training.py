# Model Training Script - Train and Save the Best Model
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Currency conversion rate: 1 USD = 83 INR
USD_TO_INR = 83

print("="*70)
print("🇮🇳 CAR PRICE PREDICTION MODEL TRAINING (INR)")
print("="*70)
print(f"💱 Currency Conversion: 1 USD = ₹{USD_TO_INR}")
print("="*70)

# Create models directory if not exists
if not os.path.exists('models'):
    os.makedirs('models')
    print("\n✅ Created 'models' directory")

print("\n📂 Loading dataset...")
df = pd.read_csv('Dataset/used_cars.csv')
print(f"✅ Loaded {len(df):,} records with {len(df.columns)} columns")

# Data Cleaning
print("\n🧹 Cleaning data...")
df_clean = df.copy()

# Convert price from USD to INR
df_clean['price_usd'] = df_clean['price'].str.replace('$', '').str.replace(',', '').astype(float)
df_clean['price_clean'] = df_clean['price_usd'] * USD_TO_INR  # Price in INR

print(f"✅ Converted prices from USD to INR")
print(f"   Original range: ${df_clean['price_usd'].min():,.0f} - ${df_clean['price_usd'].max():,.0f}")
print(f"   INR range: ₹{df_clean['price_clean'].min():,.0f} - ₹{df_clean['price_clean'].max():,.0f}")

df_clean['milage_clean'] = df_clean['milage'].str.replace(' mi.', '').str.replace(',', '').astype(float)
df_clean['horsepower'] = df_clean['engine'].str.extract('(\d+\.?\d*)HP').astype(float)
df_clean['engine_size'] = df_clean['engine'].str.extract('(\d+\.?\d*)L').astype(float)

# Fill missing values
df_clean['fuel_type'] = df_clean['fuel_type'].fillna(df_clean['fuel_type'].mode()[0])
df_clean['accident'] = df_clean['accident'].fillna('None reported')
df_clean['clean_title'] = df_clean['clean_title'].fillna('Yes')

# Feature Engineering
df_model = df_clean.copy()
df_model['car_age'] = 2025 - df_model['model_year']
df_model['has_accident'] = df_model['accident'].apply(lambda x: 0 if x == 'None reported' else 1)
df_model['is_clean_title'] = df_model['clean_title'].apply(lambda x: 1 if x == 'Yes' else 0)

# Drop rows with missing values
df_model = df_model.dropna(subset=['price_clean', 'milage_clean', 'model_year'])

# Encode categorical variables
df_encoded = df_model.copy()
le_brand = LabelEncoder()
le_fuel = LabelEncoder()
le_trans = LabelEncoder()

df_encoded['brand_encoded'] = le_brand.fit_transform(df_encoded['brand'])
df_encoded['fuel_type_encoded'] = le_fuel.fit_transform(df_encoded['fuel_type'])
df_encoded['transmission_encoded'] = le_trans.fit_transform(df_encoded['transmission'])

# Fill missing horsepower and engine_size
df_encoded['horsepower'] = df_encoded['horsepower'].fillna(df_encoded['horsepower'].median())
df_encoded['engine_size'] = df_encoded['engine_size'].fillna(df_encoded['engine_size'].median())

# Prepare features and target
X = df_encoded[['brand_encoded', 'model_year', 'milage_clean', 'fuel_type_encoded', 
                'transmission_encoded', 'car_age', 'has_accident', 'is_clean_title',
                'horsepower', 'engine_size']]
y = df_encoded['price_clean']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\nTraining models...")

# Train multiple models
models = {
    'Random Forest': RandomForestRegressor(n_estimators=200, random_state=42, max_depth=15, n_jobs=-1),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=200, random_state=42, max_depth=7, learning_rate=0.1),
    'XGBoost': xgb.XGBRegressor(n_estimators=200, random_state=42, max_depth=7, learning_rate=0.1, n_jobs=-1)
}

best_model = None
best_score = 0
best_name = ""

for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"  MAE: ${mae:,.2f}")
    print(f"  RMSE: ${rmse:,.2f}")
    print(f"  R² Score: {r2:.4f}")
    
    if r2 > best_score:
        best_score = r2
        best_model = model
        best_name = name

print(f"\n🏆 Best Model: {best_name} with R² Score: {best_score:.4f}")

# Save the best model and encoders
print("\nSaving model and encoders...")
with open('models/best_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

with open('models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

with open('models/label_encoders.pkl', 'wb') as f:
    pickle.dump({
        'brand': le_brand,
        'fuel_type': le_fuel,
        'transmission': le_trans
    }, f)

# Save feature names
with open('models/feature_names.pkl', 'wb') as f:
    pickle.dump(list(X.columns), f)

# Save brand mappings for reference
brand_mapping = dict(zip(le_brand.classes_, le_brand.transform(le_brand.classes_)))
fuel_mapping = dict(zip(le_fuel.classes_, le_fuel.transform(le_fuel.classes_)))
trans_mapping = dict(zip(le_trans.classes_, le_trans.transform(le_trans.classes_)))

with open('models/mappings.pkl', 'wb') as f:
    pickle.dump({
        'brands': list(le_brand.classes_),
        'fuel_types': list(le_fuel.classes_),
        'transmissions': list(le_trans.classes_)
    }, f)

print("\n✅ Model training completed successfully!")
print(f"Model saved as: models/best_model.pkl")
print(f"Model type: {best_name}")
