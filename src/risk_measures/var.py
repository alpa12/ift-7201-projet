import numpy as np
from scipy.stats import poisson, gamma


# Paramètre de tolérance pour l'estimation des mesures de risque sur distributions composées
# TOL = 1e-8

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
