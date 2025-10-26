@echo off
echo ======================================
echo Car Price Prediction System
echo ======================================
echo.

echo Step 1: Training Model...
python model_training.py
if %errorlevel% neq 0 (
    echo Error: Model training failed!
    pause
    exit /b 1
)

echo.
echo ======================================
echo Model training completed!
echo ======================================
echo.
echo Now you can run:
echo   1. Backend API: python app.py
echo   2. Frontend UI: streamlit run streamlit_app.py
echo.
pause
