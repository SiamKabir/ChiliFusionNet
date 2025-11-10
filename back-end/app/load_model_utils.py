import logging
import os
from pathlib import Path
from tensorflow.keras.models import load_model as keras_load_model


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"


def load_keras_model(filename: str, compile: bool = False):
    """Safely load a SavedModel from the models directory."""
    path = MODEL_DIR / filename
    try:
        model = keras_load_model(path, compile=compile)
        logger.info("✅ Loaded model: %s", filename)
        return model
    except FileNotFoundError:
        logger.warning("⚠️  %s not found in %s. Skipping.", filename, MODEL_DIR)
    except Exception as exc:
        logger.error("❌ Error loading %s: %s", filename, exc)
    return None
