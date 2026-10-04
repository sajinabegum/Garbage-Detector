import argparse
import time
from pathlib import Path

import cv2

from detector import LitterDetector
from alert import AlertCooldown, beep, save_event

def parse_source(value):
    try:
        return int(value)
    except ValueError:
        return value

def main():
    parser = argparse.ArgumentParser(description="Smart Park Litter Detection Demo")
    parser.add_argument("--source", default="0", help="0 for webcam, or path/RTSP URL")
    parser.add_argument("--confidence", type=float, default=0.45)
    parser.add_argument("--cooldown", type=float, default=5.0)
    args = parser.parse_args()

    source = parse_source(args.source)
    detector = LitterDetector(confidence=args.confidence)
    cooldown = AlertCooldown(args.cooldown)

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(
            f"Could not open source: {args.source}. "
            "Check your webcam, video path, or RTSP URL."
        )

    print("Smart Park Litter Detection started.")
    print("Press Q to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            print("End of stream or camera read failed.")
            break

        detections, annotated = detector.detect(frame)

        if detections and cooldown.ready():
            best = max(detections, key=lambda x: x["confidence"])
            timestamp, evidence = save_event(
                frame, best["label"], best["confidence"], cv2
            )
            beep()
            print(
                f"[ALERT] {best['label']} "
                f"confidence={best['confidence']:.2f} "
                f"time={timestamp} evidence={evidence}"
            )

        # Demo overlay
        cv2.putText(
            annotated,
            "SMART PARK - LITTER DETECTION",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        status = "LITTER DETECTED" if detections else "MONITORING"
        cv2.putText(
            annotated,
            status,
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255) if detections else (0, 255, 0),
            2,
        )

        cv2.imshow("Smart Park Litter Detection", annotated)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
