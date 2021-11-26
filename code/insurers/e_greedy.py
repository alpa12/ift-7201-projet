# Reused code from exercises of IFT-7201

import numpy as np
from insurers.insurer import Insurer

class EGreedy(Insurer):
    def __init__(self, epsilon, K, capital=0):
        super().__init__(K, capital)
        self.epsilon = epsilon

    def get_action(self):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.K)
        else:
            return np.argmax(self.means)

    def report_results(self, k, premium, claims):
        profit = premium - np.sum(claims)
        self.means[k] = (self.plays[k] * self.means[k] + profit) / (self.plays[k] + 1)
        self.plays[k] += 1
        super().report_results(k, premium, claims)
