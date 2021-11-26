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

    def store_claims(self, k, claims):
        self.claims[k].append(claims)
