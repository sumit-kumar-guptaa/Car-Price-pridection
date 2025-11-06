@echo off
cls
echo ========================================
echo   FLASK BACKEND - CAR PRICE API
echo ========================================
echo.
echo [1/3] Activating virtual environment...
call venv\Scripts\activate
echo.

echo [2/3] Checking model files...
if not exist "models\best_model.pkl" (
    echo ERROR: Model files not found!
    echo Please run: python model_training.py
    pause
    exit /b 1
)
echo.

echo [3/3] Starting Flask backend...
echo ========================================
echo Keep this window OPEN!
echo ========================================
echo.
python app.py
pause
