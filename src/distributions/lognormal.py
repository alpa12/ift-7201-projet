import numpy as np

from distributions.distribution import Distribution

class LogNormal(Distribution):
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def get_mean(self):
        return np.exp(self.mu + self.sigma ** 2 / 2)

    def play(self, n):
        return np.random.lognormal(mean=self.mu, sigma=self.sigma, size=n)
