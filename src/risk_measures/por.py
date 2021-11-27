import numpy as np
from bisect import bisect_left
from scipy.stats import poisson, gamma
from risk_measures.risk_measure import RiskMeasure


class PoR(RiskMeasure):
    def compute_no_prior(self, sorted_claims, capital):
        if sorted_claims[-1] < capital:
            prob = 0
        else:
            index = bisect_left(sorted_claims, capital)
            prob = (len(sorted_claims) - index) / len(sorted_claims)
        return prob

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

    def __str__(self):
        return "PoR"
