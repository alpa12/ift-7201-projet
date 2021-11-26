import numpy as np
from environment import Environment, Insured
from insurers import EGreedy
from distributions import Gamma, Constant


alpha_list = [1, 10]
theta_list = [100, 10]
prem_list = [100, 100]

epsilon = 0.05
capital = 500

T = 100

if __name__ == "__main__":
    np.random.seed(2021)
    insureds = [Insured(freq=Constant(1), sev=Gamma(alpha, theta), premium=prem) for alpha, theta, prem in zip(alpha_list, theta_list, prem_list)]
    insurer1 = EGreedy(epsilon=epsilon, K=len(prem_list), capital=capital)
    env = Environment(insureds=insureds, T=T)

    env.simul_plays(100, [insurer1])
