# %%
from pathlib import Path
import json
import warnings

import numpy as np
import pandas as pd
import lightgbm as lgb
import joblib

from xgboost import XGBClassifier

from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE

from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    StackingClassifier
)

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold

warnings.filterwarnings("ignore", category=FutureWarning)


# %%
SEED = 42
STACKING_FOLDS = 5

FEATURE_DIR = Path("artifacts/features")
OUTPUT_DIR = Path("artifacts/final_model")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CONFIGURATION = "No Augmentation + SMOTE"


# %%
X_dev = np.load(FEATURE_DIR / "X_development_fused.npy").astype(np.float32)
y_dev = np.load(FEATURE_DIR / "y_development.npy").astype(np.int32)
index_df = pd.read_csv(FEATURE_DIR / "development_feature_index.csv")

if X_dev.ndim != 2:
    raise ValueError(f"Expected a 2-D feature matrix, found {X_dev.shape}")

if len(X_dev) != len(y_dev) or len(X_dev) != len(index_df):
    raise ValueError("Feature, label and index lengths differ.")

if not np.isfinite(X_dev).all():
    raise ValueError("Feature matrix contains NaN or infinity.")

if not np.array_equal(y_dev, index_df["label"].to_numpy(dtype=np.int32)):
    raise ValueError("Feature and label alignment error.")

if index_df["image_id"].duplicated().any():
    raise ValueError("Duplicate image IDs found.")

CLASS_IDS = np.unique(y_dev)
NUM_CLASSES = len(CLASS_IDS)

if not np.array_equal(CLASS_IDS, np.arange(NUM_CLASSES)):
    raise ValueError("Class labels must be encoded as 0..K-1.")

ID_TO_CLASS = (
    index_df[["label", "class_name"]]
    .drop_duplicates()
    .set_index("label")["class_name"]
    .to_dict()
)

print("Development features:", X_dev.shape)
print("Development labels:", y_dev.shape)
print("Number of classes:", NUM_CLASSES)

print("\nClass distribution:")
print(index_df["class_name"].value_counts().sort_index())


# %%
def build_final_chilifusionnet(random_state=42):

    xgb_model = XGBClassifier(
        objective="multi:softprob",
        num_class=NUM_CLASSES,
        eval_metric="mlogloss",
        n_estimators=150,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=random_state,
        n_jobs=-1
    )

    lgb_model = lgb.LGBMClassifier(
        objective="multiclass",
        num_class=NUM_CLASSES,
        n_estimators=150,
        learning_rate=0.05,
        max_depth=7,
        num_leaves=31,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=random_state,
        verbosity=-1
    )

    rf_model = RandomForestClassifier(
        n_estimators=150,
        max_depth=25,
        min_samples_split=4,
        min_samples_leaf=2,
        max_features="sqrt",
        random_state=random_state,
        n_jobs=-1
    )

    et_model = ExtraTreesClassifier(
        n_estimators=150,
        max_depth=25,
        min_samples_split=4,
        min_samples_leaf=2,
        max_features="sqrt",
        random_state=random_state,
        n_jobs=-1
    )

    def make_pipeline(classifier):
        return ImbPipeline([
            ("smote", SMOTE(random_state=random_state, k_neighbors=5)),
            ("classifier", classifier)
        ])

    stacking_cv = StratifiedKFold(
        n_splits=STACKING_FOLDS,
        shuffle=True,
        random_state=random_state
    )

    meta_learner = LogisticRegression(
        solver="lbfgs",
        C=0.5,
        max_iter=1000,
        random_state=random_state
    )

    return StackingClassifier(
        estimators=[
            ("xgb", make_pipeline(xgb_model)),
            ("lgb", make_pipeline(lgb_model)),
            ("rf", make_pipeline(rf_model)),
            ("et", make_pipeline(et_model))
        ],
        final_estimator=meta_learner,
        stack_method="predict_proba",
        passthrough=True,
        cv=stacking_cv,
        n_jobs=-1
    )


# %%
model = build_final_chilifusionnet(random_state=SEED)

print("Configuration:", CONFIGURATION)
print("Training samples:", len(X_dev))
print("Feature dimension:", X_dev.shape[1])
print("Stacking folds:", STACKING_FOLDS)

model.fit(X_dev, y_dev)

print("\nFinal model training completed.")


# %%
if not hasattr(model, "estimators_"):
    raise RuntimeError("Base estimators were not fitted successfully.")

if not hasattr(model, "final_estimator_"):
    raise RuntimeError("Meta-learner was not fitted successfully.")

print("Base estimators:", len(model.estimators_))
print("Meta-learner:", type(model.final_estimator_).__name__)
print("Model classes:", model.classes_)


# %%
MODEL_PATH = OUTPUT_DIR / "chilifusionnet_final.joblib"

joblib.dump(model, MODEL_PATH, compress=3)

class_mapping = {
    str(label): str(ID_TO_CLASS[label])
    for label in sorted(ID_TO_CLASS)
}

with open(OUTPUT_DIR / "class_mapping.json", "w", encoding="utf-8") as file:
    json.dump(class_mapping, file, indent=4)

print("Final model saved to:", MODEL_PATH)