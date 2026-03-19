class RiskEngine:
    def __init__(self):
        self.risk_history = []

    def compute(self, fatigue_prob, attention_score):
        attention_risk = (100 - attention_score) / 100.0
        combined = 0.55 * fatigue_prob + 0.45 * attention_risk

        raw_score = combined * 100

        self.risk_history.append(raw_score)
        if len(self.risk_history) > 15:
            self.risk_history.pop(0)

        risk_score = sum(self.risk_history) / len(self.risk_history)

        if risk_score >= 80:
            return int(risk_score), "Critical"
        elif risk_score >= 65:
            return int(risk_score), "High"
        elif risk_score >= 45:
            return int(risk_score), "Moderate"
        else:
            return int(risk_score), "Safe"