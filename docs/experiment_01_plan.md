# Resolution experiment record

Experiment `exp01_imgsz960_seed42` was registered and run on 2026-08-19. This is the public summary of the recorded procedure and results; preregistration hashes in the [manifest](../results/experiment_01/experiment_manifest.json) refer to the original pre-training documents.

## Configuration

Question: does increasing input resolution improve validation detection quality without materially reducing precision or recall? Small or partially occluded fish motivated the hypothesis; the experiment does not establish a causal explanation for individual misses.

The [baseline](../configs/baseline.yaml) and [960 experiment](../configs/exp01_imgsz960.yaml) differ only in `imgsz` (640 vs. 960) and run `name`. Both use pretrained YOLO11n, 50 epochs, batch 8, seed 42, patience 10, and the same dataset split. Each checkpoint is evaluated at its training resolution.

Validation settings: `split=val`, `batch=8`, `device=0`, `conf=0.001`, `iou=0.7`, `rect=true`. Precision and recall use Ultralytics' smoothed mean-F1 operating point; `conf=0.001` is the prediction floor used to construct metric curves.

Only one 960 training run was registered. An out-of-memory failure would have ended the experiment as infeasible, without reducing batch size or trying another resolution.

## Validation-first selection

All four preregistered checks had to pass to select 960:

| Metric | Required change vs. 640 | Observed change |
|---|---:|---:|
| mAP50–95 | ≥ +0.005 | +0.023618 |
| Precision | ≥ −0.020 | −0.002176 |
| Recall | ≥ −0.020 | +0.034768 |
| Fish recall | ≥ −0.020 | +0.071103 |

| Validation metric | 640 | 960 |
|---|---:|---:|
| Precision | 0.799777 | 0.797601 |
| Recall | 0.681453 | 0.716221 |
| mAP50 | 0.766924 | 0.776219 |
| mAP50–95 | 0.465872 | 0.489490 |
| Fish recall | 0.672598 | 0.743701 |

The 960 checkpoint passed all checks and was selected before accessing test results. The [sealed test protocol](frozen_test_protocol.md) prohibits post-test tuning. One seed and one split provide no estimate of run-to-run uncertainty or evidence of broad superiority across datasets.

## Recorded artifacts

| Field | Value |
|---|---|
| Run status | Completed |
| Training duration | 26.367 minutes |
| Environment | Tesla T4; Python 3.12.13; PyTorch 2.11.0+cu128; Ultralytics 8.4.115 |
| Dataset YAML SHA256 | `dcb44902aac3e46a31ba85b3fa8cc7e3e4a131f69ed035b7181ab045a3ee89a7` |
| Selected checkpoint SHA256 | `ff7284669dd3d1b30b83f2d9eaacbdefdf8b50836f6f4e629bfd16f877a2f281` |

The [experiment manifest](../results/experiment_01/experiment_manifest.json) contains configuration checksums, timestamps, pretrained-weight provenance, and software versions. [Validation comparison](../results/experiment_01/validation_comparison.csv) and [per-class metrics](../results/experiment_01/val_metrics.csv) retain the numerical evidence.
