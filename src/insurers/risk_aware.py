# Reused code from exercises of IFT-7201

import numpy as np
from insurers.insurer import Insurer
from risk_measures.tvar import TVaR

class RiskAware(Insurer):
    def __init__(self, A, K, risk_measure=TVaR(0.95), name=None, capital=0, interest_rate=0):
        super().__init__(K=K, name=name, capital=capital, interest_rate=interest_rate)
        if name is None:
            # Overwrite name to add A parameter
            self.name = f"{self.__class__.__name__} A = {A}, risk_measure = {risk_measure.__class__.__name__}"
        self.A = A
        self.risk_quantity_list = np.zeros(K)
        self.parameters = [None] * K
        self.risk_measure = risk_measure


    def get_action(self):

        return np.argmin(self.means - self.A * self.risk_quantity_list)
        

    def report_results(self, k, premium, claims):
        profit = premium - np.sum(claims)
        self.means[k] = (self.plays[k] * self.means[k] + profit) / (self.plays[k] + 1)
        self.plays[k] += 1
        super().report_results(k, premium, claims)
        self.parameters[k] = self.risk_measure.update_parameters(self.parameters[k], self.claims[k])
        self.risk_quantity_list[k] = self.risk_measure.compute(parameters=self.parameters[k], capital=self.capital)


    def reset(self):
        self.__init__(
            A=self.A,
            K=self.K,
            risk_measure=TVaR(0.95),
            name=self.name,
            capital=self.initial_capital,
            interest_rate=self.interest_rate
        )

