import time
from config import GAZE_AWAY_YAW


class GazeTracker:
    def __init__(self):
        self.away_start = None

    def update(self, yaw):
        now = time.time()

        if abs(yaw) > GAZE_AWAY_YAW:
            if self.away_start is None:
                self.away_start = now
            return now - self.away_start
        else:
            self.away_start = None
            return 0.0