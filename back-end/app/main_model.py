# backend/model_loader.py
import os
import json
import joblib
import logging

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Base directory for all artifacts (joblib, json, and SavedModel folders)
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')

def _join(*parts: str) -> str:
    return os.path.normpath(os.path.join(MODEL_DIR, *parts))

# --- Helpers in the same style as your pattern ---

def load_joblib(filename: str):
    """Safely load a .joblib file from MODEL_DIR."""
    path = _join(filename)
    try:
        obj = joblib.load(path)
        logger.info(f"Loaded: {filename}")
        print("Fusion Net Done")
        return obj
    except FileNotFoundError:
        logger.error(f"{filename} not found in {MODEL_DIR}")
    except Exception as e:
        logger.error(f"Error loading {filename}: {e}")
    return None

def load_json(filename: str):
    """Safely load a JSON file from MODEL_DIR."""
    path = _join(filename)
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        logger.info(f"Loaded: {filename}")
        return data
    except FileNotFoundError:
        logger.error(f"{filename} not found in {MODEL_DIR}")
    except Exception as e:
        logger.error(f"Error loading {filename}: {e}")
    return None



