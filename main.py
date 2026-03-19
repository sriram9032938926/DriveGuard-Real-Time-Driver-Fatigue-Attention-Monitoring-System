import time
import cv2
import mediapipe as mp
import pandas as pd
import streamlit as st

from config import *
from eye_detector import EyeDetector
from blink_detector import BlinkDetector
from perclos import PERCLOS
from gaze_tracker import GazeTracker
from head_pose import get_head_pose
from yawn_detector import YawnDetector
from attention import AttentionModel
from bayesian_fatigue import BayesianFatigue
from risk_engine import RiskEngine
from alert import AlertSystem
from database import DatabaseManager
from vehicle import VehicleSimulator


st.set_page_config(page_title="Driver Monitoring Dashboard", layout="wide")
st.title("Driver Fatigue & Attention Monitoring Dashboard")
st.caption("Real-time monitoring with camera verification and 2-minute behavioral summary")


# --------------------------
# Sidebar
# --------------------------
st.sidebar.header("Controls")
vehicle_speed = st.sidebar.slider("Vehicle Speed (km/h)", 0, 120, int(DEFAULT_SPEED), 5)
start_monitoring = st.sidebar.button("Start Monitoring")
stop_monitoring = st.sidebar.button("Stop Monitoring")

# optional tuning
show_debug = st.sidebar.checkbox("Show Debug Info", value=False)


# --------------------------
# Session State
# --------------------------
if "running" not in st.session_state:
    st.session_state.running = False

if "summary_ready" not in st.session_state:
    st.session_state.summary_ready = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "summary_df" not in st.session_state:
    st.session_state.summary_df = pd.DataFrame()

if start_monitoring:
    st.session_state.running = True
    st.session_state.summary_ready = False
    st.session_state.start_time = time.time()
    st.session_state.summary_df = pd.DataFrame()

if stop_monitoring:
    st.session_state.running = False


# --------------------------
# Dashboard placeholders
# --------------------------
col1, col2, col3, col4 = st.columns(4)
fatigue_metric = col1.empty()
attention_metric = col2.empty()
risk_metric = col3.empty()
speed_metric = col4.empty()

status_box = st.empty()
frame_placeholder = st.empty()
chart_placeholder = st.empty()
debug_box = st.empty()
summary_placeholder = st.empty()


