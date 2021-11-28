import numpy as np
from environment import Environment, Insured
from insurers import ETGreedy, AlwaysTheSame, RiskAware, UCB, Insurer
from distributions import Gamma, Constant
from risk_measures import VaR, TVaR, PoR

# 2 insureds
# mu_1 = mu_2 = 100
# var = alpha * theta**2, so:
# var_1 = 1000, var_2 = 10000

# Hypothesis:
# Insured #1 (k=0) is a better, less risky choice
# Will lead to same average profit, but lower probability of ruin

filename = "experiment5"

prem_list = [100, 105]
prior = "gamma"
mu_list = [100, 100]
var_list = [1000, 100000]

theta_list = [var/mu for mu, var in zip(mu_list, var_list)]
alpha_list = [mu/theta for theta, mu in zip(theta_list, mu_list)]

epsilon = 0.05
capital = 500

T = 200
M = 5000

K = len(prem_list)

if __name__ == "__main__":
    np.random.seed(2021)
    insureds = [Insured(freq=Constant(1), sev=Gamma(alpha, theta), premium=prem) for alpha, theta, prem in zip(alpha_list, theta_list, prem_list)]

    insurers = []
    insurers.append(RiskAware(A=1, K=K, risk_measure=TVaR(kappa=0.5, prior=prior), capital=capital))
    insurers.append(RiskAware(A=1, K=K, risk_measure=TVaR(kappa=0.75, prior=prior), capital=capital))
    insurers.append(RiskAware(A=1, K=K, risk_measure=TVaR(kappa=0.95, prior=prior), capital=capital))
    insurers.append(RiskAware(A=1, K=K, risk_measure=TVaR(kappa=0.99, prior=prior), capital=capital))
    insurers.append(RiskAware(A=1, K=K, risk_measure=TVaR(kappa=0.999, prior=prior), capital=capital))
    env = Environment(insureds=insureds, T=T)

    env.simul_plays(M, insurers, a = 0.5, b = 0.5, filename=filename)
