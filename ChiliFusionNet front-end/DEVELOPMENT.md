# ChiliFusionNet Frontend Development Guide

## 🚀 Quick Start

1. **Run setup script:**
   ```bash
   # On Windows
   setup.bat
   
   # On Linux/Mac
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Start development server:**
   ```bash
   pnpm dev
   # or npm run dev / yarn dev
   ```

3. **Open your browser to:** [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure Overview

```
chiliFusionNet-frontend/
├── 📋 Configuration Files
│   ├── package.json          # Dependencies and scripts
│   ├── vite.config.ts        # Vite build configuration
│   ├── tsconfig.json         # TypeScript configuration
│   ├── tailwind.config.js    # Tailwind CSS configuration
│   ├── .eslintrc.cjs         # ESLint rules
│   ├── .prettierrc           # Prettier formatting
│   └── .husky/               # Git hooks
│
├── 🌐 Public Assets
│   ├── index.html            # HTML template
│   ├── favicon.ico           # Site icon
│   └── examples/             # Demo images (TODO: add real images)
│
├── 💻 Source Code
│   ├── main.tsx              # App entry point
│   ├── App.tsx               # Main app component
│   ├── styles/globals.css    # Global styles
│   │
│   ├── 🧩 components/        # Reusable UI components
│   │   ├── Navbar.tsx        # Navigation bar
│   │   ├── Footer.tsx        # Page footer
│   │   └── Toast.tsx         # Notifications (placeholder)
│   │
│   ├── 📄 pages/             # Page components
│   │   ├── Home.tsx          # Landing page
│   │   ├── Introduction.tsx  # Research intro
│   │   ├── Method.tsx        # Methodology
│   │   ├── Results.tsx       # Results & metrics
│   │   ├── Dataset.tsx       # Dataset info
│   │   ├── Demo.tsx          # Interactive demo
│   │   └── Team.tsx          # Team, references, 404
│   │
│   ├── 📚 lib/               # Utilities and constants
│   │   ├── constants.ts      # App constants
│   │   ├── formatters.ts     # Data formatting
│   │   └── classLabels.json  # Disease classes
│   │
│   └── 🔧 mocks/             # API mocking with MSW
│       ├── handlers.ts       # Mock API responses
│       └── browser.ts        # MSW setup
│
└── 📖 Documentation
    ├── README.md             # Main documentation
    ├── DEVELOPMENT.md        # This file
    ├── setup.sh              # Linux/Mac setup
    └── setup.bat             # Windows setup
```

## 🎯 Current Implementation Status

### ✅ Completed
- [x] **Project Setup**: Vite + React + TypeScript configured
- [x] **Styling**: Tailwind CSS with dark mode support
- [x] **Routing**: React Router v6 with all routes
- [x] **Components**: Basic Navbar, Footer, Toast placeholder
- [x] **Pages**: All page components with placeholders
- [x] **Mocking**: MSW setup for API simulation
- [x] **Development Tools**: ESLint, Prettier, Husky configured
- [x] **Constants**: Disease classes and sample metrics defined

### 🚧 TODO - High Priority
- [ ] **Extract PDF Content**: Replace TODO placeholders with actual research content
- [ ] **Demo UI**: Implement complete side-by-side inference interface
- [ ] **File Upload**: Drag-and-drop component with validation
- [ ] **Charts**: Implement results visualization with Recharts
- [ ] **Real Images**: Add actual chili disease images to examples/
- [ ] **API Integration**: Connect to real ML model backend

### 🔮 TODO - Future Enhancements
- [ ] **Accessibility**: Complete ARIA labels and keyboard navigation
- [ ] **Performance**: Image optimization and lazy loading
- [ ] **Testing**: Unit and integration tests
- [ ] **PWA**: Progressive Web App features
- [ ] **Internationalization**: Multi-language support

## 🛠️ Development Tasks

### 1. Content Integration (Priority 1)

**Extract from PDFs and update:**

1. **Introduction Page** (`src/pages/Introduction.tsx`)
   - Replace TODO with content from `introduction chili.pdf`
   - Add methodology highlights
   - Include smart agriculture context

2. **Method Page** (`src/pages/Method.tsx`)
   - Add IEX-FeatureNet details
   - Describe ChiliFusionNet ensemble
   - Include algorithm descriptions (XGBoost, LGBM, RF, Extra Trees, LR)

3. **Results Page** (`src/pages/Results.tsx`)
   - Extract metrics from `Result analysis and discussion.pdf`
   - Add confusion matrix data
   - Include ROC curve information
   - Add cross-validation results

4. **Constants** (`src/lib/constants.ts`)
   - Update `MODEL_METRICS` with real values
   - Add actual dataset information
   - Update sample metrics with real data

### 2. Demo Implementation (Priority 2)

**Create comprehensive demo interface:**

1. **File Upload Component** (`src/components/FileDropzone.tsx`)
   ```typescript
   interface FileDropzoneProps {
     onFileSelect: (file: File) => void;
     accept: string[];
     maxSize: number;
     disabled?: boolean;
   }
   ```

2. **Split Pane Layout** (`src/components/SplitPane.tsx`)
   - Left: Image preview with zoom/pan
   - Right: Results display
   - Responsive mobile layout

3. **Results Display** (`src/features/demo/ResultPanel.tsx`)
   - Top-1 prediction with confidence
   - Top-k results list with progress bars
   - Optional Grad-CAM heatmap overlay

4. **Example Gallery** (`src/features/demo/ExampleGallery.tsx`)
   - 6 example images for each disease class
   - Click to load into preview

### 3. UI Components (Priority 3)

**Implement missing components:**

1. **Button** (`src/components/Button.tsx`)
2. **Card** (`src/components/Card.tsx`)
3. **Badge** (`src/components/Badge.tsx`)
4. **Tooltip** (`src/components/Tooltip.tsx`)
5. **Toast System** (`src/components/Toast.tsx`) - integrate Radix UI
6. **Skeleton Loaders** (`src/components/Skeleton.tsx`)
7. **Progress Bars** (`src/components/ProgressList.tsx`)

### 4. Charts and Visualization (Priority 4)

**Implement with Recharts:**

1. **Bar Chart** - Per-class F1 scores
2. **Line Chart** - Training/validation curves
3. **Confusion Matrix** - Custom table or heatmap
4. **ROC Curves** - Multi-class ROC visualization

## 🎨 Design System

### Color Palette
```css
/* Primary (Green - leaf theme) */
--primary-50: #f0fdf4
--primary-500: #22c55e
--primary-600: #16a34a

