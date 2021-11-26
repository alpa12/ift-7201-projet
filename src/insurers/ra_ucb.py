# Reused code from exercises of IFT-7201

import numpy as np
from insurers.insurer import Insurer
from utils.risk_measures import TVaR

class RA_UCB(Insurer):
    def __init__(self, risk_aversion, K, risk_measure=TVaR, name=None, capital=0, interest_rate=0):
        super().__init__(K=K, name=name, capital=capital, interest_rate=interest_rate)
        if name is None:
            # Overwrite name to add risk_aversion parameter
            self.name = f"{self.__class__.__name__} risk_aversion = {risk_aversion}"
        self.risk_aversion = risk_aversion
        self.risk_quantity_list = np.zeros(K)
        self.risk_measure = risk_measure


    def get_action(self):
        return np.argmin(self.means - self.risk_aversion * self.risk_quantity_list)
        

    def report_results(self, k, premium, claims):
        profit = premium - np.sum(claims)
        self.means[k] = (self.plays[k] * self.means[k] + profit) / (self.plays[k] + 1)
        self.plays[k] += 1
        super().report_results(k, premium, claims)
        self.risk_quantity_list[k] = self.risk_measure.compute(self.claims[k])


    def reset(self):
        self.__init__(
            risk_aversion=self.risk_aversion,
            K=self.K,
            prior=self.prior,
            name=self.name,
            capital=self.initial_capital,
            interest_rate=self.interest_rate
        )

