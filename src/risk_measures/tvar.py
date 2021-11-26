import numpy as np
from scipy.stats import poisson, gamma
from risk_measure import RiskMeasure


class TVaR(RiskMeasure):
    def __init__(self, kappa, prior=None):
        super().__init__(prior)
        self.kappa = kappa

    def compute_no_prior(self, claims, _):
        totals = [np.sum(c) for c in claims]
        totals.sort()
        index = int(np.ceil(len(claims) * self.kappa) - 1)
        return np.mean(totals[index:])

    def compute_poisson(self, claims, _):
        # Hypothèse de sévérité constante
        severity = self.estimate_avg_severity(claims)
        _lambda = self.estimate_poisson_parameters(claims)
        var = poisson.ppf(self.kappa, _lambda)
        E_x_LE_VaR = 0
        val = 1
        while (val <= var):
            E_x_LE_VaR += val * poisson.pmf(val, _lambda)
            val += 1
        E_x = _lambda
        E_x_GE_VaR = E_x - E_x_LE_VaR
        tvar = (E_x_GE_VaR + var * (poisson.cdf(var, _lambda) - self.kappa)) / (1 - self.kappa)
        return tvar * severity

    def compute_gamma(self, claims, _):
        # Hypothèse de fréquence constante
        frequency = self.estimate_avg_frequency(claims)
        alpha, theta = self.estimate_gamma_parameters(claims)
        tvar = self.estimate_gamma_tvar(kappa, frequency * alpha, theta)
        return tvar * frequency

    def compute_poisson_gamma(self, claims, _, tol=1e-6): # E. Marceau, Modelisation et evaluation quantitative des risques en actuariat, p. 86
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

    def estimate_gamma_tvar(self, alpha, theta):
        var = gamma.ppf(self.kappa, alpha, scale=theta)
        tvar = (1 / (1 - self.kappa)) * alpha * theta * gamma.sf(var, alpha + 1, scale=theta)
        return tvar