/* Accent (Red - chili theme) */
--accent-500: #ef4444
--accent-600: #dc2626

/* Neutral */
--neutral-100: #f5f5f5
--neutral-500: #737373
--neutral-900: #171717
```

### Typography
- **Font**: Inter (system fallback)
- **Headings**: Bold, multiple sizes
- **Body**: Regular weight, high contrast
- **Code**: Monospace for metrics

### Layout
- **Container**: Max width 7xl with responsive padding
- **Sections**: Consistent padding classes
- **Cards**: Rounded corners, subtle shadows
- **Hover Effects**: Scale and shadow transitions

## 🔧 Development Commands

```bash
# Development
pnpm dev                 # Start dev server
pnpm build              # Build for production
pnpm preview            # Preview production build

# Code Quality
pnpm lint               # Run ESLint
pnpm lint:fix           # Fix ESLint issues
pnpm format             # Format with Prettier
pnpm type-check         # TypeScript checking

# Dependencies
pnpm add <package>      # Add dependency
pnpm add -D <package>   # Add dev dependency
pnpm update             # Update all packages
```

## 🐛 Debugging

### Common Issues

1. **Build Errors**
   - Check TypeScript types
   - Verify all imports exist
   - Run `pnpm type-check`

2. **Style Issues**
   - Check Tailwind class names
   - Verify dark mode classes
   - Inspect with browser dev tools

3. **MSW Not Working**
   - Check service worker registration
   - Verify handlers in browser dev tools
   - Clear browser cache

### Development Tools

- **VS Code Extensions**: 
  - TypeScript Hero
  - Tailwind CSS IntelliSense
  - ESLint
  - Prettier
  - Auto Rename Tag

- **Browser Extensions**:
  - React Developer Tools
  - Lighthouse for performance

## 📊 Performance Targets

- **Lighthouse Score**: 95+ in all categories
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Bundle Size**: < 500KB gzipped
- **Accessibility**: WCAG AA compliant

## 🚢 Deployment

### Build Process
```bash
pnpm build              # Creates dist/ folder
pnpm preview            # Test production build locally
```

### Environment Variables
```env
VITE_API_URL=https://your-api-url.com  # Switch from MSW to real API
```

### Static Hosting
- **Vercel**: Connect GitHub repo for auto-deploy
- **Netlify**: Drag & drop dist folder
- **GitHub Pages**: Use GitHub Actions workflow

## 🤝 Contributing

1. **Code Style**: Follow Prettier and ESLint rules
2. **Commits**: Use conventional commit format
3. **Branches**: Use feature branches for development
4. **Testing**: Add tests for new components
5. **Documentation**: Update README for new features

## 📞 Support

For questions about this implementation:
- Check existing TODO comments in code
- Review component prop interfaces
- Refer to library documentation (Tailwind, Radix UI, etc.)
- Test with MSW mock API first before real backend integration

---

**Happy coding! 🌶️✨**
