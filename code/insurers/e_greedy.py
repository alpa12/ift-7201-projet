# Reused code from exercises of IFT-7201

import numpy as np

class EGreedy():
    def __init__(self, epsilon, K, capital=0):
        self.epsilon = epsilon
        self.K = K
        self.means = np.zeros(K)
        self.plays = np.zeros(K)
        self.capital = capital

    def get_action(self):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.K)
        else:
            return np.argmax(self.means)

    def store_claims(self, k, claims):
        claims = np.sum(claims)
        self.means[k] = (self.plays[k] * self.means[k] + claims)/(self.plays[k] + 1)
        self.plays[k] += 1
