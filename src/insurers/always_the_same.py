# Reused code from exercises of IFT-7201

import numpy as np
from insurers.insurer import Insurer

class AlwaysTheSame(Insurer):
    def __init__(self, k, K, capital=0, interest_rate=0):
        super().__init__(K=K, capital=capital, interest_rate=interest_rate)
        self.k = k

    def get_action(self):
        return self.k

    def report_results(self, k, premium, claims):
        profit = premium - np.sum(claims)
        self.means[k] = (self.plays[k] * self.means[k] + profit) / (self.plays[k] + 1)
        self.plays[k] += 1
        super().report_results(k, premium, claims)

    def __str__(self):
        return f"Always k={self.k}"
