@echo off
REM ChiliFusionNet Frontend Setup Script for Windows

echo 🌶️ Setting up ChiliFusionNet Frontend...

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    pause
    exit /b 1
)

echo ✅ Node.js detected
node --version

REM Install dependencies
echo 📦 Installing dependencies...
where pnpm >nul 2>&1
if %errorlevel% equ 0 (
    echo Using pnpm...
    pnpm install
) else (
    where yarn >nul 2>&1
    if %errorlevel% equ 0 (
        echo Using yarn...
        yarn install
    ) else (
        echo Using npm...
        npm install
    )
)

REM Initialize git hooks
echo 🔧 Setting up git hooks...
if exist ".git" (
    npx husky install
    echo ✅ Git hooks initialized
) else (
    echo ⚠️  Not a git repository. Skipping git hooks setup.
)

REM Generate MSW service worker
echo 🔧 Setting up MSW service worker...
npx msw init public/ --save

echo 🎉 Setup complete!
echo.
echo 🚀 To start development:
echo    pnpm dev (or npm run dev / yarn dev)
echo.
echo 📝 Next steps:
echo    1. Replace TODO placeholders with actual research content
echo    2. Add real chili leaf disease images to public/examples/
echo    3. Update constants.ts with actual metrics from PDFs
echo    4. Implement complete Demo UI with file upload
echo    5. Add real API integration when backend is ready
echo.
echo 📚 See README.md for detailed documentation
pause
