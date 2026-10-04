# Project Presentation Notes

## Title
**AI-Based Smart Park Litter Detection and Alert System**

## Problem
People sometimes leave plastic bottles, cups and other waste in open park areas. Manual monitoring is difficult and waste can remain unnoticed.

## Proposed solution
Use computer vision to monitor a camera feed, detect litter-like objects and generate an audible alert while storing evidence of the detection.

## AI component
A YOLO object-detection model processes each frame and identifies supported objects. The demo uses bottle and cup as litter-like classes.

## Current prototype
Webcam/video → YOLO → detection → beep → evidence image → CSV log → dashboard.

## Future enhancement
The next version can use an IP CCTV RTSP stream and object tracking to determine a stronger littering event: a person drops an object and leaves it behind.

## Important limitation
Object detection alone cannot prove that a person threw the garbage. The prototype therefore reports a **litter-like object detection**, not a definitive accusation of littering.
