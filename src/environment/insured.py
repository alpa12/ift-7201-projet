import numpy as np
from distributions.distribution import Distribution


class Insured():
    """
    Replaces the arm of a bandit in a traditional
    stochastic bandit problem
    """
    def __init__(self, freq=1, sev=1, premium=0):
        """
        frequency and severity are either constants, or
        functions, which when they are called with argument n,
        simulate n numbers.
        """
        for x in [freq, sev]:
            assert isinstance(x, Distribution)

        self.frequency = freq
        self.severity = sev
        self.premium = premium

    def play(self):
        n_claims = self.frequency.play(1)
        claims = np.array([]) if n_claims == 0 else self.severity.play(n_claims)
        return (self.premium, claims)
