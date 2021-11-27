import numpy as np
import bisect
from scipy.stats import poisson, gamma
from welford import Welford


class RiskMeasure:
    def __init__(self, prior=None):
        self.prior = prior

    def compute(self, parameters, capital=0):
        if self.prior is None:
            sorted_claims = parameters
            return self.compute_no_prior(sorted_claims, capital)
        elif self.prior == "poisson":
            _lambda, _ = parameters
            return self.compute_poisson(_lambda, capital)
        elif self.prior == "gamma":
            alpha, theta, _ = parameters
            return self.compute_gamma(alpha, theta, capital)
        elif self.prior == "poisson-gamma":
            poisson_parameters, gamma_parameters = parameters
            _lambda, _ = poisson_parameters
            alpha, theta, _ = gamma_parameters
            return self.compute_poisson_gamma(_lambda, alpha, theta, capital)

    def update_parameters(self, claims, old_parameters=None):
        if self.prior is None:
            updated_parameters = self.estimate_no_prior_parameters(claims, old_parameters)
        elif self.prior == "poisson":
            updated_parameters = self.estimate_poisson_parameters(claims, old_parameters)
        elif self.prior == "gamma":
            updated_parameters = self.estimate_gamma_parameters(claims, old_parameters)
        elif self.prior == "poisson-gamma":
            old_poisson_parameters, old_gamma_parameters = old_parameters
            updated_poisson_parameters = self.estimate_poisson_parameters(claims, old_poisson_parameters)
            updated_gamma_parameters = self.estimate_poisson_parameters(claims, old_gamma_parameters)
            updated_parameters = (updated_poisson_parameters, updated_gamma_parameters)
        return updated_parameters

    def estimate_no_prior_parameters(self, claims, old_parameters=None):
        if old_parameters is None:
            sorted_claims = [np.sum(c) for c in claims]
            sorted_claims.sort()
            parameters = sorted_claims
        else:
            sorted_claims = old_parameters
            new_claim = np.sum(claims[-1])
            bisect.insort(sorted_claims, new_claim)
            parameters = sorted_claims
        return parameters

    def estimate_poisson_parameters(self, claims, old_parameters=None):
        if old_parameters is None:
            n_claims = [len(c) for c in claims]
            _lambda = np.mean(n_claims)
            n_obs = len(claims)
        else:
            old_lambda, old_n_obs = old_parameters
            n_obs = old_n_obs + 1
            new_n_claims = np.sum(claims[-1])
            _lambda = (old_lambda * old_n_obs + new_n_claims) / n_obs
        return _lambda, n_obs

    def estimate_gamma_parameters(self, claims, old_parameters=None):
        # Algorithme Welford pour calcul en ligne de la variance
        if old_parameters is None:
            w = Welford()
            severities = [c for claim_list in claims for c in claim_list]
        else:
            _, _, w = old_parameters
            severities = claims[-1]

        for severity in severities:
            w.add(np.array([severity]))

        variance = w.mean[0] if np.isnan(w.var_s[0]) else w.var_s[0]
        theta = variance / w.mean[0]
        alpha = w.mean[0] / theta
        return alpha, theta, w

    def __str__(self):
        return "RiskMeasure"

    def compute_no_prior(self, claims):
        pass

    def compute_poisson(self, claims):
        pass

    def compute_gamma(self, claims):
        pass

    def compute_poisson_gamma(self, claims):
        pass
