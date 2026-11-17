# %%
from pathlib import Path
import gc
import json
import warnings

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle
from scipy.ndimage import label as connected_components

import shap
from lime.lime_tabular import LimeTabularExplainer
from lime import lime_image
from skimage.segmentation import mark_boundaries, slic

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

warnings.filterwarnings("ignore", category=FutureWarning)


# %%
SEED = 42

FEATURE_DIR = Path("artifacts/features")
MODEL_PATH = Path("artifacts/final_model/chilifusionnet_final.joblib")
RESULT_DIR = Path("artifacts/xai")

SHAP_DIR = RESULT_DIR / "shap"
LIME_DIR = RESULT_DIR / "lime"
VISUAL_LIME_DIR = RESULT_DIR / "visual_lime"
ELI5_DIR = RESULT_DIR / "eli5"

for directory in (SHAP_DIR, LIME_DIR, VISUAL_LIME_DIR, ELI5_DIR):
    directory.mkdir(parents=True, exist_ok=True)

SHAP_BACKGROUND_CLUSTERS = 10
SHAP_NSAMPLES = 500
SHAP_TOP_FEATURES = 5

LIME_NUM_SAMPLES = 5000
LIME_NUM_FEATURES = 10

VISUAL_LIME_NUM_SAMPLES = 1000
VISUAL_LIME_NUM_FEATURES = 8
SLIC_SEGMENTS = 50
SLIC_COMPACTNESS = 10
SLIC_SIGMA = 1

BACKBONES = {
    "InceptionResNetV2": (InceptionResNetV2, 1536),
    "EfficientNetB3": (EfficientNetB3, 1536),
    "Xception": (Xception, 2048)
}


# %%
final_model = joblib.load(MODEL_PATH)

X_dev = np.load(FEATURE_DIR / "X_development_fused.npy").astype(np.float32)
X_test = np.load(FEATURE_DIR / "X_holdout_fused.npy").astype(np.float32)
y_test = np.load(FEATURE_DIR / "y_holdout.npy").astype(np.int32)

development_index = pd.read_csv(FEATURE_DIR / "development_feature_index.csv")
holdout_index = pd.read_csv(FEATURE_DIR / "holdout_feature_index.csv")

FEATURE_DIM = X_test.shape[1]

if X_dev.shape[1] != FEATURE_DIM or final_model.n_features_in_ != FEATURE_DIM:
    raise ValueError("Feature dimensions of the model and the data differ.")

if len(X_dev) != len(development_index):
    raise ValueError("Development feature index mismatch.")

if len(X_test) != len(y_test) or len(X_test) != len(holdout_index):
    raise ValueError("Holdout feature, label and index lengths differ.")

if not np.array_equal(y_test, holdout_index["label"].to_numpy(dtype=np.int32)):
    raise ValueError("Holdout labels and index are misaligned.")

if not (np.isfinite(X_dev).all() and np.isfinite(X_test).all()):
    raise ValueError("Non-finite feature values detected.")

if list(final_model.named_estimators_.keys()) != ["xgb", "lgb", "rf", "et"]:
    raise ValueError("Unexpected base-estimator names or order.")

if final_model.passthrough is not True:
    raise ValueError("The stacking model must use passthrough=True.")

if type(final_model.final_estimator_).__name__ != "LogisticRegression":
    raise TypeError("The meta-learner must be a Logistic Regression.")

CLASS_IDS = np.asarray(final_model.classes_)
NUM_CLASSES = len(CLASS_IDS)

if not np.array_equal(CLASS_IDS, np.arange(NUM_CLASSES)):
    raise ValueError("Model classes must be encoded from 0 to K-1.")

ID_TO_CLASS = (
    development_index[["label", "class_name"]]
    .drop_duplicates()
    .set_index("label")["class_name"]
    .to_dict()
)

CLASS_NAMES = [ID_TO_CLASS[int(i)] for i in CLASS_IDS]
FEATURE_NAMES = [f"IEX_Feature_{i + 1}" for i in range(FEATURE_DIM)]

print("Development features:", X_dev.shape)
print("Holdout features:", X_test.shape)
print("Classes:", CLASS_NAMES)


# %%
y_pred = final_model.predict(X_test)
y_prob = final_model.predict_proba(X_test)

xai_predictions = holdout_index[
    ["image_id", "relative_path", "filepath", "class_name", "label"]
].copy()

xai_predictions["predicted_label"] = y_pred
xai_predictions["predicted_class"] = [ID_TO_CLASS[int(v)] for v in y_pred]
xai_predictions["confidence"] = np.max(y_prob, axis=1)
xai_predictions["correct"] = y_pred == y_test

xai_predictions.to_csv(RESULT_DIR / "xai_holdout_predictions.csv", index=False)


