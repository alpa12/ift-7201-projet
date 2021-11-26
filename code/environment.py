import numpy as np


class Environment():
    def __init__(self, insureds, insurer, T):
        self.insureds = insureds
        self.insurer = insurer
        self.T = T

    def play(self):
        for t in range(self.T):
            k = self.insurer.get_action()
            premium, claims = self.insureds[k].play()
            self.insurer.report_results(k, premium, claims)
            if self.insurer.is_ruined():
                print(f"L'assureur s'est ruiné au pas {t}")
                # return t
            print(self.insurer.capital)
