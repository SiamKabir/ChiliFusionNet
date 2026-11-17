from pathlib import Path
import hashlib
import json

import pandas as pd

DATASET_DIR = r"/Users/siam3432/Chili (Discover Computing)/archive_extracted"
OUTPUT_DIR = "artifacts/data"               

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"
}


def is_image_file(path):
    return (
        path.is_file()
        and path.suffix.lower() in IMAGE_EXTENSIONS
        and not path.name.startswith(".")
    )


def is_class_dir(path):
    return (
        path.is_dir()
        and not path.name.startswith(".")
        and path.name != "__MACOSX"
    )

def get_dataset_root(dataset_dir):
    dataset_dir = Path(dataset_dir).resolve()

    if not dataset_dir.is_dir():
        raise FileNotFoundError(
            f"Dataset directory not found: {dataset_dir}"
        )

    class_dirs = sorted([
        p for p in dataset_dir.iterdir()
        if is_class_dir(p)
    ])
    image_in_first_level = any(
        any(is_image_file(f) for f in folder.iterdir())
        for folder in class_dirs
    )

    if not image_in_first_level and len(class_dirs) == 1:
        dataset_dir = class_dirs[0]

    return dataset_dir


def create_manifest(dataset_dir):
    dataset_dir = get_dataset_root(dataset_dir)

    class_dirs = sorted([
        p for p in dataset_dir.iterdir()
        if is_class_dir(p)
    ])

    rows = []

    for class_dir in class_dirs:
        for image_path in sorted(class_dir.rglob("*")):
            if is_image_file(image_path):
                relative_path = image_path.relative_to(
                    dataset_dir
                ).as_posix()

                rows.append({
                    "image_id": relative_path,
                    "relative_path": relative_path,
                    "filepath": str(image_path.resolve()),
                    "class_name": class_dir.name,
                    "filename": image_path.name
                })

    manifest = pd.DataFrame(rows)

    if manifest.empty:
        raise ValueError("No images found in dataset.")

    return manifest

def calculate_sha256(filepath):
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:
        while True:
            block = file.read(1024 * 1024)

            if not block:
                break

            sha256.update(block)

    return sha256.hexdigest()


def audit_duplicates(manifest):
    manifest = manifest.copy()

    manifest["sha256"] = manifest["filepath"].apply(
        calculate_sha256
    )

    duplicate_groups = manifest[
        manifest.duplicated(
            subset="sha256",
            keep=False
        )
    ].copy()

    hash_class_count = (
        duplicate_groups
        .groupby("sha256")["class_name"]
        .nunique()
    )

    conflicting_hashes = set(
        hash_class_count[
            hash_class_count > 1
        ].index
    )

    duplicate_groups["group_type"] = duplicate_groups["sha256"].apply(
        lambda h: (
            "conflicting_label"
            if h in conflicting_hashes
            else "same_class"
        )
    )
    without_conflicts = manifest[
        ~manifest["sha256"].isin(conflicting_hashes)
    ].copy()
    manifest_clean = (
        without_conflicts
        .drop_duplicates(
            subset="sha256",
            keep="first"
        )
        .reset_index(drop=True)
    )

    retained_ids = set(manifest_clean["image_id"])

    audit_manifest = manifest.copy()

    audit_manifest["audit_status"] = audit_manifest.apply(
        lambda row: (
            "removed_conflicting_label"
            if row["sha256"] in conflicting_hashes
            else (
                "retained"
                if row["image_id"] in retained_ids
                else "removed_same_class_duplicate"
            )
        ),
        axis=1
    )

    return manifest_clean, duplicate_groups, audit_manifest


def encode_classes(manifest_clean):
    manifest_clean = manifest_clean.copy()

    class_names = sorted(
        manifest_clean["class_name"].unique()
    )

    class_to_id = {
        name: index
        for index, name in enumerate(class_names)
    }

    manifest_clean["label"] = (
        manifest_clean["class_name"]
        .map(class_to_id)
        .astype(int)
    )

    return manifest_clean, class_to_id


def verify_clean_set(manifest_clean):
    """Independent check: re-hash the retained files from disk."""
    rehash = manifest_clean["filepath"].apply(calculate_sha256)

    if not (rehash == manifest_clean["sha256"]).all():
        raise RuntimeError(
            "Retained file content differs from the audited hash."
        )

    return int(rehash.duplicated(keep=False).sum())

def main(dataset_dir, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = create_manifest(dataset_dir)

    manifest_clean, duplicate_groups, audit_manifest = (
        audit_duplicates(manifest)
    )
    audit_manifest.to_csv(
        output_dir / "original_manifest.csv",
        index=False
    )

    audit_manifest.to_csv(
        output_dir / "duplicate_audit_report.csv",
        index=False
    )

    duplicate_groups.to_csv(
        output_dir / "duplicate_groups.csv",
        index=False
    )

    manifest_clean, class_to_id = encode_classes(
        manifest_clean
    )

    remaining_duplicates = verify_clean_set(manifest_clean)

    manifest_clean.to_csv(
        output_dir / "clean_manifest.csv",
        index=False
    )

    with open(
        output_dir / "class_mapping.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(class_to_id, file, indent=4)

    original_count = len(manifest)
    clean_count = len(manifest_clean)
    removed_count = original_count - clean_count

    status_counts = (
        audit_manifest["audit_status"]
        .value_counts()
        .to_dict()
    )

    summary = {
        "original_images": original_count,
        "clean_images": clean_count,
        "removed_images": removed_count,
        "removed_same_class_duplicates": int(
            status_counts.get("removed_same_class_duplicate", 0)
        ),
        "removed_conflicting_label_images": int(
            status_counts.get("removed_conflicting_label", 0)
        ),
        "remaining_exact_duplicates": remaining_duplicates,
        "number_of_classes": len(class_to_id),
        "original_class_distribution": (
            manifest["class_name"]
            .value_counts()
            .sort_index()
            .to_dict()
        ),
        "clean_class_distribution": (
            manifest_clean["class_name"]
            .value_counts()
            .sort_index()
            .to_dict()
        ),
    }

    with open(
        output_dir / "duplicate_audit_summary.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(summary, file, indent=4)

    print("\n========================================")
    print("CHILIFUSIONNET - DUPLICATE AUDIT")
    print("========================================")

    print("Original images             :", original_count)
    print("Clean images                :", clean_count)
    print("Removed images              :", removed_count)
    print(
        "  same-class copies removed :",
        summary["removed_same_class_duplicates"]
    )
    print(
        "  conflicting-label removed :",
        summary["removed_conflicting_label_images"]
    )
    print("Classes                     :", len(class_to_id))

    print("\nClass mapping:")
    for name, label in class_to_id.items():
        print(f"{label}: {name}")

    print("\nOriginal class distribution:")
    print(
        manifest["class_name"]
        .value_counts()
        .sort_index()
    )

    print("\nClean class distribution:")
    print(
        manifest_clean["class_name"]
        .value_counts()
        .sort_index()
    )

    print("\nRemaining exact duplicates:", remaining_duplicates)
    print("Audit artifacts saved to:", output_dir)

    return manifest_clean, audit_manifest, summary


manifest_clean, audit_manifest, summary = main(
    dataset_dir=DATASET_DIR,
    output_dir=OUTPUT_DIR
)

audit_manifest[
    audit_manifest["audit_status"] != "retained"
][["image_id", "class_name", "sha256", "audit_status"]]