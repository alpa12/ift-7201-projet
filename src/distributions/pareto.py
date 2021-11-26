import numpy as np

from distributions.distribution import Distribution

class Pareto(Distribution):
    def __init__(self, alpha, _lambda):
        # If alpha <= 1 the mean doesn't exist
        assert alpha > 1 and _lambda > 0
        self.alpha = alpha
        self._lambda = _lambda

    def get_mean(self):
        return self._lambda / (self.alpha - 1)

    def play(self, n):
        return self._lambda * ((1 - np.random.uniform(n)) ** (-1 / self.alpha) - 1)
