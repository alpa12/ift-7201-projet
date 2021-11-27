import numpy as np
from scipy.stats import poisson, gamma
from risk_measure import RiskMeasure


class VaR(RiskMeasure):
    def __init__(self, kappa, prior=None):
        super().__init__(prior)
        self.kappa = kappa

    def compute_no_prior(self, sorted_claims, _):
        index = int(np.ceil(len(sorted_claims) * self.kappa) - 1)
        return sorted_claims[index]
    
    def compute_poisson(self, _lambda, _):
        # Hypothèse de sévérité constante de 1
        return poisson.ppf(self.kappa, _lambda)

    def compute_gamma(self, alpha, theta, _):
        # Hypothèse de fréquence constante de 1
        return gamma.ppf(self.kappa, alpha, scale=theta)

    def compute_poisson_gamma(self, _lambda, alpha, theta, _, tol=1e-6):
        raise NotImplemented
        # _lambda = estimate_poisson_parameters(claims)
        # alpha, theta = estimate_gamma_parameters(claims)
        # var = 0
        # var_increment = 0
        # val = 1
        # cum_poisson = poisson.pmf(0, _lambda)
        # while (cum_poisson < kappa):
        #     prob_poisson = poisson.pmf(val, _lambda)
        #     adj_kappa = (kappa - cum_poisson) / (1 - cum_poisson)
        #     var_gamma = gamma.ppf(adj_kappa, val * alpha, scale=theta)
        #     var_increment = prob_poisson * var_gamma
        #     var += var_increment
        #     val += 1
        #     cum_poisson += prob_poisson
        # var += (1 - cum_poisson) * gamma.ppf(adj_kappa, val * alpha, scale=theta)
        # return var * (1 + TOL)
