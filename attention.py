class AttentionModel:
    def __init__(self):
        self.pitch_history = []
        self.attention_history = []

    def compute(self, perclos, blink_rate, pitch, gaze_duration):
        self.pitch_history.append(pitch)
        if len(self.pitch_history) > 10:
            self.pitch_history.pop(0)

        avg_pitch = sum(self.pitch_history) / len(self.pitch_history)

        score = 100.0

        # softer penalties
        score -= perclos * 0.35

        if blink_rate > 30:
            score -= min((blink_rate - 30) * 0.4, 12)

        if avg_pitch > 25:
            score -= min((avg_pitch - 25) * 0.4, 12)

        if gaze_duration > 2:
            score -= 8
        if gaze_duration > 3.5:
            score -= 8

        score = max(0, min(100, score))

        self.attention_history.append(score)
        if len(self.attention_history) > 15:
            self.attention_history.pop(0)

        smooth_score = sum(self.attention_history) / len(self.attention_history)
        return round(smooth_score, 2)