# Attribution and scope

## Aquarium Combined v6

Source: [Aquarium Combined, Brad Dwyer's Roboflow Universe workspace](https://universe.roboflow.com/brad-dwyer/aquarium-combined/dataset/6). License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The published split contains 448 training, 127 validation, and 63 test images. Classes: fish, jellyfish, penguin, puffin, shark, starfish, stingray.

The complete dataset is obtained separately. Included case visualizations and evaluation plots containing dataset images are adaptations: boxes, labels, confidence annotations, resizing, and panel layouts were added. Dataset imagery and annotations retain CC BY 4.0; this repository does not relicense them. Credit remains with the linked dataset source and its contributors.

## Ultralytics YOLO

The experiment fine-tunes the Ultralytics `yolo11n.pt` pretrained checkpoint using Ultralytics 8.4.115. Source code and the released checkpoint use [AGPL-3.0](LICENSE), following [Ultralytics' open-source licensing terms](https://www.ultralytics.com/license).

The [experiment manifest](results/experiment_01/experiment_manifest.json) records pretrained-weight provenance and software versions. The [release manifest](results/final_test/release_manifest.json) records the selected checkpoint's SHA256, input resolution, dataset attribution, and metrics.

## Experiment scope

This independent experiment reproduces its documented training and evaluation procedure. It does not claim to reproduce a published paper or an official FishSense implementation, and is not affiliated with or endorsed by UC San Diego Engineers for Exploration or FishSense. It evaluates 2D object detection, not RGB-D measurement, fish length or volume estimation, or field deployment.
