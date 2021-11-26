import numpy as np

from distributions.distribution import Distribution

class Constant(Distribution):
    def __init__(self, x):
        self.x = x

    def get_mean(self):
        return self.x

    def play(self, n):
        return np.repeat(self.x, n)
