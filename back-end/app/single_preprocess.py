import numpy as np
from tensorflow.keras.preprocessing import image
from .load_model_utils import load_keras_model


feature_model1 = load_keras_model("inception_resnet_v2_feature_extractor.keras", compile=False)
feature_model2 = load_keras_model("efficientnet_b3_feature_extractor.keras", compile=False)
feature_model3 = load_keras_model("xception_feature_extractor.keras", compile=False)

models = [feature_model1, feature_model2, feature_model3]

# --- Define a helper function ---
def extract_and_concatenate_features_single(img_path, models, img_size=(224, 224)):
    # 1️⃣ Load and resize
    img = image.load_img(img_path, target_size=img_size)

    # 2️⃣ Convert to array
    img_array = image.img_to_array(img)

    # 3️⃣ Rescale (since you used rescale=1./255 during training)
    img_array = img_array / 255.0

    # 4️⃣ Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)  # (1, 224, 224, 3)

    # 5️⃣ Extract features from each model
    features = []
    for model in models:
        feat = model.predict(img_array, verbose=0)  # shape: (1, feature_dim)
        features.append(feat)

    # 6️⃣ Concatenate along the feature dimension
    concatenated = np.concatenate(features, axis=1)  # shape: (1, total_feature_dim)
    return concatenated


def get_single_test_feature(img_path):
    features = extract_and_concatenate_features_single(img_path, models)
    return features