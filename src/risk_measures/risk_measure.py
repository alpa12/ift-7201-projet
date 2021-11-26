import numpy as np


class RiskMeasure:
    def __init__(self, capital, prior=None):
        self.capital = capital
        self.prior = prior
    def compute(self):
        if prior==None

# alpha = 1
# theta = 1
# _lambda = 1
# kappa = 0.95
# M = 100000
# claims = list()
# for i in range(M):
#     claim_list = list()
#     n_claims = 1#poisson.rvs(_lambda)
#     if n_claims > 0:
#         claim_list.append([gamma.rvs(n_claims*alpha, scale=theta)])
#     claims.append(claim_list)

# VaR(kappa, claims)
# TVaR(kappa, claims)
