import math


class BayesianFatigue:
    def __init__(self):
        self.pitch_history = []
        self.score_history = []

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def compute(self, perclos, blink, yawn, pitch, gaze):
        self.pitch_history.append(pitch)
        if len(self.pitch_history) > 10:
            self.pitch_history.pop(0)

        avg_pitch = sum(self.pitch_history) / len(self.pitch_history)

        score = 0.0

        # lower effect of perclos
        score += 0.04 * perclos

        # only mild yawn effect
        score += 0.35 * yawn

        # gaze adds only after longer duration
        if gaze > 2:
            score += 0.25
        if gaze > 3:
            score += 0.35

        # blink effect reduced
        if blink > 35:
            score += 1.0
        elif blink > 28:
            score += 0.5

        # pitch effect reduced
        if avg_pitch > 35:
            score += 1.0
        elif avg_pitch > 25:
            score += 0.5

        prob = self.sigmoid(score)

        self.score_history.append(prob)
        if len(self.score_history) > 15:
            self.score_history.pop(0)

        smooth_prob = sum(self.score_history) / len(self.score_history)
        return round(smooth_prob, 3)