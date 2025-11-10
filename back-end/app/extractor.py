from tensorflow.keras.applications import InceptionResNetV2, EfficientNetB3, Xception
from tensorflow.keras.models import Model
import numpy as np

import os

# Define the model folder
model_dir = "models"
os.makedirs(model_dir, exist_ok=True)

def build_and_save_models(model_dir="models"):
    """Create and save pretrained feature extractors if they don't already exist."""
    
    os.makedirs(model_dir, exist_ok=True)

    # Define model file paths
    model_files = {
        "inception": os.path.join(model_dir, "inception_resnet_v2_feature_extractor.keras"),
        "efficient": os.path.join(model_dir, "efficientnet_b3_feature_extractor.keras"),
        "xception": os.path.join(model_dir, "xception_feature_extractor.keras"),
    }

    # Check if all model files already exist
    all_exist = all(os.path.exists(path) for path in model_files.values())

    if all_exist:
        print("✅ All pretrained models already exist. Skipping creation.")
        return
    else:
        print("⚙️ Some models are missing — building and saving now...")
        input_shape = (224, 224, 3)

        # Initialize three pretrained base models
        model1 = InceptionResNetV2(weights='imagenet', include_top=False, pooling='avg', input_shape=input_shape)
        model2 = EfficientNetB3(weights='imagenet', include_top=False, pooling='avg', input_shape=input_shape)
        model3 = Xception(weights='imagenet', include_top=False, pooling='avg', input_shape=input_shape)

        # Create feature extractors
        feature_model1 = Model(inputs=model1.input, outputs=model1.output)
        feature_model2 = Model(inputs=model2.input, outputs=model2.output)
        feature_model3 = Model(inputs=model3.input, outputs=model3.output)


        # Save models as .keras files in "model" folder
        feature_model1.save(os.path.join(model_dir, "inception_resnet_v2_feature_extractor.keras"))
        feature_model2.save(os.path.join(model_dir, "efficientnet_b3_feature_extractor.keras"))
        feature_model3.save(os.path.join(model_dir, "xception_feature_extractor.keras"))

        print("✅ Models saved successfully in 'model/' folder!")