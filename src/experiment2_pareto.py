import numpy as np
from environment import Environment, Insured
from insurers import EGreedy, AlwaysTheSame
from distributions import Pareto, Constant

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

filename = "experiment2_pareto"

prem_list = [100, 100]
mu_list = [99, 95]
var_list = [100**2, 100000000 * 100**2]

alpha_list = [2 / (1 - mu**2/var) for mu, var in zip(mu_list, var_list)]
_lambda_list = [(alpha-1) * mu for alpha, mu in zip(alpha_list, mu_list)]

epsilon = 0.05
capital = 300

T = 100

if __name__ == "__main__":
    np.random.seed(2021)
    insureds = [Insured(freq=Constant(1), sev=Pareto(alpha, _lambda), premium=prem) for alpha, _lambda, prem in zip(alpha_list, _lambda_list, prem_list)]
    insurer1 = EGreedy(epsilon=epsilon, K=len(prem_list), capital=capital) # Standard EGreedy strategy
    insurer2 = AlwaysTheSame(k=0, K=len(prem_list), capital=capital) # Always chooses the less risky, less profitable insured
    insurer3 = AlwaysTheSame(k=1, K=len(prem_list), capital=capital) # Always chooses the riskier, more profitable insured
    env = Environment(insureds=insureds, T=T)

    env.simul_plays(1000, [insurer1, insurer2, insurer3], a = 0.01, b = 0.99, filename=filename)
