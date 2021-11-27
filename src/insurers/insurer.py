import numpy as np


class Insurer():
    def __init__(self, K, capital=0, interest_rate=0):
        self.K = K
        self.initial_capital = capital
        self.capital = capital
        self.interest_rate = interest_rate
        self.means = np.zeros(K)
        self.plays = np.zeros(K)
        self.claims = [[] for k in range(K)]

    def get_action(self):
        return np.random.choice(self.K)

    def report_results(self, k, premium, claims):
        self.claims[k].append(claims)
        self.capital += premium - np.sum(claims)
        self.capital *= 1 + self.interest_rate

    def is_ruined(self):
        return self.capital < 0

    def reset(self):
        self.means = np.zeros(self.K)
        self.plays = np.zeros(self.K)
        self.claims = [[] for k in range(self.K)]
        self.capital = self.initial_capital

    def __str__(self):
        return "Random"
