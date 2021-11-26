import numpy as np
from scipy.stats import poisson, gamma


class RiskMeasure:
    def __init__(self, prior=None):
        self.prior = prior

    def compute(self, claims, capital=0):
        if self.prior is None:
            return self.compute_no_prior(claims, capital)
        elif self.prior == "poisson":
            return self.compute_poisson(claims, capital)
        elif self.prior == "gamma":
            return self.compute_gamma(claims, capital)
        elif self.prior == "poisson-gamma":
            return self.compute_poisson_gamma(claims, capital)

    def compute_no_prior(self, claims):
        pass

    def compute_poisson(self, claims):
        pass

    def compute_gamma(self, claims):
        pass

    def compute_poisson_gamma(self, claims):
        pass

    def estimate_poisson_parameters(self, claims):
        n_claims = [len(c) for c in claims]
        _lambda = np.mean(n_claims)
        return _lambda

    def estimate_gamma_parameters(self, claims):
        severities = [c for claim_list in claims for c in claim_list]
        avg_severity = np.mean(severities)
        variance_severity = np.var(severities)
        theta = variance_severity / avg_severity
        alpha = avg_severity / theta
        return alpha, theta

    def estimate_avg_frequency(self, claims):
        n_claims = [len(c) for c in claims]
        frequency = np.mean(n_claims)
        return frequency

    def estimate_avg_severity(self, claims):
        severities = [c for claim_list in claims for c in claim_list]
        avg_severity = np.mean(severities)
        return avg_severity
