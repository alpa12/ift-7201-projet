import numpy as np
from environment import Environment, Insured
from insurers import EGreedy, AlwaysTheSame, RA_UCB
from distributions import Gamma, Constant

# 2 insureds
# mu_1 = mu_2 = 100
# var = alpha * theta**2, so:
# var_1 = 1000, var_2 = 10000

# Hypothesis:
# Insured #1 (k=0) is a better, less risky choice
# Will lead to same average profit, but lower probability of ruin

filename = "experiment1"

prem_list = [100, 100]
mu_list = [100, 100]
var_list = [1000, 100000]

theta_list = [var/mu for mu, var in zip(mu_list, var_list)]
alpha_list = [mu/theta for theta, mu in zip(theta_list, mu_list)]

epsilon = 0.05
capital = 500

T = 500

K = len(prem_list)

if __name__ == "__main__":
    np.random.seed(2021)
    insureds = [Insured(freq=Constant(1), sev=Gamma(alpha, theta), premium=prem) for alpha, theta, prem in zip(alpha_list, theta_list, prem_list)]
    insurer1 = EGreedy(epsilon=epsilon, K=K, capital=capital) # Standard EGreedy strategy
    insurer2 = AlwaysTheSame(k=0, K=K, capital=capital) # Always chooses the less risky insured
    insurer3 = AlwaysTheSame(k=1, K=K, capital=capital) # Always chooses the riskier insured
    insurer4 = RA_UCB(kappa=0.90, K=K, prior="gamma", capital=capital)
    env = Environment(insureds=insureds, T=T)

    env.simul_plays(500, [insurer1, insurer2, insurer3, insurer4], a = 0.33, b = 0.67, filename=filename)
