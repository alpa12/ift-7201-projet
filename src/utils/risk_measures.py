import numpy as np
from scipy.stats import poisson, gamma


# Paramètre de tolérance pour l'estimation des mesures de risque sur distributions composées
TOL = 1e-6

def VaR(kappa, claims, prior=None):
    if prior is None:
        totals = [np.sum(c) for c in claims]
        index = int(np.ceil(len(claims) * kappa) - 1)
        return np.partition(totals, index)[index]
    if prior == "poisson":
        # Hypothèse de sévérité constante
        severity = estimate_avg_severity(claims)
        _lambda = estimate_poisson_parameters(claims)
        return poisson.ppf(kappa, _lambda) * severity
    if prior == "gamma":
        # Hypothèse de fréquence constante
        frequency = estimate_avg_frequency(claims)
        alpha, theta = estimate_gamma_parameters(claims)
        return gamma.ppf(kappa, frequency * alpha, scale=theta)
    if prior == "poisson-gamma":
        _lambda = estimate_poisson_parameters(claims)
        alpha, theta = estimate_gamma_parameters(claims)
        var = 0
        var_increment = 0
        val = 1
        while (var_increment >= var * TOL):
            prob_poisson = poisson.pmf(val, _lambda)
            var_gamma = gamma.ppf(kappa, val * alpha, scale=theta)
            var_increment = prob_poisson * var_gamma
            var += var_increment
            val += 1
        return var * (1 + TOL)

def TVaR(kappa, claims, prior=None):
    if prior is None:
        (totals := [np.sum(c) for c in claims]).sort()
        index = int(np.ceil(len(claims) * (1 - kappa)) - 1)
        return np.mean(totals[index:])
    if prior == "poisson":
        # Hypothèse de sévérité constante
        severity = estimate_avg_severity(claims)
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
        return tvar * severity
    if prior == "gamma":
        # Hypothèse de fréquence constante
        frequency = estimate_avg_frequency(claims)
        alpha, theta = estimate_gamma_parameters(claims)
        tvar = estimate_gamma_tvar(kappa, frequency * alpha, theta)
        return tvar * frequency
    if prior == "poisson-gamma": # E. Marceau, Modelisation et evaluation quantitative des risques en actuariat, p. 86
        _lambda = estimate_poisson_parameters(claims)
        alpha, theta = estimate_gamma_parameters(claims)
        tvar = 0
        tvar_increment = 0
        val = 1
        while (tvar_increment >= tvar * TOL):
            prob_poisson = poisson.pmf(val, _lambda)
            tvar_gamma = estimate_gamma_tvar(kappa, val * alpha, theta)
            tvar_increment = prob_poisson * tvar_gamma
            tvar += tvar_increment
            val += 1
        return tvar * (1 + TOL)

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

claims = [[], [1,2,3], [4,2], [], [1,6], [8], [], [2], [1, 5], [], [5]]
TVaR(0.9, claims, prior=None)
TVaR(0.9, claims, prior="poisson")
TVaR(0.9, claims, prior="gamma")
TVaR(0.9, claims, prior="poisson-gamma")

alpha = 1
theta = 1
_lambda = 1
kappa = 0.95
M = 1000000
claims = list()
for i in range(M):
    claim_list = list()
    n_claims = poisson.rvs(_lambda)
    for j in range(n_claims):
        claim_list.append(gamma.rvs(alpha, scale=theta))
    claims.append(claim_list)
VaR(kappa, claims)
TVaR(kappa, claims)

