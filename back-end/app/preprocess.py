import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from .load_model_utils import load_keras_model


feature_model1 = load_keras_model("inception_resnet_v2_feature_extractor.keras", compile=False)
feature_model2 = load_keras_model("efficientnet_b3_feature_extractor.keras", compile=False)
feature_model3 = load_keras_model("xception_feature_extractor.keras", compile=False)

models = [feature_model1, feature_model2, feature_model3]

# --- 2) Build test generator (NO augmentation, NO shuffle) ---
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
data_path = "images"

test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
    os.path.join(data_path, "test"),
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="sparse",
    shuffle=False     # <- IMPORTANT: keep order stable
)

def extract_and_concatenate_features(generator, models, num_samples):
    generator.reset()  # <- start from the first batch each time
    features_list = [[] for _ in models]
    labels = []

    for images, lbls in generator:
        # Extract features for each model
        for i, model in enumerate(models):
            batch_features = model.predict(images, verbose=0)
            features_list[i].extend(batch_features)

        labels.extend(lbls)
        if len(labels) >= num_samples:
            break

    # Stack features and labels
    features = [np.array(feats[:num_samples]) for feats in features_list]
    concatenated = np.concatenate(features, axis=1)  # concat along feature dimension
    return concatenated, np.array(labels[:num_samples], dtype=int) 

# ✨ Helper: get fused features + labels + filenames
def get_test_features():
    X, y = extract_and_concatenate_features(test_generator, models, test_generator.samples)
    filenames = test_generator.filenames  # relative paths under test/
    return X, y, filenames, test_generator.class_indices