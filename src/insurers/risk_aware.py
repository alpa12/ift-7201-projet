# Reused code from exercises of IFT-7201

import numpy as np
from insurers.insurer import Insurer
from risk_measures.tvar import TVaR

class RiskAware(Insurer):
    def __init__(self, A, K, risk_measure, capital=0, interest_rate=0):
        super().__init__(K=K, capital=capital, interest_rate=interest_rate)
        self.A = A
        self.risk_quantity_list = np.zeros(K)
        self.parameters = [None] * K
        self.risk_measure = risk_measure

    def get_action(self):
        utility = self.means - self.A * self.risk_quantity_list
        best_actions = np.argwhere(utility == np.amax(utility)).flatten()
        return np.random.choice(best_actions)

    def report_results(self, k, premium, claims):
        profit = premium - np.sum(claims)
        self.means[k] = (self.plays[k] * self.means[k] + profit) / (self.plays[k] + 1)
        self.plays[k] += 1
        super().report_results(k, premium, claims)
        self.parameters[k] = self.risk_measure.update_parameters(self.claims[k], self.parameters[k])
        self.risk_quantity_list[k] = self.risk_measure.compute(parameters=self.parameters[k], capital=self.capital + premium)

    def reset(self):
        super().reset()
        self.risk_quantity_list = np.zeros(self.K)
        self.parameters = [None] * self.K

    def __str__(self):
        return f"RiskAware{self.A} {self.risk_measure}"
