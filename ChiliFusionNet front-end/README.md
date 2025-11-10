# ChiliFusionNet Frontend

A modern React TypeScript application for chili leaf disease detection using machine learning.

## Features

- 🌶️ **Advanced Disease Detection**: Classify 6 types of chili leaf diseases
- 🚀 **Fast & Accurate**: 95%+ accuracy with ensemble learning
- 🎨 **Modern UI**: Built with Tailwind CSS and Radix UI
- 🌙 **Dark Mode**: Elegant light/dark theme switching
- 📱 **Responsive**: Mobile-first design
- ♿ **Accessible**: WCAG AA compliant
- 🔧 **Developer Experience**: TypeScript, ESLint, Prettier, Husky

## Tech Stack

- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Routing**: React Router v6
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Charts**: Recharts
- **API Mocking**: MSW (Mock Service Worker)
- **Linting**: ESLint + Prettier
- **Git Hooks**: Husky + lint-staged

## Disease Classes

The model can detect the following chili leaf diseases:

1. **Bacterial Spot** - Bacterial infection causing dark spots
2. **Cercospora Leaf Spot** - Fungal disease with circular lesions
3. **Curl Virus** - Viral disease causing leaf curling
4. **Healthy Leaf** - No disease detected
5. **Nutrition Deficiency** - Nutrient-related issues
6. **White Spot** - Fungal infection with white lesions

## Getting Started

### Prerequisites

- Node.js 18+ 
- pnpm (recommended) or npm/yarn

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd chiliFusionNet-frontend
   ```

2. Install dependencies:
   ```bash
   pnpm install
   # or
   npm install
   ```

3. Start the development server:
   ```bash
   pnpm dev
   # or
   npm run dev
   ```

4. Open your browser to [http://localhost:3000](http://localhost:3000)

### Available Scripts

- `pnpm dev` - Start development server
- `pnpm build` - Build for production
- `pnpm preview` - Preview production build
- `pnpm lint` - Run ESLint
- `pnpm lint:fix` - Fix ESLint issues
- `pnpm format` - Format code with Prettier
- `pnpm type-check` - Run TypeScript type checking

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Navbar.tsx      # Navigation bar
│   ├── Footer.tsx      # Page footer
│   ├── Button.tsx      # Button component
│   ├── Card.tsx        # Card component
│   ├── Badge.tsx       # Badge component
│   ├── Tooltip.tsx     # Tooltip component
│   ├── Toast.tsx       # Toast notifications
│   ├── Skeleton.tsx    # Loading skeletons
│   ├── FileDropzone.tsx # File upload area
│   ├── SplitPane.tsx   # Split layout component
│   ├── HeatmapOverlay.tsx # Grad-CAM visualization
│   ├── ProgressList.tsx # Progress bar list
│   └── Charts/         # Chart components
├── features/demo/      # Demo page features
│   ├── UploadPanel.tsx # Image upload panel
│   ├── ResultPanel.tsx # Results display
│   ├── ExampleGallery.tsx # Example images
│   └── api.ts          # API functions
├── pages/              # Page components
│   ├── Home.tsx        # Landing page
│   ├── Introduction.tsx # Research introduction
│   ├── Method.tsx      # Methodology
│   ├── Results.tsx     # Results & metrics
│   ├── Dataset.tsx     # Dataset information
│   ├── Demo.tsx        # Interactive demo
│   ├── Team.tsx        # Team information
│   ├── References.tsx  # Citations
│   └── NotFound.tsx    # 404 page
├── lib/                # Utilities
│   ├── constants.ts    # App constants
│   ├── formatters.ts   # Data formatters
│   └── classLabels.json # Disease classes
├── mocks/              # MSW mock handlers
│   ├── handlers.ts     # API mock handlers
│   └── browser.ts      # MSW setup
├── styles/
│   └── globals.css     # Global styles
├── App.tsx             # Main app component
└── main.tsx            # App entry point
```

## API Integration

The app currently uses Mock Service Worker (MSW) for development. To switch to a real API:

1. Set the `VITE_API_URL` environment variable:
   ```bash
   echo "VITE_API_URL=https://your-api-url.com" > .env.local
   ```

2. The app will automatically use the real API instead of mocks when this variable is set.

### API Endpoints

- `POST /api/infer` - Upload image for disease detection
- `GET /api/examples` - Get example images metadata

### Request/Response Format

**Inference Request:**
```javascript
FormData with 'image' field containing the uploaded file
```

**Inference Response:**
```javascript
{
  model: "ChiliFusionNet",
  timestamp: "2025-12-09T12:00:00Z",
  fileName: "example.jpg",
  top1: {
    label: "Bacterial Spot",
    confidence: 0.92
  },
  topk: [
    { label: "Bacterial Spot", confidence: 0.92 },
    { label: "Cercospora Leaf Spot", confidence: 0.05 },
    { label: "White Spot", confidence: 0.02 }
  ],
  heatmap?: "data:image/png;base64,..." // Optional Grad-CAM
}
```

## Dark Mode

The app supports system preference detection and manual theme switching. Theme preference is persisted in localStorage.

## Accessibility

- Keyboard navigation support
- Screen reader compatibility
- High contrast ratios (WCAG AA)
- Focus indicators
- Semantic HTML
- ARIA labels where needed

## Performance

- Optimized bundle size with Vite
- Lazy loading for routes
- Image optimization
- Tree shaking
- Code splitting

## Browser Support

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run linting and tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Research Citation

If you use this work in your research, please cite:

```bibtex
@article{chilifusionnet2025,
  title={ChiliFusionNet: Advanced Chili Leaf Disease Detection using Ensemble Learning},
  author={TODO: Add authors},
  journal={TODO: Add journal},
  year={2025}
}
```

## TODO

- [ ] Replace placeholder content with real research data
- [ ] Add actual confusion matrix and ROC curves
- [ ] Implement real training curve visualizations
- [ ] Add more example images for each disease class
- [ ] Integrate with real ML model backend
- [ ] Add more detailed methodology diagrams
- [ ] Include cross-validation results
- [ ] Add XAI (Explainable AI) visualizations

## Contact

For questions about this research or the application, please contact:

- **Research Team**: TODO: Add contact information
- **Technical Issues**: Please open an issue on GitHub
