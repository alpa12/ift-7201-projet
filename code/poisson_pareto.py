import numpy as np
from environment import Environment
from insurers import EGreedy
from insured import Insured
from distributions import Poisson, Pareto


pois_lambda_list = [0.15, 0.01]
alpha_list = [3, 2]
par_lambda_list = [13000, 97500]
prem_list = [1000, 1000]

epsilon = 0.1
capital = 100000

T = 10000

if __name__ == "__main__":
    np.random.seed(2021)
    insureds = [Insured(freq=Poisson(pois_lambda), sev=Pareto(alpha, par_lambda), premium=prem) \
        for pois_lambda, alpha, par_lambda, prem in zip(pois_lambda_list, alpha_list, par_lambda_list, prem_list)]
    insurer = EGreedy(epsilon, len(prem_list), capital)
    env = Environment(insureds, T)

    env.play(insurer)