# %%
SELECTION_RANK = {"shap": 0, "lime": 1, "visual_lime": 2, "eli5": 0}


def select_instances(rank):
    chosen = []

    for class_id in CLASS_IDS:
        members = np.where(y_test == class_id)[0]

        if len(members) <= rank:
            raise RuntimeError(f"Class {class_id} has fewer than {rank + 1} holdout images.")

        chosen.append(int(members[rank]))

    return np.asarray(chosen, dtype=int)


selected = {method: select_instances(rank) for method, rank in SELECTION_RANK.items()}

selection_frames = []

for method, indices in selected.items():
    frame = xai_predictions.iloc[indices].copy()
    frame.insert(0, "method", method)
    selection_frames.append(frame)

selected_df = pd.concat(selection_frames, ignore_index=True)
selected_df.to_csv(RESULT_DIR / "xai_selected_instances.csv", index=False)

print(
    selected_df[
        ["method", "image_id", "class_name", "predicted_class", "confidence", "correct"]
    ].to_string(index=False)
)

# %%
background = shap.kmeans(X_dev, SHAP_BACKGROUND_CLUSTERS)

np.random.seed(SEED)

shap_explainer = shap.KernelExplainer(final_model.predict_proba, background)

X_shap = X_test[selected['shap']]

shap_values = shap_explainer.shap_values(X_shap, nsamples=SHAP_NSAMPLES)

if isinstance(shap_values, np.ndarray):
    if shap_values.ndim != 3:
        raise ValueError(f"Unexpected SHAP array shape: {shap_values.shape}")
    shap_by_class = [shap_values[:, :, c] for c in range(shap_values.shape[2])]
else:
    shap_by_class = [np.asarray(v) for v in shap_values]

if len(shap_by_class) != NUM_CLASSES:
    raise ValueError("SHAP output class count does not match model classes.")

shap_rows = []

for position, original_index in enumerate(selected['shap']):
    predicted_class = int(y_pred[original_index])
    values = shap_by_class[predicted_class][position].reshape(-1)
    top = np.argsort(np.abs(values))[::-1][:SHAP_TOP_FEATURES]

    for rank, feature_index in enumerate(top, start=1):
        shap_rows.append({
            "sample_index": int(original_index),
            "image_id": str(holdout_index.iloc[original_index]["image_id"]),
            "true_class": ID_TO_CLASS[int(y_test[original_index])],
            "predicted_class": ID_TO_CLASS[predicted_class],
            "confidence": float(y_prob[original_index, predicted_class]),
            "rank": rank,
            "feature_index": int(feature_index),
            "feature_name": FEATURE_NAMES[feature_index],
            "shap_value": float(values[feature_index])
        })

shap_df = pd.DataFrame(shap_rows)
shap_df.to_csv(SHAP_DIR / "full_model_local_shap_top5.csv", index=False)

