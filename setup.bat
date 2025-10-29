@echo off
echo ========================================
echo   ChiliFusionNet - Quick Start Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ and try again
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ and try again
    pause
    exit /b 1
)

echo [1/6] Setting up Backend...
cd back-end

REM Create virtual environment if it doesn't exist
if not exist chilifusionnet (
    echo Creating virtual environment...
    python -m venv chilifusionnet
)

REM Activate virtual environment and install dependencies
echo Installing backend dependencies...
call chilifusionnet\Scripts\activate.bat
pip install -r requirements.txt
pip install python-multipart

REM Create uploads directory
if not exist uploads mkdir uploads

echo.
echo [2/6] Backend setup complete!
echo.

cd ..

echo [3/6] Setting up Frontend...
cd "ChiliFusionNet front-end"

REM Install frontend dependencies
echo Installing frontend dependencies...
call npm install

echo.
echo [4/6] Frontend setup complete!
echo.

cd ..

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo.
echo 1. Start Backend (in terminal 1):
echo    cd back-end
echo    chilifusionnet\Scripts\activate.bat
echo    uvicorn app.main:app --reload
echo.
echo 2. Start Frontend (in terminal 2):
echo    cd "ChiliFusionNet front-end"
echo    npm run dev
echo.
echo 3. Open browser: http://localhost:5173
echo.
echo ========================================

pause
