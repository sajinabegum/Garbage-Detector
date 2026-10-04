# Smart Park Litter Detection 🚮🤖

An AI-based computer-vision prototype that detects litter-like objects in a park camera feed and triggers an audible alert. The current demo works with a webcam or video file and is designed so an IP CCTV/RTSP stream can be added later.

## Demo flow

**Camera / Video → YOLO detection → litter-like object detected → beep + evidence snapshot + event log**

The prototype treats common COCO classes such as **bottle** and **cup** as litter-like objects for demonstration purposes. For a production system, train a custom YOLO model on park-specific litter classes (wrappers, plastic bags, cans, food containers, etc.).

## Features

- Live webcam detection
- Video-file detection
- YOLO object detection
- Litter-like classes: bottle, cup
- Audible alert with cooldown
- Evidence image saved for each alert
- CSV event log
- Simple Streamlit dashboard
- CCTV/RTSP extension documented
- No claim of full littering-event understanding; this demo detects objects

## Requirements

- Python 3.10+ recommended
- Laptop/desktop
- Webcam OR an MP4 video
- Internet once, to download the YOLO model

## Install

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the live demo

```bash
python app/main.py --source 0
```

Press `q` to quit.

The first run downloads `yolo11n.pt` automatically through Ultralytics.

## Run on a video

```bash
python app/main.py --source assets/demo.mp4
```

## Run the dashboard

```bash
streamlit run app/dashboard.py
```

The dashboard shows recent alert events and saved evidence images.

## Important demo note

This prototype detects **litter-like objects**, not the human action of throwing garbage. For a stronger second phase, add person/object tracking and temporal rules:

1. person is detected,
2. litter object is near the person,
3. object moves toward the ground,
4. person moves away,
5. object remains stationary.

That can be implemented with tracking and a custom litter dataset.

## CCTV / IP camera integration

Many IP cameras expose an RTSP stream. Once you have the stream URL, the same program can be pointed at it:

```bash
python app/main.py --source "rtsp://USER:PASSWORD@CAMERA_IP:554/stream"
```

Check your camera manufacturer's documentation for the correct RTSP URL. The current repository is intentionally demo-first and does not assume a particular CCTV brand.

## Project structure

```text
smart-park-litter-detection/
├── app/
│   ├── main.py
│   ├── detector.py
│   ├── alert.py
│   └── dashboard.py
├── assets/
├── logs/
├── .gitignore
├── requirements.txt
└── README.md
```

## Future scope

- Custom litter dataset and YOLO training
- Person + litter tracking
- Littering-event classification
- Multi-camera support
- Email/WhatsApp/SMS notification
- Park-zone mapping
- Cloud dashboard
- Edge deployment using Jetson/Raspberry Pi-class hardware
