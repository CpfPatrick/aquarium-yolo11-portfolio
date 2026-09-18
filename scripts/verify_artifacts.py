from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "results" / "baseline"
EXPERIMENT = ROOT / "results" / "experiment_01"
FINAL_TEST = ROOT / "results" / "final_test"
EXPECTED_COLUMNS = [
    "Class",
    "Images",
    "Instances",
    "Box-P",
    "Box-R",
    "Box-F1",
    "mAP50",
    "mAP50-95",
]
EXPECTED_BASELINE_SHA256 = "837d249c93ee487b262190adcd6287cece0af8b51c25654c5c9e4f4a25cd33e3"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    metrics_path = BASELINE / "val_metrics.csv"
    manifest_path = BASELINE / "val_manifest.json"
    cases_path = BASELINE / "val_cases.csv"

    for path in (metrics_path, manifest_path, cases_path):
        require(path.is_file(), f"missing required artifact: {path.relative_to(ROOT)}")

    with metrics_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        require(reader.fieldnames == EXPECTED_COLUMNS, "unexpected baseline metric columns")
        rows = list(reader)
    require(len(rows) == 8, "baseline metrics must contain overall plus seven classes")
    lookup = {row["Class"]: row for row in rows}
    require(int(lookup["all"]["Instances"]) == 909, "overall support must be 909")
    require(int(lookup["fish"]["Instances"]) == 459, "fish support must be 459")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["run_id"] == "val_best_imgsz640-2", "baseline run pointer is stale")
    require(manifest["dataset"]["split"] == "val", "baseline manifest must use validation")
    require(manifest["dataset"]["test_accessed"] is False, "test must remain sealed")
    checkpoint_sha = manifest["model"]["checkpoint_sha256"]
    require(re.fullmatch(r"[0-9a-f]{64}", checkpoint_sha) is not None, "invalid checkpoint SHA256")
    require(checkpoint_sha == EXPECTED_BASELINE_SHA256, "unexpected baseline checkpoint SHA256")
    require(
        manifest["outputs"]["metrics_csv_sha256"] == sha256_file(metrics_path),
        "baseline CSV checksum mismatch",
    )
    run_dir = ROOT / manifest["outputs"]["run_directory"]
    require(run_dir.is_dir() and run_dir.name == "val_best_imgsz640-2", "invalid baseline run directory")
    for filename in manifest["outputs"]["diagnostic_files"]:
        require((run_dir / filename).is_file(), f"missing diagnostic file: {filename}")

    result_dict = manifest["overall_metrics"]
    require(abs(float(lookup["all"]["Box-P"]) - result_dict["metrics/precision(B)"]) < 1e-6, "precision mismatch")
    require(abs(float(lookup["all"]["Box-R"]) - result_dict["metrics/recall(B)"]) < 1e-6, "recall mismatch")
    require(abs(float(lookup["all"]["mAP50"]) - result_dict["metrics/mAP50(B)"]) < 1e-6, "mAP50 mismatch")
    require(abs(float(lookup["all"]["mAP50-95"]) - result_dict["metrics/mAP50-95(B)"]) < 1e-6, "mAP50-95 mismatch")

    with cases_path.open(newline="", encoding="utf-8") as file:
        cases = list(csv.DictReader(file))
    require(len(cases) == 5, "exactly five fixed cases are required")
    require(len({row["image_id"] for row in cases}) == 5, "case image IDs must be unique")
    composition = {row["desired_slot"] for row in cases}
    require(
        composition == {"success_dense", "success_typical", "fn_case", "fp_case", "mixed_error"},
        "unexpected five-case composition",
    )
    require(all(abs(float(row["conf"]) - 0.5115115115115115) < 1e-12 for row in cases), "case conf mismatch")
    require(all(float(row["match_iou"]) == 0.5 for row in cases), "case match IoU mismatch")
    require(all(float(row["nms_iou"]) == 0.7 for row in cases), "case NMS IoU mismatch")
    require(
        any(row["contains_fish"].lower() == "true" and int(row["fn"]) > 0 for row in cases),
        "at least one fish-containing FN candidate is required",
    )
    require((BASELINE / "val_cases_contact_sheet.jpg").is_file(), "missing case contact sheet")
    require(
        any(row.get("fish_fn_confirmed", "").lower() == "true" for row in cases),
        "Patrick must confirm at least one fish-specific FN before publication",
    )

    experiment_metrics_path = EXPERIMENT / "val_metrics.csv"
    experiment_manifest_path = EXPERIMENT / "experiment_manifest.json"
    comparison_path = EXPERIMENT / "validation_comparison.csv"
    selection_path = EXPERIMENT / "model_selection_candidate.json"
    for path in (
        experiment_metrics_path,
        experiment_manifest_path,
        comparison_path,
        selection_path,
        EXPERIMENT / "config.diff",
    ):
        require(path.is_file(), f"missing experiment artifact: {path.relative_to(ROOT)}")

    with experiment_metrics_path.open(newline="", encoding="utf-8") as file:
        experiment_reader = csv.DictReader(file)
        require(experiment_reader.fieldnames == EXPECTED_COLUMNS, "unexpected experiment metric columns")
        experiment_rows = list(experiment_reader)
    require(len(experiment_rows) == 8, "experiment metrics must contain overall plus seven classes")
    experiment_lookup = {row["Class"]: row for row in experiment_rows}

    experiment_manifest = json.loads(experiment_manifest_path.read_text(encoding="utf-8"))
    require(experiment_manifest["changed_keys"] == ["imgsz", "name"], "experiment changed unexpected keys")
    require(experiment_manifest["preregistration"]["created_before_training"] is True, "experiment was not preregistered")
    require(experiment_manifest["validation"]["split"] == "val", "experiment manifest must use validation")
    require(experiment_manifest["validation"]["test_accessed"] is False, "experiment accessed test early")
    require(
        experiment_manifest["validation"]["metrics_csv_sha256"] == sha256_file(experiment_metrics_path),
        "experiment CSV checksum mismatch",
    )
    require(
        experiment_manifest["config_sha256"] == sha256_file(ROOT / experiment_manifest["config"]),
        "portable experiment config checksum mismatch",
    )
    experiment_run_dir = ROOT / experiment_manifest["validation"]["run_directory"]
    require(experiment_run_dir.is_dir(), "experiment validation directory is missing")

    with comparison_path.open(newline="", encoding="utf-8") as file:
        comparison = {row["model"]: row for row in csv.DictReader(file)}
    require(set(comparison) == {"baseline", "imgsz960"}, "comparison must contain two registered models")
    require(abs(float(comparison["imgsz960"]["mAP50-95"]) - float(experiment_lookup["all"]["mAP50-95"])) < 1e-6, "experiment comparison mismatch")

    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    require(selection["status"] == "approved_and_test_sealed", "unexpected selection status")
    require(selection["candidate"] == "imgsz960", "selection rule did not choose the registered winner")
    require(selection["approved_checkpoint"] == "imgsz960", "approved checkpoint mismatch")
    require(all(selection["checks"].values()), "not all preregistered checks passed")
    require(selection["test_accessed"] is True, "sealed test was not recorded")
    require(selection["post_test_tuning"] is False, "post-test tuning must remain disabled")

    sealed_manifest_path = FINAL_TEST / "sealed_test_manifest.json"
    test_lock_path = FINAL_TEST / "SEALED_DO_NOT_TUNE.json"
    release_manifest_path = FINAL_TEST / "release_manifest.json"
    baseline_test_csv = FINAL_TEST / "baseline_test_metrics.csv"
    selected_test_csv = FINAL_TEST / "selected_test_metrics.csv"
    for path in (
        sealed_manifest_path,
        test_lock_path,
        release_manifest_path,
        baseline_test_csv,
        selected_test_csv,
    ):
        require(path.is_file(), f"missing sealed-test artifact: {path.relative_to(ROOT)}")

    sealed = json.loads(sealed_manifest_path.read_text(encoding="utf-8"))
    require(sealed["status"] == "sealed_complete", "sealed-test status mismatch")
    require(sealed["dataset"]["split"] == "test", "sealed manifest must use test")
    require(sealed["dataset"]["images"] == 63, "unexpected test image count")
    require(sealed["post_test_tuning"] is False, "post-test tuning flag changed")
    require(sealed["no_further_training_authorized"] is True, "training lock missing")
    require(sealed["recovery"]["model_inference_repeated"] is False, "test inference was repeated")
    require(sealed["recovery"]["thresholds_changed"] is False, "test thresholds changed")

    models = {model["role"]: model for model in sealed["models"]}
    require(set(models) == {"baseline_reference", "selected_final"}, "sealed model set mismatch")
    require(models["selected_final"]["checkpoint_sha256"] == selection["checkpoint_sha256"], "selected SHA mismatch")

    for model in models.values():
        metrics_file = ROOT / model["metrics_csv"]
        run_directory = ROOT / model["run_directory"]
        require(metrics_file.is_file(), "sealed metrics CSV is missing")
        require(sha256_file(metrics_file) == model["metrics_csv_sha256"], "sealed CSV checksum mismatch")
        require(run_directory.is_dir(), "sealed diagnostic directory is missing")
        for filename in model["diagnostic_files"]:
            require((run_directory / filename).is_file(), f"missing sealed diagnostic: {filename}")

    test_lock = json.loads(test_lock_path.read_text(encoding="utf-8"))
    sealed_sha = sha256_file(sealed_manifest_path)
    require(test_lock["sealed_test_manifest_sha256"] == sealed_sha, "test-lock manifest SHA mismatch")
    require(test_lock["post_test_tuning"] is False, "test lock allows tuning")
    require(test_lock["no_further_training_authorized"] is True, "test lock allows training")

    release_manifest = json.loads(release_manifest_path.read_text(encoding="utf-8"))
    require(release_manifest["checkpoint_sha256"] == selection["checkpoint_sha256"], "release SHA mismatch")
    require(release_manifest["registered_imgsz"] == 960, "release imgsz mismatch")
    require(release_manifest["sealed_test_manifest_sha256"] == sealed_sha, "release manifest references stale test manifest")
    require(release_manifest["post_test_tuning"] is False, "release manifest allows tuning")

    print("Artifact checks passed")


if __name__ == "__main__":
    main()
