import numpy as np
from scipy.stats import poisson, gamma


def TVaR(kappa, claims, prior=None):
    if prior is None:
        totals = [np.sum(c) for c in claims]
        totals.sort()
        index = int(np.ceil(len(claims) * kappa) - 1)
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
        raise NotImplemented
        # _lambda = estimate_poisson_parameters(claims)
        # alpha, theta = estimate_gamma_parameters(claims)
        # tvar = 0
        # tvar_increment = 0
        # val = 1
        # while (tvar_increment >= tvar * TOL):
        #     prob_poisson = poisson.pmf(val, _lambda)
        #     tvar_gamma = estimate_gamma_tvar(kappa, val * alpha, theta)
        #     tvar_increment = prob_poisson * tvar_gamma
        #     tvar += tvar_increment
        #     val += 1
        # return tvar * (1 + TOL)
