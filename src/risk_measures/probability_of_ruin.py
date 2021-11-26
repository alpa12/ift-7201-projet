import numpy as np
from scipy.stats import poisson, gamma
from risk_measure import RiskMeasure


class probability_of_ruin(RiskMeasure):
    def compute(self):
        ruins = [1 if np.sum(c) > capital else 0 for c in claims]
        return np.mean(ruins)
    def compute_poisson(self):
        # Hypothèse de sévérité constante
        severity = estimate_avg_severity(claims)
        _lambda = estimate_poisson_parameters(claims)
        
        return tvar * severity
