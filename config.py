# =====================================
# DRIVER MONITORING SYSTEM CONFIG
# =====================================

# Eye & Blink Detection
EAR_THRESHOLD = 0.20
MICROSLEEP_THRESHOLD = 2.0 # seconds
BLINK_WARNING = 25
BLINK_DANGER = 30

# Yawn Detection
YAWN_ALERT = 3
YAWN_SEVERE = 5
MOUTH_OPEN_THRESHOLD = 0.05

# Head Pose
PITCH_WARNING = 22
PITCH_SEVERE = 30
YAW_WARNING = 20
GAZE_AWAY_YAW = 35

# Gaze Tracking
GAZE_WARNING_SEC = 2
GAZE_SEVERE_SEC = 3

# PERCLOS
PERCLOS_WINDOW = 60  # seconds
PERCLOS_WARNING = 40.0
PERCLOS_SEVERE = 55.0

# Paths
ALARM_SOUND_PATH = "sounds/sounds_alarm.wav"
DRIVER_ID = "DRIVER_001"
DB_NAME = "driver_monitoring.db"

# Other
IMG_SIZE = 64
MIN_SPEED = 5.0
DEFAULT_SPEED = 40.0
SUMMARY_WINDOW_SEC = 120  # 2 minutes
FRAME_SLEEP = 0.01