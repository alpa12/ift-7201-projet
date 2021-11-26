import numpy as np


def estimate_poisson_parameters(claims):
    n_claims = [len(c) for c in claims]
    _lambda = np.mean(n_claims)
    return _lambda

def estimate_gamma_parameters(claims):
    severities = [c for claim_list in claims for c in claim_list]
    avg_severity = np.mean(severities)
    variance_severity = np.var(severities)
    theta = variance_severity / avg_severity
    alpha = avg_severity / theta
    return alpha, theta

def estimate_gamma_tvar(kappa, alpha, theta):
    var = gamma.ppf(kappa, alpha, scale=theta)
    tvar = (1 / (1 - kappa)) * alpha * theta * gamma.sf(var, alpha + 1, scale=theta)
    return tvar

def estimate_avg_frequency(claims):
    n_claims = [len(c) for c in claims]
    frequency = np.mean(n_claims)
    return frequency

def estimate_avg_severity(claims):
    severities = [c for claim_list in claims for c in claim_list]
    avg_severity = np.mean(severities)
    return avg_severity
