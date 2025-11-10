#!/bin/bash

# ChiliFusionNet Frontend Setup Script
echo "🌶️ Setting up ChiliFusionNet Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check Node.js version
node_version=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$node_version" -lt 18 ]; then
    echo "❌ Node.js version 18 or higher is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) detected"

# Install dependencies
echo "📦 Installing dependencies..."
if command -v pnpm &> /dev/null; then
    echo "Using pnpm..."
    pnpm install
elif command -v yarn &> /dev/null; then
    echo "Using yarn..."
    yarn install
else
    echo "Using npm..."
    npm install
fi

# Initialize git hooks
echo "🔧 Setting up git hooks..."
if [ -d ".git" ]; then
    npx husky install
    echo "✅ Git hooks initialized"
else
    echo "⚠️  Not a git repository. Skipping git hooks setup."
fi

# Generate MSW service worker
echo "🔧 Setting up MSW service worker..."
npx msw init public/ --save

echo "🎉 Setup complete!"
echo ""
echo "🚀 To start development:"
echo "   pnpm dev (or npm run dev / yarn dev)"
echo ""
echo "📝 Next steps:"
echo "   1. Replace TODO placeholders with actual research content"
echo "   2. Add real chili leaf disease images to public/examples/"
echo "   3. Update constants.ts with actual metrics from PDFs"
echo "   4. Implement complete Demo UI with file upload"
echo "   5. Add real API integration when backend is ready"
echo ""
echo "📚 See README.md for detailed documentation"
