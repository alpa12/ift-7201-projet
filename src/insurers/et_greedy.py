# Reused code from exercises of IFT-7201

import numpy as np
from insurers.insurer import Insurer

class ETGreedy(Insurer):
    def __init__(self, K, capital=0, interest_rate=0):
        super().__init__(K=K, capital=capital, interest_rate=interest_rate)
        self.t = 0

    def get_action(self):
        epsilon = 1 / np.sqrt(self.t)
        if np.random.rand() < epsilon:
            return np.random.choice(self.K)
        else:
            return np.argmax(self.means)

    def report_results(self, k, premium, claims):
        profit = premium - np.sum(claims)
        self.means[k] = (self.plays[k] * self.means[k] + profit) / (self.plays[k] + 1)
        self.plays[k] += 1
        self.t += 1
        super().report_results(k, premium, claims)

    def reset(self):
        super().reset()
        self.t = 0

    def __str__(self):
        return "ET-Greedy"