for original_index in selected['shap']:
    rows = shap_df[shap_df["sample_index"] == int(original_index)].iloc[::-1]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(
        rows["feature_name"],
        rows["shap_value"],
        color=["tab:red" if v > 0 else "tab:blue" for v in rows["shap_value"]]
    )
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("SHAP value for predicted class")
    ax.set_title(
        f"Kernel SHAP - {ID_TO_CLASS[int(y_pred[original_index])]} "
        f"({y_prob[original_index].max() * 100:.2f}%)"
    )
    fig.tight_layout()
    fig.savefig(
        SHAP_DIR / f"shap_{original_index}_{ID_TO_CLASS[int(y_pred[original_index])]}.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)


# %%
lime_explainer = LimeTabularExplainer(
    training_data=X_dev,
    feature_names=FEATURE_NAMES,
    class_names=CLASS_NAMES,
    mode="classification",
    discretize_continuous=True,
    random_state=SEED
)

lime_rows = []

for original_index in selected['lime']:
    predicted_class = int(y_pred[original_index])

    explanation = lime_explainer.explain_instance(
        data_row=X_test[original_index],
        predict_fn=final_model.predict_proba,
        labels=[predicted_class],
        num_features=LIME_NUM_FEATURES,
        num_samples=LIME_NUM_SAMPLES
    )

    for rank, (rule, weight) in enumerate(
        explanation.as_list(label=predicted_class), start=1
    ):
        lime_rows.append({
            "sample_index": int(original_index),
            "image_id": str(holdout_index.iloc[original_index]["image_id"]),
            "true_class": ID_TO_CLASS[int(y_test[original_index])],
            "predicted_class": ID_TO_CLASS[predicted_class],
            "confidence": float(y_prob[original_index, predicted_class]),
            "rank": rank,
            "feature_rule": rule,
            "lime_weight": float(weight)
        })

    fig = explanation.as_pyplot_figure(label=predicted_class)
    fig.tight_layout()
    fig.savefig(
        LIME_DIR / f"lime_{original_index}_{ID_TO_CLASS[predicted_class]}.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)

pd.DataFrame(lime_rows).to_csv(LIME_DIR / "full_model_local_lime.csv", index=False)


# %%
for gpu in tf.config.list_physical_devices("GPU"):
    try:
        tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError:
        pass

INPUT_SHAPE = (IMG_SIZE[1], IMG_SIZE[0], 3)

backbone_models = {}

for name, (builder, dim) in BACKBONES.items():
    backbone = builder(
        weights="imagenet",
        include_top=False,
        pooling="avg",
        input_shape=INPUT_SHAPE
    )
    backbone.trainable = False
    backbone_models[name] = (backbone, dim)


def extract_fused_features(images):
    images = np.asarray(images, dtype=np.float32)
    parts = []

    for name, (backbone, dim) in backbone_models.items():
        batch = preprocess_for_backbone(images.copy(), name)
        features = backbone.predict(batch, verbose=0)

        if features.shape != (len(images), dim):
            raise RuntimeError(f"{name}: unexpected feature shape {features.shape}")

        parts.append(features)

    fused = np.concatenate(parts, axis=1).astype(np.float32)

    if fused.shape[1] != FEATURE_DIM:
        raise RuntimeError(f"Expected {FEATURE_DIM} fused features, got {fused.shape[1]}")

    return fused


def visual_lime_predict(batch):
    pixels = (np.asarray(batch) * 255.0).astype(np.float32)
    return final_model.predict_proba(extract_fused_features(pixels))


def segment(image):
    return slic(
        image,
        n_segments=SLIC_SEGMENTS,
        compactness=SLIC_COMPACTNESS,
        sigma=SLIC_SIGMA,
        start_label=0
    )


visual_explainer = lime_image.LimeImageExplainer(random_state=SEED)
visual_rows = []

for original_index in selected['visual_lime']:
    image_path = Path(holdout_index.iloc[original_index]["filepath"])

    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = load_image(image_path)
    predicted_class = int(y_pred[original_index])

    cached = X_test[original_index:original_index + 1]
    recomputed = extract_fused_features(image[np.newaxis])

    if not np.allclose(cached, recomputed, rtol=1e-3, atol=1e-3):
        raise RuntimeError(
            f"Recomputed features differ from cached features for {image_path.name}."
        )

    explanation = visual_explainer.explain_instance(
        image.astype(np.double) / 255.0,
        classifier_fn=visual_lime_predict,
        labels=(predicted_class,),
        hide_color=0,
        num_samples=VISUAL_LIME_NUM_SAMPLES,
        segmentation_fn=segment
    )

    temp, mask = explanation.get_image_and_mask(
        predicted_class,
        positive_only=True,
        num_features=VISUAL_LIME_NUM_FEATURES,
        hide_rest=False
    )

    display_image = np.clip(image, 0, 255).astype(np.uint8)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(display_image)
    axes[0].set_title("Enhanced Image")
    axes[0].axis("off")

    axes[1].imshow(mark_boundaries(temp, mask))
    axes[1].set_title("Visual LIME Superpixels")
    axes[1].axis("off")

    axes[2].imshow(display_image)
    axes[2].set_title("Important Regions")
    axes[2].axis("off")

    components, number_components = connected_components(mask > 0)

    for component_id in range(1, number_components + 1):
        ys, xs = np.where(components == component_id)

        axes[2].add_patch(
            Rectangle(
                (xs.min(), ys.min()),
                xs.max() - xs.min(),
                ys.max() - ys.min(),
                fill=False,
                edgecolor="red",
                linewidth=2
            )
        )

    fig.suptitle(
        f"Visual LIME - {ID_TO_CLASS[predicted_class]} "
        f"({y_prob[original_index, predicted_class] * 100:.2f}%)"
    )
    fig.tight_layout()
    fig.savefig(
        VISUAL_LIME_DIR / f"visual_lime_{original_index}_{ID_TO_CLASS[predicted_class]}.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)

    visual_rows.append({
        "sample_index": int(original_index),
        "image_id": str(holdout_index.iloc[original_index]["image_id"]),
        "true_class": ID_TO_CLASS[int(y_test[original_index])],
        "predicted_class": ID_TO_CLASS[predicted_class],
        "confidence": float(y_prob[original_index, predicted_class]),
        "positive_superpixels": int(len(np.unique(segment(image)[mask > 0])))
    })

pd.DataFrame(visual_rows).to_csv(
    VISUAL_LIME_DIR / "visual_lime_summary.csv", index=False
)

del backbone_models
tf.keras.backend.clear_session()
gc.collect()


# %%
meta_model = final_model.final_estimator_
X_meta_test = final_model.transform(X_test)

if not np.array_equal(meta_model.predict(X_meta_test), y_pred):
    raise RuntimeError("Meta-learner predictions differ from model predictions.")

probability_width = len(final_model.estimators_) * NUM_CLASSES

if X_meta_test.shape[1] != probability_width + FEATURE_DIM:
    raise ValueError(f"Unexpected meta-feature width {X_meta_test.shape[1]}.")

dims = [dim for _, dim in BACKBONES.values()]
offsets = np.concatenate([[0], np.cumsum(dims)]) + probability_width

component_groups = {
    "XGBoost": slice(0, NUM_CLASSES),
    "LightGBM": slice(NUM_CLASSES, 2 * NUM_CLASSES),
    "RandomForest": slice(2 * NUM_CLASSES, 3 * NUM_CLASSES),
    "ExtraTrees": slice(3 * NUM_CLASSES, 4 * NUM_CLASSES)
}

for k, name in enumerate(BACKBONES):
    component_groups[name] = slice(int(offsets[k]), int(offsets[k + 1]))

decision_scores = meta_model.decision_function(X_meta_test)

eli5_rows = []
check_rows = []

for original_index in selected['eli5']:
    predicted_class = int(y_pred[original_index])
    class_position = list(meta_model.classes_).index(predicted_class)

    contributions = X_meta_test[original_index] * meta_model.coef_[class_position]

    component_total = 0.0

    for component, feature_slice in component_groups.items():
        part = contributions[feature_slice]
        component_total += float(part.sum())

        eli5_rows.append({
            "sample_index": int(original_index),
            "image_id": str(holdout_index.iloc[original_index]["image_id"]),
            "true_class": ID_TO_CLASS[int(y_test[original_index])],
            "predicted_class": ID_TO_CLASS[predicted_class],
            "component": component,
            "signed_contribution": float(part.sum()),
            "absolute_contribution": float(np.abs(part).sum())
        })

    intercept = float(meta_model.intercept_[class_position])
    actual = float(decision_scores[original_index, class_position])

    if not np.isclose(component_total + intercept, actual, rtol=1e-6, atol=1e-6):
        raise RuntimeError(
            f"Component contributions do not reconstruct the decision score "
            f"for sample {original_index}."
        )

    check_rows.append({
        "sample_index": int(original_index),
        "image_id": str(holdout_index.iloc[original_index]["image_id"]),
        "predicted_class": ID_TO_CLASS[predicted_class],
        "sum_of_components": component_total,
        "intercept": intercept,
        "actual_decision_score": actual,
        "absolute_error": abs(component_total + intercept - actual)
    })

pd.DataFrame(check_rows).to_csv(
    ELI5_DIR / "meta_learner_decision_score_check.csv", index=False
)

eli5_df = pd.DataFrame(eli5_rows)
eli5_df.to_csv(ELI5_DIR / "meta_learner_component_contributions.csv", index=False)

for original_index in selected['eli5']:
    rows = eli5_df[eli5_df["sample_index"] == int(original_index)].sort_values(
        "signed_contribution"
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(rows["component"], rows["signed_contribution"])
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Signed contribution to predicted-class decision score")
    ax.set_title(
        f"Meta-Learner Component Contributions - "
        f"{ID_TO_CLASS[int(y_pred[original_index])]}"
    )
    fig.tight_layout()
    fig.savefig(ELI5_DIR / f"eli5_components_{original_index}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


# %%
metadata = {
    "classes": CLASS_NAMES,
    "feature_dimension": FEATURE_DIM,
    "random_seed": SEED,
    "explained_function": "final_model.predict_proba",
    "instance_selection": {method: f"holdout image number {rank + 1} of each true class" for method, rank in SELECTION_RANK.items()},
    "shap_background": f"k-means, {SHAP_BACKGROUND_CLUSTERS} clusters, development features",
    "shap_nsamples": SHAP_NSAMPLES,
    "shap_top_features": SHAP_TOP_FEATURES,
    "lime_num_samples": LIME_NUM_SAMPLES,
    "lime_num_features": LIME_NUM_FEATURES,
    "visual_lime_num_samples": VISUAL_LIME_NUM_SAMPLES,
    "visual_lime_num_features": VISUAL_LIME_NUM_FEATURES,
    "slic": {
        "n_segments": SLIC_SEGMENTS,
        "compactness": SLIC_COMPACTNESS,
        "sigma": SLIC_SIGMA
    },
    "selected_instances_correct": {method: bool(xai_predictions.iloc[indices]["correct"].all()) for method, indices in selected.items()}
}

with open(RESULT_DIR / "xai_metadata.json", "w", encoding="utf-8") as file:
    json.dump(metadata, file, indent=4)

print(json.dumps(metadata, indent=2))