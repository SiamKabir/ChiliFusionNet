from fastapi import FastAPI, HTTPException, Query
import pandas as pd
from typing import List

from fastapi.middleware.cors import CORSMiddleware
from .schemas import PredictionItem, SinglePredictionItem, ImagePathInput
from .predict import run_single_predict
from .extractor import build_and_save_models

import warnings
warnings.filterwarnings("ignore", message=".*does not have valid feature names.*")
# from .save_model import save_model
app = FastAPI(title="ChiliFusionNet")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ✅ React dev server origin
    allow_credentials=True,
    allow_methods=["*"],                      # or specify: ["POST", "GET"]
    allow_headers=["*"],
)


@app.get("/")
def heath():
    # save_model()
    return { "message": "Health is ok!"}

@app.get("/save")
def save():
    # save_model()
    build_and_save_models()
    return { "message": "Health is ok!"}

# @app.get("/predict", response_model=List[PredictionItem])
# def predict_endpoint():
#     """
#     Calls the batch predict() which runs over images/test.
#     """
#     try:
#         results = run_batch_predict()
#         if results is None:
#             raise HTTPException(status_code=500, detail="Prediction returned None")
#         return results
#     except Exception as e:
#         # Surface the error message for easier debugging
#         raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
    
@app.post("/predict", response_model=SinglePredictionItem)
def predict_endpoint(image: ImagePathInput):
    img_path = image.path
    try:
        results = run_single_predict(img_path)
        print(results)
        if results is None:
            raise HTTPException(status_code=500, detail="Prediction returned None")
        return results
    except Exception as e:
        # Surface the error message for easier debugging
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")