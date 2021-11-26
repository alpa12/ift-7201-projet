import numpy as np


class Insurer():
    def __init__(self, K, capital=0):
        self.K = K
        self.capital = capital
        self.means = np.zeros(K)
        self.plays = np.zeros(K)
        self.claims = [[] for k in range(K)]

    def get_action(self):
        return np.random.choice(self.K)

    def report_results(self, k, premium, claims):
        self.claims[k].append(claims)
        self.capital += premium - np.sum(claims)

    def is_ruined(self):
        return self.capital < 0
