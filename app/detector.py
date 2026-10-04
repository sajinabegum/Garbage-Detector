from pathlib import Path
from ultralytics import YOLO

# COCO classes available in the lightweight pretrained model.
# We intentionally use only common litter-like objects for this demo.
LITTER_CLASSES = {
    "bottle",
    "cup",
}

class LitterDetector:
    def __init__(self, model_path="yolo11n.pt", confidence=0.45):
        self.model = YOLO(model_path)
        self.confidence = confidence

    def detect(self, frame):
        results = self.model.predict(
            source=frame,
            conf=self.confidence,
            verbose=False,
        )
        result = results[0]
        detections = []

        if result.boxes is None:
            return detections, result.plot()

        names = result.names

        for box in result.boxes:
            cls_id = int(box.cls[0])
            label = names[cls_id]
            conf = float(box.conf[0])

            if label.lower() in LITTER_CLASSES:
                xyxy = [int(v) for v in box.xyxy[0].tolist()]
                detections.append({
                    "label": label,
                    "confidence": conf,
                    "bbox": xyxy,
                })

        annotated = result.plot()
        return detections, annotated
