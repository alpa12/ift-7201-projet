import numpy as np
from scipy.stats import poisson, gamma


def VaR(kappa, claims, prior=None):
    if prior is None:
        (totals := [np.sum(c) for c in claims]).sort()
        index = int(np.ceil(len(claims) * (1 - kappa)) - 1)
        return totals[index]
    if prior == "poisson":
        _lambda = estimate_poisson_parameters(claims)
        return poisson.isf(kappa, _lambda)
    if prior == "gamma":
        alpha, theta = estimate_gamma_parameters(claims)
        return gamma.isf(kappa, alpha, scale=theta)
    if prior == "poisson-gamma":
        return 

def TVaR(kappa, claims, prior=None):
    if prior is None:
        (totals := [np.sum(c) for c in claims]).sort()
        index = int(np.ceil(len(claims) * (1 - kappa)) - 1)
        return np.mean(totals[index:])
    if prior == "poisson":
        _lambda = estimate_poisson_parameters(claims)
        VaR = poisson.isf(kappa, _lambda)
        E_x_LE_VaR = 0
        val = 1
        while (val <= VaR):
            E_x_LE_VaR += val * poisson.pdf(val, _lambda)
            val += 1
        E_x = _lambda
        E_x_GE_VaR = E_x - E_x_LE_VaR
        severities = [c for claim_list in claims for c in claim_list]
        avg_severity = np.mean(severities)
        return TVaR * avg_severity
    if prior == "gamma":
        return
    if prior == "poisson-gamma": # E. Marceau, Modelisation et evaluation quantitative des risques en actuariat, p. 86
        return

def estimate_poisson_parameters(claims):
    n_claims = [len(c) for c in claims]
    _lambda = np.mean(n_claims)
    return _lambda

def estimate_gamma_parameters(claims):
    severities = [c for claim_list in claims for c in claim_list]
    avg_severity = np.mean(severities)
    var_severity = np.var(severities)
    theta = var_severity / avg_severity
    alpha = avg_severity / theta
    return alpha, theta