# --------------------------
# Monitoring
# --------------------------
def run_monitoring():
    eye = EyeDetector()
    blink = BlinkDetector()
    perclos = PERCLOS()
    gaze = GazeTracker()
    yawn = YawnDetector()
    attention_model = AttentionModel()
    bayes = BayesianFatigue()
    risk_engine = RiskEngine()
    alert = AlertSystem(ALARM_SOUND_PATH)
    db = DatabaseManager()
    vehicle = VehicleSimulator(initial_speed=float(vehicle_speed))

    calibration_seconds = 8
    last_log_time = 0.0
    history = []

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Could not open webcam.")
        return

    mp_face = mp.solutions.face_mesh
    mesh = mp_face.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    while st.session_state.running:
        ret, frame = cap.read()
        if not ret:
            status_box.error("Failed to read frame from camera.")
            break

        vehicle.speed = float(vehicle_speed)

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mesh.process(rgb)

        fatigue_prob = 0.0
        attention_score = 100.0
        risk_score = 0
        risk_level = "Safe"
        perclos_val = 0.0
        blink_rate = 0
        yawn_flag = 0
        pitch = 0.0
        yaw = 0.0
        roll = 0.0
        gaze_duration = 0.0
        closed_duration = 0.0
        ear = 0.0

        current_time = time.time()
        elapsed = current_time - st.session_state.start_time

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark

            # --------------------------
            # Eye metrics
            # --------------------------
            ear = eye.get_ear(landmarks)
            blink_rate = blink.update(ear, EAR_THRESHOLD)
            closed_duration = blink.closed_duration()
            eye_closed_flag = int(ear < EAR_THRESHOLD)
            perclos_val = perclos.update(eye_closed_flag)

            # --------------------------
            # Head pose
            # --------------------------
            pitch, yaw, roll = get_head_pose(landmarks, w, h)

            # Ignore tiny natural movements
            if abs(yaw) < 10:
                yaw = 0.0
            if abs(pitch) < 10:
                pitch = 0.0

            head_warning_flag = int(pitch > 22 or abs(yaw) > 20)

            # --------------------------
            # Gaze
            # --------------------------
            gaze_duration = gaze.update(yaw)

            # --------------------------
            # Yawn
            # --------------------------
            yawn_flag = int(yawn.is_yawning(landmarks))

            # --------------------------
            # Fatigue
            # --------------------------
            if vehicle.is_moving(MIN_SPEED):
                fatigue_prob = bayes.compute(
                    perclos=perclos_val,
                    blink=blink_rate,
                    yawn=yawn_flag,
                    pitch=pitch,
                    gaze=gaze_duration,
                )

                # extra penalty only for real microsleep
                if closed_duration >= MICROSLEEP_THRESHOLD:
                    fatigue_prob = min(1.0, fatigue_prob + 0.20)

                # small extra penalty for persistent head warning
                if head_warning_flag and gaze_duration > 2.0:
                    fatigue_prob = min(1.0, fatigue_prob + 0.08)
            else:
                fatigue_prob = 0.0

            # --------------------------
            # Attention
            # --------------------------
            attention_score = attention_model.compute(
                perclos_val,
                blink_rate,
                pitch,
                gaze_duration
            )

            # --------------------------
            # Risk
            # --------------------------
            speed_factor = min(vehicle.speed / 120.0, 0.20)
            total_fatigue = min(1.0, fatigue_prob + speed_factor)

            risk_score, risk_level = risk_engine.compute(
                total_fatigue,
                attention_score
            )

            # During calibration, don't allow high alerts
            if elapsed < calibration_seconds:
                risk_score = min(risk_score, 40)
                if risk_score < 45:
                    risk_level = "Calibrating"

            # --------------------------
            # Alerts
            # --------------------------
            if vehicle.is_moving(MIN_SPEED) and elapsed > calibration_seconds:
                alert.alert(risk_score)

            # --------------------------
            # Overlay
            # --------------------------
            cv2.putText(frame, f"EAR: {ear:.2f}", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            cv2.putText(frame, f"PERCLOS: {perclos_val:.1f}%", (20, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            cv2.putText(frame, f"Blinks/min: {blink_rate}", (20, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

            cv2.putText(frame, f"Yawns: {yawn_flag}", (20, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

            cv2.putText(frame, f"Pitch: {pitch:.1f} | Yaw: {yaw:.1f}", (20, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.putText(frame, f"Gaze Away: {gaze_duration:.1f}s", (20, 180),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 255, 0), 2)

            cv2.putText(frame, f"Fatigue: {fatigue_prob * 100:.1f}%", (20, 210),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.putText(frame, f"Attention: {attention_score:.1f}%", (20, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.putText(frame, f"Risk: {risk_level} ({risk_score})", (20, 270),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 128, 255), 2)

            # --------------------------
            # Save once per second
            # --------------------------
            if current_time - last_log_time >= 1:
                last_log_time = current_time

                db.insert(
                    DRIVER_ID,
                    perclos_val,
                    blink_rate,
                    yawn_flag,
                    pitch,
                    yaw,
                    gaze_duration,
                    fatigue_prob,
                    attention_score,
                    risk_score,
                    risk_level,
                )

                history.append({
                    "time": pd.Timestamp.now(),
                    "perclos": perclos_val,
                    "blink_rate": blink_rate,
                    "yawn_freq": yawn_flag,
                    "pitch": pitch,
                    "yaw": yaw,
                    "gaze_duration": gaze_duration,
                    "fatigue_prob": fatigue_prob * 100,
                    "attention_score": attention_score,
                    "risk_score": risk_score,
                })
        else:
            cv2.putText(frame, "Face not detected", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # --------------------------
        # Frame to Streamlit
        # --------------------------
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(rgb_frame, channels="RGB", use_container_width=True)

        # --------------------------
        # Dashboard metrics
        # --------------------------
        fatigue_metric.metric("Fatigue", f"{fatigue_prob * 100:.1f}%")
        attention_metric.metric("Attention", f"{attention_score:.1f}%")
        risk_metric.metric("Risk", f"{risk_level} ({risk_score})")
        speed_metric.metric("Speed", f"{vehicle.speed:.1f} km/h")

        remaining = max(0, SUMMARY_WINDOW_SEC - int(elapsed))
        if elapsed < calibration_seconds:
            status_box.info(f"Calibrating system... {int(calibration_seconds - elapsed)} sec left")
        else:
            status_box.info(f"Monitoring live. 2-minute summary in {remaining} sec")

        # --------------------------
        # Debug info
        # --------------------------
        if show_debug:
            debug_box.write({
                "EAR": round(ear, 3),
                "PERCLOS": round(perclos_val, 2),
                "Blink Rate": blink_rate,
                "Closed Duration": round(closed_duration, 2),
                "Pitch": round(pitch, 2),
                "Yaw": round(yaw, 2),
                "Gaze Duration": round(gaze_duration, 2),
                "Yawn": yawn_flag,
                "Fatigue Prob": round(fatigue_prob, 3),
                "Attention Score": round(attention_score, 2),
                "Risk Score": risk_score,
                "Risk Level": risk_level,
            })

        # --------------------------
        # Live chart
        # --------------------------
        if history:
            df_live = pd.DataFrame(history)
            chart_placeholder.line_chart(
                df_live.set_index("time")[["fatigue_prob", "attention_score", "risk_score"]]
            )

        # --------------------------
        # End after 2 minutes
        # --------------------------
        if elapsed >= SUMMARY_WINDOW_SEC:
            st.session_state.summary_ready = True
            st.session_state.summary_df = pd.DataFrame(history)
            st.session_state.running = False
            break

        time.sleep(FRAME_SLEEP)

    cap.release()


# --------------------------
# Start monitoring
# --------------------------
if st.session_state.running:
    run_monitoring()


# --------------------------
# Final summary
# --------------------------
if st.session_state.summary_ready and not st.session_state.summary_df.empty:
    df = st.session_state.summary_df.copy()

    avg_fatigue = df["fatigue_prob"].mean()
    avg_attention = df["attention_score"].mean()
    max_risk = df["risk_score"].max()
    avg_perclos = df["perclos"].mean()
    avg_blinks = df["blink_rate"].mean()
    total_yawns = int(df["yawn_freq"].sum())
    max_gaze = df["gaze_duration"].max()

    summary_placeholder.success("2-minute verification summary is ready")

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Avg Fatigue", f"{avg_fatigue:.1f}%")
    s2.metric("Avg Attention", f"{avg_attention:.1f}%")
    s3.metric("Max Risk Score", f"{max_risk:.0f}")
    s4.metric("Total Yawn Events", f"{total_yawns}")

    st.subheader("2-Minute Dashboard Summary")
    st.dataframe(
        pd.DataFrame({
            "Metric": [
                "Average PERCLOS",
                "Average Blink Rate",
                "Maximum Gaze-Away Duration",
                "Average Fatigue",
                "Average Attention",
                "Maximum Risk Score",
                "Total Yawn Events",
            ],
            "Value": [
                f"{avg_perclos:.2f}%",
                f"{avg_blinks:.2f}",
                f"{max_gaze:.2f} sec",
                f"{avg_fatigue:.2f}%",
                f"{avg_attention:.2f}%",
                f"{max_risk:.0f}",
                f"{total_yawns}",
            ],
        }),
        use_container_width=True,
    )

    st.subheader("Behavior Trend")
    st.line_chart(df.set_index("time")[["fatigue_prob", "attention_score", "risk_score"]])

    verdict = "SAFE"
    if max_risk >= 85 or avg_fatigue >= 70:
        verdict = "CRITICAL"
    elif max_risk >= 65 or avg_fatigue >= 50:
        verdict = "HIGH RISK"
    elif max_risk >= 45 or avg_fatigue >= 30:
        verdict = "MODERATE"

    st.subheader("Final Assessment")
    st.write(f"**Driver verification status:** {verdict}")
    st.write(
        "This assessment is based on eye closure behavior, blink rate, yawning, "
        "head pose, gaze-away duration, fatigue probability, and risk trend "
        "during the last 2 minutes."
    )