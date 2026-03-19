import numpy as np

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


class EyeDetector:
    def ear(self, pts):
        def dist(a, b):
            return np.linalg.norm(np.array([a.x, a.y]) - np.array([b.x, b.y]))

        A = dist(pts[1], pts[5])
        B = dist(pts[2], pts[4])
        C = dist(pts[0], pts[3])

        if C == 0:
            return 0.0
        return (A + B) / (2 * C)

    def get_ear(self, landmarks):
        left = [landmarks[i] for i in LEFT_EYE]
        right = [landmarks[i] for i in RIGHT_EYE]
        return (self.ear(left) + self.ear(right)) / 2