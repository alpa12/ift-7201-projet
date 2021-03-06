import numpy as np
from environment import Environment, Insured
from insurers import ETGreedy, AlwaysTheSame, RiskAware, UCB, Insurer
from distributions import Gamma, Poisson
from risk_measures import VaR, TVaR, PoR

# 2 insureds
# mu_1 = mu_2 = 100
# var = alpha * theta**2, so:
# var_1 = 1000, var_2 = 10000

# Hypothesis:
# Insured #1 (k=0) is a better, less risky choice
# Will lead to same average profit, but lower probability of ruin

filename = "experiment6_poisson_gamma"

prem_list = [100, 105]
prior = "poisson-gamma"
mu_list = [100, 200]
var_list = [1000, 100000]

lambda_list = [1, 0.5]
theta_list = [var/mu for mu, var in zip(mu_list, var_list)]
alpha_list = [mu/theta for theta, mu in zip(theta_list, mu_list)]

capital = 500

T = 200
M = 10000

K = len(prem_list)

if __name__ == "__main__":
    np.random.seed(2021)
    insureds = [Insured(freq=Poisson(_lambda), sev=Gamma(alpha, theta), premium=prem) for \
        _lambda, alpha, theta, prem in zip(lambda_list, alpha_list, theta_list, prem_list)]

    insurers = []
    insurers.append(ETGreedy(K=K, capital=capital)) # ETGreedy strategy with epsilon = 1 / sqrt(t)
    insurers.append(AlwaysTheSame(k=0, K=K, capital=capital)) # Always chooses the less risky insured
    insurers.append(AlwaysTheSame(k=1, K=K, capital=capital)) # Always chooses the riskier insured
    insurers.append(Insurer(K=K, capital=capital)) # Chooses insured randomly
    insurers.append(RiskAware(A=1e2, K=K, risk_measure=VaR(kappa=0.95, prior=None), capital=capital))
    insurers.append(RiskAware(A=1e2, K=K, risk_measure=TVaR(kappa=0.95, prior=None), capital=capital))
    insurers.append(RiskAware(A=1e5, K=K, risk_measure=PoR(prior="poisson-gamma"), capital=capital))
    insurers.append(UCB(K=K, capital=capital))
    env = Environment(insureds=insureds, T=T)

    env.simul_plays(M, insurers, a = 0.33, b = 0.67, filename=filename)
