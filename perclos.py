import time
from collections import deque
from config import PERCLOS_WINDOW


class PERCLOS:
    """
    Percentage of eye closure in a time window.
    Returns value in percentage (0-100).
    """
    def __init__(self, window=PERCLOS_WINDOW):
        self.window = window
        self.data = deque()

    def update(self, closed_flag):
        now = time.time()
        self.data.append((now, int(closed_flag)))

        while self.data and now - self.data[0][0] > self.window:
            self.data.popleft()

        if len(self.data) < 2:
            return 0.0

        closed_time = 0.0
        for i in range(1, len(self.data)):
            prev_t, prev_closed = self.data[i - 1]
            curr_t, _ = self.data[i]
            if prev_closed:
                closed_time += (curr_t - prev_t)

        total_time = self.data[-1][0] - self.data[0][0]
        if total_time <= 0:
            return 0.0

        perclos_val = (closed_time / total_time) * 100.0
        return max(0.0, min(100.0, perclos_val))