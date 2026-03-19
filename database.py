import sqlite3
from datetime import datetime
from config import DB_NAME


class DatabaseManager:
    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS driver_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                driver_id TEXT,
                timestamp TEXT,
                perclos REAL,
                blink_rate REAL,
                yawn_freq REAL,
                pitch REAL,
                yaw REAL,
                gaze_duration REAL,
                fatigue_prob REAL,
                attention_score REAL,
                risk_score REAL,
                risk_level TEXT
            )
            """
        )
        self.conn.commit()

    def insert(
        self,
        driver_id,
        perclos,
        blink_rate,
        yawn_freq,
        pitch,
        yaw,
        gaze_duration,
        fatigue_prob,
        attention_score,
        risk_score,
        risk_level,
    ):
        self.cursor.execute(
            """
            INSERT INTO driver_data (
                driver_id, timestamp, perclos, blink_rate,
                yawn_freq, pitch, yaw, gaze_duration,
                fatigue_prob, attention_score, risk_score, risk_level
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                driver_id,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                perclos,
                blink_rate,
                yawn_freq,
                pitch,
                yaw,
                gaze_duration,
                fatigue_prob,
                attention_score,
                risk_score,
                risk_level,
            ),
        )
        self.conn.commit()