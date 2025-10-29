from fastapi import FastAPI, HTTPException, UploadFile, File
import shutil
from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .schemas import SinglePredictionItem, ImagePathInput
from .predict import run_single_predict
from .extractor import build_and_save_models

import warnings
warnings.filterwarnings("ignore", message=".*does not have valid feature names.*")
# from .save_model import save_model
app = FastAPI(title="ChiliFusionNet")

# ✅ CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Added Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve important directories relative to backend root
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
IMAGES_DIR = BASE_DIR / "images"

UPLOAD_DIR.mkdir(exist_ok=True)

if IMAGES_DIR.exists():
    app.mount("/static", StaticFiles(directory=IMAGES_DIR), name="static")


@app.get("/")
def health():
    return {"message": "ChiliFusionNet API is running!", "status": "healthy"}

@app.get("/save")
def save():
    build_and_save_models()
    return {"message": "Models saved successfully!"}

@app.post("/predict", response_model=SinglePredictionItem)
async def predict_endpoint(file: UploadFile = File(...)):
    """
    Upload an image file and get chili disease prediction
    """
    try:
        # Save uploaded file temporarily
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Run prediction
        results = run_single_predict(str(file_path))
        
        # Optional: Clean up uploaded file after prediction
        # file_path.unlink()
        
        if results is None:
            raise HTTPException(status_code=500, detail="Prediction returned None")
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict-path", response_model=SinglePredictionItem)
def predict_by_path(image: ImagePathInput):
    """
    Predict using local image path (for testing with example images)
    """
    candidate = Path(image.path)
    images_root = IMAGES_DIR.resolve() if IMAGES_DIR.exists() else None

    if not candidate.is_absolute():
        if images_root is None:
            raise HTTPException(status_code=404, detail="Images directory not available")
        candidate = (images_root / candidate).resolve()

    if not candidate.exists():
        raise HTTPException(status_code=404, detail="Image not found")

    # Prevent escaping the images directory
    if images_root and images_root not in candidate.parents and candidate != images_root:
        raise HTTPException(status_code=400, detail="Image path must be within images directory")

    try:
        results = run_single_predict(str(candidate))
        if results is None:
            raise HTTPException(status_code=500, detail="Prediction returned None")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/example-images")
def get_example_images():
    """
    Get list of example images from the test directory
    """
    test_dir = IMAGES_DIR / "test"
    if not test_dir.exists():
        return {"images": []}
    
    images = []
    for class_dir in test_dir.iterdir():
        if class_dir.is_dir():
            for img_file in class_dir.glob("*.*"):
                if img_file.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                    continue

                rel_path = img_file.relative_to(IMAGES_DIR)
                rel_posix = rel_path.as_posix()
                images.append({
                    "filename": img_file.name,
                    "relative_path": rel_posix,
                    "url": f"/static/{rel_posix}",
                    "class": class_dir.name
                })
    
    return {"images": images}