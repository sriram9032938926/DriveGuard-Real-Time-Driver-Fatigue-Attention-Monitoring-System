
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


## 🏗️ System Architecture

```mermaid
flowchart TD

A[Start System] --> B[Initialize Camera]
B --> C[Capture Frame]
C --> D{Face Detected?}

D -- No --> C
D -- Yes --> E[Extract Facial Landmarks]

E --> F[Eye Detection (EAR)]
E --> G[Blink Detection]
E --> H[PERCLOS Calculation]
E --> I[Head Pose (Pitch, Yaw)]
E --> J[Gaze Tracking]
E --> K[Yawn Detection]

F --> L[Feature Fusion]
G --> L
H --> L
I --> L
J --> L
K --> L

L --> M[Fatigue Estimation]
M --> N[Attention Score Calculation]
N --> O[Risk Engine]

O --> P{Risk Level}

P -->|Safe| Q[Continue Monitoring]
P -->|Moderate| R[Display Warning]
P -->|High| S[Trigger Alert]
P -->|Critical| T[Trigger Alarm]

Q --> C
R --> C
S --> C
T --> C

O --> U[Store Data in Database]

U --> V{2 Minutes Completed?}

V -- No --> C
V -- Yes --> W[Generate Summary Report]

W --> X[Display Dashboard Summary]
X --> Y[End System]
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
