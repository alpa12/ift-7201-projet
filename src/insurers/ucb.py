# Reused code from exercises of IFT-7201

import numpy as np
from insurers.insurer import Insurer

class UCB(Insurer):
    def __init__(self, K, name=None, capital=0, interest_rate=0):
        super().__init__(K=K, name=name, capital=capital, interest_rate=interest_rate)
        self.t = 0

    def get_action(self):
        if self.t < self.K:
            k = self.t
            return k
        else:
            self.ucbs = self.means + np.sqrt(2 * np.log(self.t) / self.plays)
            return np.argmax(self.ucbs)

    def report_results(self, k, premium, claims):
        profit = premium - np.sum(claims)
        self.means[k] = (self.plays[k] * self.means[k] + profit) / (self.plays[k] + 1)
        self.plays[k] += 1
        self.t += 1
        super().report_results(k, premium, claims)

    def reset(self):
        self.__init__(
            K=self.K,
            name=self.name,
            capital=self.initial_capital,
            interest_rate=self.interest_rate
        )

