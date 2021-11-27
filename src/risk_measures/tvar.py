import numpy as np
from scipy.stats import poisson, gamma
from risk_measures.risk_measure import RiskMeasure


class TVaR(RiskMeasure):
    def __init__(self, kappa, prior=None):
        super().__init__(prior)
        self.kappa = kappa

    def compute_no_prior(self, sorted_claims, _):
        index = int(np.ceil(len(sorted_claims) * self.kappa) - 1)
        return np.mean(sorted_claims[index:])

    def compute_poisson(self, _lambda, _):
        # Hypothèse de sévérité constante de 1
        var = poisson.ppf(self.kappa, _lambda)
        E_x_LE_VaR = 0
        val = 1
        while (val <= var):
            E_x_LE_VaR += val * poisson.pmf(val, _lambda)
            val += 1
        E_x = _lambda
        E_x_GE_VaR = E_x - E_x_LE_VaR
        tvar = (E_x_GE_VaR + var * (poisson.cdf(var, _lambda) - self.kappa)) / (1 - self.kappa)
        return tvar

    def compute_gamma(self, alpha, theta, _):
        # Hypothèse de fréquence constante de 1
        tvar = self.estimate_gamma_tvar(alpha, theta)
        return tvar

    def compute_poisson_gamma(self, _lambda, alpha, theta, _, tol=1e-6): # E. Marceau, Modelisation et evaluation quantitative des risques en actuariat, p. 86
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

    def __str__(self):
        return f"TVaR{self.kappa}"
