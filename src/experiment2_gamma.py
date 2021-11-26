import numpy as np
from environment import Environment, Insured
from insurers import EGreedy, AlwaysTheSame, RA_UCB
from distributions import Gamma, Constant

# 2 insureds
# mu = alpha * theta, so:
# mu_1 = 100, mu_2 = 90
# var = alpha * theta**2, so:
# var_1 = 500, var_2 = 1000

# Hypothèse:
# Insured 1 is not profitable, but much less risky
# Insured 2 is profitable, but riskier
# We think mainly choosing insured 2 (which all standard bandit algorithms should do)
# will lead to a higher proportion of ruins.

filename = "experiment2_gamma"

prem_list = [100, 100]
mu_list = [100, 95]
var_list = [500, 5000]

theta_list = [var/mu for mu, var in zip(mu_list, var_list)]
alpha_list = [mu/theta for theta, mu in zip(theta_list, mu_list)]

epsilon = 0.05
capital = 500

T = 200

K = len(prem_list)

if __name__ == "__main__":
    np.random.seed(2021)
    insureds = [Insured(freq=Constant(1), sev=Gamma(alpha, theta), premium=prem) for alpha, theta, prem in zip(alpha_list, theta_list, prem_list)]
    insurer1 = EGreedy(epsilon=epsilon, K=K, capital=capital) # Standard EGreedy strategy
    insurer2 = AlwaysTheSame(k=0, K=K, capital=capital) # Always chooses the less risky insured
    insurer3 = AlwaysTheSame(k=1, K=K, capital=capital) # Always chooses the riskier insured
    insurer4 = RA_UCB(kappa=0.90, K=K, capital=capital)
    env = Environment(insureds=insureds, T=T)

    env.simul_plays(100, [insurer1, insurer2, insurer3, insurer4], a = 0.33, b = 0.67, filename=filename)
