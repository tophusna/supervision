## 👋 hello

This script provides functionality for processing videos using YOLOv8 for object
detection and Supervision for tracking and annotation.

## 💻 install

```bash
pip install -r requirements.txt
```

## ⚙️ run

```bash
python script.py \
--source_weights_path yolov8s.pt \
--source_video_path input.mp4 \
--target_video_path tracking_result.mp4
```


## ⚙️ parameters

| parameter                | required | description                                                                       |
|:-------------------------|:--------:|:----------------------------------------------------------------------------------|
| `--source_weights_path`  |    ✓     | Path to the source weights file for YOLOv8.                                       |
| `--source_video_path`    |    ✓     | Path to the source video file to be processed.                                    |
| `--target_video_path`    |    ✓     | Path to the target video file (output).                                           |
| `--confidence_threshold` |    ✗     | Confidence threshold for YOLO model detection. Default is 0.3.                    |
| `--iou_threshold`        |    ✗     | IOU (Intersection over Union) threshold for YOLO model detection. Default is 0.7. |
