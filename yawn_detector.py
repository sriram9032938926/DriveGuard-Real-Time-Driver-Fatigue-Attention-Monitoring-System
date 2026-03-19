from config import MOUTH_OPEN_THRESHOLD


class YawnDetector:
    def __init__(self):
        self.yawn_history = []
        self.open_count = 0

    def is_yawning(self, landmarks):
        mouth_top = landmarks[13].y
        mouth_bottom = landmarks[14].y
        mouth_open = mouth_bottom - mouth_top

        # require stronger opening
        yawning_now = mouth_open > 0.065

        if yawning_now:
            self.open_count += 1
        else:
            self.open_count = 0

        # only count as yawn if open for multiple frames
        yawn_flag = int(self.open_count >= 8)

        self.yawn_history.append(yawn_flag)
        if len(self.yawn_history) > 10:
            self.yawn_history.pop(0)

        return int(sum(self.yawn_history) > 1)