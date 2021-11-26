import numpy as np
from scipy.stats import poisson, gamma
from risk_measure import RiskMeasure


class VaR(RiskMeasure):
    def __init__(self, kappa, prior=None):
        super().__init__(prior)
        self.kappa = kappa

    def compute_no_prior(self, claims, _):
        totals = [np.sum(c) for c in claims]
        index = int(np.ceil(len(claims) * self.kappa) - 1)
        return np.partition(totals, index)[index]
    
    def compute_poisson(self, claims, _):
        # Hypothèse de sévérité constante
        severity = self.estimate_avg_severity(claims)
        _lambda = self.estimate_poisson_parameters(claims)
        return poisson.ppf(self.kappa, _lambda) * severity

    def compute_gamma(self, claims, _):
        # Hypothèse de fréquence constante
        frequency = self.estimate_avg_frequency(claims)
        alpha, theta = self.estimate_gamma_parameters(claims)
        return gamma.ppf(self.kappa, frequency * alpha, scale=theta)

    def compute_poisson_gamma(self, claims, _, tol=1e-6):
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
