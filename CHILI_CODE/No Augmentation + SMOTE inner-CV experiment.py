from pathlib import Path
import gc
import warnings

import numpy as np
import pandas as pd
import lightgbm as lgb

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
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

warnings.filterwarnings("ignore", category=FutureWarning)

SEED = 42
OUTER_FOLDS = 5
INNER_FOLDS = 5
STACKING_FOLDS = 5
INNER_SEEDS = [1001, 1002, 1003, 1004, 1005]

FEATURE_DIR = Path("artifacts/features")

CONFIGURATION = "No Augmentation + SMOTE"


# %%
X = np.load(FEATURE_DIR / "X_development_fused.npy")
y = np.load(FEATURE_DIR / "y_development.npy").astype(np.int32)
index_df = pd.read_csv(FEATURE_DIR / "development_feature_index.csv")

if X.ndim != 2:
    raise ValueError(f"Expected a 2-D feature matrix, received {X.shape}")

if len(X) != len(y) or len(X) != len(index_df):
    raise ValueError("Feature, label and index lengths differ.")

if not np.isfinite(X).all():
    raise ValueError("Feature matrix contains NaN or infinity.")

if not np.array_equal(y, index_df["label"].to_numpy(dtype=np.int32)):
    raise ValueError("Feature index and labels are misaligned.")

if index_df["image_id"].duplicated().any():
    raise ValueError("Duplicate image IDs found.")

CLASS_IDS = np.unique(y)
NUM_CLASSES = len(CLASS_IDS)

if not np.array_equal(CLASS_IDS, np.arange(NUM_CLASSES)):
    raise ValueError("Class labels must be encoded as 0..K-1.")

print("Development features:", X.shape)
print("Development labels:", y.shape)
print("Classes:", NUM_CLASSES)


def build_chilifusionnet_noaug_smote(random_state=42):

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
            ("smote", SMOTE(random_state=random_state)),
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


outer_cv = StratifiedKFold(
    n_splits=OUTER_FOLDS,
    shuffle=True,
    random_state=SEED
)

outer_splits = list(outer_cv.split(X, y))


COLUMNS = [
    "Configuration",
    "Outer Fold",
    "Inner Fold",
    "Outer Seed",
    "Inner Seed",
    "Model Seed",
    "Inner Train N",
    "Inner Validation N",
    "Accuracy",
    "Macro Precision",
    "Macro Recall",
    "Macro F1"
]

results = []



for outer_fold, (outer_train_idx, outer_val_idx) in enumerate(
    outer_splits, start=1
):

    print(f"\n{'=' * 65}")
    print(f"OUTER FOLD {outer_fold}/{OUTER_FOLDS}")
    print(f"{'=' * 65}")

    X_outer_train = X[outer_train_idx]
    y_outer_train = y[outer_train_idx]

    print("Outer training:", len(outer_train_idx))
    print("Outer validation reserved:", len(outer_val_idx))

    inner_seed = INNER_SEEDS[outer_fold - 1]

    inner_cv = StratifiedKFold(
        n_splits=INNER_FOLDS,
        shuffle=True,
        random_state=inner_seed
    )

    for inner_fold, (inner_train_idx, inner_val_idx) in enumerate(
        inner_cv.split(X_outer_train, y_outer_train),
        start=1
    ):

        X_train = X_outer_train[inner_train_idx]
        y_train = y_outer_train[inner_train_idx]

        X_val = X_outer_train[inner_val_idx]
        y_val = y_outer_train[inner_val_idx]

        model = build_chilifusionnet_noaug_smote(random_state=SEED)

        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)

        row = {
            "Configuration": CONFIGURATION,
            "Outer Fold": outer_fold,
            "Inner Fold": inner_fold,
            "Outer Seed": SEED,
            "Inner Seed": inner_seed,
            "Model Seed": SEED,
            "Inner Train N": len(inner_train_idx),
            "Inner Validation N": len(inner_val_idx),
            "Accuracy": accuracy_score(y_val, y_pred),
            "Macro Precision": precision_score(
                y_val, y_pred, average="macro", zero_division=0
            ),
            "Macro Recall": recall_score(
                y_val, y_pred, average="macro", zero_division=0
            ),
            "Macro F1": f1_score(
                y_val, y_pred, average="macro", zero_division=0
            )
        }

        results.append(row)

        print(
            f"Outer {outer_fold} | Inner {inner_fold} | "
            f"Accuracy: {row['Accuracy']:.4f} | "
            f"Macro F1: {row['Macro F1']:.4f}"
        )

        del model
        gc.collect()


results_df = (
    pd.DataFrame(results, columns=COLUMNS)
    .sort_values(["Outer Fold", "Inner Fold"])
    .reset_index(drop=True)
)

if len(results_df) != OUTER_FOLDS * INNER_FOLDS:
    raise RuntimeError(
        f"Expected {OUTER_FOLDS * INNER_FOLDS} inner-fold results, "
        f"found {len(results_df)}"
    )

metric_columns = [
    "Accuracy",
    "Macro Precision",
    "Macro Recall",
    "Macro F1"
]

summary = (
    results_df
    .groupby("Outer Fold")[metric_columns]
    .agg(["mean", "std"])
)

summary.columns = [f"{metric}_{stat}" for metric, stat in summary.columns]
summary = summary.reset_index()



print("\nINNER-CV SUMMARY BY OUTER FOLD")
print(summary.round(4).to_string(index=False))

print("\nOVERALL INNER-CV DESCRIPTIVE SUMMARY")

for metric in metric_columns:
    print(
        f"{metric}: "
        f"{results_df[metric].mean() * 100:.2f} "
        f"± {results_df[metric].std(ddof=1) * 100:.2f}%"
    )

print("\nCompleted inner fits:", len(results_df))