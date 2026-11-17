from pathlib import Path
import gc

import numpy as np
import pandas as pd
import tensorflow as tf

from tensorflow.keras.applications import (
    InceptionResNetV2,
    EfficientNetB3,
    Xception
)

from preprocessing import (
    IMG_SIZE,
    load_image,
    preprocess_for_backbone
)

DATA_DIR = Path("artifacts/data")
FEATURE_DIR = Path("artifacts/features")
FEATURE_DIR.mkdir(parents=True, exist_ok=True)

BATCH_SIZE = 1
INPUT_SHAPE = (IMG_SIZE[1], IMG_SIZE[0], 3)

BACKBONES = {
    "InceptionResNetV2": (InceptionResNetV2, 1536),
    "EfficientNetB3": (EfficientNetB3, 1536),
    "Xception": (Xception, 2048)
}

def extract_features(model, dataframe, backbone_name, expected_dim):
    features = []

    for start in range(0, len(dataframe), BATCH_SIZE):
        paths = dataframe["filepath"].iloc[start:start + BATCH_SIZE]

        images = np.stack([load_image(p) for p in paths]).astype(np.float32)
        images = preprocess_for_backbone(images, backbone_name)

        batch = model.predict(images, batch_size=BATCH_SIZE, verbose=0)

        if batch.shape != (len(paths), expected_dim):
            raise RuntimeError(f"{backbone_name}: unexpected shape {batch.shape}")

        features.append(batch.astype(np.float32))

    return np.concatenate(features, axis=0)

dev_df = pd.read_csv(DATA_DIR / "development_manifest.csv")
holdout_df = pd.read_csv(DATA_DIR / "holdout_manifest.csv")

dev_parts, holdout_parts = [], []

for name, (builder, dim) in BACKBONES.items():
    tf.keras.backend.clear_session()
    gc.collect()

    model = builder(
        weights="imagenet",
        include_top=False,
        pooling="avg",
        input_shape=INPUT_SHAPE
    )
    model.trainable = False

    print("Extracting:", name)

    dev_parts.append(extract_features(model, dev_df, name, dim))
    holdout_parts.append(extract_features(model, holdout_df, name, dim))

    del model

X_development = np.concatenate(dev_parts, axis=1)
X_holdout = np.concatenate(holdout_parts, axis=1)

y_development = dev_df["label"].to_numpy(dtype=np.int32)
y_holdout = holdout_df["label"].to_numpy(dtype=np.int32)

np.save(FEATURE_DIR / "X_development_fused.npy", X_development)
np.save(FEATURE_DIR / "X_holdout_fused.npy", X_holdout)
np.save(FEATURE_DIR / "y_development.npy", y_development)
np.save(FEATURE_DIR / "y_holdout.npy", y_holdout)

print("Development features:", X_development.shape)
print("Holdout features:", X_holdout.shape)