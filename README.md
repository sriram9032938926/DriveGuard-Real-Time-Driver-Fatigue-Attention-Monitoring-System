
#  DriveGuard — Vision-Based Driver Fatigue & Attention Monitoring System

DriveGuard is a real-time driver monitoring system that detects fatigue, distraction, and unsafe driving behavior using computer vision and behavioral analysis.

It analyzes eye activity, head movement, gaze direction, and yawning patterns to compute fatigue, attention, and risk levels.

---

##  Overview

This system is designed to improve road safety by continuously monitoring the driver through a webcam and identifying early signs of drowsiness or inattention.

It combines multiple signals:
- Eye closure (EAR)
- Blink rate
- PERCLOS (Percentage of Eye Closure)
- Head pose (pitch & yaw)
- Gaze direction
- Yawn detection

These are fused into:
- **Fatigue Score**
- **Attention Score**
- **Risk Level (Safe / Moderate / High / Critical)**

---

## 🎯 Features

- 🎥 Real-time webcam monitoring  
- 👁️ Eye tracking & blink detection  
- 😴 Fatigue estimation using PERCLOS  
- 🧠 Attention scoring system  
- 🧭 Head pose & gaze tracking  
- 😮 Yawn detection  
- 🚨 Smart alert system (reduces false alarms)  
- 📊 Interactive Streamlit dashboard  
- 🧾 2-minute behavioral summary report  
- 🗄️ SQLite database logging  

---

## 🏗️ System Architecture

Camera Input
↓
Face Detection (MediaPipe)
↓
Feature Extraction
(EAR, Blink, PERCLOS, Head Pose, Gaze, Yawn)
↓
Fatigue Estimation (Bayesian + Smoothing)
↓
Attention Scoring
↓
Risk Engine
↓
Alert System + Dashboard + Database


---

## ⚙️ Tech Stack

- Python
- OpenCV
- MediaPipe
- Streamlit
- NumPy, Pandas
- SQLite
- Pygame (alert system)

---

## 📊 Key Metrics

| Metric | Description |
|------|-------------|
| EAR | Detects eye closure |
| PERCLOS | Measures fatigue level |
| Blink Rate | Indicates alertness |
| Head Pose | Detects distraction |
| Gaze Duration | Measures attention |
| Yawn Frequency | Detects drowsiness |

---
