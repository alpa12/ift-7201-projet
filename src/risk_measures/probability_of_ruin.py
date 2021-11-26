import numpy as np
from scipy.stats import poisson, gamma
from risk_measure import RiskMeasure


class ProbabilityOfRuin(RiskMeasure):
    def compute_no_prior(self, claims, capital):
        ruins = [1 if np.sum(c) > capital else 0 for c in claims]
        return np.mean(ruins)

    def compute_poisson(self, claims, capital):
        # Hypothèse de sévérité constante
        severity = self.estimate_avg_severity(claims)
        _lambda = self.estimate_poisson_parameters(claims)
        critical_n_claim = np.ceil(capital / severity)
        prob = poisson.sf(critical_n_claim, _lambda)
        return prob

    def compute_gamma(self, claims, capital):
        # Hypothèse de fréquence constante
        frequency = self.estimate_avg_frequency(claims)
        alpha, theta = self.estimate_gamma_parameters(claims)
        prob = gamma.sf(capital, frequency * alpha, scale=theta)
        return prob

    def compute_poisson_gamma(self, claims, capital, tol=1e-6):
        _lambda = self.estimate_poisson_parameters(claims)
        alpha, theta = self.estimate_gamma_parameters(claims)
        prob = 0
        prob_increment = 1
        val = 1
        while (prob_increment >= tol):
            prob_poisson = poisson.pmf(val, _lambda)
            prob_gamma = gamma.sf(capital, val * alpha, scale=theta)
            prob_increment = prob_poisson * prob_gamma
            prob += prob_increment
            val += 1
        return prob + tol
