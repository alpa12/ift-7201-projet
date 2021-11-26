import numpy as np
from scipy.stats import poisson, gamma


def VaR(kappa, claims, prior=None):
    if prior is None:
        (totals := [np.sum(c) for c in claims]).sort()
        index = int(np.ceil(len(claims) * kappa) - 1)
        return totals[index]
    if prior == "poisson":
        _lambda = estimate_poisson_parameters(claims)
        return poisson.ppf(kappa, _lambda)
    if prior == "gamma":
        alpha, theta = estimate_gamma_parameters(claims)
        return gamma.ppf(kappa, alpha, scale=theta)
    if prior == "poisson-gamma":
        return 

def TVaR(kappa, claims, prior=None):
    if prior is None:
        (totals := [np.sum(c) for c in claims]).sort()
        index = int(np.ceil(len(claims) * (1 - kappa)) - 1)
        return np.mean(totals[index:])
    if prior == "poisson":
        # Hypothèse de sévérité constante
        _lambda = estimate_poisson_parameters(claims)
        var = poisson.ppf(kappa, _lambda)
        E_x_LE_VaR = 0
        val = 1
        while (val <= var):
            E_x_LE_VaR += val * poisson.pmf(val, _lambda)
            val += 1
        E_x = _lambda
        E_x_GE_VaR = E_x - E_x_LE_VaR
        tvar = (E_x_GE_VaR + var * (poisson.cdf(var, _lambda) - kappa)) / (1 - kappa)
        severities = [c for claim_list in claims for c in claim_list]
        severity = np.mean(severities)
        return tvar * avg_severity
    if prior == "gamma":
        # Hypothèse de fréquence constante
        alpha, theta = estimate_gamma_parameters(claims)
        var = gamma.ppf(kappa, alpha, scale=theta)
        tvar = (1 / (1 - kappa)) * alpha * theta * gamma.sf(var, alpha + 1, scale=theta)
        n_claims = [len(c) for c in claims]
        frequency = np.mean(n_claims)
        return tvar * frequency
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

claims = [[], [1,2,3], [4,2], [], [1,6], [8], [], [2], [1, 5], [], [5]]
TVaR(0.9, claims, prior=None)
TVaR(0.9, claims, prior="poisson")
