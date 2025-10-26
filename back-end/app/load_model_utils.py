import os
import logging
from tensorflow.keras.models import load_model as keras_load_model

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

MODEL_DIR = "models"   # base directory where you saved your models

def load_keras_model(filename: str, compile: bool = False):
    """
    Load a Keras SavedModel safely from artifacts/.
    """
    path = os.path.join(MODEL_DIR, filename)
    try:
        model = keras_load_model(path, compile = compile)
        logger.info(f"✅ Loaded model: {filename}")
        return model
    except FileNotFoundError:
        logger.error(f"❌ {filename} not found in {MODEL_DIR}")
    except Exception as e:
        logger.error(f"❌ Error loading {filename}: {e}")
    return None
