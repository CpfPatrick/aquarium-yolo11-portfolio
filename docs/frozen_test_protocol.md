# Sealed test protocol

Model selection used validation metrics only. The selected 960 checkpoint and its SHA256 were recorded before the test split was opened.

Both checkpoints were evaluated in one sealed session: baseline at `imgsz=640`, selected model at `imgsz=960`. Other settings were fixed: `split=test`, `batch=8`, `device=0`, `conf=0.001`, `iou=0.7`, `rect=true`. The split contains 63 images and 584 annotated objects.

The [baseline CSV](../results/final_test/baseline_test_metrics.csv), [selected-model CSV](../results/final_test/selected_test_metrics.csv), and [sealed manifest](../results/final_test/sealed_test_manifest.json) record overall and per-class metrics, checkpoint checksums, and evaluation metadata.

The initial postprocessing step failed while serializing NumPy scalars after both inference runs had completed. [Recovery metadata](../results/final_test/postprocess_recovery.json) records that the existing results were serialized without repeating inference or changing thresholds.

No model, threshold, configuration, or validation case selection was changed in response to test performance. `post_test_tuning=false` is preserved in the sealed evidence. Reproduction runs should write new outputs and leave the archived results unchanged.
