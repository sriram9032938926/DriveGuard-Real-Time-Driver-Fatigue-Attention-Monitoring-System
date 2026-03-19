import time


class BlinkDetector:
    def __init__(self):
        self.timestamps = []
        self.last_closed = None

    def update(self, ear, threshold):
        now = time.time()

        if ear < threshold:
            if self.last_closed is None:
                self.last_closed = now
        else:
            if self.last_closed is not None:
                duration = now - self.last_closed
                if duration > 0.1:
                    self.timestamps.append(now)
                self.last_closed = None

        self.timestamps = [t for t in self.timestamps if now - t <= 60]
        return len(self.timestamps)

    def closed_duration(self):
        if self.last_closed is None:
            return 0.0
        return time.time() - self.last_closed