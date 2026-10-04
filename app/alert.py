import csv
import time
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")
EVIDENCE_DIR = LOG_DIR / "evidence"
CSV_PATH = LOG_DIR / "events.csv"

LOG_DIR.mkdir(exist_ok=True)
EVIDENCE_DIR.mkdir(exist_ok=True)

def beep():
    """Cross-platform best-effort audible alert."""
    try:
        import winsound
        winsound.Beep(1000, 250)
    except Exception:
        print("\a", end="", flush=True)

def save_event(frame, label, confidence, cv2_module):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".jpg"
    path = EVIDENCE_DIR / filename

    cv2_module.imwrite(str(path), frame)

    new_file = not CSV_PATH.exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["timestamp", "object", "confidence", "evidence"])
        writer.writerow([timestamp, label, f"{confidence:.2f}", str(path)])

    return timestamp, path

class AlertCooldown:
    def __init__(self, seconds=5):
        self.seconds = seconds
        self.last_alert = 0

    def ready(self):
        now = time.time()
        if now - self.last_alert >= self.seconds:
            self.last_alert = now
            return True
        return False
