# ChiliFusionNet - Quick Start Script (PowerShell)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ChiliFusionNet - Quick Start Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "  Please install Python 3.10+ and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Node.js is installed
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "  Please install Node.js 18+ and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[1/6] Setting up Backend..." -ForegroundColor Yellow

Set-Location back-end

# Create virtual environment if it doesn't exist
if (-Not (Test-Path "chilifusionnet")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv chilifusionnet
}

# Activate virtual environment and install dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Cyan
& .\chilifusionnet\Scripts\Activate.ps1
pip install -r requirements.txt
pip install python-multipart

# Create uploads directory
if (-Not (Test-Path "uploads")) {
    New-Item -ItemType Directory -Path "uploads" | Out-Null
}

Write-Host ""
Write-Host "✓ [2/6] Backend setup complete!" -ForegroundColor Green
Write-Host ""

Set-Location ..

Write-Host "[3/6] Setting up Frontend..." -ForegroundColor Yellow
Set-Location "ChiliFusionNet front-end"

# Install frontend dependencies
Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
npm install

Write-Host ""
Write-Host "✓ [4/6] Frontend setup complete!" -ForegroundColor Green
Write-Host ""

Set-Location ..

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Start Backend (in terminal 1):" -ForegroundColor Cyan
Write-Host "   cd back-end" -ForegroundColor White
Write-Host "   .\chilifusionnet\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   uvicorn app.main:app --reload" -ForegroundColor White
Write-Host ""
Write-Host "2. Start Frontend (in terminal 2):" -ForegroundColor Cyan
Write-Host "   cd 'ChiliFusionNet front-end'" -ForegroundColor White
Write-Host "   npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "3. Open browser: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

Read-Host "Press Enter to exit"
