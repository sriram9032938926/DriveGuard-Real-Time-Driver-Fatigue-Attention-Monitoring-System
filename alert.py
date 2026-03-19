import threading
import time
import pygame
from config import ALARM_SOUND_PATH


class AlertSystem:
    """
    Alarm only if high risk persists for some time.
    Prevents false alarms due to noisy frames.
    """
    def __init__(self, sound_path=ALARM_SOUND_PATH, cooldown=4, trigger_seconds=2.5):
        self.cooldown = cooldown
        self.trigger_seconds = trigger_seconds
        self.last_played = 0.0
        self.high_risk_start = None
        self.enabled = False
        self.sound = None

        try:
            pygame.mixer.init()
            self.sound = pygame.mixer.Sound(sound_path)
            self.enabled = True
        except Exception as e:
            print(f"[AlertSystem] Audio disabled: {e}")

    def alert(self, risk_score):
        if not self.enabled:
            return

        now = time.time()

        if risk_score >= 85:
            if self.high_risk_start is None:
                self.high_risk_start = now

            high_risk_duration = now - self.high_risk_start

            if high_risk_duration >= self.trigger_seconds and (now - self.last_played) > self.cooldown:
                self.last_played = now
                threading.Thread(target=self._play_sound, daemon=True).start()
        else:
            self.high_risk_start = None

    def _play_sound(self):
        try:
            if self.sound:
                self.sound.play()
        except Exception as e:
            print(f"[AlertSystem] Failed to play sound: {e}")