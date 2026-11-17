# %%
from pathlib import Path

import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve,
    auc
)
from sklearn.preprocessing import label_binarize


# %%
FEATURE_DIR = Path("artifacts/features")
MODEL_PATH = Path("artifacts/final_model/chilifusionnet_final.joblib")
RESULT_DIR = Path("artifacts/holdout_results")
RESULT_DIR.mkdir(parents=True, exist_ok=True)


# %%
model = joblib.load(MODEL_PATH)

X_holdout = np.load(FEATURE_DIR / "X_holdout_fused.npy").astype(np.float32)
y_holdout = np.load(FEATURE_DIR / "y_holdout.npy").astype(np.int32)

holdout_index = pd.read_csv(FEATURE_DIR / "holdout_feature_index.csv")
development_index = pd.read_csv(FEATURE_DIR / "development_feature_index.csv")

ID_TO_CLASS = (
    development_index[["label", "class_name"]]
    .drop_duplicates()
    .set_index("label")["class_name"]
    .to_dict()
)

NUM_CLASSES = len(ID_TO_CLASS)
CLASS_LABELS = np.arange(NUM_CLASSES)
CLASS_NAMES = [ID_TO_CLASS[i] for i in CLASS_LABELS]

if X_holdout.shape[1] != model.n_features_in_:
    raise ValueError(
        f"Holdout has {X_holdout.shape[1]} features; "
        f"the model expects {model.n_features_in_}."
    )

if len(X_holdout) != len(y_holdout) or len(X_holdout) != len(holdout_index):
    raise ValueError("Holdout features, labels and index lengths differ.")

if not np.array_equal(
    y_holdout,
    holdout_index["label"].to_numpy(dtype=np.int32)
):
    raise ValueError("Holdout index and labels are misaligned.")

if not np.array_equal(model.classes_, CLASS_LABELS):
    raise ValueError("Model classes do not match the class mapping.")

print("Holdout features:", X_holdout.shape)


# %%
y_pred = model.predict(X_holdout)
y_prob = model.predict_proba(X_holdout)

accuracy = accuracy_score(y_holdout, y_pred)

precision = precision_score(
    y_holdout, y_pred, average="macro", zero_division=0
)

recall = recall_score(
    y_holdout, y_pred, average="macro", zero_division=0
)

macro_f1 = f1_score(
    y_holdout, y_pred, average="macro", zero_division=0
)

number_correct = int(np.sum(y_holdout == y_pred))
number_incorrect = int(len(y_holdout) - number_correct)

print("Holdout samples :", len(y_holdout))
print("Correct         :", number_correct)
print("Incorrect       :", number_incorrect)
print(f"Accuracy        : {accuracy * 100:.2f}%")
print(f"Macro Precision : {precision * 100:.2f}%")
print(f"Macro Recall    : {recall * 100:.2f}%")
print(f"Macro F1        : {macro_f1 * 100:.2f}%")


# %%
cm = confusion_matrix(y_holdout, y_pred, labels=CLASS_LABELS)

cm_df = pd.DataFrame(
    cm,
    index=[f"True_{name}" for name in CLASS_NAMES],
    columns=[f"Pred_{name}" for name in CLASS_NAMES]
)

report_df = pd.DataFrame(
    classification_report(
        y_holdout,
        y_pred,
        labels=CLASS_LABELS,
        target_names=CLASS_NAMES,
        output_dict=True,
        zero_division=0
    )
).transpose()

print("\nConfusion matrix:")
print(cm_df.to_string())

print("\nClassification report:")
print(report_df.round(4).to_string())


# %%
y_bin = label_binarize(y_holdout, classes=CLASS_LABELS)

class_auc = {
    CLASS_NAMES[i]: roc_auc_score(y_bin[:, i], y_prob[:, i])
    for i in range(NUM_CLASSES)
}

macro_auc = roc_auc_score(
    y_bin,
    y_prob,
    average="macro",
    multi_class="ovr"
)

print("Class-wise ROC-AUC:")
for name, value in class_auc.items():
    print(f"  {name}: {value:.4f}")

print(f"Macro ROC-AUC: {macro_auc:.4f}")


# %%
predictions = holdout_index[["image_id", "relative_path", "class_name", "label", "sha256"]].copy()

predictions["predicted_label"] = y_pred.astype(np.int32)
predictions["predicted_class"] = [ID_TO_CLASS[int(v)] for v in y_pred]
predictions["correct"] = (
    predictions["label"].to_numpy() == predictions["predicted_label"].to_numpy()
)

print("\nMisclassified holdout images:")
print(predictions[~predictions["correct"]].to_string(index=False))


# %%
for i in range(NUM_CLASSES):
    predictions[f"prob_{CLASS_NAMES[i]}"] = y_prob[:, i]

summary = pd.DataFrame([{
    "holdout_n": len(y_holdout),
    "correct": number_correct,
    "incorrect": number_incorrect,
    "accuracy": accuracy,
    "macro_precision": precision,
    "macro_recall": recall,
    "macro_f1": macro_f1,
    "macro_roc_auc": macro_auc
}])

summary.to_csv(RESULT_DIR / "holdout_summary.csv", index=False)
cm_df.to_csv(RESULT_DIR / "holdout_confusion_matrix.csv")
report_df.to_csv(RESULT_DIR / "holdout_classification_report.csv")
pd.DataFrame({
    "class_name": list(class_auc.keys()),
    "roc_auc": list(class_auc.values())
}).to_csv(RESULT_DIR / "holdout_roc_auc.csv", index=False)
predictions.to_csv(RESULT_DIR / "holdout_predictions.csv", index=False)


# %%
fig, ax = plt.subplots(figsize=(9, 7))
image = ax.imshow(cm, cmap="Oranges")
fig.colorbar(image, ax=ax)
ax.set_xticks(CLASS_LABELS)
ax.set_yticks(CLASS_LABELS)
ax.set_xticklabels(CLASS_NAMES, rotation=90)
ax.set_yticklabels(CLASS_NAMES)
ax.set_xlabel("Predicted Class")
ax.set_ylabel("Actual Class")
ax.set_title("ChiliFusionNet Confusion Matrix - Holdout")

for r in range(NUM_CLASSES):
    for c in range(NUM_CLASSES):
        ax.text(
            c, r, str(cm[r, c]),
            ha="center", va="center",
            color="white" if cm[r, c] > cm.max() / 2.0 else "black"
        )

fig.tight_layout()
fig.savefig(RESULT_DIR / "holdout_confusion_matrix.png", dpi=300, bbox_inches="tight")
plt.show()


# %%
fig, ax = plt.subplots(figsize=(8, 7))

for i in CLASS_LABELS:
    fpr, tpr, _ = roc_curve(y_bin[:, i], y_prob[:, i])
    ax.plot(fpr, tpr, lw=2, label=f"{CLASS_NAMES[i]} (AUC = {auc(fpr, tpr):.3f})")

ax.plot([0, 1], [0, 1], "k--", lw=1)
ax.set_xlim(0.0, 1.0)
ax.set_ylim(0.0, 1.05)
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.set_title("ChiliFusionNet One-vs-Rest ROC Curves - Holdout")
ax.legend(loc="lower right")

fig.tight_layout()
fig.savefig(RESULT_DIR / "holdout_roc_curve.png", dpi=300, bbox_inches="tight")
plt.show()