from pathlib import Path
import hashlib
import json

import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split


CLEAN_MANIFEST_PATH = "artifacts/data/clean_manifest.csv"
OUTPUT_DIR = "artifacts/data"

TEST_SIZE = 0.10
SPLIT_SEED = 2026
OVERWRITE_EXISTING_SPLIT = False

def fingerprint(image_ids):
    """SHA-256 fingerprint of a set of image IDs (order independent)."""
    joined = "\n".join(sorted(image_ids)).encode("utf-8")
    return hashlib.sha256(joined).hexdigest()


def validate_manifest(manifest_clean):
    required_columns = {
        "image_id",
        "filepath",
        "class_name",
        "label",
        "sha256"
    }

    missing = required_columns - set(manifest_clean.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    if manifest_clean[list(required_columns)].isna().any().any():
        raise ValueError("Missing values detected in clean manifest.")

    if manifest_clean["image_id"].duplicated().any():
        raise ValueError("Duplicate image IDs detected.")

    if manifest_clean["sha256"].duplicated().any():
        raise ValueError("Exact duplicates remain in clean manifest.")
    if (
        manifest_clean.groupby("class_name")["label"].nunique().gt(1).any()
        or manifest_clean.groupby("label")["class_name"].nunique().gt(1).any()
    ):
        raise ValueError("Inconsistent class-label mapping.")

def create_dataset_split(clean_manifest_path, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    split_file = output_dir / "split_manifest.csv"
    if split_file.exists() and not OVERWRITE_EXISTING_SPLIT:
        raise FileExistsError(
            f"{split_file} already exists. The existing split is kept so "
            "the holdout is not regenerated. Set "
            "OVERWRITE_EXISTING_SPLIT = True only if this is intended."
        )

    manifest_clean = pd.read_csv(clean_manifest_path)
    validate_manifest(manifest_clean)
    manifest_clean = (
        manifest_clean
        .sort_values("image_id")
        .reset_index(drop=True)
    )
    dev_df, test_df = train_test_split(
        manifest_clean,
        test_size=TEST_SIZE,
        random_state=SPLIT_SEED,
        stratify=manifest_clean["label"]
    )

    dev_df = dev_df.sort_values("image_id").reset_index(drop=True)
    test_df = test_df.sort_values("image_id").reset_index(drop=True)

    overlapping_ids = set(dev_df["image_id"]) & set(test_df["image_id"])
    overlapping_hashes = set(dev_df["sha256"]) & set(test_df["sha256"])

    if overlapping_ids:
        raise RuntimeError(f"{len(overlapping_ids)} image IDs overlap.")

    if overlapping_hashes:
        raise RuntimeError(
            f"{len(overlapping_hashes)} exact-image hashes overlap."
        )

    if len(dev_df) + len(test_df) != len(manifest_clean):
        raise RuntimeError("Dataset partition size mismatch.")

    dev_df["partition"] = "development"
    test_df["partition"] = "holdout"

    combined_manifest = pd.concat(
        [dev_df, test_df],
        ignore_index=True
    )
    class_distribution = pd.DataFrame({
        "development": dev_df["class_name"].value_counts(),
        "holdout": test_df["class_name"].value_counts()
    }).fillna(0).astype(int).sort_index()

    class_distribution["total"] = (
        class_distribution["development"]
        + class_distribution["holdout"]
    )
    dev_df.to_csv(output_dir / "development_manifest.csv", index=False)
    test_df.to_csv(output_dir / "holdout_manifest.csv", index=False)
    combined_manifest.to_csv(split_file, index=False)
    class_distribution.to_csv(output_dir / "split_class_distribution.csv")

    summary = {
        "split_seed": SPLIT_SEED,
        "test_size": TEST_SIZE,
        "total_images": len(manifest_clean),
        "development_images": len(dev_df),
        "holdout_images": len(test_df),
        "overlapping_image_ids": len(overlapping_ids),
        "overlapping_sha256_hashes": len(overlapping_hashes),
        "development_fingerprint": fingerprint(dev_df["image_id"]),
        "holdout_fingerprint": fingerprint(test_df["image_id"]),
        "software": {
            "pandas": pd.__version__,
            "scikit-learn": sklearn.__version__
        },
        "class_distribution": class_distribution.to_dict(orient="index")
    }

    with open(
        output_dir / "split_summary.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(summary, file, indent=4)
    print("\n========================================")
    print("CHILIFUSIONNET - DATASET PARTITION")
    print("========================================")

    print("Total images :", len(manifest_clean))
    print("Development  :", len(dev_df))
    print("Holdout      :", len(test_df))
    print("Split seed   :", SPLIT_SEED)

    print("\nClass distribution:")
    print(class_distribution)

    print("\nImage ID overlap :", len(overlapping_ids))
    print("SHA-256 overlap  :", len(overlapping_hashes))
    print("Holdout fingerprint:", summary["holdout_fingerprint"])

    print("\nArtifacts saved to:", output_dir)

    return dev_df, test_df, summary

dev_df, test_df, split_summary = create_dataset_split(
    clean_manifest_path=CLEAN_MANIFEST_PATH,
    output_dir=OUTPUT_DIR
)