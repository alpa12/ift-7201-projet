import numpy as np

from distributions.distribution import Distribution

class Poisson(Distribution):
    def __init__(self, _lambda):
        self._lambda = _lambda

    def get_mean(self):
        return self._lambda

    def play(self, n):
        return np.random.poisson(self._lambda, n)
