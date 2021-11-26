# Reused code from exercises of IFT-7201

import numpy as np
from insurers.insurer import Insurer

class EGreedy(Insurer):
    def __init__(self, epsilon, K, name=None, capital=0, interest_rate=0):
        super().__init__(K=K, name=name, capital=capital, interest_rate=interest_rate)
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

    def reset(self):
        self.__init__(
            epsilon=self.epsilon,
            K=self.K,
            name=self.name,
            capital=self.initial_capital,
            interest_rate=self.interest_rate
        )

