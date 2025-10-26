import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array
from .load_model_utils import load_keras_model

# 1) Load your saved feature-extractor models
feature_model1 = load_keras_model("inception_resnet_v2_feature_extractor.keras", compile=False)
feature_model2 = load_keras_model("efficientnet_b3_feature_extractor.keras", compile=False)
feature_model3 = load_keras_model("xception_feature_extractor.keras", compile=False)
models = [feature_model1, feature_model2, feature_model3]

# 2) Utilities
def _infer_target_size(model):
    """Infer (H,W) from model.input_shape; default to (224,224)."""
    s = model.input_shape
    if isinstance(s, list): s = s[0]
    try:
        h, w = s[1], s[2]
        if h and w: return (int(h), int(w))
    except Exception:
        pass
    return (224, 224)

def _get_preprocess(size_hw):
    """
    Choose preprocessing by expected input size.
    - (299,299): Inception/Xception style ([-1,1])
    - (300,300): EfficientNet-B3 style
    - fallback: /255
    """
    try:
        if size_hw == (299, 299):
            from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input
            return preprocess_input
        if size_hw == (300, 300):
            from tensorflow.keras.applications.efficientnet import preprocess_input
            return preprocess_input
    except Exception:
        pass
    def _fallback(x): return x / 255.0
    return _fallback

def _load_and_prep(img_path, size_hw, preprocess_fn):
    img = Image.open(img_path).convert("RGB").resize(size_hw)
    x = img_to_array(img)
    x = np.expand_dims(x, 0)  # (1,H,W,3)
    x = preprocess_fn(x)
    return x

def _predict_vec(model, img_path):
    size_hw = _infer_target_size(model)
    preprocess_fn = _get_preprocess(size_hw)
    x = _load_and_prep(img_path, size_hw, preprocess_fn)
    feats = model.predict(x, verbose=0)
    return np.ravel(feats)  # 1-D

# 3) Public API —> returns one fused vector for the image
def extract_concat_feature_for_image(img_path: str) -> np.ndarray:
    vecs = [ _predict_vec(m, img_path) for m in models ]
    return np.concatenate(vecs, axis=0)

# Example:
# fused = extract_concat_feature_for_image("images/test/cat/cat001.jpg")
# print(fused.shape)  # e.g., (1536 + 1536 + 2048,)
