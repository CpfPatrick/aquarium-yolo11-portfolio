# YOLO11n Aquarium Detection — Experiment Reproduction

Reproducible fine-tuning and evaluation of [Ultralytics YOLO11n](https://docs.ultralytics.com/models/yolo11/) at two input resolutions.

**Dataset:** [Aquarium Combined v6](https://universe.roboflow.com/brad-dwyer/aquarium-combined/dataset/6), 638 images; 448 train / 127 validation / 63 test; 7 classes.

**Training:** 50 epochs, batch 8, seed 42, patience 10; pretrained `yolo11n.pt`; Ultralytics 8.4.115, Tesla T4. Input resolution is the only configuration change apart from run names.

Test results (63 images, 584 objects):

| Model | Precision | Recall | mAP50 | mAP50–95 |
|---|---:|---:|---:|---:|
| YOLO11n 640 | 0.7930 | 0.6615 | 0.7483 | 0.4648 |
| YOLO11n 960 | 0.7729 | 0.7221 | 0.7740 | 0.4936 |

The 960 checkpoint was selected using validation metrics before a single sealed test session. No post-test tuning was performed. This single-seed comparison does not measure run-to-run uncertainty. Full per-class metrics: [640 CSV](results/final_test/baseline_test_metrics.csv), [960 CSV](results/final_test/selected_test_metrics.csv).

```bash
python -m pip install -r requirements.txt
```

Download the dataset separately. Open [train/eval](notebooks/train_eval.ipynb) in Colab or Jupyter and set the dataset path; use [inference demo](notebooks/inference_demo.ipynb) for a local or uploaded image. The demo downloads and verifies the [v1.0.0 model](https://github.com/CpfPatrick/aquarium-yolo11-portfolio/releases/tag/v1.0.0).

[Experiment record](docs/experiment_01_plan.md) · [Error analysis](docs/error_analysis.md) · [Test protocol](docs/frozen_test_protocol.md)

![Baseline validation cases](results/baseline/val_cases_contact_sheet.jpg)

Adapted validation images: Aquarium Combined v6, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code and checkpoint: [AGPL-3.0](LICENSE). See [attribution and scope](NOTICE.md). This reproduces the documented experiment, not a published paper or the FishSense system.
