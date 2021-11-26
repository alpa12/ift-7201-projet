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
            profit = premium - np.sum(claims)
            self.insurer.store_claims(k, claims)
            print(profit)
