import numpy as np

from distributions.distribution import Distribution

class Gamma(Distribution):
    def __init__(self, alpha, theta):
        self.alpha = alpha
        self.theta = theta

    def get_mean(self):
        return self.alpha * self.theta

    def play(self, n):
        return np.random.gamma(self.alpha, self.theta, n)
