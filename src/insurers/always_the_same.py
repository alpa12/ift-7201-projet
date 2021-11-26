# Reused code from exercises of IFT-7201

import numpy as np
from insurers.insurer import Insurer

class AlwaysTheSame(Insurer):
    def __init__(self, k, K, name=None, capital=0, interest_rate=0):
        super().__init__(K=K, name=name, capital=capital, interest_rate=interest_rate)
        if name is None:
            # Overwrite name to add k parameter
            self.name = f"{self.__class__.__name__} k = {k}"
        self.k = k

    def get_action(self):
        return self.k

    def report_results(self, k, premium, claims):
        profit = premium - np.sum(claims)
        self.means[k] = (self.plays[k] * self.means[k] + profit) / (self.plays[k] + 1)
        self.plays[k] += 1
        super().report_results(k, premium, claims)

    def reset(self):
        self.__init__(
            k=self.k,
            K=self.K,
            name=self.name,
            capital=self.initial_capital,
            interest_rate=self.interest_rate
        )

