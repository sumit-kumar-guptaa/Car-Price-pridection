@echo off
echo ========================================
echo RETRAINING MODEL WITH USD PRICES
echo ========================================
echo.
echo This will:
echo 1. Delete old model files
echo 2. Train new model on USD prices
echo 3. Save corrected model files
echo.
pause

echo.
echo Step 1: Cleaning old models...
if exist "models\best_model.pkl" (
    del /Q "models\*.pkl"
    echo ✅ Old models deleted
) else (
    echo ℹ️ No old models found
)

echo.
echo Step 2: Training new model on USD...
python model_training.py

echo.
echo ========================================
echo ✅ RETRAINING COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Run: python app.py (to start backend)
echo 2. Run: cd frontend ^&^& npm start (to start frontend)
echo 3. Test predictions on http://localhost:3000
echo.
pause
