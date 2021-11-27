import numpy as np
from scipy.stats import poisson, gamma
from risk_measures.risk_measure import RiskMeasure


class ProbabilityOfRuin(RiskMeasure):
    def compute_no_prior(self, parameters, capital):
        ruins = [1 if np.sum(c) > capital else 0 for c in claims]
        return np.mean(ruins)

    def compute_poisson(self, _lambda, capital):
        # Hypothèse de sévérité constante de 1
        prob = poisson.sf(capital, _lambda)
        return prob

    def compute_gamma(self, alpha, theta, capital):
        # Hypothèse de fréquence constante de 1
        prob = gamma.sf(capital, alpha, scale=theta)
        return prob

    def compute_poisson_gamma(self, _lambda, alpha, theta, capital, tol=1e-6):
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
