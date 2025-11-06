@echo off
echo ========================================
echo Installing React Dependencies
echo ========================================
cd frontend
npm install

echo.
echo ========================================
echo Starting React Frontend
echo ========================================
echo Frontend will be available at: http://localhost:3000
echo Backend should be running at: http://localhost:5000
echo.
npm start
