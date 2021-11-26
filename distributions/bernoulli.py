import numpy as np

from distributions.distribution import Distribution

class Bernoulli(Distribution):
    def __init__(self, p):
        self.p = p

    def get_mean(self):
        return self.p

    def play(self, n):
        return np.random.binomial(n=1, p=self.p, size=n)
