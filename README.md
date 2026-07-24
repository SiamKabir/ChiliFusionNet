# ChiliFusionNet - Fast and Accurate Chili Leaf Disease Detection

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15+-FF6F00.svg)](https://www.tensorflow.org/)

> **Explainable chili leaf disease classification using an interpretable stacking ensemble framework with feature-level fusion**

## 📋 Table of Contents

- [Overview](#-overview)
- [Video Walkthrough](#-video-walkthrough)
- [Methodology](#-methodology)
- [Web Interface](#️-web-interface)
- [Features](#-features)
- [Dataset Information](#-dataset-information)
- [Model Performance](#-model-performance)
- [System Architecture](#️-system-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Model Development](#-model-development)
- [Contributing](#-contributing)
- [Authors](#-authors)
- [License](#-license)

## 🔬 Overview

ChiliFusionNet is a comprehensive deep learning framework designed for accurate chili leaf disease detection using advanced computer vision techniques. This research implements an ensemble approach combining three state-of-the-art CNN architectures (InceptionResNetV2, EfficientNetB3, and Xception) with a machine learning classifier to achieve optimal disease classification accuracy.

### Key Research Contributions

- **Ensemble Feature Extraction**: Fusion of features from InceptionResNetV2, EfficientNetB3, and Xception models
- **Multi-Disease Classification**: Detection of 6 chili leaf disease categories
- **Real-time Web Platform**: Interactive disease detection interface for agricultural professionals
- **High Accuracy**: Robust performance across diverse disease manifestations
- **Transfer Learning**: Leveraging pre-trained ImageNet weights for enhanced feature extraction

### 🎯 Research Objective

The primary goal is to develop an accurate, efficient, and accessible deep learning model for chili leaf disease detection that can assist farmers and agricultural experts in early diagnosis, enabling timely intervention and reducing crop losses.

## 🎥 Video Walkthrough

Watch our comprehensive demonstration of ChiliFusionNet:

[![ChiliFusionNet Demo](https://img.youtube.com/vi/oKB9zI70Df0/maxresdefault.jpg)](https://youtu.be/oKB9zI70Df0)

**[▶️ Watch on YouTube](https://youtu.be/oKB9zI70Df0)**

The video covers:
- System architecture overview
- Live disease detection demo
- Feature extraction process
- Web interface walkthrough
- Performance comparison

## 🧬 Methodology

![Methodology Diagram](Diagrams/Methodology%20Diagram.png)

Our research methodology follows a systematic approach combining deep learning feature extraction with ensemble learning. The framework integrates three powerful CNN architectures to extract complementary features from chili leaf images, followed by a machine learning classifier for final disease classification. This comprehensive pipeline ensures robust model validation and agricultural relevance assessment.

## 🖥️ Web Interface

![Web Implementation Diagram](Diagrams/Web%20Implementation%20Diagram.png)

The ChiliFusionNet framework implements a comprehensive multi-tier architecture integrating:
1. **Feature Extraction Layer**: Three parallel CNN feature extractors (InceptionResNetV2, EfficientNetB3, Xception)
2. **Feature Fusion Layer**: Concatenation of extracted feature vectors
3. **Classification Layer**: Machine learning classifier (trained ensemble model)
4. **Web Deployment Layer**: FastAPI backend with React frontend for real-time predictions

This scalable design ensures seamless integration between the deep learning models, API backend, and interactive web interface for real-time agricultural decision support.

### Ensemble Architecture Details

**Feature Extractors:**
- **InceptionResNetV2**: 
  - Input: 224×224×3 images
  - Pre-trained on ImageNet
  - Extraction from last pooling layer
  
- **EfficientNetB3**: 
  - Input: 224×224×3 images
  - Compound scaling optimization
  - Efficient feature representation
  
- **Xception**: 
  - Input: 224×224×3 images
  - Depthwise separable convolutions
  - Enhanced gradient flow

**Fusion Strategy:**
- Concatenation of all feature vectors
- Dimensionality: Combined feature space from all three models
- Classifier: Joblib-serialized ensemble model (chili_fusionnet.joblib)

## ✨ Features

### 🔍 Deep Learning Models

- **InceptionResNetV2**: Hybrid architecture combining Inception modules with residual connections
- **EfficientNetB3**: Compound scaling for optimal accuracy-efficiency trade-off
- **Xception**: Extreme inception with depthwise separable convolutions
- **ChiliFusionNet Ensemble**: Fused feature extraction with ML classifier

### 🌱 Disease Classification

The system detects and classifies 6 chili leaf disease categories:

1. **Bacterial Spot** - Bacterial infection causing leaf spots
2. **Cercospora Leaf Spot** - Fungal disease with circular lesions
3. **Curl Virus** - Viral disease causing leaf curling
4. **Healthy Leaf** - Normal healthy chili leaves
5. **Nutrition Deficiency** - Nutrient-related leaf discoloration
6. **White Spot** - Fungal/bacterial white spotting

### 🌐 Web Platform Features

- **Image Upload**: Direct image upload for disease detection
- **Example Gallery**: Pre-loaded sample images from each disease category
- **Real-time Prediction**: Instant disease classification with confidence scores
- **Probability Distribution**: Detailed probability breakdown for all disease classes
- **Responsive Design**: Mobile-friendly interface for field use
- **Visual Feedback**: Color-coded confidence indicators

## 📊 Dataset Information

The study utilizes a comprehensive dataset of chili leaf images:

- **Total Images**: Extensive collection across 6 disease categories
- **Image Format**: RGB color images
- **Image Preprocessing**: Model-specific resizing and normalization
- **Class Distribution**: Balanced representation across disease types

### Disease Categories

| Category | Description | Symptoms |
|----------|-------------|----------|
| **Bacterial Spot** | Bacterial pathogen infection | Dark spots with yellow halos |
| **Cercospora Leaf Spot** | Fungal infection | Circular brown lesions |
| **Curl Virus** | Viral infection | Leaf curling, yellowing |
| **Healthy Leaf** | No disease present | Normal green coloration |
| **Nutrition Deficiency** | Nutrient imbalance | Chlorosis, discoloration |
| **White Spot** | Fungal/bacterial infection | White powdery spots |

## 🏆 Model Performance

### Ensemble Performance

The ChiliFusionNet ensemble model achieves robust performance across all disease categories:

- 🎯 **High Accuracy**: Superior classification performance
- 📈 **Robust Predictions**: Consistent probability distributions
- ⚡ **Fast Inference**: Sub-second prediction time
- 🔄 **Model Reliability**: Stable predictions across varied image conditions

### Performance Highlights

- **Multi-Model Feature Extraction**: Leverages strengths of 3 CNN architectures
- **Comprehensive Feature Space**: Rich feature representation from ensemble approach
- **Real-time Processing**: Optimized for web-based deployment
- **Cross-Disease Accuracy**: Effective discrimination across all 6 categories

## 🏗️ System Architecture

```
ChiliFusionNet/
├── 🎨 ChiliFusionNet front-end/    # React.js + Vite Web Interface
│   ├── src/
│   │   ├── components/             # UI Components
│   │   │   ├── ExampleImages.tsx   # Sample image gallery
│   │   │   ├── Footer.tsx          # Footer component
│   │   │   ├── Navbar.tsx          # Navigation bar
│   │   │   └── Toast.tsx           # Notification system
│   │   ├── pages/                  # Application pages
│   │   │   ├── Home.tsx            # Landing page
│   │   │   ├── Demo.tsx            # Prediction interface
│   │   │   ├── Introduction.tsx    # Project overview
│   │   │   ├── Method.tsx          # Methodology page
│   │   │   ├── Abstract.tsx        # Research abstract
│   │   │   ├── Dataset.tsx         # Dataset information
│   │   │   ├── Results.tsx         # Model performance
│   │   │   └── Team.tsx            # Author information
│   │   ├── services/
│   │   │   └── api.ts              # API client
│   │   ├── lib/
│   │   │   ├── classLabels.json    # Disease labels
│   │   │   ├── constants.ts        # Configuration
│   │   │   └── formatters.ts       # Utility functions
│   │   └── styles/
│   │       └── globals.css         # Global styling
│   ├── public/
│   │   └── sample images/          # Example images (8 samples)
│   ├── vite.config.ts              # Vite configuration
│   └── package.json                # Node.js dependencies
│
├── 🚀 back-end/                    # FastAPI Server
│   ├── app/
│   │   ├── main.py                 # FastAPI application & routes
│   │   ├── predict.py              # Prediction orchestration
│   │   ├── single_pre.py           # Feature extraction pipeline
│   │   ├── load_model_utils.py     # Model loading utilities
│   │   ├── schemas.py              # Pydantic schemas
│   │   ├── preprocess.py           # Image preprocessing
│   │   └── utils.py                # Helper functions
│   ├── models/                     # Trained models
│   │   ├── chili_fusionnet.joblib  # Ensemble classifier
│   │   ├── class_map.json          # Class label mapping
│   │   ├── inception_resnet_v2_feature_extractor.keras
│   │   ├── efficientnet_b3_feature_extractor.keras
│   │   └── xception_feature_extractor.keras
│   ├── uploads/                    # User uploaded images
│   ├── images/                     # Test dataset
│   │   └── test/                   # Test images by category
│   │       ├── Bacterial Spot/
│   │       ├── Cercospora Leaf Spot/
│   │       ├── Curl Virus/
│   │       ├── Healthy Leaf/
│   │       ├── Nutrition Deficiency/
│   │       └── White spot/
│   └── requirements.txt            # Python dependencies
│
├── 📊 Diagrams/                    # Research diagrams
│   ├── Methodology Diagram.png
│   └── Web Implementation Diagram.png
│
├── .gitignore                      # Git ignore rules
└── README.md                       # Project documentation
```

### Technology Stack

**Frontend:**
- React 18.3+ with TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- Axios (HTTP client)
- React Router (navigation)

**Backend:**
- FastAPI (high-performance API framework)
- TensorFlow/Keras (deep learning)
- Scikit-learn (machine learning)
- Joblib (model serialization)
- Pillow (image processing)
- Python 3.10+

**Deep Learning:**
- InceptionResNetV2 (TensorFlow/Keras)
- EfficientNetB3 (TensorFlow/Keras)
- Xception (TensorFlow/Keras)
- Pre-trained on ImageNet

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- Node.js 16+ and npm
- Git
- 8GB+ RAM recommended (for model loading)
- CUDA-compatible GPU (optional, for faster inference)

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ChiliFusionNet.git
cd ChiliFusionNet
```

2. **Navigate to backend directory**
```bash
cd back-end
```

3. **Create and activate virtual environment**
```bash
# Create virtual environment
python -m venv chilifusionnet

# Activate virtual environment
# Windows:
chilifusionnet\Scripts\activate
# macOS/Linux:
source chilifusionnet/bin/activate
```

4. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

5. **Verify models directory**
Ensure the following files exist in `back-end/models/`:
- `chili_fusionnet.joblib`
- `class_map.json`
- `inception_resnet_v2_feature_extractor.keras`
- `efficientnet_b3_feature_extractor.keras`
- `xception_feature_extractor.keras`

6. **Start FastAPI server**
```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd "ChiliFusionNet front-end"
```

2. **Install Node.js dependencies**
```bash
npm install
```

3. **Configure environment variables**

Create a `.env` file in the `ChiliFusionNet front-end` directory:
```env
VITE_API_URL=http://localhost:8000
```

4. **Start React development server**
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

5. **Build for production**
```bash
npm run build
```

The production build will be created in the `dist/` directory.

### 🔧 Environment Configuration

**Backend `.env` (optional):**
```env
# API Configuration
HOST=0.0.0.0
PORT=8000

# CORS Origins
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Model Paths
MODEL_DIR=./models/
UPLOAD_DIR=./uploads/
```

**Frontend `.env`:**
```env
VITE_API_URL=http://localhost:8000
```

## 📖 Usage

### Web Interface

1. **Start both servers**
   - Backend: `http://localhost:8000` (FastAPI)
   - Frontend: `http://localhost:5173` (Vite dev server)

2. **Navigate to the Demo page**
   - Click "Try Our Model" from the home page
   - Or directly visit the Demo section

3. **Upload an image for disease detection**
   - Click "Upload Image" or drag-and-drop
   - Supported formats: JPG, JPEG, PNG
   - Maximum file size: 10MB

4. **Use example images**
   - Browse the example gallery (8 sample images)
   - Click any example to load it for prediction

5. **View prediction results**
   - Disease classification label
   - Confidence score (percentage)
   - Probability distribution across all 6 disease categories
   - Color-coded confidence indicator

### API Usage

**Health Check:**
```bash
curl http://localhost:8000/
```

**Single Image Prediction (File Upload):**
```python
import requests

# Upload image file
with open('chili_leaf.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/predict', files=files)

result = response.json()
print(f"Predicted Disease: {result['predicted_label']}")
print(f"Confidence: {result['confidence']:.2f}%")
print(f"Probabilities: {result['probabilities']}")
```

**Prediction by File Path (Backend-side images):**
```python
import requests

data = {
    "image_path": "images/test/Bacterial Spot/image_001.jpg"
}

response = requests.post('http://localhost:8000/predict-path', json=data)
result = response.json()
print(f"Disease: {result['predicted_label']}")
```

**Get Example Images List:**
```python
import requests

response = requests.get('http://localhost:8000/example-images')
examples = response.json()

for category, images in examples['examples'].items():
    print(f"{category}: {len(images)} images")
```

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check and API info |
| POST | `/predict` | Upload image for disease prediction |
| POST | `/predict-path` | Predict from backend file path |
| GET | `/example-images` | List available example images |
| GET | `/docs` | Interactive Swagger API documentation |
| GET | `/redoc` | ReDoc API documentation |

### Request Schema

**`POST /predict` (Multipart Form Data):**
```
file: <image file> (JPEG, PNG)
```

**`POST /predict-path` (JSON):**
```json
{
  "image_path": "string (relative path from backend root)"
}
```

### Response Schema

**Success Response:**
```json
{
  "predicted_label": "Bacterial Spot",
  "confidence": 95.73,
  "probabilities": {
    "Bacterial Spot": 95.73,
    "Cercospora Leaf Spot": 2.14,
    "Curl Virus": 0.89,
    "Healthy Leaf": 0.56,
    "Nutrition Deficiency": 0.45,
    "White spot": 0.23
  }
}
```

**Error Response:**
```json
{
  "detail": "Error message description"
}
```

### CORS Configuration

The API allows cross-origin requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Alternative React dev port)

Modify `app/main.py` to add additional origins.

## 🧪 Model Development

### Development Workflow

1. **Data Collection and Preparation**
   - Chili leaf image acquisition
   - Disease category labeling
   - Dataset organization

2. **Feature Extractor Training**
   - Fine-tuning InceptionResNetV2 on chili leaf dataset
   - Fine-tuning EfficientNetB3 on chili leaf dataset
   - Fine-tuning Xception on chili leaf dataset
   - Extraction of feature vectors from pre-pooling layers

3. **Feature Fusion**
   - Concatenation of feature vectors from all three models
   - Dimensionality analysis
   - Feature space optimization

4. **Ensemble Classifier Training**
   - Training machine learning classifier on fused features
   - Hyperparameter optimization
   - Cross-validation evaluation

5. **Model Serialization**
   - Saving feature extractors (.keras format)
   - Saving ensemble classifier (.joblib format)
   - Class mapping (class_map.json)

6. **Web Deployment**
   - FastAPI integration
   - Image preprocessing pipeline
   - Real-time inference optimization

### Best Practices Implemented

- **Transfer Learning**: Leveraging ImageNet pre-trained weights
- **Model-Specific Preprocessing**: Each CNN architecture uses its appropriate preprocessing
- **Defensive Model Loading**: Error handling for corrupted model files
- **Input Validation**: Pydantic schemas for API request validation
- **CORS Security**: Configured cross-origin policies
- **Static File Serving**: Efficient serving of test images and uploads
- **Virtual Environment**: Isolated Python environment for dependency management
- **Git Ignore Configuration**: Comprehensive exclusion of models, uploads, and build artifacts

## 🤝 Contributing

We welcome contributions from researchers, developers, and agricultural professionals!

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Add tests** (if applicable)
5. **Commit your changes**
   ```bash
   git commit -m "Add your descriptive commit message"
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

### Areas for Contribution

- 🔬 **Research**: New architectures, improved ensemble techniques
- 💻 **Development**: UI/UX improvements, performance optimization
- 📊 **Data**: Additional disease categories, expanded datasets
- 📖 **Documentation**: Tutorials, deployment guides, translations
- 🧪 **Testing**: Unit tests, integration tests, field validation
- 🌾 **Agricultural**: Domain expertise, field testing feedback

## 👥 Authors

| Name | Designation | Institution | Email |
|------|-------------|-------------|-------|
| **Izaz Ahmmed Tuhin** | Lecturer | Dept. of Software Engineering<br>Daffodil International University | izaz35-634@diu.edu.bd |
| **A K M Fazlul Kobir Siam** | Student | Dept. of Computer Science and Engineering<br>Daffodil International University | fazlul15-3432@diu.edu.bd |
| **Md Mahfuzur Rahman Shanto** | Student | Dept. of Software Engineering<br>Daffodil International University | shanto35-917@diu.edu.bd |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Daffodil International University for research support
- Agricultural experts who provided domain insights
- TensorFlow and Keras teams for deep learning frameworks
- FastAPI and React communities for excellent tools
- Open-source contributors whose libraries made this work possible

## 📞 Support

For questions, suggestions, or collaboration opportunities:

- 📧 **Primary Contact**: izaz35-634@diu.edu.bd
- 🐛 **Issues**: GitHub Issues (link to be added)
- 💬 **Discussions**: GitHub Discussions (link to be added)

---

<div align="center">

**🌶️ Protecting Chili Crops with AI 🤖**

*Advancing agricultural technology through deep learning research*

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/ChiliFusionNet?style=social)](https://github.com/yourusername/ChiliFusionNet)

**Made with ❤️ by the ChiliFusionNet Team**

</div>
